import { useState } from "react";
import { createLead } from "../services/api";

const initialForm = {
  name: "",
  email: "",
  company: "",
  phone: "",
  message: "",
};

export default function ContactForm() {
  const [form, setForm] = useState(initialForm);
  const [state, setState] = useState("idle");
  const [error, setError] = useState("");

  function updateField(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function submit(event) {
    event.preventDefault();
    if (!form.name.trim() || !form.email.trim() || !form.message.trim()) {
      setError("Please fill in your name, email and project requirements.");
      setState("error");
      return;
    }
    setState("submitting");
    setError("");
    try {
      await createLead({ ...form, lead_type: "contact", source: "website" });
      setForm(initialForm);
      setState("success");
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
      setState("error");
    }
  }

  return (
    <form className="contact-form-card" onSubmit={submit} noValidate>
      <div className="form-row-dual">
        <div className="form-group">
          <label htmlFor="contact-name">Your Name</label>
          <input
            id="contact-name"
            name="name"
            placeholder="Enter your name"
            value={form.name}
            onChange={updateField}
            required
            autoComplete="name"
          />
        </div>
        <div className="form-group">
          <label htmlFor="contact-email">Email Address</label>
          <input
            id="contact-email"
            name="email"
            type="email"
            placeholder="Enter your email"
            value={form.email}
            onChange={updateField}
            required
            autoComplete="email"
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="contact-message">How can we help you?</label>
        <textarea
          id="contact-message"
          name="message"
          placeholder="Tell us about your project or requirements..."
          value={form.message}
          onChange={updateField}
          rows="4"
          required
        />
      </div>

      <button className="button button-primary submit-btn" type="submit" disabled={state === "submitting"}>
        {state === "submitting" ? (
          <span>Sending...</span>
        ) : (
          <>
            <span>Send Message</span> <span className="btn-arrow" aria-hidden="true">→</span>
          </>
        )}
      </button>

      {state === "success" && (
        <div className="form-success-banner" role="status">
          ✓ Thanks! Your message has been received. We'll be in touch shortly.
        </div>
      )}
      {state === "error" && (
        <div className="form-error-banner" role="alert">
          {error}
        </div>
      )}
    </form>
  );
}
