from rest_framework import generics
from rest_framework.response import Response

from .meta_audit import run_live_social_audit
from .meta_client import MetaGraphError
from .services import generate_caption, generate_content_ideas, run_social_audit
from .tool_serializers import CaptionGenerateSerializer, ContentIdeasSerializer, SocialAuditSerializer


class CaptionGenerateView(generics.GenericAPIView):
    serializer_class = CaptionGenerateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(generate_caption(**serializer.validated_data))


class ContentIdeasView(generics.GenericAPIView):
    serializer_class = ContentIdeasSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(generate_content_ideas(**serializer.validated_data))


class SocialAuditView(generics.GenericAPIView):
    serializer_class = SocialAuditSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Meta is an enrichment layer, not a hard dependency. If the target
        # account is unavailable to Business Discovery or Meta is temporarily
        # unavailable, still return a useful strategy audit without inventing
        # live metrics.
        try:
            live_result = run_live_social_audit(**data)
        except MetaGraphError:
            live_result = None

        if live_result:
            return Response(live_result)

        fallback = run_social_audit(**data)
        fallback["data_source"] = "strategy_baseline"
        fallback["live_data_available"] = False
        return Response(fallback)
