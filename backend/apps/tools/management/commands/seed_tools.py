from django.core.management.base import BaseCommand

from apps.tools.models import Tool


TOOLS = [
    {
        "name": "Social Media Audit",
        "slug": "social-media-audit",
        "description": "Get a quick assessment of your social media presence and discover opportunities to improve it.",
    },
    {
        "name": "AI Caption Generator",
        "slug": "caption-generator",
        "description": "Generate platform-ready social media captions from a business, topic and tone.",
    },
    {
        "name": "Social Media Content Ideas",
        "slug": "content-ideas",
        "description": "Generate practical content ideas tailored to a business, audience and social platform.",
    },
]


class Command(BaseCommand):
    help = "Seed the initial Flayer Wings free tools."

    def handle(self, *args, **options):
        for data in TOOLS:
            tool, created = Tool.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "is_active": True,
                },
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action}: {tool.name}"))
