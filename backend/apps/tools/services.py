from io import BytesIO

from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _money(value):
    return f"Rs. {float(value or 0):,.2f}"


def _p(text, style):
    return Paragraph(str(text or "").replace("&", "&amp;"), style)


def _invoice_pdf(document):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm, topMargin=12 * mm, bottomMargin=12 * mm)
    styles = getSampleStyleSheet()
    normal = ParagraphStyle("InvoiceNormal", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=colors.HexColor("#263244"))
    small = ParagraphStyle("InvoiceSmall", parent=normal, fontSize=7.5, leading=9.5, textColor=colors.HexColor("#526176"))
    bold = ParagraphStyle("InvoiceBold", parent=normal, fontName="Helvetica-Bold")
    blue = ParagraphStyle("InvoiceBlue", parent=bold, fontSize=8, textColor=colors.HexColor("#2474E6"))
    right = ParagraphStyle("InvoiceRight", parent=normal, alignment=TA_RIGHT)
    right_bold = ParagraphStyle("InvoiceRightBold", parent=bold, alignment=TA_RIGHT)
    title_style = ParagraphStyle("InvoiceTitle", parent=bold, fontSize=15, textColor=colors.HexColor("#2474E6"), alignment=TA_RIGHT)

    business = document.business_details or {}
    customer = document.customer_details or {}
    tax = document.tax_details or {}
    totals = document.totals or {}
    metadata = document.metadata or {}
    story = []

    seller_name = business.get("name") or "Your Business"
    seller_lines = [
        _p(seller_name, ParagraphStyle("SellerName", parent=bold, fontSize=17, leading=20, textColor=colors.HexColor("#101828"))),
    ]
    if business.get("gstin"): seller_lines.append(_p(f"GSTIN: {business['gstin']}", small))
    contact = " | ".join(str(x) for x in (business.get("email"), business.get("phone")) if x)
    if contact: seller_lines.append(_p(contact, small))
    if business.get("address"): seller_lines.append(_p(business["address"], small))

    header = Table([
        [Table([["FW"], ["FLAYER WINGS"]], colWidths=[18 * mm]), Table([[x] for x in seller_lines], colWidths=[92 * mm]), Table([[_p("TAX INVOICE", title_style)], [_p(document.document_number, right_bold)],], colWidths=[58 * mm])]
    ], colWidths=[20 * mm, 94 * mm, 58 * mm])
    header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#2474E6")), ("TEXTCOLOR", (0, 0), (0, 0), colors.white), ("ALIGN", (0, 0), (0, 0), "CENTER"), ("FONTSIZE", (0, 0), (0, 0), 12), ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story += [header, Spacer(1, 6 * mm)]

    bill_lines = [_p("BILL TO", blue), _p(customer.get("name") or "Customer Name", bold)]
    if customer.get("gstin"): bill_lines.append(_p(f"GSTIN: {customer['gstin']}", small))
    contact = " | ".join(str(x) for x in (customer.get("email"), customer.get("phone")) if x)
    if contact: bill_lines.append(_p(contact, small))
    if customer.get("address"): bill_lines.append(_p(customer["address"], small))

    meta_lines = [
        ["Invoice Date", metadata.get("invoice_date") or document.created_at.strftime("%Y-%m-%d")],
        ["Due Date", metadata.get("due_date") or "—"],
        ["Tax Type", "IGST" if tax.get("tax_mode") == "inter" else "CGST + SGST"],
        ["GST Rate", f"{float(tax.get('gst_rate', 0) or 0):g}%"],
    ]
    meta_table = Table([[ _p(k, small), _p(v, right_bold)] for k, v in meta_lines], colWidths=[32 * mm, 42 * mm])
    meta_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    info = Table([[Table([[x] for x in bill_lines], colWidths=[92 * mm]), meta_table]], colWidths=[108 * mm, 76 * mm])
    info.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), .5, colors.HexColor("#D8E0EA")), ("INNERGRID", (0, 0), (-1, -1), .5, colors.HexColor("#D8E0EA")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story += [info, Spacer(1, 6 * mm)]

    rows = [[_p("#", bold), _p("Item / Service", bold), _p("HSN / SAC", bold), _p("Qty", bold), _p("Rate", bold), _p("Amount", bold)]]
    for index, item in enumerate(document.line_items or [], 1):
        qty = float(item.get("quantity", 0) or 0)
        rate = float(item.get("rate", item.get("amount", 0)) or 0)
        amount = float(item.get("amount", qty * rate) or 0)
        rows.append([_p(index, normal), _p(item.get("name") or "Item / Service", normal), _p(item.get("hsn") or "—", normal), _p(f"{qty:g}", right), _p(f"{rate:,.2f}", right), _p(f"{amount:,.2f}", right)])
    items_table = Table(rows, colWidths=[8 * mm, 61 * mm, 27 * mm, 17 * mm, 28 * mm, 35 * mm], repeatRows=1)
    items_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2878E8")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#DCE3EC")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (3, 1), (-1, -1), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [items_table, Spacer(1, 5 * mm)]

    gross = totals.get("gross", totals.get("subtotal", 0))
    discount = totals.get("discount", 0)
    taxable = totals.get("taxable", totals.get("subtotal", gross))
    total_tax = totals.get("tax", 0)
    rate = float(tax.get("gst_rate", 0) or 0)
    summary_rows = [[_p("Subtotal", normal), _p(_money(gross), right_bold)], [_p("Discount", normal), _p(f"- {_money(discount)}", right_bold)], [_p("Taxable Amount", normal), _p(_money(taxable), right_bold)]]
    if tax.get("tax_mode") == "inter":
        summary_rows.append([_p(f"IGST ({rate:g}%)", normal), _p(_money(tax.get("igst", total_tax)), right_bold)])
    else:
        summary_rows += [[_p(f"CGST ({rate / 2:g}%)", normal), _p(_money(tax.get("cgst", total_tax / 2)), right_bold)], [_p(f"SGST ({rate / 2:g}%)", normal), _p(_money(tax.get("sgst", total_tax / 2)), right_bold)]]
    summary_rows.append([_p("TOTAL", blue), _p(_money(totals.get("total", taxable + total_tax)), ParagraphStyle("Grand", parent=right_bold, fontSize=13, textColor=colors.HexColor("#2474E6")))])
    summary = Table(summary_rows, colWidths=[48 * mm, 48 * mm], hAlign="RIGHT")
    summary.setStyle(TableStyle([("ALIGN", (1, 0), (1, -1), "RIGHT"), ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#9AA7B8")), ("TOPPADDING", (0, -1), (-1, -1), 7), ("BOTTOMPADDING", (0, -1), (-1, -1), 7)]))
    story += [summary, Spacer(1, 12 * mm), Table([[_p("Thank you for your business!", small)]], colWidths=[184 * mm], style=[("LINEABOVE", (0, 0), (-1, -1), 1, colors.HexColor("#2B80EF")), ("TOPPADDING", (0, 0), (-1, -1), 5)])]
    doc.build(story)
    buffer.seek(0)
    return buffer


def build_document_pdf(document):
    """Render a stable PDF from persisted document JSON."""
    if document.document_type == "invoice":
        return _invoice_pdf(document)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    normal.fontName = "Helvetica"
    normal.fontSize = 9
    story = [Paragraph(dict(document.DocumentType.choices).get(document.document_type, document.document_type), styles["Title"]), Paragraph(f"Document No: {document.document_number}", normal), Spacer(1, 8)]
    for label, value in (("Business", (document.business_details or {}).get("name")), ("Customer", (document.customer_details or {}).get("name"))):
        if value: story.append(Paragraph(f"{label}: {value}", normal))
    story.append(Spacer(1, 8))
    for item in document.line_items or []:
        story.append(Paragraph(f"{item.get('name', 'Item')} × {item.get('quantity', 1)} — {_money(item.get('amount', item.get('rate', 0)))}", normal))
    totals = document.totals or {}
    story += [Spacer(1, 8), Paragraph(f"Subtotal: {_money(totals.get('subtotal', totals.get('gross', 0)))}", normal), Paragraph(f"Tax: {_money(totals.get('tax', 0))}", normal), Paragraph(f"Total: {_money(totals.get('total', 0))}", styles["Heading2"])]
    doc.build(story)
    buffer.seek(0)
    return buffer


def document_pdf_response(document):
    buffer = build_document_pdf(document)
    filename = f"{document.document_type}-{document.document_number}.pdf".replace(" ", "-")
    return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")
