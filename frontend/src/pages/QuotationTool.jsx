import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { createToolDocument, getAttribution, getToolDocuments, getToolPdfUrl, getToolVisitorId, trackToolEvent } from "../services/api";

const money = (n) => `₹${Number(n || 0).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const today = () => new Date().toISOString().slice(0, 10);
const item = () => ({ id: crypto.randomUUID(), name: "", hsn: "", quantity: 1, rate: 0 });
const formatDate = (v) => { if (!v) return "—"; const [y, m, d] = v.split("-"); return d && m && y ? `${d}/${m}/${y}` : v; };

function Field({ label, required, ...props }) {
  return <label className="invoice-field"><span>{label}{required ? " *" : ""}</span><input {...props} /></label>;
}
function Section({ number, title, children }) {
  return <section className="invoice-section"><h2><span>{number}.</span> {title}</h2>{children}</section>;
}

function Preview({ seller, buyer, quote, items, totals }) {
  return <div className="invoice-paper quotation-paper">
    <header className="invoice-paper-header">
      <div className="invoice-brand">
        <div>
          <h2>{seller.name || "Your Business"}</h2>
          {seller.gstin && <p>GSTIN: {seller.gstin}</p>}
          {(seller.email || seller.phone) && <p>{seller.email}{seller.email && seller.phone ? " | " : ""}{seller.phone}</p>}
          {seller.address && <p>{seller.address}</p>}
        </div>
      </div>
      <div className="invoice-title-block"><strong>QUOTATION</strong><span>{quote.number || "QUO-001"}</span></div>
    </header>

    <div className="invoice-info-grid">
      <div className="invoice-party-box"><small>PREPARED FOR</small><strong>{buyer.name || "Customer Name"}</strong>
        {buyer.gstin && <span>GSTIN: {buyer.gstin}</span>}
        {(buyer.email || buyer.phone) && <span>{buyer.email}{buyer.email && buyer.phone ? " | " : ""}{buyer.phone}</span>}
        {buyer.address && <span>{buyer.address}</span>}
      </div>
      <div className="invoice-meta-box">
        <div><span>Quotation Date</span><b>{formatDate(quote.date)}</b></div>
        {quote.validUntil && <div><span>Valid Until</span><b>{formatDate(quote.validUntil)}</b></div>}
        <div><span>Tax Type</span><b>{quote.taxType === "igst" ? "IGST" : "CGST + SGST"}</b></div>
        <div><span>GST Rate</span><b>{Number(quote.gstRate) || 0}%</b></div>
      </div>
    </div>

    <table className="invoice-items-table"><thead><tr><th>#</th><th>Item / Service</th><th>HSN / SAC</th><th>Qty</th><th>Rate (₹)</th><th>Amount (₹)</th></tr></thead>
      <tbody>{items.filter(x => x.name.trim()).map((x, i) => <tr key={x.id}><td>{i + 1}</td><td>{x.name}</td><td>{x.hsn || "—"}</td><td>{Number(x.quantity) || 0}</td><td>{Number(x.rate || 0).toFixed(2)}</td><td>{money((Number(x.quantity) || 0) * (Number(x.rate) || 0)).replace("₹", "")}</td></tr>)}</tbody>
    </table>

    <div className="invoice-summary"><div><span>Subtotal</span><b>{money(totals.gross)}</b></div><div><span>Discount</span><b>- {money(totals.discount)}</b></div><div><span>Taxable Amount</span><b>{money(totals.taxable)}</b></div>
      {quote.taxType === "igst" ? <div><span>IGST ({Number(quote.gstRate) || 0}%)</span><b>{money(totals.tax)}</b></div> : <><div><span>CGST ({(Number(quote.gstRate) || 0) / 2}%)</span><b>{money(totals.tax / 2)}</b></div><div><span>SGST ({(Number(quote.gstRate) || 0) / 2}%)</span><b>{money(totals.tax / 2)}</b></div></>}
      <div className="invoice-grand-total"><span>ESTIMATED TOTAL</span><strong>{money(totals.total)}</strong></div>
    </div>
    <div className="quotation-note">This quotation is an estimate and is subject to the terms agreed with the customer.</div>
  </div>;
}

export default function QuotationTool() {
  const visitorId = getToolVisitorId();
  const [seller, setSeller] = useState({ name: "Your Business", gstin: "", email: "", phone: "", address: "" });
  const [buyer, setBuyer] = useState({ name: "Customer Name", gstin: "", email: "", phone: "", address: "" });
  const [quote, setQuote] = useState({ number: "QUO-001", date: today(), validUntil: "", taxType: "intra", gstRate: "18", discount: "0" });
  const [items, setItems] = useState([item()]);
  const [saved, setSaved] = useState(null); const [history, setHistory] = useState([]); const [saving, setSaving] = useState(false); const [error, setError] = useState("");

  useEffect(() => { getToolDocuments(visitorId).then(docs => setHistory(docs.filter(d => d.document_type === "quotation"))).catch(() => {}); localStorage.setItem("fw_last_tool_slug", "quotation-generator"); const a = getAttribution(); trackToolEvent({ tool: "quotation-generator", event_type: "tool_start", visitor_id: visitorId, session_id: visitorId, ...a }).catch(() => {}); }, [visitorId, saved]);

  const totals = useMemo(() => { const gross = items.reduce((s, x) => s + Math.max(0, Number(x.quantity) || 0) * Math.max(0, Number(x.rate) || 0), 0); const discount = Math.min(gross, Math.max(0, Number(quote.discount) || 0)); const taxable = gross - discount; const tax = taxable * Math.max(0, Number(quote.gstRate) || 0) / 100; return { gross, discount, taxable, tax, total: taxable + tax }; }, [items, quote.discount, quote.gstRate]);
  const update = (set, key, value) => set(v => ({ ...v, [key]: value }));
  const reset = () => { setSeller({ name: "Your Business", gstin: "", email: "", phone: "", address: "" }); setBuyer({ name: "Customer Name", gstin: "", email: "", phone: "", address: "" }); setQuote({ number: "QUO-001", date: today(), validUntil: "", taxType: "intra", gstRate: "18", discount: "0" }); setItems([item()]); setSaved(null); setError(""); };

  const save = async () => { setError(""); const validItems = items.filter(x => x.name.trim()); if (!seller.name.trim() || !buyer.name.trim() || !quote.number.trim() || !validItems.length) { setError("Please enter seller name, buyer name, quotation number and at least one item."); return; } setSaving(true); try { const a = getAttribution(); const doc = await createToolDocument({ tool: "quotation-generator", document_type: "quotation", document_number: quote.number.trim(), visitor_id: visitorId, business_details: seller, customer_details: buyer, line_items: validItems.map(({ id, ...x }) => ({ ...x, quantity: Number(x.quantity) || 0, rate: Number(x.rate) || 0, amount: (Number(x.quantity) || 0) * (Number(x.rate) || 0) })), tax_details: { gst_rate: Number(quote.gstRate) || 0, tax_mode: quote.taxType, cgst: quote.taxType === "intra" ? totals.tax / 2 : 0, sgst: quote.taxType === "intra" ? totals.tax / 2 : 0, igst: quote.taxType === "igst" ? totals.tax : 0 }, totals, metadata: { quotation_date: quote.date, valid_until: quote.validUntil, attribution: a, version: "quotation-v2" } }); setSaved(doc); trackToolEvent({ tool: "quotation-generator", event_type: "document_created", visitor_id: visitorId, session_id: visitorId, document: doc.id, ...a }).catch(() => {}); } catch (e) { setError(e.message || "Could not save quotation. Please make sure the backend is running."); } finally { setSaving(false); } };

  return <main className="invoice-tool-page"><div className="invoice-tool-container">
    <div className="invoice-toolbar"><Link to="/tools" className="invoice-back">← All Free Tools</Link><div className="invoice-toolbar-title"><span className="eyebrow-cyan">FREE TOOL</span><h1>Quotation / Estimate Generator</h1><p>Create professional quotations and estimates and download as PDF</p></div><div className="invoice-toolbar-actions"><button className="invoice-clear" onClick={reset}>Clear All</button>{saved && <a className="invoice-download" href={getToolPdfUrl(saved.id, visitorId)} onClick={() => trackToolEvent({ tool: "quotation-generator", event_type: "pdf_downloaded", visitor_id: visitorId, session_id: visitorId, document: saved.id }).catch(() => {})}>Download PDF</a>}</div></div>
    <div className="invoice-workspace"><div className="invoice-form-panel">
      <Section number="1" title="Seller (Your Business) Details"><div className="invoice-grid two"><Field label="Business Name" required value={seller.name} onChange={e => update(setSeller, "name", e.target.value)} /><Field label="GSTIN" value={seller.gstin} onChange={e => update(setSeller, "gstin", e.target.value.toUpperCase())} /><Field label="Email" type="email" value={seller.email} onChange={e => update(setSeller, "email", e.target.value)} /><Field label="Phone" value={seller.phone} onChange={e => update(setSeller, "phone", e.target.value)} /><label className="invoice-field wide"><span>Address</span><textarea rows="3" value={seller.address} onChange={e => update(setSeller, "address", e.target.value)} /></label></div></Section>
      <Section number="2" title="Buyer (Customer) Details"><div className="invoice-grid two"><Field label="Customer Name" required value={buyer.name} onChange={e => update(setBuyer, "name", e.target.value)} /><Field label="GSTIN" value={buyer.gstin} onChange={e => update(setBuyer, "gstin", e.target.value.toUpperCase())} /><Field label="Email" type="email" value={buyer.email} onChange={e => update(setBuyer, "email", e.target.value)} /><Field label="Phone" value={buyer.phone} onChange={e => update(setBuyer, "phone", e.target.value)} /><label className="invoice-field wide"><span>Address</span><textarea rows="3" value={buyer.address} onChange={e => update(setBuyer, "address", e.target.value)} /></label></div></Section>
      <Section number="3" title="Quotation Details"><div className="invoice-grid three"><Field label="Quotation Number" required value={quote.number} onChange={e => update(setQuote, "number", e.target.value)} /><Field label="Quotation Date" required type="date" value={quote.date} onChange={e => update(setQuote, "date", e.target.value)} /><Field label="Valid Until" type="date" value={quote.validUntil} onChange={e => update(setQuote, "validUntil", e.target.value)} /><label className="invoice-field"><span>Tax Type</span><select value={quote.taxType} onChange={e => update(setQuote, "taxType", e.target.value)}><option value="intra">CGST + SGST</option><option value="igst">IGST</option></select></label><Field label="GST Rate (%)" type="number" min="0" max="100" step="0.01" value={quote.gstRate} onChange={e => update(setQuote, "gstRate", e.target.value)} /><Field label="Discount (₹)" type="number" min="0" step="0.01" value={quote.discount} onChange={e => update(setQuote, "discount", e.target.value)} /></div></Section>
      <Section number="4" title="Items / Services"><div className="invoice-item-editor"><div className="invoice-item-head"><span>#</span><span>Item / Service</span><span>HSN / SAC</span><span>Qty</span><span>Rate (₹)</span><span>Amount (₹)</span><span>Action</span></div>{items.map((x, i) => <div className="invoice-item-row" key={x.id}><span>{i + 1}</span><input placeholder="Item / Service" value={x.name} onChange={e => setItems(l => l.map(v => v.id === x.id ? { ...v, name: e.target.value } : v))} /><input placeholder="HSN / SAC" value={x.hsn} onChange={e => setItems(l => l.map(v => v.id === x.id ? { ...v, hsn: e.target.value } : v))} /><input type="number" min="0" step="1" value={x.quantity} onChange={e => setItems(l => l.map(v => v.id === x.id ? { ...v, quantity: e.target.value } : v))} /><input type="number" min="0" step="0.01" value={x.rate} onChange={e => setItems(l => l.map(v => v.id === x.id ? { ...v, rate: e.target.value } : v))} /><strong>{money((Number(x.quantity) || 0) * (Number(x.rate) || 0))}</strong><button type="button" className="invoice-remove" disabled={items.length === 1} onClick={() => setItems(l => l.filter(v => v.id !== x.id))}>Remove</button></div>)}</div><button type="button" className="invoice-add-item" onClick={() => setItems(l => [...l, item()])}>+ Add Item</button></Section>
      {error && <div className="invoice-error">{error}</div>}<button className="invoice-save" disabled={saving} onClick={save}>{saving ? "Saving…" : "Save Quotation"}</button>
      {history.length > 0 && <div className="tool-history"><h3>Saved quotations</h3>{history.slice(0, 10).map(d => <div key={d.id} className="document-row"><span>{d.document_number}</span><a href={getToolPdfUrl(d.id, visitorId)}>PDF</a></div>)}</div>}
    </div><aside className="invoice-preview-panel"><div className="invoice-preview-label">LIVE PREVIEW</div><Preview seller={seller} buyer={buyer} quote={quote} items={items} totals={totals} /></aside></div>
  </div></main>;
}
