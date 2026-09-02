import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { getAttribution, getToolVisitorId, trackToolEvent } from "../services/api";

const money = (value) => `₹${Number(value || 0).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const rates = [0, 0.25, 3, 5, 12, 18, 28];

function Field({ label, ...props }) {
  return <label className="gstc-field"><span>{label}</span><input {...props} /></label>;
}

export default function GstCalculatorTool() {
  const [amount, setAmount] = useState("10000");
  const [rateOption, setRateOption] = useState("18");
  const [customRate, setCustomRate] = useState("18");
  const [mode, setMode] = useState("add");
  const [taxType, setTaxType] = useState("intra");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const visitorId = getToolVisitorId();
    const attribution = getAttribution();
    trackToolEvent({ tool: "gst-calculator", event_type: "tool_start", visitor_id: visitorId, session_id: visitorId, ...attribution }).catch(() => {});
  }, []);

  const result = useMemo(() => {
    const input = Math.max(0, Number(amount) || 0);
    const gstRate = Math.max(0, Number(rateOption === "custom" ? customRate : rateOption) || 0);
    if (mode === "remove") {
      const taxable = gstRate ? input / (1 + gstRate / 100) : input;
      const gst = input - taxable;
      return { taxable, gst, total: input, gstRate };
    }
    const gst = input * gstRate / 100;
    return { taxable: input, gst, total: input + gst, gstRate };
  }, [amount, rateOption, customRate, mode]);

  const split = result.gst / 2;
  const summary = `GST Calculator\nTaxable amount: ${money(result.taxable)}\n${taxType === "intra" ? `CGST: ${money(split)}\nSGST: ${money(split)}` : `IGST: ${money(result.gst)}`}\nGST: ${money(result.gst)}\nTotal: ${money(result.total)}`;

  const copyResult = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
      const visitorId = getToolVisitorId();
      trackToolEvent({ tool: "gst-calculator", event_type: "copy", visitor_id: visitorId, session_id: visitorId, ...getAttribution(), metadata: { mode, tax_type: taxType, gst_rate: result.gstRate } }).catch(() => {});
    } catch {
      setCopied(false);
    }
  };

  const reset = () => {
    setAmount("10000");
    setRateOption("18");
    setCustomRate("18");
    setMode("add");
    setTaxType("intra");
    setCopied(false);
  };

  return (
    <main className="gstc-page">
      <div className="gstc-container">
        <Link className="tool-back" to="/tools">← All Free Tools</Link>
        <header className="gstc-heading">
          <span className="eyebrow-cyan">FREE GST TOOL</span>
          <h1>GST Calculator</h1>
          <p>Calculate GST instantly with an accurate tax breakdown for inclusive or exclusive pricing.</p>
        </header>

        <section className="gstc-workspace">
          <div className="gstc-panel">
            <div className="gstc-section-title"><div><span>01</span><h2>Enter your amount</h2></div><button type="button" onClick={reset}>Reset</button></div>
            <div className="gstc-amount-wrap"><span>₹</span><input aria-label="Amount" type="number" min="0" step="0.01" value={amount} onChange={(e) => setAmount(e.target.value)} /></div>
            <div className="gstc-presets">{[1000, 5000, 10000, 50000, 100000].map((value) => <button type="button" key={value} className={Number(amount) === value ? "active" : ""} onClick={() => setAmount(String(value))}>{money(value)}</button>)}</div>

            <div className="gstc-section-title compact"><div><span>02</span><h2>Calculation type</h2></div></div>
            <div className="gstc-toggle" role="group" aria-label="GST calculation type">
              <button type="button" className={mode === "add" ? "active" : ""} onClick={() => setMode("add")}><strong>Add GST</strong><small>Amount is before GST</small></button>
              <button type="button" className={mode === "remove" ? "active" : ""} onClick={() => setMode("remove")}><strong>Remove GST</strong><small>Amount already includes GST</small></button>
            </div>

            <div className="gstc-form-grid">
              <label className="gstc-field"><span>GST Rate</span><select value={rateOption} onChange={(e) => setRateOption(e.target.value)}>{rates.map((value) => <option value={value} key={value}>{value}%</option>)}<option value="custom">Custom</option></select></label>
              {rateOption === "custom" && <Field label="Custom GST Rate (%)" type="number" min="0" step="0.01" value={customRate} onChange={(e) => setCustomRate(e.target.value)} />}
              <label className="gstc-field"><span>Tax Type</span><select value={taxType} onChange={(e) => setTaxType(e.target.value)}><option value="intra">CGST + SGST (Intra-state)</option><option value="inter">IGST (Inter-state)</option></select></label>
            </div>
            <p className="gstc-note">For intra-state sales, GST is split equally between CGST and SGST. For inter-state sales, the full GST is shown as IGST.</p>
          </div>

          <aside className="gstc-result-panel">
            <div className="gstc-result-top"><span>CALCULATION RESULT</span><strong>{mode === "add" ? "GST added" : "GST removed"}</strong></div>
            <div className="gstc-total"><small>Final amount</small><strong>{money(result.total)}</strong><span>{result.gstRate}% GST included</span></div>
            <div className="gstc-breakdown">
              <div><span>Taxable amount</span><strong>{money(result.taxable)}</strong></div>
              {taxType === "intra" ? <><div><span>CGST ({result.gstRate / 2}%)</span><strong>{money(split)}</strong></div><div><span>SGST ({result.gstRate / 2}%)</span><strong>{money(split)}</strong></div></> : <div><span>IGST ({result.gstRate}%)</span><strong>{money(result.gst)}</strong></div>}
              <div className="gstc-gst-total"><span>Total GST</span><strong>{money(result.gst)}</strong></div>
              <div className="gstc-grand"><span>Total</span><strong>{money(result.total)}</strong></div>
            </div>
            <button className="button button-primary gstc-copy" type="button" onClick={copyResult}>{copied ? "✓ Result Copied" : "Copy Result"}</button>
          </aside>
        </section>

        <section className="gstc-info">
          <h2>How GST calculation works</h2>
          <div className="gstc-info-grid">
            <div><strong>Add GST</strong><p>GST is calculated on the entered taxable amount and added to it. Example: ₹10,000 at 18% GST = ₹11,800.</p></div>
            <div><strong>Remove GST</strong><p>When your entered amount already includes GST, the calculator separates the taxable value from the included tax.</p></div>
            <div><strong>CGST + SGST</strong><p>For an intra-state transaction, the GST amount is split equally into Central GST and State GST.</p></div>
            <div><strong>IGST</strong><p>For an inter-state transaction, the complete GST amount is represented as Integrated GST.</p></div>
          </div>
        </section>
      </div>
    </main>
  );
}
