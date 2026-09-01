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
Avoid buzzword stuffing and generic marketing language."""

GENERIC_PATTERNS = ("the 3 biggest", "behind the scenes:", "myth vs fact:", "save-worthy checklist", "do not need more information", "the useful approach is to focus on one outcome", "at flayer wings, we use this principle")


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
"""
    result = generate_json(AI_SYSTEM, prompt, temperature=0.85, max_tokens=2200)
    required = ("caption", "hashtags", "hook", "cta", "platform", "format", "strategy_note")
    if not isinstance(result, dict) or any(not result.get(k) for k in required) or not isinstance(result["hashtags"], list):
        raise AIProviderError("Invalid AI caption contract")
    if _bad_text(result["caption"]) or _bad_text(result["hook"]):
        raise AIProviderError("AI caption was too generic")
    result["cta"] = requested_cta if requested_cta else result["cta"]
    result["platform"] = _platform_label(data.get("platform"))
    if requested_cta and requested_cta not in result["caption"]:
        result["caption"] = result["caption"].rstrip() + "\n\n" + requested_cta
    return result


def _ideas(data):
    prompt = f"""Build a 10-post content strategy for this business.
INPUT: {data}
Reason privately about audience problems, workflow friction, objections, desired outcomes, buying questions, proof needs and engagement triggers.
Return JSON with exactly: business, audience, platform, goal, content_pillars, ideas. Each idea: title, format, pillar, goal, hook, outline.
Exactly 10 materially different opportunities; at least 6 formats. Cover education, problem/solution, proof, objection handling, utility, authority and conversion. Titles must describe specific problems, decisions, lessons, use cases or outcomes. Hooks must add curiosity. Outlines must contain concrete production beats. Do not stuff input keywords into every title. Avoid generic templates and invented claims."""
    result = generate_json(AI_SYSTEM, prompt, temperature=0.95, max_tokens=4500)
    ideas = result.get("ideas") if isinstance(result, dict) else None
    required = ("title", "format", "pillar", "goal", "hook", "outline")
    if not isinstance(ideas, list) or len(ideas) != 10 or any(not isinstance(i, dict) or any(not i.get(k) for k in required) for i in ideas):
        raise AIProviderError("Invalid AI content idea contract")
    titles = [str(i["title"]).strip().lower() for i in ideas]
    if len(set(titles)) != 10 or any(_bad_text(i["title"]) for i in ideas):
        raise AIProviderError("AI content ideas were too generic")
    return result


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
        except AIProviderError: result = generate_caption(**data)
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
        except AIProviderError: result = generate_content_ideas(**data)
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
