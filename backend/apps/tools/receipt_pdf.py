from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _money(value):
    return f"Rs. {float(value or 0):,.2f}"


def _p(text, style):
    return Paragraph(str(text or "").replace("&", "&amp;"), style)


def render_receipt_pdf(document):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm, topMargin=14 * mm, bottomMargin=14 * mm)
    styles = getSampleStyleSheet()
    normal = ParagraphStyle("ReceiptNormal", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#263244"))
    small = ParagraphStyle("ReceiptSmall", parent=normal, fontSize=7.5, leading=9.5, textColor=colors.HexColor("#526176"))
    bold = ParagraphStyle("ReceiptBold", parent=normal, fontName="Helvetica-Bold")
    right = ParagraphStyle("ReceiptRight", parent=normal, alignment=TA_RIGHT)
    right_bold = ParagraphStyle("ReceiptRightBold", parent=bold, alignment=TA_RIGHT)
    title = ParagraphStyle("ReceiptTitle", parent=bold, fontSize=16, textColor=colors.HexColor("#2474E6"), alignment=TA_RIGHT)

    seller = document.business_details or {}
    buyer = document.customer_details or {}
    meta = document.metadata or {}
    tax = document.tax_details or {}
    totals = document.totals or {}
    story = []

    seller_lines = [_p(seller.get("name") or "Your Business", ParagraphStyle("ReceiptSeller", parent=bold, fontSize=17, textColor=colors.HexColor("#101828")))]
    if seller.get("gstin"):
        seller_lines.append(_p(f"GSTIN: {seller['gstin']}", small))
    contact = " | ".join(str(x) for x in (seller.get("email"), seller.get("phone")) if x)
    if contact:
        seller_lines.append(_p(contact, small))
    if seller.get("address"):
        seller_lines.append(_p(seller["address"], small))

    header = Table([
        [Table([[x] for x in seller_lines], colWidths=[112 * mm]), Table([[_p("PAYMENT RECEIPT", title)], [_p(document.document_number, right_bold)]], colWidths=[58 * mm])]
    ], colWidths=[112 * mm, 62 * mm])
    header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [header, Spacer(1, 6 * mm)]

    customer_lines = [_p("RECEIVED FROM", ParagraphStyle("ReceiptBlue", parent=bold, fontSize=8, textColor=colors.HexColor("#2474E6"))), _p(buyer.get("name") or "Customer Name", bold)]
    if buyer.get("gstin"):
        customer_lines.append(_p(f"GSTIN: {buyer['gstin']}", small))
    contact = " | ".join(str(x) for x in (buyer.get("email"), buyer.get("phone")) if x)
    if contact:
        customer_lines.append(_p(contact, small))
    if buyer.get("address"):
        customer_lines.append(_p(buyer["address"], small))

    details = [
        ["Receipt Date", meta.get("receipt_date") or document.created_at.strftime("%Y-%m-%d")],
        ["Payment Method", meta.get("payment_method") or tax.get("payment_method") or "—"],
        ["Reference", meta.get("reference") or "—"],
    ]
    detail_table = Table([[_p(k, small), _p(v, right_bold)] for k, v in details], colWidths=[34 * mm, 42 * mm])
    info = Table([[Table([[x] for x in customer_lines], colWidths=[100 * mm]), detail_table]], colWidths=[108 * mm, 76 * mm])
    info.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), .5, colors.HexColor("#D8E0EA")), ("INNERGRID", (0, 0), (-1, -1), .5, colors.HexColor("#D8E0EA")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story += [info, Spacer(1, 5 * mm)]

    status = Table([[_p("PAYMENT RECEIVED", ParagraphStyle("Status", parent=bold, fontSize=9, textColor=colors.HexColor("#18794E")))]], colWidths=[184 * mm])
    status.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF8F0")), ("BOX", (0, 0), (-1, -1), .5, colors.HexColor("#B9E4C9")), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [status, Spacer(1, 5 * mm)]

    rows = [[_p("#", bold), _p("Description", bold), _p("Qty", bold), _p("Rate", bold), _p("Amount", bold)]]
    for index, item in enumerate(document.line_items or [], 1):
        qty = float(item.get("quantity", 0) or 0)
        rate = float(item.get("rate", 0) or 0)
        amount = float(item.get("amount", qty * rate) or 0)
        rows.append([_p(index, normal), _p(item.get("description") or item.get("name") or "Item / Service", normal), _p(f"{qty:g}", right), _p(f"{rate:,.2f}", right), _p(f"{amount:,.2f}", right)])
    items = Table(rows, colWidths=[10 * mm, 88 * mm, 18 * mm, 30 * mm, 38 * mm], repeatRows=1)
    items.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2878E8")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#DCE3EC")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 1), (-1, -1), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [items, Spacer(1, 5 * mm)]

    summary_rows = [
        [_p("Subtotal", normal), _p(_money(totals.get("gross", totals.get("subtotal", 0))), right_bold)],
        [_p("Discount", normal), _p(f"- {_money(totals.get('discount', 0))}", right_bold)],
        [_p("Taxable Amount", normal), _p(_money(totals.get("taxable", totals.get("subtotal", 0))), right_bold)],
        [_p(f"GST ({float(tax.get('gst_rate', 0) or 0):g}%)", normal), _p(_money(totals.get("tax", 0)), right_bold)],
        [_p("AMOUNT RECEIVED", bold), _p(_money(totals.get("total", 0)), ParagraphStyle("ReceiptGrand", parent=right_bold, fontSize=13, textColor=colors.HexColor("#2474E6")))]
    ]
    summary = Table(summary_rows, colWidths=[48 * mm, 48 * mm], hAlign="RIGHT")
    summary.setStyle(TableStyle([("ALIGN", (1, 0), (1, -1), "RIGHT"), ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#9AA7B8")), ("TOPPADDING", (0, -1), (-1, -1), 7), ("BOTTOMPADDING", (0, -1), (-1, -1), 7)]))
    story += [summary, Spacer(1, 10 * mm)]

    if meta.get("notes"):
        story.append(_p(meta["notes"], small))
        story.append(Spacer(1, 6 * mm))
    story.append(Table([[_p("Thank you for your payment!", small)]], colWidths=[184 * mm], style=[("LINEABOVE", (0, 0), (-1, -1), 1, colors.HexColor("#2B80EF")), ("TOPPADDING", (0, 0), (-1, -1), 5)]))
    doc.build(story)
    buffer.seek(0)
    return buffer
