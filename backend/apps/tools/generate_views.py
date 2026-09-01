from rest_framework import generics
from rest_framework.response import Response

from .ai_client import AIProviderError, generate_json
from .meta_audit import run_live_social_audit
from .meta_client import MetaGraphError
from .services import generate_caption, generate_content_ideas, run_social_audit
from .tool_serializers import CaptionGenerateSerializer, ContentIdeasSerializer, SocialAuditSerializer

AI_SYSTEM = """You are a senior social-media strategist for Flayer Wings. Return JSON only.
Your job is to reason from the business context, audience, offer, goal and platform — not to fill templates.
Write like an experienced strategist who understands why a piece of content would work.
Never invent metrics, testimonials, customer results, awards, clients, platform data or factual claims.
Do not merely repeat input fields as phrases. Translate them into audience problems, desired outcomes,
objections, decisions and useful content angles. Avoid buzzword stuffing and generic marketing language."""

GENERIC_PATTERNS = (
    "the 3 biggest",
    "behind the scenes:",
    "myth vs fact:",
    "save-worthy checklist",
    "explain " ,
    "one question to learn",
    "do not need more information",
    "the useful approach is to focus on one outcome",
    "at flayer wings, we use this principle",
)


def _bad_text(text):
    value = str(text or "").lower()
    return any(pattern in value for pattern in GENERIC_PATTERNS)


def _caption(data):
    prompt = f"""Create one genuinely useful, publish-ready {data.get('platform', 'social media')} post.

INPUT:
{data}

First reason privately about:
1. the most likely real problem this audience has related to the topic;
2. the specific useful insight the post can teach;
3. why this insight matters for the stated business goal;
4. a natural action the reader should take next.

Then return JSON with exactly these keys:
caption, hashtags, hook, cta, platform, format, strategy_note.

Requirements:
- 120–220 words for the caption unless the platform strongly calls for shorter copy.
- The opening must create curiosity around the audience's problem, not restate the topic.
- Give at least one concrete framework, example, checklist, decision rule, or actionable takeaway.
- Mention the offer/business naturally only where it adds context; never make the post a generic advertisement.
- Match {data.get('tone', 'professional')} tone and {data.get('goal', 'engagement')} goal.
- Use a CTA that logically follows from the post.
- Hashtags must be relevant and specific; no more than 5.
- Do NOT use generic templates such as 'the 3 biggest', 'behind the scenes', 'myth vs fact',
  'do not need more information', or 'the useful approach is to focus on one outcome'.
- Do not invent evidence or claims."""
    result = generate_json(AI_SYSTEM, prompt, temperature=0.85, max_tokens=2200)
    if not isinstance(result, dict) or any(not result.get(k) for k in ("caption", "hashtags", "hook", "cta", "platform", "format", "strategy_note")):
        raise AIProviderError("Invalid AI caption contract")
    if not isinstance(result["hashtags"], list) or _bad_text(result["caption"]) or _bad_text(result["hook"]):
        raise AIProviderError("AI caption was too generic")
    return result


def _ideas(data):
    prompt = f"""Build a 10-post content strategy for this business.

INPUT:
{data}

Before writing the JSON, reason privately about the audience's likely:
- recurring problems and workflow friction;
- buying objections and misconceptions;
- desired business outcomes;
- questions they ask before buying;
- proof they would trust;
- practical actions they can take;
- reasons they would engage or share a post.

Then return JSON with exactly: business, audience, platform, goal, content_pillars, ideas.
Each idea must contain exactly: title, format, pillar, goal, hook, outline.

QUALITY RULES:
- Exactly 10 ideas and each must represent a genuinely different strategic opportunity.
- At least 6 different formats across the set.
- Cover at least education, problem/solution, proof, objection handling, utility, authority and conversion.
- Titles should describe a specific audience problem, decision, lesson, use case or outcome.
- Hooks must make a reader want to continue; do not simply restate the title.
- Outlines must contain concrete beats someone could actually turn into a post.
- Connect the offer to the audience's real need without making every idea a sales pitch.
- Use the platform's natural content behavior.
- Do not stuff industry/audience/offer keywords into every title.
- Do NOT use generic templates such as 'the 3 biggest', 'behind the scenes', 'myth vs fact',
  'save-worthy checklist', or 'one question to learn'.
- Do not invent customer results, statistics or claims."""
    result = generate_json(AI_SYSTEM, prompt, temperature=0.95, max_tokens=4500)
    ideas = result.get("ideas") if isinstance(result, dict) else None
    if not isinstance(ideas, list) or len(ideas) != 10:
        raise AIProviderError("AI must return exactly 10 ideas")
    required = ("title", "format", "pillar", "goal", "hook", "outline")
    if any(not isinstance(i, dict) or any(not i.get(k) for k in required) for i in ideas):
        raise AIProviderError("Invalid AI content idea contract")
    titles = [str(i["title"]).strip().lower() for i in ideas]
    if len(set(titles)) != 10 or any(_bad_text(i["title"]) for i in ideas):
        raise AIProviderError("AI content ideas were too generic")
    return result


def _enrich_audit(data):
    prompt = f"""Act as a senior social-media growth consultant.

Improve this audit using ONLY the supplied evidence:
{data}

Do not change profile, performance, publishing, score, score_scale, data_source, platform,
business, profile_url or audit_type. Do not create metrics.

Return JSON containing the full audit object. Rewrite the recommendations so they explain:
- what the evidence/problem means for the business;
- why it matters;
- exactly what to change;
- what a good implementation looks like.
Make quick wins and the seven-day plan concrete enough for a business owner to execute.
Do not use generic motivational language."""
    result = generate_json(AI_SYSTEM, prompt, temperature=0.45, max_tokens=4000)
    if not isinstance(result, dict) or not isinstance(result.get("checks"), list):
        raise AIProviderError("Invalid AI audit contract")
    for key in ("profile", "performance", "publishing", "score", "score_scale", "data_source", "platform", "business", "profile_url", "audit_type"):
        result[key] = data.get(key)
    return result


class CaptionGenerateView(generics.GenericAPIView):
    serializer_class = CaptionGenerateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            return Response(_caption(data))
        except AIProviderError:
            return Response(generate_caption(**data))


class ContentIdeasView(generics.GenericAPIView):
    serializer_class = ContentIdeasSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            return Response(_ideas(data))
        except AIProviderError:
            return Response(generate_content_ideas(**data))


class SocialAuditView(generics.GenericAPIView):
    serializer_class = SocialAuditSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            live_result = run_live_social_audit(**data)
        except MetaGraphError:
            live_result = None
        if live_result:
            try:
                live_result = _enrich_audit(live_result)
                live_result["ai_enriched"] = True
            except AIProviderError:
                live_result["ai_enriched"] = False
            return Response(live_result)
        fallback = run_social_audit(**data)
        fallback["data_source"] = "strategy_baseline"
        fallback["live_data_available"] = False
        try:
            fallback = _enrich_audit(fallback)
            fallback["data_source"] = "strategy_baseline"
            fallback["live_data_available"] = False
            fallback["ai_enriched"] = True
        except AIProviderError:
            fallback["ai_enriched"] = False
        return Response(fallback)
