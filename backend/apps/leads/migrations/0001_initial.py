from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("company", models.CharField(blank=True, max_length=160)),
                ("website", models.URLField(blank=True)),
                ("lead_type", models.CharField(choices=[("contact", "Contact"), ("social_audit", "Social Media Audit"), ("tool", "Free Tool"), ("project", "Project Inquiry")], default="contact", max_length=30)),
                ("source", models.CharField(blank=True, max_length=80)),
                ("message", models.TextField(blank=True)),
                ("social_profile_url", models.URLField(blank=True)),
                ("status", models.CharField(choices=[("new", "New"), ("contacted", "Contacted"), ("qualified", "Qualified"), ("converted", "Converted"), ("lost", "Lost")], default="new", max_length=20)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["status", "created_at"], name="leads_lead_status_0d2a7d_idx"),
                    models.Index(fields=["lead_type", "created_at"], name="leads_lead_lead_typ_8e5d45_idx"),
                    models.Index(fields=["email"], name="leads_lead_email_4b9f24_idx"),
                ],
            },
        ),
    ]
