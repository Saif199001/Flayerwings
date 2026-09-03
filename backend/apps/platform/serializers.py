from rest_framework import serializers

from .models import ProductSubscription, Workspace, WorkspaceMembership


class WorkspaceSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ("id", "name", "slug", "role", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "slug", "role", "is_active", "created_at", "updated_at")

    def get_role(self, obj):
        user = self.context["request"].user
        membership = obj.memberships.filter(user=user, is_active=True).first()
        return membership.role if membership else None


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = WorkspaceMembership
        fields = ("id", "user_id", "username", "role", "is_active", "created_at")
        read_only_fields = fields


class ProductSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubscription
        fields = (
            "id", "product_key", "plan_key", "status", "trial_ends_at",
            "current_period_start", "current_period_end", "provider",
            "created_at", "updated_at",
        )
        read_only_fields = fields
