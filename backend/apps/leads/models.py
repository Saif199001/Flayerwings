from django.db import models


class Lead(models.Model):
    class LeadType(models.TextChoices):
        CONTACT = "contact", "Contact"
        SOCIAL_AUDIT = "social_audit", "Social Media Audit"
        TOOL = "tool", "Free Tool"
        PROJECT = "project", "Project Inquiry"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUALIFIED = "qualified", "Qualified"
        CONVERTED = "converted", "Converted"
        LOST = "lost", "Lost"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=160, blank=True)
    website = models.URLField(blank=True)
    lead_type = models.CharField(max_length=30, choices=LeadType.choices, default=LeadType.CONTACT)
    source = models.CharField(max_length=80, blank=True)
    message = models.TextField(blank=True)
    social_profile_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    notes = models.TextField(blank=True)
    tool_slug = models.CharField(max_length=80, blank=True, db_index=True)
    tool_document_id = models.UUIDField(null=True, blank=True, db_index=True)
    visitor_id = models.CharField(max_length=100, blank=True, db_index=True)
    session_id = models.CharField(max_length=100, blank=True, db_index=True)
    landing_path = models.CharField(max_length=500, blank=True)
    attribution = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"], name="leads_lead_status_0d2a7d_idx"),
            models.Index(fields=["lead_type", "created_at"], name="leads_lead_lead_typ_8e5d45_idx"),
            models.Index(fields=["email"], name="leads_lead_email_4b9f24_idx"),
            models.Index(fields=["tool_slug", "created_at"], name="leads_lead_tool_slu_2d6a61_idx"),
        ]

    def __str__(self):
        return f"{self.name} <{self.email}>"
