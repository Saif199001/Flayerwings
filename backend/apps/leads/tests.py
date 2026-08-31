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
        self.assertEqual(Lead.objects.get().status, Lead.Status.NEW)

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
