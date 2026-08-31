import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  generateCaption,
  generateContentIdeas,
  generateSocialAudit,
} from "../services/api";
import ToolLeadCapture from "../components/ToolLeadCapture";

const TOOL_CONFIG = {
  "social-media-audit": {
    title: "Social Media Audit",
    eyebrow: "FREE AUDIT TOOL",
    icon: "⏱",
    badgeType: "cyan",
    description: "Get a practical assessment of your social media presence and find the highest-impact opportunities for immediate growth.",
    fields: [
      {
        name: "business",
        label: "Business / Brand Name",
        type: "text",
        placeholder: "e.g. Flayer Wings Studio",
        required: true,
      },
      {
        name: "profile_url",
        label: "Social Profile URL",
        type: "url",
        placeholder: "https://instagram.com/yourhandle or linkedin.com/company/...",
        required: true,
      },
    ],
    action: generateSocialAudit,
  },
  "caption-generator": {
    title: "AI Caption Generator",
    eyebrow: "FREE AI CONTENT TOOL",
    icon: "Aa",
    badgeType: "purple",
    description: "Turn any topic, announcement or product update into a ready-to-edit social media caption in seconds.",
    fields: [
      {
        name: "topic",
        label: "What is your post about?",
        type: "text",
        placeholder: "e.g. Launching our new AI-powered analytics feature",
        required: true,
      },
      {
        name: "tone",
        label: "Desired Tone",
        type: "text",
        placeholder: "e.g. Professional, energetic, witty, insightful",
        required: false,
      },
      {
        name: "platform",
        label: "Target Platform",
        type: "text",
        placeholder: "e.g. LinkedIn, Instagram, X (Twitter)",
        required: false,
      },
    ],
    action: generateCaption,
  },
  "content-ideas": {
    title: "Content Ideas Generator",
    eyebrow: "FREE STRATEGY TOOL",
    icon: "💡",
    badgeType: "blue",
    description: "Get 10 practical, audience-tested content starting points tailored to your business, niche and primary social channel.",
    fields: [
      {
        name: "business",
        label: "What does your business do?",
        type: "text",
        placeholder: "e.g. B2B SaaS for remote software teams",
        required: true,
      },
      {
        name: "audience",
        label: "Who is your target audience?",
        type: "text",
        placeholder: "e.g. Startup founders, CTOs, engineering leads",
        required: true,
      },
      {
        name: "platform",
        label: "Primary Platform",
        type: "text",
        placeholder: "e.g. LinkedIn, Twitter, Instagram",
        required: false,
      },
    ],
    action: generateContentIdeas,
  },
};

