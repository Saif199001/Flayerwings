from django.contrib import admin

from .models import ToolDefinition, ToolDocument, ToolEvent, ToolTemplate


@admin.register(ToolDefinition)
class ToolDefinitionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "active")
    search_fields = ("name", "slug")
    list_filter = ("active",)


@admin.register(ToolTemplate)
class ToolTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "tool", "version", "active")
    list_filter = ("active", "tool")


@admin.register(ToolDocument)
class ToolDocumentAdmin(admin.ModelAdmin):
    list_display = ("document_number", "document_type", "tool", "user", "created_at")
    search_fields = ("document_number", "visitor_id")
    list_filter = ("document_type", "tool", "created_at")


@admin.register(ToolEvent)
class ToolEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "tool", "visitor_id", "created_at")
    list_filter = ("event_type", "tool", "created_at")
