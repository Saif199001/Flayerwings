from rest_framework import serializers

from .models import ToolDefinition, ToolDocument, ToolEvent, ToolTemplate


class ToolDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolDefinition
        fields = ["slug", "name", "description", "active"]


class ToolTemplateSerializer(serializers.ModelSerializer):
    tool = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = ToolTemplate
        fields = ["id", "tool", "name", "version", "config", "active"]
        read_only_fields = ["id"]


class ToolDocumentSerializer(serializers.ModelSerializer):
    tool = serializers.SlugRelatedField(slug_field="slug", queryset=ToolDefinition.objects.filter(active=True))

    class Meta:
        model = ToolDocument
        fields = ["id", "tool", "template", "document_type", "document_number", "visitor_id", "business_details", "customer_details", "line_items", "tax_details", "totals", "metadata", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "user"]

    def validate(self, attrs):
        if not attrs.get("document_number"):
            raise serializers.ValidationError({"document_number": "Document number is required."})
        if attrs.get("template") and attrs["template"].tool_id != attrs["tool"].id:
            raise serializers.ValidationError({"template": "Template does not belong to the selected tool."})
        return attrs

    def validate_line_items(self, value):
        if not isinstance(value, list) or len(value) > 100:
            raise serializers.ValidationError("line_items must be a list with at most 100 items.")
        return value


class ToolEventSerializer(serializers.ModelSerializer):
    tool = serializers.SlugRelatedField(slug_field="slug", queryset=ToolDefinition.objects.filter(active=True))

    class Meta:
        model = ToolEvent
        fields = ["id", "tool", "event_type", "document", "visitor_id", "session_id", "source", "medium", "campaign", "landing_path", "referrer", "metadata", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_metadata(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("metadata must be an object.")
        return value
