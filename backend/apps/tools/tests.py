from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import ToolDefinition, ToolDocument


User = get_user_model()


@override_settings(SECURE_SSL_REDIRECT=False)
class ToolsApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tool = ToolDefinition.objects.get(slug="gst-invoice-generator")

    def test_tool_list_is_public(self):
        response = self.client.get("/api/v1/tools/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.tool.slug,
            [tool["slug"] for tool in response.data],
        )

    def test_anonymous_document_can_be_saved_and_retrieved_by_visitor(self):
        payload = {
            "tool": self.tool.slug,
            "document_type": "invoice",
            "document_number": "INV-100",
            "visitor_id": "visitor-123",
            "business_details": {"name": "Demo Business"},
            "customer_details": {"name": "Customer"},
            "line_items": [{"name": "Service", "quantity": 1, "amount": 1000}],
            "tax_details": {"gst_rate": 18},
            "totals": {"subtotal": 1000, "tax": 180, "total": 1180},
        }
        response = self.client.post("/api/v1/tools/documents/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ToolDocument.objects.count(), 1)
        history = self.client.get("/api/v1/tools/documents/?visitor_id=visitor-123")
        self.assertEqual(history.status_code, 200)
        self.assertEqual(len(history.data), 1)

    def test_event_can_be_recorded(self):
        response = self.client.post(
            "/api/v1/tools/events/",
            {"tool": self.tool.slug, "event_type": "tool_open", "visitor_id": "visitor-123"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_png_download_event_can_be_recorded(self):
        response = self.client.post(
            "/api/v1/tools/events/",
            {
                "tool": self.tool.slug,
                "event_type": "png_downloaded",
                "visitor_id": "visitor-123",
                "metadata": {"format": "png"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_tool_stats_are_not_public(self):
        response = self.client.get("/api/v1/tools/stats/gst-invoice-generator/")
        self.assertEqual(response.status_code, 403)

    def test_tool_stats_are_forbidden_for_non_admin_users(self):
        user = User.objects.create_user(username="regular-user", password="test-password")
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/v1/tools/stats/gst-invoice-generator/")
        self.assertEqual(response.status_code, 403)

    def test_tool_stats_are_available_to_admin_users(self):
        admin = User.objects.create_user(
            username="admin-user",
            password="test-password",
            is_staff=True,
        )
        self.client.force_authenticate(user=admin)
        response = self.client.get("/api/v1/tools/stats/gst-invoice-generator/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["tool"], self.tool.slug)
        self.assertIn("events", response.data)
        self.assertIn("documents", response.data)
