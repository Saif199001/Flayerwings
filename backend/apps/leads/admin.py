from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "lead_type", "status", "created_at")
    list_filter = ("lead_type", "status", "created_at")
    search_fields = ("name", "email", "company", "phone")
    readonly_fields = ("created_at", "updated_at")
