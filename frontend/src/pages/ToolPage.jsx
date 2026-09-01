import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  generateCaption,
  generateContentIdeas,
  generateSocialAudit,
} from "../services/api";
import ToolLeadCapture from "../components/ToolLeadCapture";
import "../styles/tools-results.css";

const TOOL_CONFIG = {
  "social-media-audit": {
    title: "Social Media Audit",
    eyebrow: "FREE GROWTH AUDIT",
    icon: "⏱",
    badgeType: "cyan",
    description: "Build a practical growth baseline from your business and profile. Get priorities, quick wins and a 7-day action plan — without fake metrics.",
    fields: [
      { name: "business", label: "Business / Brand Name", type: "text", placeholder: "e.g. Flayer Wings Studio", required: true },
      { name: "profile_url", label: "Social Profile URL", type: "url", placeholder: "https://instagram.com/yourhandle", required: true },
    ],
    action: generateSocialAudit,
  },
  "caption-generator": {
    title: "AI Caption Generator",
    eyebrow: "FREE CONTENT TOOL",
    icon: "Aa",
    badgeType: "purple",
    description: "Create a platform-aware caption package with a hook, body, CTA, hashtags and a content angle you can actually publish.",
    fields: [
      { name: "business", label: "Business / Brand", type: "text", placeholder: "e.g. Flayer Wings", required: false },
      { name: "topic", label: "What are you posting about?", type: "text", placeholder: "e.g. Launching our AI-powered analytics feature", required: true },
      { name: "audience", label: "Target Audience", type: "text", placeholder: "e.g. Startup founders", required: false },
      { name: "content_type", label: "Content Type", type: "text", placeholder: "Educational, promotional, story, case study...", required: false },
      { name: "goal", label: "Primary Goal", type: "text", placeholder: "Reach, engagement, leads, sales...", required: false },
      { name: "tone", label: "Desired Tone", type: "text", placeholder: "Professional, bold, friendly...", required: false },
      { name: "platform", label: "Target Platform", type: "text", placeholder: "Instagram, LinkedIn, X...", required: false },
      { name: "cta", label: "Custom CTA (optional)", type: "text", placeholder: "e.g. Book a free strategy call", required: false },
    ],
    action: generateCaption,
  },
  "content-ideas": {
    title: "Content Strategy Generator",
    eyebrow: "FREE CONTENT PLANNER",
    icon: "💡",
    badgeType: "blue",
    description: "Get 10 structured content opportunities with format, pillar, goal, hook and outline — not a list of generic prompts.",
    fields: [
      { name: "business", label: "What does your business do?", type: "text", placeholder: "e.g. B2B SaaS for remote teams", required: true },
      { name: "audience", label: "Who is your target audience?", type: "text", placeholder: "e.g. Startup founders, CTOs", required: true },
      { name: "industry", label: "Industry / Niche", type: "text", placeholder: "e.g. SaaS, fitness, real estate", required: false },
      { name: "offer", label: "Product / Offer", type: "text", placeholder: "e.g. Social media management", required: false },
      { name: "goal", label: "Primary Goal", type: "text", placeholder: "Brand awareness, leads, trust...", required: false },
      { name: "platform", label: "Primary Platform", type: "text", placeholder: "Instagram, LinkedIn, X...", required: false },
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
              <Link className="button button-primary" to="/tools">Back to Free Tools <span className="btn-arrow">→</span></Link>
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
      window.setTimeout(() => document.getElementById("tool-results")?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
    } catch {
      setState("error");
    }
  }

  const updateField = (name, value) => setForm((current) => ({ ...current, [name]: value }));

  return (
    <div className="app-shell">
      <main className="inner-page tool-workspace-page">
        <div className="section-container">
          <div className="tool-nav-bar">
            <Link className="tool-back-link" to="/tools"><span aria-hidden="true">←</span> Back to All Free Tools</Link>
          </div>

          <div className="tool-workspace-layout">
            <div className="tool-info-pane">
              <span className={`status-pill pill-${tool.badgeType}`}>{tool.eyebrow}</span>
              <h1 className="tool-page-title">{tool.title}</h1>
              <p className="tool-page-desc">{tool.description}</p>
              <div className="tool-guarantee-box">
                <div className="guarantee-icon">⚡</div>
                <div>
                  <strong>Useful output, instantly</strong>
                  <p>No account or credit card. Your result is designed to give you something practical to use today.</p>
                </div>
              </div>
            </div>

            <div className="tool-form-pane">
              <form className="tool-interactive-form" onSubmit={submit}>
                <div className="tool-form-header">
                  <h3>Build Your Result</h3>
                  <span className="form-helper">More context = more useful output</span>
                </div>
                <div className="tool-fields-list">
                  {tool.fields.map((field) => (
                    <div className="form-group" key={field.name}>
                      <label htmlFor={`tool-${field.name}`}>{field.label} {field.required && <span className="req-star">*</span>}</label>
                      <input
                        id={`tool-${field.name}`}
                        required={field.required}
                        type={field.type}
                        placeholder={field.placeholder}
                        value={form[field.name] || ""}
                        onChange={(event) => updateField(field.name, event.target.value)}
                      />
                    </div>
                  ))}
                </div>
                <button className="button button-primary submit-btn tool-generate-btn" disabled={state === "loading"} type="submit">
                  {state === "loading" ? <span className="btn-spinner-text"><span className="inline-spinner" /> Building Your Result...</span> : <><span>Generate My Result</span><span className="btn-arrow">→</span></>}
                </button>
                {state === "error" && <div className="form-error-banner" role="alert">We couldn't generate this result right now. Please check your inputs and try again.</div>}
              </form>
            </div>
          </div>

          {result && (
            <div className="tool-results-wrapper" id="tool-results">
              <ResultView result={result} slug={slug} />
              <ToolLeadCapture
                slug={slug}
                toolName={tool.title}
                resultSummary={buildLeadSummary(result, slug)}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

function buildLeadSummary(result, slug) {
  if (slug === "social-media-audit") {
    const source = result.audit_type === "meta_live_profile_audit" ? "Live Meta profile audit" : "Strategy baseline";
    return `${source}: ${result.score}/10 on ${result.platform}. Priority: ${result.next_step}`;
  }
  if (slug === "caption-generator") return `Generated a ${result.platform} caption focused on ${result.goal || "the requested goal"}.`;
  return `Generated ${result.ideas?.length || 0} structured content opportunities for ${result.platform}.`;
}

function ResultView({ result, slug }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async (text) => {
    try { await navigator.clipboard.writeText(text); setCopied(true); window.setTimeout(() => setCopied(false), 2500); } catch { setCopied(false); }
  };

  if (slug === "content-ideas") {
    const copyText = (result.ideas || []).map((idea, index) => `${index + 1}. ${idea.title}\nFormat: ${idea.format}\nPillar: ${idea.pillar}\nGoal: ${idea.goal}\nHook: ${idea.hook}\nOutline: ${idea.outline}`).join("\n\n");
    return (
      <section className="tool-result-card" aria-label="Generated Content Strategy">
        <div className="result-header-bar">
          <div><span className="eyebrow-cyan">GENERATED STRATEGY</span><h2 className="result-main-title">10 Content Opportunities</h2><p className="result-support-copy">Built around {result.content_pillars?.join(", ") || "useful content pillars"}.</p></div>
          <button className="button button-ghost copy-all-btn" onClick={() => handleCopy(copyText)} type="button">{copied ? "✓ Copied" : "Copy Strategy"}</button>
        </div>
        <div className="ideas-structured-grid">
          {(result.ideas || []).map((idea, index) => (
            <article key={index} className="idea-card-item idea-card-rich">
              <div className="idea-card-top"><span className="idea-card-index">{String(index + 1).padStart(2, "0")}</span><span className="idea-meta-pill">{idea.format}</span></div>
              <h3>{idea.title}</h3>
              <div className="idea-meta-row"><span>{idea.pillar}</span><span>{idea.goal}</span></div>
              <p><strong>Hook</strong>{idea.hook}</p>
              <p><strong>Outline</strong>{idea.outline}</p>
            </article>
          ))}
        </div>
      </section>
    );
  }

  if (slug === "caption-generator") {
    const captionBody = (result.caption || "").replace(result.hook || "", "").trim();
    const fullText = `${result.hook}\n\n${captionBody}\n\n${result.cta}\n\n${(result.hashtags || []).join(" ")}`;
    return (
      <section className="tool-result-card" aria-label="Generated Caption">
        <div className="result-header-bar">
          <div><span className="eyebrow-cyan">READY TO PUBLISH</span><h2 className="result-main-title">Caption Package</h2></div>
          <button className="button button-ghost copy-caption-btn" onClick={() => handleCopy(fullText)} type="button">{copied ? "✓ Copied" : "Copy Caption"}</button>
        </div>
        <div className="caption-preview-box">
          <div className="result-highlight-block"><span>HOOK</span><p>{result.hook}</p></div>
          <div className="caption-text-block">{captionBody}</div>
          <div className="caption-detail-grid">
            <div><span>FORMAT</span><strong>{result.format}</strong></div>
            <div><span>CTA</span><strong>{result.cta}</strong></div>
            <div><span>STRATEGY</span><strong>{result.strategy_note}</strong></div>
          </div>
          <div className="caption-hashtags-row">{(result.hashtags || []).map((tag) => <span key={tag} className="hashtag-chip">{tag}</span>)}</div>
        </div>
      </section>
    );
  }

  const live = result.audit_type === "meta_live_profile_audit";
  const performance = result.performance;
  return (
    <section className="tool-result-card" aria-label="Social Media Audit Results">
      <div className="result-header-bar">
        <div>
          <span className="eyebrow-cyan">{live ? "LIVE META AUDIT" : "STRATEGY BASELINE"}</span>
          <h2 className="result-main-title">{result.score}/10 {live ? "Profile Growth Score" : "Growth Baseline"}</h2>
          <p className="result-support-copy">{result.platform} · {result.business}{live && result.profile?.username ? ` · @${result.profile.username}` : ""}</p>
          {live && <p className="result-support-copy">Evidence source: {result.data_source}</p>}
        </div>
      </div>
      <div className="audit-overview-panel">
        <div className="audit-score-circle"><div className="score-ring"><span className="score-number">{result.score}</span><span className="score-total">/10</span></div><span className="score-label">{live ? "Live Score" : "Starting Score"}</span></div>
        <div className="audit-next-step-box"><span className="next-step-badge">FIX THIS FIRST</span><p className="next-step-content">{result.next_step}</p></div>
      </div>

      {live && performance && (
        <div className="audit-plan-grid">
          <div>
            <span className="eyebrow-cyan">LIVE PROFILE DATA</span>
            <ul>
              <li>{performance.followers?.toLocaleString() || 0} followers returned by Meta</li>
              <li>{performance.sample_size} recent posts sampled</li>
              <li>{performance.average_interactions} average likes + comments per sampled post</li>
              <li>{performance.average_engagement_rate_percent == null ? "Engagement rate unavailable" : `${performance.average_engagement_rate_percent}% average sampled engagement rate`}</li>
            </ul>
          </div>
          <div>
            <span className="eyebrow-cyan">PUBLISHING SIGNAL</span>
            <ul>
              <li>{result.publishing?.posts_in_last_14_days || 0} sampled posts in the last 14 days</li>
              <li>{result.publishing?.latest_post_days_ago == null ? "Latest post date unavailable" : `Latest sampled post was ${result.publishing.latest_post_days_ago} days ago`}</li>
              <li>Top-performing sampled posts are ranked by observed likes + comments.</li>
            </ul>
          </div>
        </div>
      )}

      <div className="audit-checks-grid">
        {(result.checks || []).map((item) => (
          <article key={item.key || item.title} className="audit-check-card">
            <div className="check-card-header"><strong>{item.title}</strong><span className="check-card-score">{item.score}/10</span></div>
            <span className="audit-priority">{item.priority}</span>
            <p className="check-card-tip">{item.what_good_looks_like || (item.evidence || []).join(" ")}</p>
            {item.evidence && <p className="check-card-tip"><strong>Evidence:</strong> {item.evidence.join(" ")}</p>}
            <p className="check-card-action"><strong>Action:</strong> {item.action}</p>
          </article>
        ))}
      </div>

      {live && performance?.top_posts?.length > 0 && (
        <div className="audit-plan-grid">
          <div>
            <span className="eyebrow-cyan">TOP SAMPLED POSTS</span>
            <ul>
              {performance.top_posts.map((post) => (
                <li key={post.id}>{post.interactions} interactions · {post.media_type || "Post"}{post.permalink ? ` · ${post.permalink}` : ""}</li>
              ))}
            </ul>
          </div>
          <div>
            <span className="eyebrow-cyan">WHAT TO REPEAT</span>
            <ul>
              <li>Study the topic, format and opening of the strongest sampled post.</li>
              <li>Turn the strongest recurring audience problem into a repeatable series.</li>
              <li>Use the same primary CTA across high-intent content.</li>
            </ul>
          </div>
        </div>
      )}

      <div className="audit-plan-grid">
        <div><span className="eyebrow-cyan">QUICK WINS</span><ul>{(result.quick_wins || []).map((item) => <li key={item}>{item}</li>)}</ul></div>
        <div><span className="eyebrow-cyan">7-DAY PLAN</span><ul>{(result.seven_day_plan || []).map((item) => <li key={item}>{item}</li>)}</ul></div>
      </div>
      <div className="audit-disclaimer"><small>ℹ {result.confidence_note}</small></div>
    </section>
  );
}
