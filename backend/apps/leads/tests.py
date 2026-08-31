from django.test import TestCase
from django.urls import reverse

from .models import Lead


class LeadApiTests(TestCase):
    def test_create_contact_lead(self):
        response = self.client.post(
            reverse("lead-create"),
            data={
                "name": "Test User",
                "email": "test@example.com",
                "lead_type": "contact",
                "source": "website",
                "message": "Hello",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.get()
        self.assertEqual(lead.status, Lead.Status.NEW)
        self.assertEqual(lead.name, "Test User")
        self.assertEqual(lead.source, "website")

    def test_create_tool_lead(self):
        response = self.client.post(
            reverse("lead-create"),
            data={
                "name": "Tool User",
                "email": "tool@example.com",
                "phone": "9999999999",
                "company": "Example Co",
                "lead_type": "tool",
                "source": "content-ideas",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.get()
        self.assertEqual(lead.lead_type, Lead.LeadType.TOOL)
        self.assertEqual(lead.source, "content-ideas")
        self.assertEqual(lead.status, Lead.Status.NEW)

    def test_social_audit_requires_profile_url(self):
        response = self.client.post(
            reverse("lead-create"),
            data={
                "name": "Test User",
                "email": "test@example.com",
                "lead_type": "social_audit",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("social_profile_url", response.json())
        self.assertEqual(Lead.objects.count(), 0)

    def test_social_audit_accepts_profile_url(self):
        response = self.client.post(
            reverse("lead-create"),
            data={
                "name": "Audit User",
                "email": "audit@example.com",
                "lead_type": "social_audit",
                "social_profile_url": "https://www.instagram.com/example/",
                "source": "social-media-audit",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(Lead.objects.get().social_profile_url, "https://www.instagram.com/example/")

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            reverse("lead-create"),
            data={
                "name": "Test User",
                "email": "not-an-email",
                "lead_type": "contact",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json())
        self.assertEqual(Lead.objects.count(), 0)

    def test_invalid_lead_type_is_rejected(self):
        response = self.client.post(
            reverse("lead-create"),
            data={
                "name": "Test User",
                "email": "test@example.com",
                "lead_type": "not-a-valid-type",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("lead_type", response.json())
        self.assertEqual(Lead.objects.count(), 0)

    def test_client_cannot_set_internal_status(self):
        response = self.client.post(
            reverse("lead-create"),
            data={
                "name": "Test User",
                "email": "test@example.com",
                "lead_type": "contact",
                "status": "converted",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        lead = Lead.objects.get()
        self.assertEqual(lead.status, Lead.Status.NEW)
