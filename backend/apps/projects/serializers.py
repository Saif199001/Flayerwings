from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "slug", "project_type", "status", "short_description",
            "description", "url", "featured", "published", "sort_order",
        ]
