import { Link } from "react-router-dom";
import SEO from "../components/SEO";
import { TOOLS } from "../config/tools";

const ICONS = {
  invoice: "🧾",
  calculator: "🧮",
  qr: "▦",
  whatsapp: "◉",
  quotation: "📋",
  receipt: "🧾",
  payment: "💳",
  utm: "🔗",
};

export default function ToolsPage() {
  return (
    <main className="tools-page">
      <SEO
        title="Free Business Tools | Flayer Wings"
        description="Free business tools for GST invoices, GST calculations, QR codes, WhatsApp links, quotations, receipts, payment reminders and UTM campaigns."
        path="/tools"
      />
      <section className="tools-hero section">
        <div className="section-container">
          <span className="eyebrow-cyan">FREE TOOLS</span>
          <h1 className="tools-page-title">Useful tools for modern businesses.</h1>
          <p className="tools-page-copy">Simple, practical utilities for billing, marketing, customer communication and everyday business work. No sign up required.</p>
          <div className="tools-grid">
            {TOOLS.map((tool) => (
              <Link className="free-tool-card" to={`/tools/${tool.slug}`} key={tool.slug}>
                <span className="free-tool-icon" aria-hidden="true">{ICONS[tool.icon] || "•"}</span>
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
