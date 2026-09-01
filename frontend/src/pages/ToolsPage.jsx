import { Link } from "react-router-dom";

export const TOOLS = [
  { slug: "gst-invoice-generator", icon: "🧾", title: "GST Invoice Generator", copy: "Create professional GST invoices with automatic tax calculations and print-ready output." },
  { slug: "gst-calculator", icon: "🧮", title: "GST Calculator", copy: "Add or remove GST instantly with clear CGST, SGST and IGST calculations." },
  { slug: "qr-generator", icon: "▦", title: "QR Code Generator", copy: "Create QR codes for links, text, contact details and more, with optional logo branding." },
  { slug: "whatsapp-link-generator", icon: "◉", title: "WhatsApp Link & QR", copy: "Create click-to-chat WhatsApp links, QR codes and ready-to-use website buttons." },
  { slug: "quotation-generator", icon: "📋", title: "Quotation Generator", copy: "Build professional quotations and estimates with GST, discounts and customer details." },
  { slug: "receipt-generator", icon: "🧾", title: "Receipt Generator", copy: "Create clean payment receipts with your business branding and printable output." },
  { slug: "payment-reminder-generator", icon: "💳", title: "Payment Reminder", copy: "Generate polite, professional payment reminder messages ready to share on WhatsApp." },
  { slug: "utm-builder", icon: "🔗", title: "UTM Campaign Builder", copy: "Build accurate campaign URLs for tracking traffic from social, ads, email and more." },
];

export default function ToolsPage() {
  return (
    <main className="tools-page">
      <section className="tools-hero section">
        <div className="section-container">
          <span className="eyebrow-cyan">FREE TOOLS</span>
          <h1 className="tools-page-title">Useful tools for modern businesses.</h1>
          <p className="tools-page-copy">Simple, practical utilities for billing, marketing, customer communication and everyday business work. No sign up required.</p>
          <div className="tools-grid">
            {TOOLS.map((tool) => (
              <Link className="free-tool-card" to={`/tools/${tool.slug}`} key={tool.slug}>
                <span className="free-tool-icon" aria-hidden="true">{tool.icon}</span>
                <span className="free-tool-content">
                  <strong>{tool.title}</strong>
                  <span>{tool.copy}</span>
                  <em>Use free →</em>
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
