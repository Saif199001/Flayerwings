from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("leads", "0001_initial")]
    operations = [
        migrations.AddField(model_name="lead", name="tool_slug", field=models.CharField(blank=True, db_index=True, max_length=80)),
        migrations.AddField(model_name="lead", name="tool_document_id", field=models.UUIDField(blank=True, db_index=True, null=True)),
        migrations.AddField(model_name="lead", name="visitor_id", field=models.CharField(blank=True, db_index=True, max_length=100)),
        migrations.AddField(model_name="lead", name="session_id", field=models.CharField(blank=True, db_index=True, max_length=100)),
        migrations.AddField(model_name="lead", name="landing_path", field=models.CharField(blank=True, max_length=500)),
        migrations.AddField(model_name="lead", name="attribution", field=models.JSONField(default=dict)),
        migrations.AddIndex(model_name="lead", index=models.Index(fields=["tool_slug", "created_at"], name="leads_lead_tool_slu_2d6a61_idx")),
    ]