export default function ToolPage() {
  const { slug } = useParams();
  const tool = TOOL_CONFIG[slug];
  const [form, setForm] = useState({});
  const [result, setResult] = useState(null);
  const [state, setState] = useState("idle");

  if (!tool) {
    return (
      <div className="app-shell">
        <main className="inner-page not-found-page">
          <div className="section-container">
            <div className="tool-not-found-card">
              <span className="eyebrow-cyan">404</span>
              <h1>Tool Not Found</h1>
              <p>The requested free tool does not exist or has been moved.</p>
              <Link className="button button-primary" to="/tools">
                Back to Free Tools <span className="btn-arrow" aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </main>
      </div>
    );
  }

  async function submit(event) {
    event.preventDefault();
    setState("loading");
    setResult(null);
    try {
      const data = await tool.action(form);
      setResult(data);
      setState("success");
    } catch {
      setState("error");
    }
  }

  return (
    <div className="app-shell">
      <main className="inner-page tool-workspace-page">
        <div className="section-container">
          {/* NAVIGATION BREADCRUMB */}
          <div className="tool-nav-bar">
            <Link className="tool-back-link" to="/tools">
              <span aria-hidden="true">←</span> Back to All Free Tools
            </Link>
          </div>

          {/* MAIN TOOL WORKSPACE */}
          <div className="tool-workspace-layout">
            {/* LEFT: INFO & PROMISE */}
            <div className="tool-info-pane">
              <span className={`status-pill pill-${tool.badgeType}`}>{tool.eyebrow}</span>
              <h1 className="tool-page-title">{tool.title}</h1>
              <p className="tool-page-desc">{tool.description}</p>

              <div className="tool-guarantee-box">
                <div className="guarantee-icon">⚡</div>
                <div>
                  <strong>Instant & Free</strong>
                  <p>No credit card or account needed to generate your starting report.</p>
                </div>
              </div>
            </div>

            {/* RIGHT: INPUT FORM */}
            <div className="tool-form-pane">
              <form className="tool-interactive-form" onSubmit={submit}>
                <div className="tool-form-header">
                  <h3>Input Parameters</h3>
                  <span className="form-helper">Fill out the fields below</span>
                </div>

                <div className="tool-fields-list">
                  {tool.fields.map((field) => (
                    <div className="form-group" key={field.name}>
                      <label htmlFor={`tool-${field.name}`}>
                        {field.label} {field.required && <span className="req-star">*</span>}
                      </label>
                      <input
                        id={`tool-${field.name}`}
                        required={field.required}
                        type={field.type}
                        placeholder={field.placeholder}
                        value={form[field.name] || ""}
                        onChange={(e) =>
                          setForm({ ...form, [field.name]: e.target.value })
                        }
                      />
                    </div>
                  ))}
                </div>

                <button
                  className="button button-primary submit-btn tool-generate-btn"
                  disabled={state === "loading"}
                  type="submit"
                >
                  {state === "loading" ? (
                    <span className="btn-spinner-text">
                      <span className="inline-spinner" aria-hidden="true" /> Generating Output...
                    </span>
                  ) : (
                    <>
                      <span>Generate My Result</span>
                      <span className="btn-arrow" aria-hidden="true">→</span>
                    </>
                  )}
                </button>

                {state === "error" && (
                  <div className="form-error-banner" role="alert">
                    Something went wrong while generating the result. Please check your inputs and try again.
                  </div>
                )}
              </form>
            </div>
          </div>

          {/* RESULTS VIEW */}
          {result && (
            <div className="tool-results-wrapper">
              <ResultView result={result} slug={slug} />
              <ToolLeadCapture
                slug={slug}
                toolName={tool.title}
                resultSummary={
                  result.score
                    ? `Quick audit score: ${result.score}/10.`
                    : result.caption
                    ? result.caption
                    : "Content ideas were generated successfully."
                }
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

function ResultView({ result, slug }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  if (slug === "content-ideas") {
    return (
      <section className="tool-result-card" aria-label="Generated Content Ideas">
        <div className="result-header-bar">
          <div>
            <span className="eyebrow-cyan">GENERATED IDEAS</span>
            <h2 className="result-main-title">10 Content Starting Points</h2>
          </div>
          <button
            className="button button-ghost copy-all-btn"
            onClick={() => handleCopy(result.ideas.join("\n\n"))}
            type="button"
          >
            {copied ? "✓ Copied All Ideas" : "Copy All Ideas"}
          </button>
        </div>

        <div className="ideas-structured-grid">
          {result.ideas.map((idea, index) => (
            <div key={index} className="idea-card-item">
              <span className="idea-card-index">{String(index + 1).padStart(2, "0")}</span>
              <p className="idea-card-text">{idea}</p>
            </div>
          ))}
        </div>
      </section>
    );
  }

  if (slug === "caption-generator") {
    const fullText = `${result.caption}\n\n${result.hashtags ? result.hashtags.join(" ") : ""}`;

    return (
      <section className="tool-result-card" aria-label="Generated Caption">
        <div className="result-header-bar">
          <div>
            <span className="eyebrow-cyan">GENERATED CAPTION</span>
            <h2 className="result-main-title">Ready to Edit & Post</h2>
          </div>
          <button
            className="button button-ghost copy-caption-btn"
            onClick={() => handleCopy(fullText)}
            type="button"
          >
            {copied ? "✓ Copied to Clipboard" : "Copy Caption"}
          </button>
        </div>

        <div className="caption-preview-box">
          <div className="caption-text-block">{result.caption}</div>
          {result.hashtags && result.hashtags.length > 0 && (
            <div className="caption-hashtags-row">
              {result.hashtags.map((tag) => (
                <span key={tag} className="hashtag-chip">{tag}</span>
              ))}
            </div>
          )}
        </div>
      </section>
    );
  }

  // Social Media Audit
  return (
    <section className="tool-result-card" aria-label="Social Media Audit Results">
      <div className="result-header-bar">
        <div>
          <span className="eyebrow-cyan">AUDIT RESULTS</span>
          <h2 className="result-main-title">Overall Score & Growth Breakdown</h2>
        </div>
      </div>

      <div className="audit-overview-panel">
        <div className="audit-score-circle">
          <div className="score-ring">
            <span className="score-number">{result.score}</span>
            <span className="score-total">/10</span>
          </div>
          <span className="score-label">Starting Score</span>
        </div>

        <div className="audit-next-step-box">
          <span className="next-step-badge">RECOMMENDED NEXT STEP</span>
          <p className="next-step-content">{result.next_step}</p>
        </div>
      </div>

      <div className="audit-checks-grid">
        {result.checks &&
          result.checks.map((item) => (
            <article key={item.key || item.title} className="audit-check-card">
              <div className="check-card-header">
                <strong>{item.title}</strong>
                <span className="check-card-score">{item.score}/10</span>
              </div>
              <p className="check-card-tip">{item.tip}</p>
            </article>
          ))}
      </div>

      <div className="audit-disclaimer">
        <small>
          ℹ This audit is based on a practical evaluation framework to help identify strategic growth gaps, not an automated direct account scraper.
        </small>
      </div>
    </section>
  );
}
