from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def money(value):
    return f"Rs. {float(value or 0):,.2f}"


def p(text, style):
    return Paragraph(str(text or "").replace("&", "&amp;"), style)


def render_quotation_pdf(document):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm, topMargin=12 * mm, bottomMargin=12 * mm)
    styles = getSampleStyleSheet()
    normal = ParagraphStyle("QuoteNormal", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=colors.HexColor("#263244"))
    small = ParagraphStyle("QuoteSmall", parent=normal, fontSize=7.5, leading=9.5, textColor=colors.HexColor("#526176"))
    bold = ParagraphStyle("QuoteBold", parent=normal, fontName="Helvetica-Bold")
    blue = ParagraphStyle("QuoteBlue", parent=bold, fontSize=8, textColor=colors.HexColor("#2474E6"))
    right = ParagraphStyle("QuoteRight", parent=normal, alignment=TA_RIGHT)
    right_bold = ParagraphStyle("QuoteRightBold", parent=bold, alignment=TA_RIGHT)
    title = ParagraphStyle("QuoteTitle", parent=bold, fontSize=15, textColor=colors.HexColor("#2474E6"), alignment=TA_RIGHT)
    grand = ParagraphStyle("QuoteGrand", parent=right_bold, fontSize=13, textColor=colors.HexColor("#2474E6"))

    business = document.business_details or {}
    customer = document.customer_details or {}
    tax = document.tax_details or {}
    totals = document.totals or {}
    metadata = document.metadata or {}

    seller = [p(business.get("name") or "Your Business", ParagraphStyle("SellerName", parent=bold, fontSize=17, leading=20, textColor=colors.HexColor("#101828")))]
    if business.get("gstin"): seller.append(p(f"GSTIN: {business['gstin']}", small))
    contact = " | ".join(str(x) for x in (business.get("email"), business.get("phone")) if x)
    if contact: seller.append(p(contact, small))
    if business.get("address"): seller.append(p(business["address"], small))
    header = Table([[Table([[x] for x in seller], colWidths=[112 * mm]), Table([[p("QUOTATION", title)], [p(document.document_number, right_bold)]], colWidths=[70 * mm])]], colWidths=[112 * mm, 70 * mm])
    header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))

    buyer = [p("PREPARED FOR", blue), p(customer.get("name") or "Customer Name", bold)]
    if customer.get("gstin"): buyer.append(p(f"GSTIN: {customer['gstin']}", small))
    contact = " | ".join(str(x) for x in (customer.get("email"), customer.get("phone")) if x)
    if contact: buyer.append(p(contact, small))
    if customer.get("address"): buyer.append(p(customer["address"], small))
    meta = [["Quotation Date", metadata.get("quotation_date") or document.created_at.strftime("%Y-%m-%d")], ["Valid Until", metadata.get("valid_until") or "—"], ["Tax Type", "IGST" if tax.get("tax_mode") == "igst" else "CGST + SGST"], ["GST Rate", f"{float(tax.get('gst_rate', 0) or 0):g}%"]]
    meta_table = Table([[p(k, small), p(v, right_bold)] for k, v in meta], colWidths=[32 * mm, 42 * mm])
    meta_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    info = Table([[Table([[x] for x in buyer], colWidths=[108 * mm]), meta_table]], colWidths=[108 * mm, 76 * mm])
    info.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), .5, colors.HexColor("#D8E0EA")), ("INNERGRID", (0, 0), (-1, -1), .5, colors.HexColor("#D8E0EA")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))

    rows = [[p("#", bold), p("Item / Service", bold), p("HSN / SAC", bold), p("Qty", bold), p("Rate", bold), p("Amount", bold)]]
    for i, item in enumerate(document.line_items or [], 1):
        qty = float(item.get("quantity", 0) or 0)
        rate = float(item.get("rate", 0) or 0)
        amount = float(item.get("amount", qty * rate) or 0)
        rows.append([p(i, normal), p(item.get("name") or "Item / Service", normal), p(item.get("hsn") or "—", normal), p(f"{qty:g}", right), p(f"{rate:,.2f}", right), p(f"{amount:,.2f}", right)])
    table = Table(rows, colWidths=[8 * mm, 61 * mm, 27 * mm, 17 * mm, 28 * mm, 35 * mm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2878E8")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#DCE3EC")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (3, 1), (-1, -1), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))

    gross = float(totals.get("gross", totals.get("subtotal", 0)) or 0)
    discount = float(totals.get("discount", 0) or 0)
    taxable = float(totals.get("taxable", totals.get("subtotal", gross)) or 0)
    tax_total = float(totals.get("tax", 0) or 0)
    rate = float(tax.get("gst_rate", 0) or 0)
    summary = [[p("Subtotal", normal), p(money(gross), right_bold)], [p("Discount", normal), p(f"- {money(discount)}", right_bold)], [p("Taxable Amount", normal), p(money(taxable), right_bold)]]
    if tax.get("tax_mode") == "igst":
        summary.append([p(f"IGST ({rate:g}%)", normal), p(money(tax.get("igst", tax_total)), right_bold)])
    else:
        summary += [[p(f"CGST ({rate / 2:g}%)", normal), p(money(tax.get("cgst", tax_total / 2)), right_bold)], [p(f"SGST ({rate / 2:g}%)", normal), p(money(tax.get("sgst", tax_total / 2)), right_bold)]]
    summary.append([p("ESTIMATED TOTAL", blue), p(money(totals.get("total", taxable + tax_total)), grand)])
    summary_table = Table(summary, colWidths=[48 * mm, 48 * mm], hAlign="RIGHT")
    summary_table.setStyle(TableStyle([("ALIGN", (1, 0), (1, -1), "RIGHT"), ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#9AA7B8")), ("TOPPADDING", (0, -1), (-1, -1), 7), ("BOTTOMPADDING", (0, -1), (-1, -1), 7)]))

    story = [header, Spacer(1, 6 * mm), info, Spacer(1, 6 * mm), table, Spacer(1, 5 * mm), summary_table, Spacer(1, 12 * mm), Table([[p("This quotation is an estimate and is subject to the terms agreed with the customer.", small)]], colWidths=[184 * mm], style=[("LINEABOVE", (0, 0), (-1, -1), 1, colors.HexColor("#2B80EF")), ("TOPPADDING", (0, 0), (-1, -1), 5)])]
    doc.build(story)
    buffer.seek(0)
    return buffer
