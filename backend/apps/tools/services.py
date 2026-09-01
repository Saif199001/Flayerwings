from io import BytesIO

from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def build_document_pdf(document):
    """Render a stable, dependency-light PDF from persisted document JSON."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    def line(text, size=10, gap=16):
        nonlocal y
        if y < 50:
            pdf.showPage()
            y = height - 50
        pdf.setFont("Helvetica", size)
        pdf.drawString(40, y, str(text)[:110])
        y -= gap

    title = dict(document.DocumentType.choices).get(document.document_type, document.document_type)
    line(title, 18, 24)
    line(f"Document No: {document.document_number}")
    line(f"Date: {document.created_at.strftime('%d %b %Y')}", gap=24)

    business = document.business_details or {}
    customer = document.customer_details or {}
    if business.get("name"):
        line(f"Business: {business['name']}")
    if business.get("address"):
        line(f"Address: {business['address']}")
    if customer.get("name"):
        line(f"Customer: {customer['name']}")
    if customer.get("email"):
        line(f"Email: {customer['email']}")
    y -= 8

    line("Items", 12, 20)
    for item in document.line_items or []:
        name = item.get("name", "Item")
        amount = item.get("amount", item.get("price", ""))
        qty = item.get("quantity", 1)
        line(f"{name}  x{qty}  {amount}")

    totals = document.totals or {}
    y -= 6
    for key in ("subtotal", "tax", "total"):
        if key in totals:
            line(f"{key.title()}: {totals[key]}", 11 if key == "total" else 10)

    pdf.save()
    buffer.seek(0)
    return buffer


def document_pdf_response(document):
    buffer = build_document_pdf(document)
    filename = f"{document.document_type}-{document.document_number}.pdf".replace(" ", "-")
    return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")
