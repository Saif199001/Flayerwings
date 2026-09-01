from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .meta_client import MetaGraphError
from .models import Tool


CAPTION_AI_RESULT = {
    "caption": "AI automation can remove repetitive work from a growing team when the workflow is designed around a real bottleneck. For startup founders, the useful question is not whether AI is impressive; it is which task should stop consuming human attention first. Start by mapping one weekly process, remove the manual handoffs, add a clear review step, and measure the time saved internally. Flayer Wings uses this approach to turn AI automation into a practical business workflow rather than another tool to manage. Book a free demo if you want to see how the process can fit your team.",
    "hashtags": ["#FlayerWings", "#AIAutomation", "#Startups", "#Leads"],
    "hook": "The best AI automation opportunity is usually the repetitive task your team has stopped noticing.",
    "cta": "What workflow would you automate first?",
    "platform": "LinkedIn",
    "format": "Text post",
    "strategy_note": "Lead with a business insight and give the reader a practical next step.",
}


CONTENT_IDEAS_AI_RESULT = {
    "business": "Flayer Wings",
    "audience": "startup founders",
    "platform": "instagram",
    "goal": "leads",
    "content_pillars": ["Education", "Authority", "Proof", "Brand", "Utility"],
    "ideas": [
        {"title": "Why startup founders keep rebuilding the same workflow", "format": "Carousel", "pillar": "Education", "goal": "Reach", "hook": "The bottleneck may be the process, not the people using it.", "outline": "Show the repeated task → identify the hidden handoff → explain the cost → give a simpler workflow."},
        {"title": "What a social media management workflow should automate first", "format": "Reel", "pillar": "Utility", "goal": "Trust", "hook": "Do not automate everything at once; start where repetition is highest.", "outline": "Map the weekly workflow → rank repetitive steps → choose the first automation → show the review point."},
        {"title": "The hidden cost of creating every post from scratch", "format": "Text Post", "pillar": "Authority", "goal": "Saves", "hook": "The visible task is writing; the expensive part is deciding what to write next.", "outline": "Describe the decision load → separate planning from production → show a repeatable content system → give a starting rule."},
        {"title": "How to turn social media activity into lead generation", "format": "Carousel", "pillar": "Conversion", "goal": "Leads", "hook": "More posts do not automatically create more enquiries.", "outline": "Define the desired enquiry → connect content to one problem → add one CTA → show the next step."},
        {"title": "Which questions should a social media manager answer before you buy", "format": "Poll", "pillar": "Objection", "goal": "Trust", "hook": "The right questions reveal whether a tool will actually remove work.", "outline": "Ask about workflow fit → reporting → approvals → publishing → invite the audience to rank the priority."},
        {"title": "Before and after: replacing scattered content tasks with one workflow", "format": "Case Study", "pillar": "Proof", "goal": "Leads", "hook": "The biggest improvement can be fewer handoffs, not more content.", "outline": "Show the starting workflow → mark each handoff → redesign the sequence → explain what evidence to compare."},
        {"title": "The product decision rule we use when building Flayer Wings", "format": "Founder Post", "pillar": "Brand", "goal": "Connection", "hook": "A useful product should remove a recurring decision, not create another dashboard.", "outline": "State the principle → explain the problem it prevents → give one product example → describe who benefits."},
        {"title": "A seven-question checklist for choosing social media software", "format": "Checklist", "pillar": "Utility", "goal": "Saves", "hook": "Use these questions before comparing feature lists.", "outline": "List seven buying questions → explain why each matters → flag common warning signs → give a final decision rule."},
        {"title": "How to build a weekly content system in one afternoon", "format": "Tutorial", "pillar": "Education", "goal": "Understanding", "hook": "A repeatable system starts with fewer decisions, not more ideas.", "outline": "Choose three audience problems → assign formats → batch outlines → schedule review → prepare the next batch."},
        {"title": "What stops small teams from getting value from social media tools", "format": "Interview", "pillar": "Research", "goal": "Engagement", "hook": "The biggest blocker may be the workflow around the tool.", "outline": "Ask three operators about their bottleneck → group answers → identify recurring friction → use responses for the next content batch."},
    ],
}


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

    @patch("apps.tools.generate_views.generate_json", return_value=CAPTION_AI_RESULT)
    def test_caption_generator_returns_publishable_package(self, mock_ai):
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
        mock_ai.assert_called_once()

    @patch("apps.tools.generate_views.generate_json", return_value=CAPTION_AI_RESULT)
    def test_caption_generator_uses_requested_cta_and_platform(self, mock_ai):
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
        mock_ai.assert_called_once()

    @patch("apps.tools.generate_views.generate_json", return_value=CONTENT_IDEAS_AI_RESULT)
    def test_content_ideas_returns_structured_ideas(self, mock_ai):
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
        titles = []
        for idea in payload["ideas"]:
            self.assertTrue(idea["title"])
            self.assertTrue(idea["format"])
            self.assertTrue(idea["pillar"])
            self.assertTrue(idea["goal"])
            self.assertTrue(idea["hook"])
            self.assertTrue(idea["outline"])
            text = idea["title"] + idea["hook"] + idea["outline"]
            self.assertNotIn("{business}", text)
            self.assertNotIn("{audience}", text)
            titles.append(idea["title"].lower())
        self.assertEqual(len(set(titles)), 10)
        self.assertIn("saas", (payload["ideas"][1]["title"] + payload["ideas"][1]["outline"]).lower())
        self.assertIn("social media management", payload["ideas"][1]["title"].lower())
        self.assertIn("lead generation", payload["ideas"][3]["title"].lower())
        mock_ai.assert_called_once()

    @patch("apps.tools.generate_views.run_live_social_audit", return_value=None)
    def test_social_audit_returns_action_plan_without_fake_metrics(self, mock_live_audit):
        response = self.client.post(
            reverse("social-audit-generate"),
            data={
                "business": "Flayer Wings",
                "profile_url": "https://instagram.com/flayerwings",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_live_audit.assert_called_once_with(
            business="Flayer Wings",
            profile_url="https://instagram.com/flayerwings",
        )
        payload = response.json()
        self.assertEqual(payload["audit_type"], "strategy_baseline")
        self.assertEqual(payload["platform"], "Instagram")
        self.assertEqual(len(payload["checks"]), 6)
        self.assertEqual(len(payload["quick_wins"]), 4)
        self.assertEqual(len(payload["seven_day_plan"]), 7)
        self.assertIn("does not scrape", payload["confidence_note"])

    @patch("apps.tools.generate_views.run_live_social_audit", side_effect=MetaGraphError("Instagram account is not available to live analysis."))
    def test_social_audit_falls_back_when_meta_is_unavailable(self, mock_live_audit):
        response = self.client.post(
            reverse("social-audit-generate"),
            data={
                "business": "Flayer Wings",
                "profile_url": "https://instagram.com/flayerwings",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_live_audit.assert_called_once()
        payload = response.json()
        self.assertEqual(payload["audit_type"], "strategy_baseline")
        self.assertEqual(payload["data_source"], "strategy_baseline")
        self.assertFalse(payload["live_data_available"])
        self.assertEqual(len(payload["seven_day_plan"]), 7)
