from rest_framework import generics
from rest_framework.response import Response

from .ai_client import AIProviderError, generate_json
from .meta_audit import run_live_social_audit
from .meta_client import MetaGraphError
from .services import generate_caption, generate_content_ideas, run_social_audit
from .tool_serializers import CaptionGenerateSerializer, ContentIdeasSerializer, SocialAuditSerializer

AI_SYSTEM = "You are the Flayer Wings social media strategist. Return JSON only. Be specific and useful. Never invent metrics, customer results, testimonials, platform data, or facts not supplied."


def _caption(data):
    prompt = f'''Create one publish-ready social media caption using this input: {data}.
Return JSON with exactly: caption, hashtags, hook, cta, platform, format, strategy_note.
Make it natural, platform-specific, audience-specific, and non-generic. Do not invent claims.'''
    result = generate_json(AI_SYSTEM, prompt, temperature=0.8, max_tokens=1800)
    if not isinstance(result, dict) or any(not result.get(k) for k in ("caption", "hashtags", "hook", "cta", "platform", "format", "strategy_note")):
        raise AIProviderError("Invalid AI caption contract")
    if not isinstance(result["hashtags"], list):
        raise AIProviderError("Invalid AI hashtag contract")
    return result


def _ideas(data):
    prompt = f'''Create exactly 10 distinct social-media content opportunities from this input: {data}.
Return JSON with exactly: business, audience, platform, goal, content_pillars, ideas.
Each idea must contain title, format, pillar, goal, hook, outline.
Use different audience problems, objections, decisions, use cases, proof, education and conversion angles. Do not use the same template with substituted words.'''
    result = generate_json(AI_SYSTEM, prompt, temperature=0.9, max_tokens=3500)
    ideas = result.get("ideas") if isinstance(result, dict) else None
    if not isinstance(ideas, list) or len(ideas) != 10:
        raise AIProviderError("AI must return exactly 10 ideas")
    required = ("title", "format", "pillar", "goal", "hook", "outline")
    if any(not isinstance(i, dict) or any(not i.get(k) for k in required) for i in ideas):
        raise AIProviderError("Invalid AI content idea contract")
    return result


def _enrich_audit(data):
    prompt = f'''Improve this social audit strategically using only the supplied evidence: {data}.
Do not change profile, performance, publishing, score, data_source, platform, business, profile_url or audit_type.
Return JSON containing the full audit object. Make checks, quick_wins, seven_day_plan and next_step specific to the supplied evidence. Never invent numbers or facts.'''
    result = generate_json(AI_SYSTEM, prompt, temperature=0.5, max_tokens=3500)
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
