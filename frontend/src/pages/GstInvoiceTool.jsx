import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  createToolDocument,
  getAttribution,
  getToolDocuments,
  getToolPdfUrl,
  getToolVisitorId,
  trackToolEvent,
} from "../services/api";
import "../styles/free-tools.css";

const money = (n) => `₹${Number(n || 0).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const dateValue = () => new Date().toISOString().slice(0, 10);
const makeItem = () => ({ id: crypto.randomUUID(), name: "", hsn: "", quantity: 1, rate: 0 });

function Field({ label, required, ...props }) {
  return <label className="invoice-field"><span>{label}{required ? " *" : ""}</span><input {...props} /></label>;
}

function Section({ number, title, children }) {
  return <section className="invoice-section"><h2><span>{number}.</span> {title}</h2>{children}</section>;
}

function formatDate(value) {
  if (!value) return "—";
  const [y, m, d] = value.split("-");
  return d && m && y ? `${d}/${m}/${y}` : value;
}

function InvoicePreview({ seller, buyer, invoice, items, totals }) {
  const taxRate = Number(invoice.gstRate) || 0;
  return (
    <div className="invoice-paper">
      <header className="invoice-paper-header">
        <div className="invoice-brand">
          <div className="invoice-logo-mark">FW</div>
          <div>
            <h2>{seller.name || "Your Business"}</h2>
            {seller.gstin && <p>GSTIN: {seller.gstin}</p>}
            {(seller.email || seller.phone) && <p>{seller.email}{seller.email && seller.phone ? " | " : ""}{seller.phone}</p>}
            {seller.address && <p>{seller.address}</p>}
          </div>
        </div>
        <div className="invoice-title-block"><strong>TAX INVOICE</strong><span>{invoice.number || "INV-001"}</span></div>
      </header>

      <div className="invoice-info-grid">
        <div className="invoice-party-box">
          <small>BILL TO</small>
          <strong>{buyer.name || "Customer Name"}</strong>
          {buyer.gstin && <span>GSTIN: {buyer.gstin}</span>}
          {(buyer.email || buyer.phone) && <span>{buyer.email}{buyer.email && buyer.phone ? " | " : ""}{buyer.phone}</span>}
          {buyer.address && <span>{buyer.address}</span>}
        </div>
        <div className="invoice-meta-box">
          <div><span>Invoice Date</span><b>{formatDate(invoice.date)}</b></div>
          {invoice.dueDate && <div><span>Due Date</span><b>{formatDate(invoice.dueDate)}</b></div>}
          <div><span>Tax Type</span><b>{invoice.taxType === "igst" ? "IGST" : "CGST + SGST"}</b></div>
          <div><span>GST Rate</span><b>{taxRate}%</b></div>
        </div>
      </div>

      <table className="invoice-items-table">
        <thead><tr><th>#</th><th>Item / Service</th><th>HSN / SAC</th><th>Qty</th><th>Rate (₹)</th><th>Amount (₹)</th></tr></thead>
        <tbody>{items.map((item, index) => <tr key={item.id}><td>{index + 1}</td><td>{item.name || "Item / Service"}</td><td>{item.hsn || "—"}</td><td>{item.quantity}</td><td>{Number(item.rate || 0).toFixed(2)}</td><td>{Number(item.quantity || 0) * Number(item.rate || 0) > 0 ? (Number(item.quantity || 0) * Number(item.rate || 0)).toFixed(2) : "0.00"}</td></tr>)}</tbody>
      </table>

      <div className="invoice-summary">
        <div><span>Subtotal</span><b>{money(totals.gross)}</b></div>
        <div><span>Discount</span><b>- {money(totals.discount)}</b></div>
        <div><span>Taxable Amount</span><b>{money(totals.taxable)}</b></div>
        {invoice.taxType === "igst" ? <div><span>IGST ({taxRate}%)</span><b>{money(totals.tax)}</b></div> : <><div><span>CGST ({taxRate / 2}%)</span><b>{money(totals.tax / 2)}</b></div><div><span>SGST ({taxRate / 2}%)</span><b>{money(totals.tax / 2)}</b></div></>}
        <div className="invoice-grand-total"><span>TOTAL</span><strong>{money(totals.total)}</strong></div>
      </div>
      <div className="invoice-thankyou">Thank you for your business!</div>
    </div>
  );
}

export default function GstInvoiceTool() {
  const visitorId = getToolVisitorId();
  const [seller, setSeller] = useState({ name: "Your Business", gstin: "", email: "", phone: "", address: "" });
  const [buyer, setBuyer] = useState({ name: "Customer Name", gstin: "", email: "", phone: "", address: "" });
  const [invoice, setInvoice] = useState({ number: "INV-001", date: dateValue(), dueDate: "", taxType: "intra", gstRate: "18", discount: "0" });
  const [items, setItems] = useState([makeItem()]);
  const [saved, setSaved] = useState(null);
  const [history, setHistory] = useState([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getToolDocuments(visitorId).then((docs) => setHistory(docs.filter((doc) => doc.document_type === "invoice"))).catch(() => {});
    localStorage.setItem("fw_last_tool_slug", "gst-invoice-generator");
    const attribution = getAttribution();
    trackToolEvent({ tool: "gst-invoice-generator", event_type: "tool_start", visitor_id: visitorId, session_id: visitorId, ...attribution }).catch(() => {});
  }, [visitorId, saved]);

  const totals = useMemo(() => {
    const gross = items.reduce((sum, item) => sum + Math.max(0, Number(item.quantity) || 0) * Math.max(0, Number(item.rate) || 0), 0);
    const discount = Math.min(gross, Math.max(0, Number(invoice.discount) || 0));
    const taxable = gross - discount;
    const tax = taxable * Math.max(0, Number(invoice.gstRate) || 0) / 100;
    return { gross, discount, taxable, tax, total: taxable + tax };
  }, [items, invoice.discount, invoice.gstRate]);

  const reset = () => {
    setSeller({ name: "Your Business", gstin: "", email: "", phone: "", address: "" });
    setBuyer({ name: "Customer Name", gstin: "", email: "", phone: "", address: "" });
    setInvoice({ number: "INV-001", date: dateValue(), dueDate: "", taxType: "intra", gstRate: "18", discount: "0" });
    setItems([makeItem()]); setSaved(null); setError("");
  };

  const save = async () => {
    setError("");
    const validItems = items.filter((item) => item.name.trim());
    if (!seller.name.trim() || !buyer.name.trim() || !invoice.number.trim() || validItems.length === 0) {
      setError("Please enter seller name, buyer name, invoice number and at least one item.");
      return;
    }
    setSaving(true);
    try {
      const attribution = getAttribution();
      const doc = await createToolDocument({
        tool: "gst-invoice-generator",
        document_type: "invoice",
        document_number: invoice.number.trim(),
        visitor_id: visitorId,
        business_details: seller,
        customer_details: buyer,
        line_items: validItems.map(({ id, ...item }) => ({ ...item, quantity: Number(item.quantity) || 0, rate: Number(item.rate) || 0, amount: (Number(item.quantity) || 0) * (Number(item.rate) || 0) })),
        tax_details: { gst_rate: Number(invoice.gstRate) || 0, tax_mode: invoice.taxType, cgst: invoice.taxType === "intra" ? totals.tax / 2 : 0, sgst: invoice.taxType === "intra" ? totals.tax / 2 : 0, igst: invoice.taxType === "igst" ? totals.tax : 0 },
        totals,
        metadata: { invoice_date: invoice.date, due_date: invoice.dueDate, attribution, version: "gst-invoice-v3" },
      });
      setSaved(doc);
      trackToolEvent({ tool: "gst-invoice-generator", event_type: "document_created", visitor_id: visitorId, session_id: visitorId, document: doc.id, ...attribution }).catch(() => {});
    } catch (e) {
      setError(e.message || "Could not save invoice. Please make sure the backend is running.");
    } finally { setSaving(false); }
  };

  return (
    <main className="invoice-tool-page">
      <div className="invoice-tool-container">
        <div className="invoice-toolbar">
          <Link to="/tools" className="invoice-back">← All Free Tools</Link>
          <div className="invoice-toolbar-title"><span className="eyebrow-cyan">FREE TOOL</span><h1>GST Invoice Generator</h1><p>Create professional GST invoices and download as PDF</p></div>
          <div className="invoice-toolbar-actions"><button className="invoice-clear" onClick={reset}>Clear All</button>{saved && <a className="invoice-download" href={getToolPdfUrl(saved.id, visitorId)} onClick={() => trackToolEvent({ tool: "gst-invoice-generator", event_type: "pdf_downloaded", visitor_id: visitorId, session_id: visitorId, document: saved.id })}>Download PDF</a>}</div>
        </div>

        <div className="invoice-workspace">
          <div className="invoice-form-panel">
            <Section number="1" title="Seller (Your Business) Details">
              <div className="invoice-grid two"><Field label="Business Name" required value={seller.name} onChange={(e) => setSeller((v) => ({ ...v, name: e.target.value }))} /><Field label="GSTIN" required placeholder="22AAAAA0000A1Z5" value={seller.gstin} onChange={(e) => setSeller((v) => ({ ...v, gstin: e.target.value.toUpperCase() }))} /><Field label="Email" type="email" value={seller.email} onChange={(e) => setSeller((v) => ({ ...v, email: e.target.value }))} /><Field label="Phone" required value={seller.phone} onChange={(e) => setSeller((v) => ({ ...v, phone: e.target.value }))} /><label className="invoice-field wide"><span>Address</span><textarea rows="3" value={seller.address} onChange={(e) => setSeller((v) => ({ ...v, address: e.target.value }))} /></label></div>
            </Section>

            <Section number="2" title="Buyer (Customer) Details">
              <div className="invoice-grid two"><Field label="Customer Name" required value={buyer.name} onChange={(e) => setBuyer((v) => ({ ...v, name: e.target.value }))} /><Field label="GSTIN" value={buyer.gstin} onChange={(e) => setBuyer((v) => ({ ...v, gstin: e.target.value.toUpperCase() }))} /><Field label="Email" type="email" value={buyer.email} onChange={(e) => setBuyer((v) => ({ ...v, email: e.target.value }))} /><Field label="Phone" value={buyer.phone} onChange={(e) => setBuyer((v) => ({ ...v, phone: e.target.value }))} /><label className="invoice-field wide"><span>Address</span><textarea rows="3" value={buyer.address} onChange={(e) => setBuyer((v) => ({ ...v, address: e.target.value }))} /></label></div>
            </Section>

            <Section number="3" title="Invoice Details">
              <div className="invoice-grid three"><Field label="Invoice Number" required value={invoice.number} onChange={(e) => setInvoice((v) => ({ ...v, number: e.target.value }))} /><Field label="Invoice Date" required type="date" value={invoice.date} onChange={(e) => setInvoice((v) => ({ ...v, date: e.target.value }))} /><Field label="Due Date" type="date" value={invoice.dueDate} onChange={(e) => setInvoice((v) => ({ ...v, dueDate: e.target.value }))} /><label className="invoice-field"><span>Tax Type</span><select value={invoice.taxType} onChange={(e) => setInvoice((v) => ({ ...v, taxType: e.target.value }))}><option value="intra">CGST + SGST</option><option value="igst">IGST</option></select></label><Field label="GST Rate (%)" type="number" min="0" max="100" step="0.01" value={invoice.gstRate} onChange={(e) => setInvoice((v) => ({ ...v, gstRate: e.target.value }))} /><Field label="Discount (₹)" type="number" min="0" step="0.01" value={invoice.discount} onChange={(e) => setInvoice((v) => ({ ...v, discount: e.target.value }))} /></div>
            </Section>

            <Section number="4" title="Items / Services">
              <div className="invoice-item-editor">
                <div className="invoice-item-head"><span>#</span><span>Item / Service</span><span>HSN / SAC</span><span>Qty</span><span>Rate (₹)</span><span>Amount (₹)</span><span>Action</span></div>
                {items.map((item, index) => <div className="invoice-item-row" key={item.id}><span>{index + 1}</span><input placeholder="Item / Service" value={item.name} onChange={(e) => setItems((list) => list.map((x) => x.id === item.id ? { ...x, name: e.target.value } : x))} /><input placeholder="HSN / SAC" value={item.hsn} onChange={(e) => setItems((list) => list.map((x) => x.id === item.id ? { ...x, hsn: e.target.value } : x))} /><input type="number" min="0" step="1" value={item.quantity} onChange={(e) => setItems((list) => list.map((x) => x.id === item.id ? { ...x, quantity: e.target.value } : x))} /><input type="number" min="0" step="0.01" value={item.rate} onChange={(e) => setItems((list) => list.map((x) => x.id === item.id ? { ...x, rate: e.target.value } : x))} /><strong>{money((Number(item.quantity) || 0) * (Number(item.rate) || 0))}</strong><button type="button" className="invoice-remove" disabled={items.length === 1} onClick={() => setItems((list) => list.filter((x) => x.id !== item.id))}>Remove</button></div>)}
              </div>
              <button type="button" className="invoice-add-item" onClick={() => setItems((list) => [...list, makeItem()])}>+ Add Item</button>
            </Section>

            {error && <div className="invoice-error">{error}</div>}
            <button className="invoice-save" disabled={saving} onClick={save}>{saving ? "Saving…" : "Save Invoice"}</button>
          </div>

          <aside className="invoice-preview-panel"><div className="invoice-preview-label">LIVE PREVIEW</div><InvoicePreview seller={seller} buyer={buyer} invoice={invoice} items={items} totals={totals} /></aside>
        </div>
      </div>
    </main>
  );
}
