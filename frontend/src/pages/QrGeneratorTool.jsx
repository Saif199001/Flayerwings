import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import QRCode from "qrcode";
import { getAttribution, getToolVisitorId, trackToolEvent } from "../services/api";
import "../styles/qr-generator.css";

const presets = [
  ["Website", "https://flayerwings.com"],
  ["WhatsApp", "https://wa.me/919876543210"],
  ["Google", "https://www.google.com"],
];

export default function QrGeneratorTool() {
  const [value, setValue] = useState("https://flayerwings.com");
  const [logo, setLogo] = useState("");
  const [logoName, setLogoName] = useState("");
  const [size, setSize] = useState("600");
  const [margin, setMargin] = useState("4");
  const [errorCorrection, setErrorCorrection] = useState("H");
  const [qr, setQr] = useState("");
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const visitorId = getToolVisitorId();
    trackToolEvent({ tool: "qr-generator", event_type: "tool_start", visitor_id: visitorId, session_id: visitorId, ...getAttribution() }).catch(() => {});
  }, []);

  const contentLength = useMemo(() => value.trim().length, [value]);

  const generate = async () => {
    const text = value.trim();
    setError("");
    setCopied(false);
    if (!text) {
      setError("Enter some content before generating your QR code.");
      return;
    }
    try {
      const dataUrl = await QRCode.toDataURL(text, {
        width: Number(size),
        margin: Number(margin),
        errorCorrectionLevel: errorCorrection,
        color: { dark: "#111827", light: "#ffffff" },
      });
      if (!logo) {
        setQr(dataUrl);
        trackToolEvent({ tool: "qr-generator", event_type: "tool_complete", visitor_id: getToolVisitorId(), session_id: getToolVisitorId(), ...getAttribution(), metadata: { branded: false, content_length: text.length } }).catch(() => {});
        return;
      }

      const canvas = document.createElement("canvas");
      canvas.width = Number(size);
      canvas.height = Number(size);
      const ctx = canvas.getContext("2d");
      const base = new Image();
      base.onload = () => {
        ctx.drawImage(base, 0, 0);
        const image = new Image();
        image.onload = () => {
          const logoSize = canvas.width * 0.18;
          const x = (canvas.width - logoSize) / 2;
          const y = (canvas.height - logoSize) / 2;
          const pad = logoSize * 0.16;
          ctx.fillStyle = "#ffffff";
          ctx.fillRect(x - pad, y - pad, logoSize + pad * 2, logoSize + pad * 2);
          ctx.save();
          ctx.beginPath();
          ctx.roundRect(x, y, logoSize, logoSize, logoSize * 0.16);
          ctx.clip();
          ctx.drawImage(image, x, y, logoSize, logoSize);
          ctx.restore();
          setQr(canvas.toDataURL("image/png"));
          trackToolEvent({ tool: "qr-generator", event_type: "tool_complete", visitor_id: getToolVisitorId(), session_id: getToolVisitorId(), ...getAttribution(), metadata: { branded: true, content_length: text.length } }).catch(() => {});
        };
        image.onerror = () => setError("The selected logo could not be processed. Try another image.");
        image.src = logo;
      };
      base.onerror = () => setError("Could not generate the QR code. Try shorter content.");
      base.src = dataUrl;
    } catch {
      setError("Could not generate this QR code. Try shorter content or different settings.");
    }
  };

  const copyContent = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
      trackToolEvent({ tool: "qr-generator", event_type: "copy", visitor_id: getToolVisitorId(), session_id: getToolVisitorId(), ...getAttribution() }).catch(() => {});
    } catch {
      setCopied(false);
    }
  };

  const downloadName = logo ? "branded-qr-code.png" : "qr-code.png";

  return (
    <main className="qrg-page">
      <div className="qrg-container">
        <Link className="tool-back" to="/tools">← All Free Tools</Link>
        <header className="qrg-heading">
          <span className="eyebrow-cyan">FREE QR TOOL</span>
          <h1>QR Code Generator</h1>
          <p>Create high-quality QR codes for links, text, WhatsApp, menus, payments and campaigns — with an optional logo.</p>
        </header>

        <section className="qrg-workspace">
          <div className="qrg-panel">
            <div className="qrg-section-head"><div><span>01</span><h2>QR content</h2></div><small>{contentLength} characters</small></div>
            <textarea className="qrg-content" value={value} onChange={(e) => setValue(e.target.value)} placeholder="Enter a URL, text, contact details, payment link, etc." rows="5" />
            <div className="qrg-presets"><span>Quick start</span>{presets.map(([label, content]) => <button type="button" key={label} onClick={() => setValue(content)}>{label}</button>)}</div>

            <div className="qrg-section-head qrg-mt"><div><span>02</span><h2>Brand your QR</h2></div><small>Optional</small></div>
            <label className="qrg-upload"><input type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => { const file = e.target.files?.[0]; if (!file) return; if (file.size > 3 * 1024 * 1024) { setError("Logo must be 3 MB or smaller."); return; } const reader = new FileReader(); reader.onload = () => { setLogo(String(reader.result)); setLogoName(file.name); setError(""); }; reader.readAsDataURL(file); }} /><strong>{logoName || "Upload a logo"}</strong><span>PNG, JPG or WebP · max 3 MB</span></label>
            {logo && <button type="button" className="qrg-remove-logo" onClick={() => { setLogo(""); setLogoName(""); }}>Remove logo</button>}

            <div className="qrg-section-head qrg-mt"><div><span>03</span><h2>Output settings</h2></div></div>
            <div className="qrg-settings">
              <label><span>Size</span><select value={size} onChange={(e) => setSize(e.target.value)}><option value="400">400 × 400</option><option value="600">600 × 600</option><option value="1000">1000 × 1000</option></select></label>
              <label><span>Margin</span><select value={margin} onChange={(e) => setMargin(e.target.value)}><option value="2">Compact</option><option value="4">Standard</option><option value="6">Wide</option></select></label>
              <label><span>Error correction</span><select value={errorCorrection} onChange={(e) => setErrorCorrection(e.target.value)}><option value="M">Medium</option><option value="Q">High</option><option value="H">Highest — best for logos</option></select></label>
            </div>
            <p className="qrg-note">Highest error correction is selected automatically for logo-ready QR codes. Keep the logo small so scanners can still read the code reliably.</p>
            {error && <div className="qrg-error" role="alert">{error}</div>}
            <div className="qrg-actions"><button type="button" className="button button-primary" onClick={generate}>Generate QR Code</button><button type="button" className="button button-secondary" onClick={copyContent}>{copied ? "✓ Content Copied" : "Copy Content"}</button></div>
          </div>

          <aside className="qrg-result">
            <div className="qrg-result-head"><span>LIVE OUTPUT</span><strong>{logo ? "Branded QR" : "Standard QR"}</strong></div>
            <div className="qrg-preview">{qr ? <img src={qr} alt="Generated QR code" /> : <div className="qrg-empty"><div>QR</div><p>Your generated code will appear here.</p></div>}</div>
            {qr && <a className="button button-primary qrg-download" href={qr} download={downloadName} onClick={() => trackToolEvent({ tool: "qr-generator", event_type: "png_downloaded", visitor_id: getToolVisitorId(), session_id: getToolVisitorId(), ...getAttribution(), metadata: { format: "png", branded: Boolean(logo) } }).catch(() => {})}>Download PNG</a>}
            <div className="qrg-result-tip"><strong>Ready to use</strong><span>Print it on menus, invoices, packaging, posters or business cards.</span></div>
          </aside>
        </section>
      </div>
    </main>
  );
}
