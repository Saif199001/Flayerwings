import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import SEO from "../components/SEO";
import { getAttribution, getToolVisitorId, trackToolEvent } from "../services/api";
import GstInvoiceTool from "./GstInvoiceTool";
import QuotationTool from "./QuotationTool";
import ReceiptTool from "./ReceiptTool";
import GstCalculatorTool from "./GstCalculatorTool";
import QrGeneratorTool from "./QrGeneratorTool";
import "../styles/free-tools.css";

const money = (value) =>
  `₹${Number(value || 0).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

function Field({ label, ...props }) {
  return (
    <label className="tool-field">
      <span>{label}</span>
      <input {...props} />
    </label>
  );
}

function Shell({ title, description, children }) {
  return (
    <main className="tool-page">
      <SEO title={`${title} | Flayer Wings`} description={description} path={window.location.pathname} />
      <div className="tool-container">
        <Link className="tool-back" to="/tools">← All Free Tools</Link>
        <div className="tool-heading">
          <span className="eyebrow-cyan">FREE TOOL</span>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
        <div className="tool-workspace">{children}</div>
      </div>
    </main>
  );
}

function useToolEvent(slug) {
  useEffect(() => {
    const visitorId = getToolVisitorId();
    localStorage.setItem("fw_last_tool_slug", slug);
    trackToolEvent({ tool: slug, event_type: "tool_open", visitor_id: visitorId, session_id: visitorId, ...getAttribution() }).catch(() => {});
  }, [slug]);
}

function useToolAction(slug) {
  return (eventType, metadata = {}) => {
    const visitorId = getToolVisitorId();
    trackToolEvent({ tool: slug, event_type: eventType, visitor_id: visitorId, session_id: visitorId, metadata, ...getAttribution() }).catch(() => {});
  };
}

function CopyButton({ value, label = "Copy" }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    if (!value) return;
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch { setCopied(false); }
  };
  return <button className="button button-primary" type="button" onClick={copy} disabled={!value}>{copied ? "Copied ✓" : label}</button>;
}

function UTMBuilder() {
  const track = useToolAction("utm-builder");
  const [form, setForm] = useState({ url: "https://example.com", source: "instagram", medium: "social", campaign: "summer_sale", term: "", content: "" });
  const set = (key, value) => setForm((current) => ({ ...current, [key]: value }));
  const result = useMemo(() => {
    try {
      const url = new URL(form.url.trim());
      if (!/^https?:$/.test(url.protocol)) return "Enter a valid HTTP(S) URL";
      if (!form.source.trim() || !form.medium.trim() || !form.campaign.trim()) return "Source, medium and campaign are required";
      [["utm_source", form.source], ["utm_medium", form.medium], ["utm_campaign", form.campaign], ["utm_term", form.term], ["utm_content", form.content]].forEach(([key, value]) => { if (value.trim()) url.searchParams.set(key, value.trim()); });
      return url.toString();
    } catch { return "Enter a valid HTTP(S) URL"; }
  }, [form]);
  const valid = /^https?:\/\//.test(result);
  const reset = () => setForm({ url: "https://example.com", source: "instagram", medium: "social", campaign: "summer_sale", term: "", content: "" });
  return <Shell title="UTM Campaign Builder" description="Create clean campaign URLs for analytics without manually building query strings.">
    <div className="tool-panel"><div className="tool-form-grid">
      <Field label="Website URL *" type="url" value={form.url} onChange={(event) => set("url", event.target.value)} placeholder="https://yourwebsite.com/page" />
      <Field label="Campaign Source *" value={form.source} onChange={(event) => set("source", event.target.value)} placeholder="instagram" />
      <Field label="Campaign Medium *" value={form.medium} onChange={(event) => set("medium", event.target.value)} placeholder="social" />
      <Field label="Campaign Name *" value={form.campaign} onChange={(event) => set("campaign", event.target.value)} placeholder="summer_sale" />
      <Field label="Campaign Term" value={form.term} onChange={(event) => set("term", event.target.value)} placeholder="Optional keyword" />
      <Field label="Campaign Content" value={form.content} onChange={(event) => set("content", event.target.value)} placeholder="Optional ad or link variant" />
    </div><p className="tool-helper">Use consistent lowercase naming such as <strong>instagram</strong> / <strong>social</strong> / <strong>summer_sale</strong> to keep reports clean.</p>
    <div className="tool-output"><small>Generated campaign URL</small><code>{result}</code><div className="tool-actions"><CopyButton value={valid ? result : ""} label="Copy URL" /><button className="button button-secondary" type="button" onClick={reset}>Reset</button>{valid && <button className="button button-secondary" type="button" onClick={() => track("tool_complete", { action: "utm_generated" })}>Track Generation</button>}</div></div></div>
  </Shell>;
}

function WhatsAppTool() {
  const track = useToolAction("whatsapp-link-generator");
  const [phone, setPhone] = useState(""); const [message, setMessage] = useState("Hi, I would like to know more about your services."); const [qr, setQr] = useState(""); const [error, setError] = useState("");
  const normalized = phone.replace(/\D/g, ""); const validPhone = normalized.length >= 8 && normalized.length <= 15; const link = validPhone ? `https://wa.me/${normalized}?text=${encodeURIComponent(message.trim())}` : "";
  const generate = async () => { if (!validPhone) { setError("Enter a valid phone number with country code, for example 919876543210."); return; } if (!message.trim()) { setError("Add a pre-filled message or enter a short message before generating the QR."); return; } setError(""); try { const { default: QRCode } = await import("qrcode"); setQr(await QRCode.toDataURL(link, { width: 420, margin: 2, errorCorrectionLevel: "H" })); track("tool_complete", { action: "qr_generated" }); } catch { setError("The QR code could not be generated. Please try again."); } };
  return <Shell title="WhatsApp Link & QR Generator" description="Create a click-to-chat WhatsApp link and QR code for your business, website or campaign."><div className="tool-panel"><div className="tool-form-grid"><Field label="WhatsApp number (country code included) *" placeholder="919876543210" inputMode="tel" value={phone} onChange={(event) => { setPhone(event.target.value); setQr(""); }} /><label className="tool-field tool-field-wide"><span>Pre-filled message *</span><textarea rows="5" maxLength="1000" value={message} onChange={(event) => setMessage(event.target.value)} /><small>{message.length}/1000 characters</small></label></div><p className="tool-helper">Enter the country code without <strong>+</strong> or spaces. Example: India <strong>91</strong> + mobile number.</p>{error && <p role="alert">{error}</p>}<div className="tool-actions"><button className="button button-primary" type="button" onClick={generate}>Generate WhatsApp QR</button><CopyButton value={link} label="Copy WhatsApp Link" />{link && <a className="button button-secondary" href={link} target="_blank" rel="noreferrer" onClick={() => track("cta_click", { action: "open_whatsapp" })}>Open WhatsApp</a>}</div>{qr && <div className="qr-result"><img src={qr} alt="Generated WhatsApp QR code" width="280" height="280" /><p>Scan to open a WhatsApp chat with your pre-filled message.</p><a className="button button-secondary" href={qr} download="whatsapp-qr.png" onClick={() => track("png_downloaded", { format: "png" })}>Download PNG</a></div>}</div></Shell>;
}

