from rest_framework import generics
from rest_framework.response import Response

from .ai_client import AIProviderError, generate_json
from .meta_audit import run_live_social_audit
from .meta_client import MetaGraphError
from .services import generate_caption, generate_content_ideas, run_social_audit
from .tool_serializers import CaptionGenerateSerializer, ContentIdeasSerializer, SocialAuditSerializer

PLATFORM_LABELS = {
    "instagram": "Instagram", "facebook": "Facebook", "linkedin": "LinkedIn",
    "twitter": "Twitter", "x": "X", "youtube": "YouTube", "tiktok": "TikTok",
}

AI_SYSTEM = """You are a senior social-media strategist for Flayer Wings. Return JSON only.
Reason from business context, audience, offer, goal and platform — never fill templates.
Never invent metrics, testimonials, customer results, awards, clients, platform data or factual claims.
Avoid buzzword stuffing and generic marketing language.
Write like an experienced strategist who understands what a real customer would stop scrolling to learn.
"""

GENERIC_PATTERNS = (
    "the 3 biggest", "behind the scenes:", "myth vs fact:", "save-worthy checklist",
    "do not need more information", "the useful approach is to focus on one outcome",
    "at flayer wings, we use this principle",
)


def _bad_text(text):
    value = str(text or "").lower()
    return any(pattern in value for pattern in GENERIC_PATTERNS)


def _platform_label(value):
    return PLATFORM_LABELS.get(str(value or "").strip().lower(), value)


def _caption(data):
    requested_cta = str(data.get("cta") or "").strip()
    prompt = f"""Create one genuinely useful, publish-ready {data.get('platform', 'social media')} post.
INPUT: {data}
Reason privately about the audience problem, useful insight, business goal and natural next action.
Return JSON with exactly: caption, hashtags, hook, cta, platform, format, strategy_note.
Caption: 120–220 words unless platform strongly calls for shorter copy. Start with curiosity around the audience problem, not a topic restatement. Include a concrete framework, example, checklist, decision rule or actionable takeaway. Mention the offer naturally. Match tone and goal. Use <=5 relevant hashtags. Avoid generic templates and invented evidence.
Do not paste the full audience, industry or offer field into the opening. Use natural language and make the post sound written for the specific audience.
"""
    result = generate_json(AI_SYSTEM, prompt, temperature=0.8, max_tokens=2200)
    required = ("caption", "hashtags", "hook", "cta", "platform", "format", "strategy_note")
    if not isinstance(result, dict) or any(not result.get(k) for k in required) or not isinstance(result["hashtags"], list):
        raise AIProviderError("Invalid AI caption contract")
    caption = str(result["caption"])
    if _bad_text(caption) or _bad_text(result["hook"]):
        repair_prompt = f"""Rewrite this social post so it is specific, natural and publish-ready.
INPUT: {data}
DRAFT: {result}
Return JSON only with exactly: caption, hashtags, hook, cta, platform, format, strategy_note.
Remove generic AI phrasing, topic restatement and keyword stuffing. Lead with a real audience tension or useful insight. Include one concrete framework, example, decision rule or actionable takeaway. Mention the business/offer naturally. Never invent proof or metrics. Keep the requested CTA exact if one was supplied."""
        result = generate_json(AI_SYSTEM, repair_prompt, temperature=0.6, max_tokens=2200)
        if not isinstance(result, dict) or any(not result.get(k) for k in required) or not isinstance(result["hashtags"], list):
            raise AIProviderError("Invalid AI caption repair contract")
        if _bad_text(result["caption"]) or _bad_text(result["hook"]):
            raise AIProviderError("AI caption failed the quality contract")
    result["cta"] = requested_cta if requested_cta else result["cta"]
    result["platform"] = _platform_label(data.get("platform"))
    if requested_cta and requested_cta not in result["caption"]:
        result["caption"] = result["caption"].rstrip() + "\n\n" + requested_cta
    return result


def _idea_is_usable(idea, data):
    if not isinstance(idea, dict):
        return False
    required = ("title", "format", "pillar", "goal", "hook", "outline")
    if any(not str(idea.get(k) or "").strip() for k in required):
        return False

    title = str(idea["title"]).strip()
    hook = str(idea["hook"]).strip()
    outline = str(idea["outline"]).strip()
    title_lower = title.lower()

    if len(title.split()) < 5 or len(title) > 150:
        return False
    if _bad_text(title) or _bad_text(hook):
        return False
    if len(outline.split()) < 8:
        return False

    for field in ("audience", "industry", "offer"):
        value = str(data.get(field) or "").strip().lower()
        if len(value) >= 18 and value in title_lower:
            return False

    angle_words = {
        "why", "how", "when", "what", "which", "before", "after", "mistake", "mistakes",
        "problem", "problems", "lesson", "lessons", "framework", "checklist", "guide",
        "question", "questions", "cost", "reason", "reasons", "workflow", "process",
        "example", "examples", "comparison", "decision", "decisions", "strategy", "steps",
    }
    if not angle_words.intersection(set(title_lower.replace("?", " ").replace(":", " ").split())):
        return False
    return True


def _validate_ideas(result, data):
    if not isinstance(result, dict):
        return False
    ideas = result.get("ideas")
    if not isinstance(ideas, list) or len(ideas) != 10:
        return False
    if not isinstance(result.get("content_pillars"), list) or len(result["content_pillars"]) < 5:
        return False
    if any(not _idea_is_usable(idea, data) for idea in ideas):
        return False

    titles = [str(i["title"]).strip().lower() for i in ideas]
    hooks = [str(i["hook"]).strip().lower() for i in ideas]
    if len(set(titles)) != 10 or len(set(hooks)) < 8:
        return False

    token_sets = [set(t.replace(":", " ").replace("—", " ").split()) for t in titles]
    for index, tokens in enumerate(token_sets):
        for other in token_sets[index + 1:]:
            if len(tokens & other) / max(1, min(len(tokens), len(other))) > 0.72:
                return False
    return True


