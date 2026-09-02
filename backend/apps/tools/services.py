from io import BytesIO

from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def build_document_pdf(document):
    """Render a stable PDF from persisted document JSON."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 42 * mm
    left = 18 * mm
    right = width - 18 * mm

    def line(text, size=9, gap=14):
        nonlocal y
        if y < 22 * mm:
            pdf.showPage()
            y = height - 22 * mm
        pdf.setFont("Helvetica", size)
        pdf.drawString(left, y, str(text)[:125])
        y -= gap

    def heading(text):
        nonlocal y
        if y < 35 * mm:
            pdf.showPage()
            y = height - 22 * mm
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(left, y, text)
        y -= 18

    title = dict(document.DocumentType.choices).get(document.document_type, document.document_type)
    metadata = document.metadata or {}
    business = document.business_details or {}
    customer = document.customer_details or {}
    tax_details = document.tax_details or {}
    totals = document.totals or {}

    pdf.setTitle(f"{title} - {document.document_number}")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(left, y, title)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(right, y, str(document.document_number))
    y -= 24

    if business.get("name"):
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(left, y, str(business["name"])[:80])
        y -= 16
    for key in ("gstin", "address", "phone", "email"):
        if business.get(key):
            line(f"{key.upper() if key == 'gstin' else key.title()}: {business[key]}")
    y -= 6

    heading("Bill To")
    for key in ("name", "gstin", "address", "phone", "email"):
        if customer.get(key):
            line(f"{key.upper() if key == 'gstin' else key.title()}: {customer[key]}")
    y -= 6

    if metadata.get("invoice_date"):
        line(f"Invoice Date: {metadata['invoice_date']}")
    if metadata.get("due_date"):
        line(f"Due Date: {metadata['due_date']}")
    y -= 8

    heading("Items")
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(left, y, "Description")
    pdf.drawString(left + 95 * mm, y, "Qty")
    pdf.drawString(left + 112 * mm, y, "Rate")
    pdf.drawRightString(right, y, "Amount")
    y -= 14
    pdf.setStrokeColor(colors.lightgrey)
    pdf.line(left, y + 5, right, y + 5)

    for item in document.line_items or []:
        name = str(item.get("name", "Item"))[:58]
        qty = float(item.get("quantity", 1) or 0)
        rate = float(item.get("rate", item.get("amount", 0)) or 0)
        amount = float(item.get("amount", qty * rate) or 0)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(left, y, name)
        pdf.drawString(left + 95 * mm, y, f"{qty:g}")
        pdf.drawString(left + 112 * mm, y, f"{rate:,.2f}")
        pdf.drawRightString(right, y, f"{amount:,.2f}")
        y -= 16
        if y < 32 * mm:
            pdf.showPage()
            y = height - 22 * mm

    y -= 4
    pdf.setStrokeColor(colors.black)
    pdf.line(left + 95 * mm, y, right, y)
    y -= 18
    pdf.setFont("Helvetica", 9)
    pdf.drawString(left + 95 * mm, y, "Subtotal")
    pdf.drawRightString(right, y, f"₹{float(totals.get('subtotal', 0) or 0):,.2f}")
    y -= 15
    if float(totals.get("discount", 0) or 0):
        pdf.drawString(left + 95 * mm, y, "Discount")
        pdf.drawRightString(right, y, f"- ₹{float(totals['discount']):,.2f}")
        y -= 15

    rate = float(tax_details.get("gst_rate", 0) or 0)
    if tax_details.get("tax_mode") == "inter":
        pdf.drawString(left + 95 * mm, y, f"IGST ({rate:g}%)")
        pdf.drawRightString(right, y, f"₹{float(tax_details.get('igst', totals.get('tax', 0)) or 0):,.2f}")
        y -= 15
    else:
        half_rate = rate / 2
        pdf.drawString(left + 95 * mm, y, f"CGST ({half_rate:g}%)")
        pdf.drawRightString(right, y, f"₹{float(tax_details.get('cgst', 0) or 0):,.2f}")
        y -= 15
        pdf.drawString(left + 95 * mm, y, f"SGST ({half_rate:g}%)")
        pdf.drawRightString(right, y, f"₹{float(tax_details.get('sgst', 0) or 0):,.2f}")
        y -= 15

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(left + 95 * mm, y, "Total")
    pdf.drawRightString(right, y, f"₹{float(totals.get('total', 0) or 0):,.2f}")

    pdf.save()
    buffer.seek(0)
    return buffer


def document_pdf_response(document):
    buffer = build_document_pdf(document)
    filename = f"{document.document_type}-{document.document_number}.pdf".replace(" ", "-")
    return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")
