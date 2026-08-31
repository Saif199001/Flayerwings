from django.db import models


class SiteContent(models.Model):
    key = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return self.key
