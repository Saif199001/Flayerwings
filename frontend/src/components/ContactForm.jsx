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
    <form className="contact-form" onSubmit={submit} noValidate>
      <div className="form-grid">
        <label>Name<input name="name" value={form.name} onChange={updateField} required autoComplete="name" /></label>
        <label>Email<input name="email" type="email" value={form.email} onChange={updateField} required autoComplete="email" /></label>
        <label>Company<input name="company" value={form.company} onChange={updateField} autoComplete="organization" /></label>
        <label>Phone<input name="phone" value={form.phone} onChange={updateField} autoComplete="tel" /></label>
      </div>
      <label>What can we build for you?<textarea name="message" value={form.message} onChange={updateField} rows="5" required /></label>
      <button className="button button-primary" type="submit" disabled={state === "submitting"}>
        {state === "submitting" ? "Sending…" : "Send Inquiry →"}
      </button>
      {state === "success" && <p className="form-success" role="status">Thanks! Your inquiry has been received.</p>}
      {state === "error" && <p className="form-error" role="alert">{error}</p>}
    </form>
  );
}
