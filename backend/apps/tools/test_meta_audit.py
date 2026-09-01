from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .meta_audit import _build_meta_audit
from .models import Tool


@override_settings(SECURE_SSL_REDIRECT=False)
class MetaSocialAuditTests(TestCase):
    def setUp(self):
        Tool.objects.create(
            name="Social Media Audit",
            slug="social-media-audit",
            description="Audit an Instagram profile.",
            is_active=True,
        )

    def test_meta_audit_uses_live_profile_evidence(self):
        profile = {
            "id": "123",
            "username": "demo_brand",
            "name": "Demo Brand",
            "biography": "AI automation for growing businesses. Book a demo.",
            "website": "https://example.com",
            "followers_count": 1000,
            "follows_count": 120,
            "media_count": 40,
            "media": {
                "data": [
                    {"id": "1", "caption": "Client result: 30% faster workflow", "media_type": "IMAGE", "media_product_type": "FEED", "permalink": "https://instagram.com/p/1", "timestamp": "2026-08-30T10:00:00+0000", "like_count": 80, "comments_count": 10},
                    {"id": "2", "caption": "Three mistakes founders make", "media_type": "VIDEO", "media_product_type": "REELS", "permalink": "https://instagram.com/reel/2", "timestamp": "2026-08-27T10:00:00+0000", "like_count": 140, "comments_count": 20},
                ]
            },
        }
        with patch("apps.tools.meta_audit.get_business_discovery", return_value=profile), patch("apps.tools.meta_audit.meta_graph_configured", return_value=True):
            result = _build_meta_audit("Demo Brand", "https://instagram.com/demo_brand")

        self.assertEqual(result["audit_type"], "meta_live_profile_audit")
        self.assertEqual(result["data_source"], "Meta Graph API Business Discovery")
        self.assertEqual(result["profile"]["followers_count"], 1000)
        self.assertEqual(result["performance"]["sample_size"], 2)
        self.assertEqual(result["performance"]["top_posts"][0]["interactions"], 160)
        self.assertTrue(result["performance"]["average_engagement_rate_percent"] > 0)
        self.assertIn("live data", result["confidence_note"])

    @patch("apps.tools.meta_audit.get_business_discovery")
    @patch("apps.tools.meta_audit.meta_graph_configured", return_value=True)
    def test_api_returns_live_meta_audit(self, _configured, discovery):
        discovery.return_value = {
            "id": "123",
            "username": "demo_brand",
            "name": "Demo Brand",
            "biography": "AI automation for growing businesses. Book a demo.",
            "website": "https://example.com",
            "followers_count": 1000,
            "follows_count": 120,
            "media_count": 2,
            "media": {"data": []},
        }
        response = self.client.post(
            reverse("social-audit-generate"),
            data={"business": "Demo Brand", "profile_url": "https://instagram.com/demo_brand"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["audit_type"], "meta_live_profile_audit")
