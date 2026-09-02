from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("tools", "0003_normalize_tool_slugs")]

    operations = [
        migrations.AlterField(
            model_name="toolevent",
            name="event_type",
            field=models.CharField(
                max_length=40,
                choices=[
                    ("tool_open", "Tool Open"),
                    ("tool_start", "Tool Start"),
                    ("tool_complete", "Tool Complete"),
                    ("document_created", "Document Created"),
                    ("pdf_downloaded", "PDF Downloaded"),
                    ("png_downloaded", "PNG Downloaded"),
                    ("copy", "Copy"),
                    ("cta_click", "CTA Click"),
                    ("lead_submitted", "Lead Submitted"),
                ],
            ),
        ),
    ]