function PaymentReminder() {
  const track = useToolAction("payment-reminder-generator"); const [name, setName] = useState("Customer"); const [amount, setAmount] = useState("5000"); const [invoice, setInvoice] = useState(""); const [date, setDate] = useState(""); const [business, setBusiness] = useState(""); const [paymentLink, setPaymentLink] = useState(""); const [tone, setTone] = useState("polite");
  const message = useMemo(() => { const recipient = name.trim() || "Customer"; const numericAmount = Number(amount); const amountText = Number.isFinite(numericAmount) && numericAmount >= 0 ? money(numericAmount) : "the outstanding amount"; const businessLine = business.trim() ? ` This is from ${business.trim()}.` : ""; const invoiceLine = invoice.trim() ? ` Invoice ${invoice.trim()}` : ""; const dueLine = date ? `, due on ${new Date(`${date}T00:00:00`).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}` : ""; const linkLine = paymentLink.trim() ? ` You can make the payment here: ${paymentLink.trim()}` : ""; if (tone === "firm") return `Hello ${recipient}, this is a reminder that payment of ${amountText}${invoiceLine} is outstanding${dueLine}.${businessLine} Please arrange the payment at your earliest convenience.${linkLine} Thank you.`; return `Hello ${recipient}, just a gentle reminder regarding the outstanding payment of ${amountText}${invoiceLine}${dueLine}.${businessLine} Please let us know if you need any details.${linkLine} Thank you!`; }, [name, amount, invoice, date, business, paymentLink, tone]);
  const shareLink = `https://wa.me/?text=${encodeURIComponent(message)}`; const validPaymentLink = /^https?:\/\//i.test(paymentLink.trim());
  return <Shell title="Payment Reminder Generator" description="Create professional payment reminders ready to copy or share on WhatsApp."><div className="tool-panel"><div className="tool-form-grid"><Field label="Customer name" value={name} onChange={(event) => setName(event.target.value)} placeholder="Customer" /><Field label="Amount (₹) *" type="number" min="0" step="0.01" value={amount} onChange={(event) => setAmount(event.target.value)} /><Field label="Invoice / reference" value={invoice} onChange={(event) => setInvoice(event.target.value)} placeholder="INV-1001" /><Field label="Due date" type="date" value={date} onChange={(event) => setDate(event.target.value)} /><Field label="Business name" value={business} onChange={(event) => setBusiness(event.target.value)} placeholder="Your business" /><Field label="Payment link" type="url" value={paymentLink} onChange={(event) => setPaymentLink(event.target.value)} placeholder="https://..." /><label className="tool-field"><span>Tone</span><select value={tone} onChange={(event) => setTone(event.target.value)}><option value="polite">Polite</option><option value="firm">Firm</option></select></label></div>{paymentLink.trim() && !validPaymentLink && <p role="alert">Payment link should start with http:// or https://</p>}<div className="message-preview" aria-live="polite"><small>Message preview</small><p>{message}</p></div><div className="tool-actions"><CopyButton value={message} label="Copy Message" /><a className="button button-secondary" href={shareLink} target="_blank" rel="noreferrer" onClick={() => track("cta_click", { action: "share_whatsapp" })}>Share on WhatsApp</a>{validPaymentLink && <a className="button button-secondary" href={paymentLink.trim()} target="_blank" rel="noreferrer" onClick={() => track("cta_click", { action: "open_payment_link" })}>Open Payment Link</a>}</div></div></Shell>;
}

export default function ToolPage() {
  const { slug } = useParams(); useToolEvent(slug); useEffect(() => { window.scrollTo({ top: 0, behavior: "smooth" }); }, [slug]);
  if (slug === "gst-invoice-generator") return <GstInvoiceTool />;
  if (slug === "quotation-generator") return <QuotationTool />;
  if (slug === "receipt-generator") return <ReceiptTool />;
  if (slug === "gst-calculator") return <GstCalculatorTool />;
  if (slug === "qr-generator") return <QrGeneratorTool />;
  if (slug === "whatsapp-link-generator") return <WhatsAppTool />;
  if (slug === "payment-reminder-generator") return <PaymentReminder />;
  if (slug === "utm-builder") return <UTMBuilder />;
  return <Shell title="Free Tool" description="Choose one of our available free tools."><div className="tool-panel"><Link className="button button-primary" to="/tools">Browse Free Tools</Link></div></Shell>;
}
