from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "project_type", "status", "featured", "published", "sort_order")
    list_filter = ("project_type", "status", "featured", "published")
    search_fields = ("title", "slug", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