def _ideas(data):
    prompt = f"""Build a 10-post content strategy for this business.
INPUT: {data}

First reason privately about:
- the audience's recurring problems, frustrations, risks and desired outcomes;
- what they are trying to decide or improve;
- objections they would have before buying;
- useful lessons, workflows, checklists or frameworks that can genuinely help them;
- what proof can be shown without inventing results;
- which topics naturally support the requested business goal.

Then return JSON with exactly: business, audience, platform, goal, content_pillars, ideas.
Each idea must contain exactly: title, format, pillar, goal, hook, outline.

IMPORTANT EDITORIAL RULES:
1. Do NOT copy the audience, industry or offer field into titles. Translate the context into a specific customer problem or decision.
2. Do NOT make every idea about the product. Most ideas should teach, diagnose, compare, explain or help the audience make a decision; only some should directly connect to the offer.
3. Every title needs a distinct angle and should sound like a real post someone would publish, not an AI content template.
4. Never use generic title patterns such as “The 3 biggest…”, “Myth vs fact…”, “Behind the scenes…”, “Save-worthy checklist…”, or “Do not need more information…”.
5. Do not stuff the business name, audience list, industry keywords or full offer description into titles.
6. Hooks must create curiosity by naming a tension, mistake, overlooked detail, decision or useful promise — without fake statistics.
7. Outlines must give concrete production beats: examples, questions to answer, steps to show, comparisons to make, or evidence to gather.
8. Use exactly 10 materially different ideas and at least 7 different formats where appropriate.
9. Cover education, problem/solution, objection handling, authority, utility, proof and conversion, but do not force these labels when they make the idea unnatural.
10. Never invent customer names, metrics, testimonials, results, awards or factual claims.

Make the output specific enough that a content creator could start producing the posts immediately."""

    result = generate_json(AI_SYSTEM, prompt, temperature=0.8, max_tokens=5000)
    if _validate_ideas(result, data):
        return result

    repair_prompt = f"""Rewrite the following 10 content ideas into a genuinely publishable strategy.

ORIGINAL INPUT:
{data}

DRAFT TO REPAIR:
{result}

Return JSON only with exactly: business, audience, platform, goal, content_pillars, ideas.
Each idea must contain: title, format, pillar, goal, hook, outline.

Fix every problem below:
- remove keyword stuffing and long audience/offer/industry phrases;
- remove generic AI templates;
- give every title one concrete customer problem, decision, lesson, use case or outcome;
- make all 10 titles materially different;
- make hooks specific and curiosity-driven;
- make outlines actionable enough to film/write immediately;
- keep claims evidence-safe and never invent metrics or customer proof;
- do not make every idea a sales pitch.

Do not mention these repair instructions in the output."""
    repaired = generate_json(AI_SYSTEM, repair_prompt, temperature=0.65, max_tokens=5000)
    if not _validate_ideas(repaired, data):
        raise AIProviderError("AI content ideas failed the quality contract")
    return repaired


def _enrich_audit(data):
    prompt = f"""Improve this social audit using ONLY supplied evidence: {data}
Do not change profile, performance, publishing, score, score_scale, data_source, platform, business, profile_url or audit_type. Do not create metrics.
Return the full audit object. Make every recommendation explain what the evidence/problem means, why it matters, exactly what to change, and what good implementation looks like. Make quick wins and the seven-day plan executable. Avoid generic motivational language."""
    result = generate_json(AI_SYSTEM, prompt, temperature=0.45, max_tokens=4000)
    if not isinstance(result, dict) or not isinstance(result.get("checks"), list):
        raise AIProviderError("Invalid AI audit contract")
    for key in ("profile", "performance", "publishing", "score", "score_scale", "data_source", "platform", "business", "profile_url", "audit_type"):
        result[key] = data.get(key)
    return result


class CaptionGenerateView(generics.GenericAPIView):
    serializer_class = CaptionGenerateSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True); data = serializer.validated_data
        try: result = _caption(data)
        except AIProviderError as exc:
            return Response({"error": str(exc), "code": "ai_quality_contract_failed"}, status=502)
        if data.get("cta"):
            result["cta"] = data["cta"]
            if data["cta"] not in result.get("caption", ""):
                result["caption"] = result["caption"].rstrip() + "\n\n" + data["cta"]
        result["platform"] = _platform_label(data.get("platform"))
        return Response(result)


class ContentIdeasView(generics.GenericAPIView):
    serializer_class = ContentIdeasSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True); data = serializer.validated_data
        try: result = _ideas(data)
        except AIProviderError as exc:
            return Response({"error": str(exc), "code": "ai_quality_contract_failed"}, status=502)
        return Response(result)


class SocialAuditView(generics.GenericAPIView):
    serializer_class = SocialAuditSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True); data = serializer.validated_data
        try: live_result = run_live_social_audit(**data)
        except MetaGraphError: live_result = None
        if live_result:
            try: live_result = _enrich_audit(live_result); live_result["ai_enriched"] = True
            except AIProviderError: live_result["ai_enriched"] = False
            return Response(live_result)
        fallback = run_social_audit(**data); fallback["data_source"] = "strategy_baseline"; fallback["live_data_available"] = False
        try: fallback = _enrich_audit(fallback); fallback["data_source"] = "strategy_baseline"; fallback["live_data_available"] = False; fallback["ai_enriched"] = True
        except AIProviderError: fallback["ai_enriched"] = False
        return Response(fallback)
