from django.test import TestCase, override_settings
from django.urls import reverse

from .models import SiteContent


@override_settings(SECURE_SSL_REDIRECT=False)
class SiteContentApiTests(TestCase):
    def setUp(self):
        SiteContent.objects.create(key="home-hero", title="Build. Automate. Grow.", body="Test", is_published=True)
        SiteContent.objects.create(key="draft", title="Draft", body="Hidden", is_published=False)

    def test_list_returns_only_published_content(self):
        response = self.client.get(reverse("content-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["key"], "home-hero")

    def test_detail_returns_published_content(self):
        response = self.client.get(reverse("content-detail", kwargs={"key": "home-hero"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Build. Automate. Grow.")

    def test_detail_hides_unpublished_content(self):
        response = self.client.get(reverse("content-detail", kwargs={"key": "draft"}))
        self.assertEqual(response.status_code, 404)
