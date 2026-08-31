import { useState } from "react";
import { createLead } from "../services/api";

export default function ToolLeadCapture({ slug, toolName, resultSummary }) {
  const [form, setForm] = useState({ name: "", email: "", phone: "", company: "" });
  const [state, setState] = useState("idle");

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    setState("loading");
    try {
      await createLead({
        ...form,
        lead_type: "tool",
        source: slug,
        message: `${toolName} result follow-up request.\n${resultSummary || "User requested a detailed recommendation."}`,
      });
      setState("success");
    } catch {
      setState("error");
    }
  }

  if (state === "success") {
    return (
      <div className="tool-lead-success">
        <p className="eyebrow">REQUEST RECEIVED</p>
        <h3>We'll take it from here.</h3>
        <p>Your details are saved. We'll review your request and follow up with a practical next step.</p>
      </div>
    );
  }

  return (
    <div className="tool-lead-capture">
      <div>
        <p className="eyebrow">GO A STEP FURTHER</p>
        <h3>Want a detailed recommendation?</h3>
        <p>Leave your details and we'll turn this free result into a more useful next-step recommendation.</p>
      </div>
      <form onSubmit={submit}>
        <div className="form-grid">
          <label>Name<input required value={form.name} onChange={(e) => update("name", e.target.value)} /></label>
          <label>Email<input required type="email" value={form.email} onChange={(e) => update("email", e.target.value)} /></label>
          <label>WhatsApp / Phone<input value={form.phone} onChange={(e) => update("phone", e.target.value)} /></label>
          <label>Business<input value={form.company} onChange={(e) => update("company", e.target.value)} /></label>
        </div>
        <button className="button button-primary" disabled={state === "loading"}>
          {state === "loading" ? "Sending…" : "Get My Detailed Recommendation →"}
        </button>
        {state === "error" && <p className="form-error">We couldn't save your request. Please try again.</p>}
        <small>We'll only use these details to respond to your request.</small>
      </form>
    </div>
  );
}
