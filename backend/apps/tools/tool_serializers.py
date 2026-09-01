from rest_framework import serializers


class CaptionGenerateSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=300)
    tone = serializers.CharField(max_length=60, required=False, default="professional")
    platform = serializers.CharField(max_length=40, required=False, default="instagram")
    audience = serializers.CharField(max_length=160, required=False, default="your target audience")
    goal = serializers.CharField(max_length=60, required=False, default="engagement")
    content_type = serializers.CharField(max_length=60, required=False, default="educational")
    cta = serializers.CharField(max_length=160, required=False, default="")
    business = serializers.CharField(max_length=200, required=False, default="your business")


class ContentIdeasSerializer(serializers.Serializer):
    business = serializers.CharField(max_length=200)
    audience = serializers.CharField(max_length=200, required=False, default="general audience")
    platform = serializers.CharField(max_length=40, required=False, default="instagram")
    goal = serializers.CharField(max_length=60, required=False, default="brand awareness")
    industry = serializers.CharField(max_length=120, required=False, default="")
    offer = serializers.CharField(max_length=200, required=False, default="")


class SocialAuditSerializer(serializers.Serializer):
    business = serializers.CharField(max_length=200)
    profile_url = serializers.URLField(max_length=500)
