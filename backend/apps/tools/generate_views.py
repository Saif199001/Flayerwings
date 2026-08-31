from rest_framework import generics
from rest_framework.response import Response

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
        return Response(run_social_audit(**serializer.validated_data))
