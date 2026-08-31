from django.db import models


class Project(models.Model):
    class ProjectType(models.TextChoices):
        PRODUCT = "product", "Product"
        CLIENT = "client", "Client Project"
        CASE_STUDY = "case-study", "Case Study"

    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In Progress"
        LIVE = "live", "Live"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    project_type = models.CharField(max_length=20, choices=ProjectType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    short_description = models.CharField(max_length=280)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        indexes = [
            models.Index(fields=["published", "featured"]),
            models.Index(fields=["project_type", "status"]),
        ]

    def __str__(self):
        return self.title
