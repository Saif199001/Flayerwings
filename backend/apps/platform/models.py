import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Workspace(models.Model):
    """Tenant boundary shared by all Flayer Wings SaaS products."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_workspaces",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["owner", "is_active"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name


class WorkspaceMembership(models.Model):
    ROLE_OWNER = "owner"
    ROLE_ADMIN = "admin"
    ROLE_MEMBER = "member"
    ROLE_VIEWER = "viewer"
    ROLE_CHOICES = (
        (ROLE_OWNER, "Owner"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_MEMBER, "Member"),
        (ROLE_VIEWER, "Viewer"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workspace_memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["workspace", "user"], name="unique_workspace_member"),
        ]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["workspace", "is_active"]),
        ]

    def clean(self):
        if self.role == self.ROLE_OWNER and self.workspace.owner_id != self.user_id:
            raise ValidationError("Workspace owner membership must belong to the workspace owner.")

    def __str__(self):
        return f"{self.user} @ {self.workspace} ({self.role})"


class ProductSubscription(models.Model):
    STATUS_TRIALING = "trialing"
    STATUS_ACTIVE = "active"
    STATUS_PAST_DUE = "past_due"
    STATUS_CANCELED = "canceled"
    STATUS_EXPIRED = "expired"
    STATUS_CHOICES = (
        (STATUS_TRIALING, "Trialing"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_PAST_DUE, "Past due"),
        (STATUS_CANCELED, "Canceled"),
        (STATUS_EXPIRED, "Expired"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    product_key = models.SlugField(max_length=80)
    plan_key = models.SlugField(max_length=80)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TRIALING)
    trial_ends_at = models.DateTimeField(blank=True, null=True)
    current_period_start = models.DateTimeField(blank=True, null=True)
    current_period_end = models.DateTimeField(blank=True, null=True)
    provider = models.CharField(max_length=40, blank=True)
    provider_customer_id = models.CharField(max_length=150, blank=True)
    provider_subscription_id = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "product_key"],
                name="unique_workspace_product_subscription",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "status"]),
            models.Index(fields=["product_key", "status"]),
            models.Index(fields=["current_period_end"]),
        ]

    def __str__(self):
        return f"{self.workspace} - {self.product_key} ({self.plan_key})"


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="audit_logs",
        blank=True,
        null=True,
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="platform_audit_logs",
        blank=True,
        null=True,
    )
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=100, blank=True)
    resource_id = models.CharField(max_length=150, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["workspace", "created_at"]),
            models.Index(fields=["actor", "created_at"]),
            models.Index(fields=["action", "created_at"]),
        ]

    def __str__(self):
        return f"{self.action} - {self.resource_type}:{self.resource_id}"
