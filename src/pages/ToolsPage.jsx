import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getTools } from "../services/api";

const fallbackTools = [
  {
    slug: "social-media-audit",
    name: "Social Media Audit",
    description: "Get a practical assessment of your social presence and the biggest opportunities to improve it.",
    icon: "⏱",
  },
  {
    slug: "caption-generator",
    name: "AI Caption Generator",
    description: "Create platform-ready captions from your topic, audience and preferred tone.",
    icon: "Aa",
  },
  {
    slug: "content-ideas",
    name: "Social Media Content Ideas",
    description: "Generate practical content ideas tailored to your business and audience.",
    icon: "💡",
  },
];

const toolOrder = ["social-media-audit", "caption-generator", "content-ideas"];

const toolMeta = {
  "social-media-audit": {
    number: "01",
    category: "STRATEGY",
    outcome: "Find your biggest growth gaps",
    accent: "cyan",
    icon: "⏱",
  },
  "caption-generator": {
    number: "02",
    category: "AI CONTENT",
    outcome: "Turn ideas into ready-to-edit copy",
    accent: "purple",
    icon: "Aa",
  },
  "content-ideas": {
    number: "03",
    category: "IDEATION",
    outcome: "Build your next batch of posts",
    accent: "blue",
    icon: "💡",
  },
};

export default function ToolsPage() {
  const [tools, setTools] = useState(fallbackTools);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTools()
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          const ordered = [...data].sort(
            (a, b) => toolOrder.indexOf(a.slug) - toolOrder.indexOf(b.slug),
          );
          setTools(ordered);
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="app-shell">
      <main className="inner-page tools-page">
        {/* TOOLS HERO */}
        <section className="inner-hero-section">
          <div className="inner-hero-glow" aria-hidden="true" />
          <div className="section-container">
            <div className="inner-hero-split">
              <div className="inner-hero-content">
                <span className="eyebrow-cyan">FREE TOOLS</span>
                <h1 className="inner-hero-headline">
                  Powerful tools.<br />
                  <span className="hero-gradient-text">Free for everyone.</span>
                </h1>
                <p className="inner-hero-desc">
                  Practical tools from Flayer Wings to help you understand your social presence, create better content and take the next step with confidence.
                </p>
              </div>

              <div className="tools-hero-badge-card" aria-label="Free tool promise">
                <div className="badge-card-icon">⚡</div>
                <span className="badge-card-tag">FREE TO USE</span>
                <strong>Start with a useful answer.</strong>
                <p>No signup wall. No credit card. Just practical output you can act on immediately.</p>
              </div>
            </div>
          </div>
        </section>

        {/* TOOLS CATALOG GRID */}
        <section className="section tools-catalog-section" aria-busy={loading}>
          <div className="section-container">
            <div className="section-header-split">
              <div className="header-left">
                <span className="eyebrow-cyan">INTERACTIVE TOOLS</span>
                <h2 className="section-title">Explore tool catalog</h2>
              </div>
              <div className="header-right">
                <p className="header-desc">
                  Instant results powered by real AI prompts and algorithmic audit frameworks.
                </p>
              </div>
            </div>

            <div className="tools-catalog-grid">
              {tools.map((tool) => {
                const meta = toolMeta[tool.slug] || {
                  number: "00",
                  category: "TOOL",
                  outcome: "Get a practical result",
                  accent: "cyan",
                  icon: "🛠",
                };

                return (
                  <article
                    className={`tool-catalog-card accent-${meta.accent}`}
                    key={tool.slug}
                  >
                    <div className="tool-card-top-row">
                      <div className="tool-card-icon-box" aria-hidden="true">
                        {meta.icon || tool.icon || "⚡"}
                      </div>
                      <div className="tool-card-badges">
                        <span className="tool-card-index">{meta.number}</span>
                        <span className="status-pill">{meta.category}</span>
                      </div>
                    </div>

                    {tool.slug === "social-media-audit" && (
                      <div className="tool-featured-ribbon">
                        <span>★ BEST PLACE TO START</span>
                      </div>
                    )}

                    <h2 className="tool-card-name">{tool.name || tool.title}</h2>
                    <p className="tool-card-text">{tool.description || tool.text}</p>

                    <div className="tool-card-outcome-box">
                      <span className="outcome-icon" aria-hidden="true">→</span>
                      <span>{meta.outcome}</span>
                    </div>

                    <div className="tool-card-cta-row">
                      <Link
                        className="button button-primary tool-card-launch-btn"
                        to={`/tools/${tool.slug}`}
                      >
                        Launch Free Tool <span className="btn-arrow" aria-hidden="true">→</span>
                      </Link>
                    </div>
                  </article>
                );
              })}
            </div>
          </div>
        </section>

        {/* BOTTOM CALLOUT */}
        <section className="section tools-cta-section">
          <div className="section-container">
            <div className="tools-next-step-card">
              <div className="next-step-left">
                <span className="eyebrow-cyan">NEED MORE THAN A TOOL?</span>
                <h2 className="section-title">
                  Turn the insight into a<br />
                  <span className="hero-gradient-text">better social presence.</span>
                </h2>
                <p className="next-step-desc">
                  Use the free tools as your starting point. If you want hands-on help with strategy, content or social media management, talk to Flayer Wings.
                </p>
              </div>
              <div className="next-step-right">
                <Link className="button button-primary hero-btn-primary" to="/#contact">
                  Talk to Us <span className="btn-arrow" aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
