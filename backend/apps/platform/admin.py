from django.contrib import admin

from .models import AuditLog, ProductSubscription, Workspace, WorkspaceMembership


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "is_active", "created_at")
    search_fields = ("name", "slug", "owner__username", "owner__email")
    list_filter = ("is_active",)


@admin.register(WorkspaceMembership)
class WorkspaceMembershipAdmin(admin.ModelAdmin):
    list_display = ("workspace", "user", "role", "is_active", "created_at")
    search_fields = ("workspace__name", "user__username", "user__email")
    list_filter = ("role", "is_active")


@admin.register(ProductSubscription)
class ProductSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("workspace", "product_key", "plan_key", "status", "current_period_end")
    search_fields = ("workspace__name", "product_key", "provider_customer_id", "provider_subscription_id")
    list_filter = ("product_key", "status", "provider")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "workspace", "actor", "resource_type", "resource_id")
    search_fields = ("action", "resource_type", "resource_id", "actor__username", "actor__email")
    list_filter = ("action", "resource_type")
    readonly_fields = [field.name for field in AuditLog._meta.fields]
