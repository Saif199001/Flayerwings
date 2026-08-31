from rest_framework import serializers

from .models import Tool


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ["id", "name", "slug", "description", "is_active"]
        read_only_fields = ["id"]
