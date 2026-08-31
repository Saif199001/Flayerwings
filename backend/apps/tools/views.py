from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tool
from .services import generate_caption, generate_content_ideas, run_social_audit
from .serializers import ToolSerializer


class ToolListView(generics.ListAPIView):
    serializer_class = ToolSerializer

    def get_queryset(self):
        return Tool.objects.filter(is_active=True)


class ToolDetailView(generics.RetrieveAPIView):
    serializer_class = ToolSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Tool.objects.filter(is_active=True)


class SocialAuditRequestSerializer(serializers.Serializer):
    business = serializers.CharField(max_length=160)
    profile_url = serializers.URLField()


class CaptionRequestSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=280)
    tone = serializers.CharField(max_length=60, required=False, default="professional")
    platform = serializers.CharField(max_length=40, required=False, default="instagram")


class ContentIdeasRequestSerializer(serializers.Serializer):
    business = serializers.CharField(max_length=160)
    audience = serializers.CharField(max_length=160, required=False, default="general audience")
    platform = serializers.CharField(max_length=40, required=False, default="instagram")


class SocialAuditGenerateView(APIView):
    def post(self, request):
        serializer = SocialAuditRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(run_social_audit(**serializer.validated_data))


class CaptionGenerateView(APIView):
    def post(self, request):
        serializer = CaptionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(generate_caption(**serializer.validated_data))


class ContentIdeasGenerateView(APIView):
    def post(self, request):
        serializer = ContentIdeasRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(generate_content_ideas(**serializer.validated_data))
