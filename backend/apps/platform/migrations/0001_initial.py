import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Workspace",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField(max_length=160, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="owned_workspaces", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["owner", "is_active"], name="platform_wo_owner_i_0c8d8f_idx"),
                    models.Index(fields=["created_at"], name="platform_wo_created_7d9f4e_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("action", models.CharField(max_length=100)),
                ("resource_type", models.CharField(blank=True, max_length=100)),
                ("resource_id", models.CharField(blank=True, max_length=150)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="platform_audit_logs", to=settings.AUTH_USER_MODEL)),
                ("workspace", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="audit_logs", to="platform.workspace")),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["workspace", "created_at"], name="platform_au_workspac_11f9fb_idx"),
                    models.Index(fields=["actor", "created_at"], name="platform_au_actor_i_0e0f1c_idx"),
                    models.Index(fields=["action", "created_at"], name="platform_au_action_8d7df6_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="ProductSubscription",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("product_key", models.SlugField(max_length=80)),
                ("plan_key", models.SlugField(max_length=80)),
                ("status", models.CharField(choices=[("trialing", "Trialing"), ("active", "Active"), ("past_due", "Past due"), ("canceled", "Canceled"), ("expired", "Expired")], default="trialing", max_length=20)),
                ("trial_ends_at", models.DateTimeField(blank=True, null=True)),
                ("current_period_start", models.DateTimeField(blank=True, null=True)),
                ("current_period_end", models.DateTimeField(blank=True, null=True)),
                ("provider", models.CharField(blank=True, max_length=40)),
                ("provider_customer_id", models.CharField(blank=True, max_length=150)),
                ("provider_subscription_id", models.CharField(blank=True, max_length=150)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("workspace", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subscriptions", to="platform.workspace")),
            ],
            options={
                "indexes": [
                    models.Index(fields=["workspace", "status"], name="platform_pr_workspac_3e2d93_idx"),
                    models.Index(fields=["product_key", "status"], name="platform_pr_product__d70e62_idx"),
                    models.Index(fields=["current_period_end"], name="platform_pr_current_7f6e0a_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="WorkspaceMembership",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("role", models.CharField(choices=[("owner", "Owner"), ("admin", "Admin"), ("member", "Member"), ("viewer", "Viewer")], default="member", max_length=20)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="workspace_memberships", to=settings.AUTH_USER_MODEL)),
                ("workspace", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="platform.workspace")),
            ],
            options={
                "indexes": [
                    models.Index(fields=["user", "is_active"], name="platform_ws_user_id_8a2f62_idx"),
                    models.Index(fields=["workspace", "is_active"], name="platform_ws_workspac_5b70a4_idx"),
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="workspacemembership",
            constraint=models.UniqueConstraint(fields=("workspace", "user"), name="unique_workspace_member"),
        ),
        migrations.AddConstraint(
            model_name="productsubscription",
            constraint=models.UniqueConstraint(fields=("workspace", "product_key"), name="unique_workspace_product_subscription"),
        ),
    ]
