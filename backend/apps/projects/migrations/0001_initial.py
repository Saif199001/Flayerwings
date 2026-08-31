from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("slug", models.SlugField(max_length=180, unique=True)),
                ("project_type", models.CharField(choices=[("product", "Product"), ("client", "Client Project"), ("case-study", "Case Study")], max_length=20)),
                ("status", models.CharField(choices=[("planned", "Planned"), ("in_progress", "In Progress"), ("live", "Live"), ("archived", "Archived")], default="planned", max_length=20)),
                ("short_description", models.CharField(max_length=280)),
                ("description", models.TextField(blank=True)),
                ("url", models.URLField(blank=True)),
                ("featured", models.BooleanField(default=False)),
                ("published", models.BooleanField(default=False)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["sort_order", "-created_at"],
                "indexes": [
                    models.Index(fields=["published", "featured"], name="projects_project_publis_9a1d72_idx"),
                    models.Index(fields=["project_type", "status"], name="projects_project_projec_8b61d4_idx"),
                ],
            },
        ),
    ]
