from django.db import models


class Tool(models.Model):
    class Slug(models.TextChoices):
        SOCIAL_MEDIA_AUDIT = "social-media-audit", "Social Media Audit"
        CAPTION_GENERATOR = "caption-generator", "AI Caption Generator"
        CONTENT_IDEAS = "content-ideas", "Social Media Content Ideas"

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, choices=Slug.choices)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
