import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { generateCaption, generateContentIdeas, generateSocialAudit } from "../services/api";

const TOOL_CONFIG = {
  "social-media-audit": {
    title: "Social Media Audit", eyebrow: "FREE AUDIT",
    description: "Get a practical starting point for improving your social media presence.",
    fields: [["business", "Business / Brand name", "text"], ["profile_url", "Social profile URL", "url"]],
    action: generateSocialAudit,
  },
  "caption-generator": {
    title: "AI Caption Generator", eyebrow: "FREE AI TOOL",
    description: "Turn a topic into a ready-to-edit social caption in seconds.",
    fields: [["topic", "What is your post about?", "text"], ["tone", "Tone (e.g. professional, friendly)", "text"], ["platform", "Platform (e.g. Instagram)", "text"]],
    action: generateCaption,
  },
  "content-ideas": {
    title: "Content Ideas Generator", eyebrow: "FREE IDEAS",
    description: "Get 10 practical content starting points tailored to your business and audience.",
    fields: [["business", "What does your business do?", "text"], ["audience", "Who is your target audience?", "text"], ["platform", "Platform (e.g. Instagram)", "text"]],
    action: generateContentIdeas,
  },
};

export default function ToolPage() {
  const { slug } = useParams();
  const tool = TOOL_CONFIG[slug];
  const [form, setForm] = useState({});
  const [result, setResult] = useState(null);
  const [state, setState] = useState("idle");

  if (!tool) return <main className="section"><h1>Tool not found</h1><Link to="/tools">Back to Free Tools</Link></main>;

  async function submit(event) {
    event.preventDefault(); setState("loading"); setResult(null);
    try { setResult(await tool.action(form)); setState("success"); }
    catch { setState("error"); }
  }

  return (
    <main className="section tool-workspace">
      <Link className="back-link" to="/tools">← All Free Tools</Link>
      <div className="tool-workspace-grid">
        <div>
          <p className="eyebrow">{tool.eyebrow}</p>
          <h1>{tool.title}</h1>
          <p className="section-copy">{tool.description}</p>
          <div className="tool-promise"><strong>Built to be useful.</strong><span>No account is required to try the basic tool.</span></div>
        </div>
        <form className="tool-form" onSubmit={submit}>
          {tool.fields.map(([name, label, type]) => (
            <label key={name}>{label}<input required type={type} value={form[name] || ""} onChange={(e) => setForm({ ...form, [name]: e.target.value })} /></label>
          ))}
          <button className="button button-primary" disabled={state === "loading"}>{state === "loading" ? "Generating…" : "Generate My Result →"}</button>
          {state === "error" && <p className="form-error" role="alert">Something went wrong. Please check your inputs and try again.</p>}
        </form>
      </div>
      {result && <ResultView result={result} slug={slug} />}
    </main>
  );
}

function ResultView({ result, slug }) {
  if (slug === "content-ideas") return <section className="tool-result result-full"><span className="result-label">YOUR IDEAS</span><h2>10 content starting points.</h2><ol className="result-list">{result.ideas.map((idea, i) => <li key={i}>{idea}</li>)}</ol></section>;
  if (slug === "caption-generator") return <section className="tool-result result-full"><span className="result-label">YOUR CAPTION</span><h2>Ready to edit and post.</h2><p className="result-text">{result.caption}</p><p className="hashtags">{result.hashtags.join(" ")}</p></section>;
  return <section className="tool-result result-full"><span className="result-label">QUICK AUDIT</span><h2>{result.score}/10 starting score.</h2><div className="audit-grid">{result.checks.map((item) => <article key={item.key}><strong>{item.title}</strong><span>{item.score}/10</span><p>{item.tip}</p></article>)}</div><p className="next-step"><strong>Next step:</strong> {result.next_step}</p><small>This is a quick framework, not an automated scrape or platform-inspection report.</small></section>;
}
