from django.db import migrations


TOOLS = [
    ("gst-invoice-generator", "GST Invoice Generator", "Create and save professional GST invoices."),
    ("gst-calculator", "GST Calculator", "Calculate GST inclusive and exclusive amounts."),
    ("qr-code-generator", "QR Code Generator", "Generate QR codes with optional branding."),
    ("whatsapp-link-qr-generator", "WhatsApp Link & QR Generator", "Create shareable WhatsApp links and QR codes."),
    ("quotation-estimate-generator", "Quotation / Estimate Generator", "Create and save quotations and estimates."),
    ("receipt-generator", "Receipt Generator", "Create and save customer receipts."),
    ("payment-reminder-generator", "Payment Reminder Generator", "Create payment reminder messages quickly."),
    ("utm-campaign-builder", "UTM Campaign Builder", "Build clean trackable campaign URLs."),
]


def seed(apps, schema_editor):
    ToolDefinition = apps.get_model("tools", "ToolDefinition")
    ToolTemplate = apps.get_model("tools", "ToolTemplate")
    for slug, name, description in TOOLS:
        tool, _ = ToolDefinition.objects.get_or_create(slug=slug, defaults={"name": name, "description": description})
        ToolTemplate.objects.get_or_create(tool=tool, name="Classic", version=1, defaults={"config": {"layout": "classic"}})


def unseed(apps, schema_editor):
    apps.get_model("tools", "ToolDefinition").objects.filter(slug__in=[x[0] for x in TOOLS]).delete()


class Migration(migrations.Migration):
    dependencies = [("tools", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
