from rest_framework import serializers

from .models import Lead


class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            "name",
            "email",
            "phone",
            "company",
            "website",
            "lead_type",
            "source",
            "message",
            "social_profile_url",
        ]

    def validate(self, attrs):
        lead_type = attrs.get("lead_type")
        if lead_type == Lead.LeadType.SOCIAL_AUDIT and not attrs.get("social_profile_url"):
            raise serializers.ValidationError({"social_profile_url": "A social profile URL is required for an audit request."})
        return attrs


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"
        read_only_fields = ["id", "status", "notes", "created_at", "updated_at"]
