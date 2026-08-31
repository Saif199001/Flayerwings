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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["lead_type", "created_at"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.name} <{self.email}>"
