from django.urls import reverse
from rest_framework.test import APITestCase

from .models import ToolDefinition, ToolDocument


class ToolsApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tool = ToolDefinition.objects.create(slug="gst-invoice-generator", name="GST Invoice Generator")

    def test_tool_list_is_public(self):
        response = self.client.get("/api/v1/tools/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["slug"], self.tool.slug)

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
        response = self.client.post("/api/v1/tools/events/", {"tool": self.tool.slug, "event_type": "tool_open", "visitor_id": "visitor-123"}, format="json")
        self.assertEqual(response.status_code, 201)
