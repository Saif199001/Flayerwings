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
      <div className="tool-lead-success-card" role="status">
        <div className="success-icon-badge">✓</div>
        <span className="eyebrow-cyan">REQUEST RECEIVED</span>
        <h3 className="success-heading">We'll take it from here.</h3>
        <p className="success-desc">
          Your details are saved. We'll review your request and follow up with a practical next step.
        </p>
      </div>
    );
  }

  return (
    <div className="tool-lead-capture-card">
      <div className="lead-capture-header">
        <span className="eyebrow-cyan">GO A STEP FURTHER</span>
        <h3 className="lead-capture-title">Want a detailed custom recommendation?</h3>
        <p className="lead-capture-desc">
          Leave your details and our team will turn this automated result into a personalized, actionable strategy review.
        </p>
      </div>

      <form className="lead-capture-form" onSubmit={submit}>
        <div className="lead-form-grid">
          <div className="form-group">
            <label htmlFor="lead-name">Your Name</label>
            <input
              id="lead-name"
              required
              placeholder="e.g. Rahul Sharma"
              value={form.name}
              onChange={(e) => update("name", e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="lead-email">Email Address</label>
            <input
              id="lead-email"
              required
              type="email"
              placeholder="e.g. rahul@company.com"
              value={form.email}
              onChange={(e) => update("email", e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="lead-phone">WhatsApp / Phone</label>
            <input
              id="lead-phone"
              placeholder="e.g. +91 98765 43210"
              value={form.phone}
              onChange={(e) => update("phone", e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="lead-company">Business / Brand</label>
            <input
              id="lead-company"
              placeholder="e.g. Acme Tech Solutions"
              value={form.company}
              onChange={(e) => update("company", e.target.value)}
            />
          </div>
        </div>

        <div className="lead-form-actions">
          <button
            className="button button-primary submit-btn lead-submit-btn"
            disabled={state === "loading"}
            type="submit"
          >
            {state === "loading" ? (
              <span>Submitting Request...</span>
            ) : (
              <>
                <span>Get My Detailed Recommendation</span>
                <span className="btn-arrow" aria-hidden="true">→</span>
              </>
            )}
          </button>
          <small className="lead-privacy-note">
            🛡 We respect your privacy. No spam — strictly relevant recommendations.
          </small>
        </div>

        {state === "error" && (
          <div className="form-error-banner" role="alert">
            We couldn't save your request right now. Please check your connection and try again.
          </div>
        )}
      </form>
    </div>
  );
}
