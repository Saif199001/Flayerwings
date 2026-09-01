from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="ToolDefinition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=80, unique=True)),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="ToolTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("version", models.PositiveIntegerField(default=1)),
                ("config", models.JSONField(default=dict)),
                ("active", models.BooleanField(default=True)),
                ("tool", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="templates", to="tools.tooldefinition")),
            ],
            options={"indexes": [models.Index(fields=["tool", "active"], name="tools_tool_too_9e0f8c_idx")]},
        ),
        migrations.CreateModel(
            name="ToolDocument",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("document_type", models.CharField(choices=[("invoice", "GST Invoice"), ("quotation", "Quotation / Estimate"), ("receipt", "Receipt")], max_length=20)),
                ("document_number", models.CharField(max_length=80)),
                ("visitor_id", models.CharField(blank=True, db_index=True, max_length=100)),
                ("business_details", models.JSONField(default=dict)),
                ("customer_details", models.JSONField(default=dict)),
                ("line_items", models.JSONField(default=list)),
                ("tax_details", models.JSONField(default=dict)),
                ("totals", models.JSONField(default=dict)),
                ("metadata", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("template", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="documents", to="tools.tooltemplate")),
                ("tool", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="documents", to="tools.tooldefinition")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tool_documents", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["document_type", "created_at"], name="tools_toold_documen_3a8c55_idx"), models.Index(fields=["visitor_id", "created_at"], name="tools_toold_visito_42e6b2_idx")]},
        ),
        migrations.CreateModel(
            name="ToolEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("visitor_id", models.CharField(blank=True, db_index=True, max_length=100)),
                ("event_type", models.CharField(choices=[("tool_open", "Tool Open"), ("tool_start", "Tool Start"), ("tool_complete", "Tool Complete"), ("document_created", "Document Created"), ("pdf_downloaded", "PDF Downloaded"), ("copy", "Copy"), ("cta_click", "CTA Click"), ("lead_submitted", "Lead Submitted")], max_length=40)),
                ("session_id", models.CharField(blank=True, db_index=True, max_length=100)),
                ("source", models.CharField(blank=True, max_length=100)),
                ("medium", models.CharField(blank=True, max_length=100)),
                ("campaign", models.CharField(blank=True, max_length=160)),
                ("landing_path", models.CharField(blank=True, max_length=500)),
                ("referrer", models.CharField(blank=True, max_length=1000)),
                ("metadata", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("document", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="events", to="tools.tooldocument")),
                ("tool", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="events", to="tools.tooldefinition")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tool_events", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["tool", "event_type", "created_at"], name="tools_toole_tool_id_2d5a4b_idx"), models.Index(fields=["visitor_id", "created_at"], name="tools_toole_visito_4a15d8_idx")]},
        ),
        migrations.AddConstraint(
            model_name="tooltemplate",
            constraint=models.UniqueConstraint(fields=("tool", "name", "version"), name="uniq_tool_template_version"),
        ),
    ]
