export const TOOLS = [
  { slug: "gst-invoice-generator", icon: "invoice", title: "GST Invoice Generator", copy: "Create professional GST invoices with automatic tax calculations and print-ready output." },
  { slug: "gst-calculator", icon: "calculator", title: "GST Calculator", copy: "Add or remove GST instantly with clear CGST, SGST and IGST calculations." },
  { slug: "qr-generator", icon: "qr", title: "QR Code Generator", copy: "Create QR codes for links, text, contact details and more, with optional logo branding." },
  { slug: "whatsapp-link-generator", icon: "whatsapp", title: "WhatsApp Link & QR", copy: "Create click-to-chat WhatsApp links, QR codes and ready-to-use website buttons." },
  { slug: "quotation-generator", icon: "quotation", title: "Quotation Generator", copy: "Build professional quotations and estimates with GST, discounts and customer details." },
  { slug: "receipt-generator", icon: "receipt", title: "Receipt Generator", copy: "Create clean payment receipts with your business branding and printable output." },
  { slug: "payment-reminder-generator", icon: "payment", title: "Payment Reminder", copy: "Generate polite, professional payment reminder messages ready to share on WhatsApp." },
  { slug: "utm-builder", icon: "utm", title: "UTM Campaign Builder", copy: "Build accurate campaign URLs for tracking traffic from social, ads, email and more." },
];

export function getTool(slug) {
  return TOOLS.find((tool) => tool.slug === slug);
}
