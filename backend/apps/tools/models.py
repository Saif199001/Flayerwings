import uuid

from django.conf import settings
from django.db import models


class ToolDefinition(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ToolTemplate(models.Model):
    tool = models.ForeignKey(ToolDefinition, on_delete=models.CASCADE, related_name="templates")
    name = models.CharField(max_length=100)
    version = models.PositiveIntegerField(default=1)
    config = models.JSONField(default=dict)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tool", "name", "version"], name="uniq_tool_template_version")]
        indexes = [models.Index(fields=["tool", "active"])]

    def __str__(self):
        return f"{self.tool.slug}: {self.name} v{self.version}"


class ToolDocument(models.Model):
    class DocumentType(models.TextChoices):
        INVOICE = "invoice", "GST Invoice"
        QUOTATION = "quotation", "Quotation / Estimate"
        RECEIPT = "receipt", "Receipt"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="tool_documents")
    tool = models.ForeignKey(ToolDefinition, on_delete=models.PROTECT, related_name="documents")
    template = models.ForeignKey(ToolTemplate, null=True, blank=True, on_delete=models.SET_NULL, related_name="documents")
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    document_number = models.CharField(max_length=80)
    visitor_id = models.CharField(max_length=100, blank=True, db_index=True)
    business_details = models.JSONField(default=dict)
    customer_details = models.JSONField(default=dict)
    line_items = models.JSONField(default=list)
    tax_details = models.JSONField(default=dict)
    totals = models.JSONField(default=dict)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["document_type", "created_at"]), models.Index(fields=["visitor_id", "created_at"])]

    def __str__(self):
        return f"{self.document_type}:{self.document_number}"


class ToolEvent(models.Model):
    class EventType(models.TextChoices):
        OPEN = "tool_open", "Tool Open"
        START = "tool_start", "Tool Start"
        COMPLETE = "tool_complete", "Tool Complete"
        DOCUMENT_CREATED = "document_created", "Document Created"
        PDF_DOWNLOADED = "pdf_downloaded", "PDF Downloaded"
        COPY = "copy", "Copy"
        CTA_CLICK = "cta_click", "CTA Click"
        LEAD_SUBMITTED = "lead_submitted", "Lead Submitted"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool = models.ForeignKey(ToolDefinition, on_delete=models.PROTECT, related_name="events")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="tool_events")
    visitor_id = models.CharField(max_length=100, blank=True, db_index=True)
    event_type = models.CharField(max_length=40, choices=EventType.choices)
    document = models.ForeignKey(ToolDocument, null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
    session_id = models.CharField(max_length=100, blank=True, db_index=True)
    source = models.CharField(max_length=100, blank=True)
    medium = models.CharField(max_length=100, blank=True)
    campaign = models.CharField(max_length=160, blank=True)
    landing_path = models.CharField(max_length=500, blank=True)
    referrer = models.CharField(max_length=1000, blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["tool", "event_type", "created_at"]), models.Index(fields=["visitor_id", "created_at"])]

    def __str__(self):
        return f"{self.tool.slug}:{self.event_type}"
