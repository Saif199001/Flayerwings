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

const money = (n) =>
  `₹${Number(n || 0).toLocaleString("en-IN", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;

const makeItem = () => ({ id: crypto.randomUUID(), name: "", quantity: 1, rate: 0 });

function Field({ label, ...props }) {
  return (
    <label className="tool-field">
      <span>{label}</span>
      <input {...props} />
    </label>
  );
}

export default function GstInvoiceTool() {
  const visitorId = getToolVisitorId();
  const [business, setBusiness] = useState({ name: "Your Business", gstin: "", address: "", phone: "", email: "" });
  const [customer, setCustomer] = useState({ name: "Customer Name", gstin: "", address: "", phone: "", email: "" });
  const [number, setNumber] = useState("INV-001");
  const [invoiceDate, setInvoiceDate] = useState(new Date().toISOString().slice(0, 10));
  const [dueDate, setDueDate] = useState("");
  const [taxMode, setTaxMode] = useState("intra");
  const [gstRate, setGstRate] = useState("18");
  const [discount, setDiscount] = useState("0");
  const [items, setItems] = useState([makeItem()]);
  const [saved, setSaved] = useState(null);
  const [history, setHistory] = useState([]);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    getToolDocuments(visitorId).then(setHistory).catch(() => {});
  }, [visitorId, saved]);

  const calculations = useMemo(() => {
    const gross = items.reduce((sum, item) => sum + (Number(item.quantity) || 0) * (Number(item.rate) || 0), 0);
    const discountAmount = Math.min(Math.max(Number(discount) || 0, 0), gross);
    const subtotal = gross - discountAmount;
    const tax = subtotal * (Math.max(Number(gstRate) || 0, 0) / 100);
    return { gross, discountAmount, subtotal, tax, total: subtotal + tax };
  }, [items, discount, gstRate]);

  const updateBusiness = (key, value) => setBusiness((current) => ({ ...current, [key]: value }));
  const updateCustomer = (key, value) => setCustomer((current) => ({ ...current, [key]: value }));
  const updateItem = (id, key, value) => setItems((current) => current.map((item) => (item.id === id ? { ...item, [key]: value } : item)));
  const removeItem = (id) => setItems((current) => current.length === 1 ? current : current.filter((item) => item.id !== id));

  const save = async () => {
    setSaving(true);
    try {
      const attribution = getAttribution();
      const doc = await createToolDocument({
        tool: "gst-invoice-generator",
        document_type: "invoice",
        document_number: number.trim() || "INV-001",
        visitor_id: visitorId,
        business_details: business,
        customer_details: customer,
        line_items: items.map(({ id, name, quantity, rate }) => ({
          name: name.trim() || "Item / Service",
          quantity: Number(quantity) || 0,
          rate: Number(rate) || 0,
          amount: (Number(quantity) || 0) * (Number(rate) || 0),
        })),
        tax_details: {
          gst_rate: Number(gstRate) || 0,
          tax_mode: taxMode,
          cgst: taxMode === "intra" ? calculations.tax / 2 : 0,
          sgst: taxMode === "intra" ? calculations.tax / 2 : 0,
          igst: taxMode === "inter" ? calculations.tax : 0,
        },
        totals: {
          gross: calculations.gross,
          discount: calculations.discountAmount,
          subtotal: calculations.subtotal,
          tax: calculations.tax,
          total: calculations.total,
        },
        metadata: { invoice_date: invoiceDate, due_date: dueDate, attribution },
      });
      setSaved(doc);
      trackToolEvent({ tool: "gst-invoice-generator", event_type: "document_created", visitor_id: visitorId, document: doc.id, ...attribution }).catch(() => {});
    } catch (error) {
      window.alert(error.message || "Could not save invoice");
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="tool-page">
      <div className="tool-container">
        <Link className="tool-back" to="/tools">← All Free Tools</Link>
        <div className="tool-heading">
          <span className="eyebrow-cyan">FREE TOOL</span>
          <h1>GST Invoice Generator</h1>
          <p>Create a professional GST invoice with multiple items, tax breakdown, customer details and a downloadable PDF.</p>
        </div>

        <div className="tool-workspace">
          <div className="tool-panel">
            <h2>Business details</h2>
            <div className="tool-form-grid">
              <Field label="Business name" value={business.name} onChange={(e) => updateBusiness("name", e.target.value)} />
              <Field label="GSTIN (optional)" value={business.gstin} onChange={(e) => updateBusiness("gstin", e.target.value.toUpperCase())} placeholder="22AAAAA0000A1Z5" />
              <Field label="Phone (optional)" value={business.phone} onChange={(e) => updateBusiness("phone", e.target.value)} />
              <Field label="Email (optional)" type="email" value={business.email} onChange={(e) => updateBusiness("email", e.target.value)} />
              <label className="tool-field tool-field-wide"><span>Business address</span><textarea rows="3" value={business.address} onChange={(e) => updateBusiness("address", e.target.value)} /></label>
            </div>

            <h2>Customer details</h2>
            <div className="tool-form-grid">
              <Field label="Customer name" value={customer.name} onChange={(e) => updateCustomer("name", e.target.value)} />
              <Field label="Customer GSTIN (optional)" value={customer.gstin} onChange={(e) => updateCustomer("gstin", e.target.value.toUpperCase())} />
              <Field label="Phone (optional)" value={customer.phone} onChange={(e) => updateCustomer("phone", e.target.value)} />
              <Field label="Email (optional)" type="email" value={customer.email} onChange={(e) => updateCustomer("email", e.target.value)} />
              <label className="tool-field tool-field-wide"><span>Customer address</span><textarea rows="3" value={customer.address} onChange={(e) => updateCustomer("address", e.target.value)} /></label>
            </div>

            <h2>Invoice details</h2>
            <div className="tool-form-grid">
              <Field label="Invoice number" value={number} onChange={(e) => setNumber(e.target.value)} />
              <Field label="Invoice date" type="date" value={invoiceDate} onChange={(e) => setInvoiceDate(e.target.value)} />
              <Field label="Due date (optional)" type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} />
              <Field label="GST rate (%)" type="number" min="0" max="100" step="0.01" value={gstRate} onChange={(e) => setGstRate(e.target.value)} />
              <label className="tool-field"><span>Tax type</span><select value={taxMode} onChange={(e) => setTaxMode(e.target.value)}><option value="intra">CGST + SGST</option><option value="inter">IGST</option></select></label>
              <Field label="Discount (₹)" type="number" min="0" value={discount} onChange={(e) => setDiscount(e.target.value)} />
            </div>

            <div className="tool-history">
              <div className="document-row document-row-head"><span>Item / Service</span><span>Qty × Rate</span></div>
              {items.map((item) => (
                <div className="document-row" key={item.id} style={{ gap: "12px", alignItems: "center" }}>
                  <input aria-label="Item or service" value={item.name} placeholder="Item / Service" onChange={(e) => updateItem(item.id, "name", e.target.value)} style={{ flex: 2 }} />
                  <input aria-label="Quantity" type="number" min="0" step="0.01" value={item.quantity} onChange={(e) => updateItem(item.id, "quantity", e.target.value)} style={{ width: "80px" }} />
                  <input aria-label="Rate" type="number" min="0" step="0.01" value={item.rate} onChange={(e) => updateItem(item.id, "rate", e.target.value)} style={{ width: "120px" }} />
                  <strong>{money((Number(item.quantity) || 0) * (Number(item.rate) || 0))}</strong>
                  <button type="button" className="button button-secondary" onClick={() => removeItem(item.id)} disabled={items.length === 1}>Remove</button>
                </div>
              ))}
              <button type="button" className="button button-secondary" onClick={() => setItems((current) => [...current, makeItem()])}>+ Add item</button>
            </div>

            <div className="document-preview">
              <div className="document-head">
                <div><h2>{business.name || "Your Business"}</h2><span>GST Invoice {business.gstin && `• ${business.gstin}`}</span></div>
                <strong>{number || "INV-001"}</strong>
              </div>
              <div className="document-meta">
                <span>Bill To<br /><b>{customer.name || "Customer Name"}</b>{customer.gstin && <><br />{customer.gstin}</>}</span>
                <span>Date<br /><b>{invoiceDate || "—"}</b>{dueDate && <><br />Due: <b>{dueDate}</b></>}</span>
              </div>
              {items.map((item) => <div className="document-row" key={item.id}><span>{item.name || "Item / Service"} × {item.quantity || 0}</span><span>{money((Number(item.quantity) || 0) * (Number(item.rate) || 0))}</span></div>)}
              <div className="document-total">
                <span>Subtotal</span><b>{money(calculations.gross)}</b>
                <span>Discount</span><b>- {money(calculations.discountAmount)}</b>
                {taxMode === "intra" ? <><span>CGST ({Number(gstRate || 0) / 2}%)</span><b>{money(calculations.tax / 2)}</b><span>SGST ({Number(gstRate || 0) / 2}%)</span><b>{money(calculations.tax / 2)}</b></> : <><span>IGST ({gstRate}%)</span><b>{money(calculations.tax)}</b></>}
                <span>Total</span><strong>{money(calculations.total)}</strong>
              </div>
            </div>

            <div className="tool-actions">
              <button className="button button-primary" disabled={saving || !number.trim() || calculations.total < 0} onClick={save}>{saving ? "Saving…" : "Save Invoice"}</button>
              {saved && <a className="button button-secondary" href={getToolPdfUrl(saved.id, visitorId)} onClick={() => trackToolEvent({ tool: "gst-invoice-generator", event_type: "pdf_downloaded", visitor_id: visitorId, document: saved.id })}>Download PDF</a>}
            </div>

            {history.length > 0 && <div className="tool-history"><h3>Saved invoices</h3>{history.slice(0, 10).filter((d) => d.document_type === "invoice").map((d) => <div key={d.id} className="document-row"><span>{d.document_number}</span><a href={getToolPdfUrl(d.id, visitorId)}>PDF</a></div>)}</div>}
          </div>
        </div>
      </div>
    </main>
  );
}
