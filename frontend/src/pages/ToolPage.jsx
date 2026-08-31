import { useState } from "react";
import { Link, useParams } from "react-router-dom";

const TOOL_CONFIG = {
  "social-media-audit": {
    title: "Social Media Audit",
    eyebrow: "FREE AUDIT",
    description: "Get a practical starting point for improving your social media presence.",
    fields: [
      ["business", "Business / Brand name", "text"],
      ["profile", "Social profile URL", "url"],
      ["email", "Email for your audit", "email"],
    ],
    leadType: "social_audit",
  },
  "caption-generator": {
    title: "AI Caption Generator",
    eyebrow: "FREE AI TOOL",
    description: "Prepare a caption brief and get ready to turn it into platform-ready content.",
    fields: [["topic", "What is your post about?", "text"], ["tone", "Tone (e.g. professional, friendly)", "text"]],
    leadType: "tool",
  },
  "content-ideas": {
    title: "Content Ideas Generator",
    eyebrow: "FREE IDEAS",
    description: "Tell us about your business and get a tailored starting brief for content ideas.",
    fields: [["business", "What does your business do?", "text"], ["audience", "Who is your target audience?", "text"]],
    leadType: "tool",
  },
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export default function ToolPage() {
  const { slug } = useParams();
  const tool = TOOL_CONFIG[slug];
  const [form, setForm] = useState({});
  const [state, setState] = useState("idle");

  if (!tool) return <main className="section"><h1>Tool not found</h1><Link to="/tools">Back to Free Tools</Link></main>;

  async function submit(event) {
    event.preventDefault();
    setState("loading");
    try {
      const payload = tool.leadType === "social_audit"
        ? { name: form.business, email: form.email, social_profile_url: form.profile, lead_type: tool.leadType, source: slug }
        : { name: form.business || form.topic || "Free Tool User", email: form.email || "tool-lead@placeholder.invalid", lead_type: tool.leadType, source: slug, message: Object.entries(form).map(([k, v]) => `${k}: ${v}`).join("\n") };
      const response = await fetch(`${API_BASE_URL}/leads/`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      if (!response.ok) throw new Error("Unable to submit request");
      setState("success");
    } catch {
      setState("error");
    }
  }

  return (
    <main className="section tool-workspace">
      <Link className="back-link" to="/tools">← All Free Tools</Link>
      <div className="tool-workspace-grid">
        <div>
          <p className="eyebrow">{tool.eyebrow}</p>
          <h1>{tool.title}</h1>
          <p className="section-copy">{tool.description}</p>
          <div className="tool-promise"><strong>Built to be useful.</strong><span>We keep the experience simple and focused on practical next steps.</span></div>
        </div>
        <form className="tool-form" onSubmit={submit}>
          {tool.fields.map(([name, label, type]) => <label key={name}>{label}<input required type={type} value={form[name] || ""} onChange={(e) => setForm({ ...form, [name]: e.target.value })} /></label>)}
          {tool.leadType === "tool" && <label>Email (optional)<input type="email" value={form.email || ""} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>}
          <button className="button button-primary" disabled={state === "loading"}>{state === "loading" ? "Preparing…" : "Get My Free Result →"}</button>
          {state === "success" && <p className="form-success">Thanks — your request has been received. We'll use this information to prepare the next step.</p>}
          {state === "error" && <p className="form-error">Something went wrong. Please try again.</p>}
        </form>
      </div>
    </main>
  );
}
