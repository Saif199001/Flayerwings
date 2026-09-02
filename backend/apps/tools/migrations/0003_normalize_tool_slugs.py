from django.db import migrations


SLUG_MAP = {
    "qr-code-generator": "qr-generator",
    "whatsapp-link-qr-generator": "whatsapp-link-generator",
    "quotation-estimate-generator": "quotation-generator",
    "utm-campaign-builder": "utm-builder",
}


def normalize_slugs(apps, schema_editor):
    ToolDefinition = apps.get_model("tools", "ToolDefinition")
    for old_slug, new_slug in SLUG_MAP.items():
        ToolDefinition.objects.filter(slug=old_slug).update(slug=new_slug)


def restore_slugs(apps, schema_editor):
    ToolDefinition = apps.get_model("tools", "ToolDefinition")
    for old_slug, new_slug in SLUG_MAP.items():
        ToolDefinition.objects.filter(slug=new_slug).update(slug=old_slug)


class Migration(migrations.Migration):
    dependencies = [("tools", "0002_seed_tools")]
    operations = [migrations.RunPython(normalize_slugs, restore_slugs)]
