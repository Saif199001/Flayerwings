from rest_framework import serializers


class CaptionGenerateSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=300)
    tone = serializers.CharField(max_length=60, required=False, default="professional")
    platform = serializers.CharField(max_length=40, required=False, default="instagram")


class ContentIdeasSerializer(serializers.Serializer):
    business = serializers.CharField(max_length=200)
    audience = serializers.CharField(max_length=200, required=False, default="general audience")
    platform = serializers.CharField(max_length=40, required=False, default="instagram")


class SocialAuditSerializer(serializers.Serializer):
    business = serializers.CharField(max_length=200)
    profile_url = serializers.URLField(max_length=500)
