from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import ProductSubscription, Workspace, WorkspaceMembership


class PlatformAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="StrongPass123!",
        )
        self.other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(self.user)

    def test_create_workspace_creates_owner_membership(self):
        response = self.client.post(
            "/api/v1/platform/workspaces/",
            {"name": "Ajniha Stay"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        workspace = Workspace.objects.get(name="Ajniha Stay")
        membership = WorkspaceMembership.objects.get(workspace=workspace, user=self.user)
        self.assertEqual(membership.role, WorkspaceMembership.ROLE_OWNER)
        self.assertEqual(response.data["role"], "owner")

    def test_workspace_list_isolated_by_membership(self):
        own = Workspace.objects.create(name="Own", slug="own", owner=self.user)
        WorkspaceMembership.objects.create(workspace=own, user=self.user, role="owner")
        foreign = Workspace.objects.create(name="Foreign", slug="foreign", owner=self.other)
        WorkspaceMembership.objects.create(workspace=foreign, user=self.other, role="owner")

        response = self.client.get("/api/v1/platform/workspaces/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["slug"] for item in response.data["data"]], ["own"])

    def test_workspace_detail_denies_non_member(self):
        foreign = Workspace.objects.create(name="Foreign", slug="foreign", owner=self.other)
        WorkspaceMembership.objects.create(workspace=foreign, user=self.other, role="owner")
        response = self.client.get(f"/api/v1/platform/workspaces/{foreign.id}/")
        self.assertEqual(response.status_code, 404)

    def test_subscription_is_unique_per_workspace_product(self):
        workspace = Workspace.objects.create(name="Own", slug="own", owner=self.user)
        first = ProductSubscription.objects.create(
            workspace=workspace,
            product_key="rent-manager",
            plan_key="starter",
        )
        with self.assertRaises(Exception):
            ProductSubscription.objects.create(
                workspace=workspace,
                product_key="rent-manager",
                plan_key="pro",
            )
        self.assertEqual(first.plan_key, "starter")
