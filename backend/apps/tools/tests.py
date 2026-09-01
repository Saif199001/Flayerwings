from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Tool


@override_settings(SECURE_SSL_REDIRECT=False)
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

    def test_caption_generator_returns_publishable_package(self):
        response = self.client.post(
            reverse("caption-generate"),
            data={
                "business": "Flayer Wings",
                "topic": "AI automation for modern businesses",
                "audience": "startup founders",
                "goal": "leads",
                "content_type": "case study",
                "tone": "professional",
                "platform": "linkedin",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["caption"])
        self.assertTrue(payload["hook"])
        self.assertTrue(payload["cta"])
        self.assertTrue(payload["hashtags"])
        self.assertEqual(payload["platform"], "LinkedIn")
        self.assertNotIn("{business}", payload["caption"])
        self.assertNotIn("{audience}", payload["caption"])
        self.assertIn("AI automation", payload["caption"])
        self.assertIn("startup founders", payload["caption"].lower())
        self.assertGreaterEqual(len(payload["caption"].split()), 35)

    def test_caption_generator_uses_requested_cta_and_platform(self):
        response = self.client.post(
            reverse("caption-generate"),
            data={
                "business": "Flayer Wings",
                "topic": "launching a social media manager",
                "audience": "startups, freelancers and brand owners",
                "goal": "sales",
                "content_type": "promotional",
                "tone": "bold",
                "platform": "instagram",
                "cta": "Book a free demo",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["platform"], "Instagram")
        self.assertEqual(payload["cta"], "Book a free demo")
        self.assertIn("Book a free demo", payload["caption"])
        self.assertNotIn("a startups", payload["caption"].lower())
        self.assertNotIn("looking to launching", payload["caption"].lower())

    def test_content_ideas_returns_structured_ideas(self):
        response = self.client.post(
            reverse("content-ideas-generate"),
            data={
                "business": "Flayer Wings",
                "audience": "startup founders",
                "industry": "SaaS",
                "offer": "social media management",
                "goal": "leads",
                "platform": "instagram",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["ideas"]), 10)
        self.assertEqual(len(payload["content_pillars"]), 5)
        for idea in payload["ideas"]:
            self.assertTrue(idea["title"])
            self.assertTrue(idea["format"])
            self.assertTrue(idea["pillar"])
            self.assertTrue(idea["goal"])
            self.assertTrue(idea["hook"])
            self.assertTrue(idea["outline"])
            self.assertNotIn("{business}", idea["title"] + idea["hook"] + idea["outline"])
            self.assertNotIn("{business}", idea["title"] + idea["hook"] + idea["outline"])
        self.assertIn("SaaS", payload["ideas"][0]["title"])
        self.assertIn("social media management", payload["ideas"][1]["title"].lower())

    def test_social_audit_returns_action_plan_without_fake_metrics(self):
        response = self.client.post(
            reverse("social-audit-generate"),
            data={
                "business": "Flayer Wings",
                "profile_url": "https://instagram.com/flayerwings",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["audit_type"], "strategy_baseline")
        self.assertEqual(payload["platform"], "Instagram")
        self.assertEqual(len(payload["checks"]), 6)
        self.assertEqual(len(payload["quick_wins"]), 4)
        self.assertEqual(len(payload["seven_day_plan"]), 7)
        self.assertIn("does not scrape", payload["confidence_note"])
