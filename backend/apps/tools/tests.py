from django.test import TestCase
from django.urls import reverse

from .models import Tool


class ToolApiTests(TestCase):
    def setUp(self):
        Tool.objects.create(
            name="Caption Generator",
            slug="caption-generator",
            description="Generate captions.",
            is_active=True,
        )
        Tool.objects.create(
            name="Disabled Tool",
            slug="disabled-tool",
            description="Hidden.",
            is_active=False,
        )

    def test_list_returns_only_active_tools(self):
        response = self.client.get(reverse("tool-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_detail_returns_active_tool(self):
        response = self.client.get(reverse("tool-detail", kwargs={"slug": "caption-generator"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slug"], "caption-generator")

    def test_detail_hides_inactive_tool(self):
        response = self.client.get(reverse("tool-detail", kwargs={"slug": "disabled-tool"}))
        self.assertEqual(response.status_code, 404)
