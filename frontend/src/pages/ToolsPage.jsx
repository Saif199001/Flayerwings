import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getTools } from "../services/api";

const fallbackTools = [
  { slug: "social-media-audit", name: "Social Media Audit", description: "Get a practical assessment of your social presence and the biggest opportunities to improve it." },
  { slug: "caption-generator", name: "AI Caption Generator", description: "Create platform-ready captions from your topic, audience and preferred tone." },
  { slug: "content-ideas", name: "Social Media Content Ideas", description: "Generate practical content ideas tailored to your business and audience." },
];

const toolOrder = ["social-media-audit", "caption-generator", "content-ideas"];

const toolMeta = {
  "social-media-audit": {
    number: "01",
    category: "STRATEGY",
    outcome: "Find your biggest growth gaps",
  },
  "caption-generator": {
    number: "02",
    category: "CONTENT",
    outcome: "Turn ideas into ready-to-edit copy",
  },
  "content-ideas": {
    number: "03",
    category: "CONTENT",
    outcome: "Build your next batch of posts",
  },
};

export default function ToolsPage() {
  const [tools, setTools] = useState(fallbackTools);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTools()
      .then((data) => {
        const ordered = [...data].sort(
          (a, b) => toolOrder.indexOf(a.slug) - toolOrder.indexOf(b.slug),
        );
        setTools(ordered);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page-shell page-content tools-page">
      <section className="page-hero tools-page-hero">
        <div>
          <p className="eyebrow">FREE TOOLS</p>
          <h1>Useful tools.<br /><span>No paywall.</span></h1>
          <p className="hero-copy">Practical tools from Flayer Wings to help you understand your social presence, create better content and take the next step with confidence.</p>
        </div>
        <div className="tools-hero-note" aria-label="Free tool promise">
          <span>FREE TO USE</span>
          <strong>Start with a useful answer.</strong>
          <p>No signup wall. No fluff. Just practical output you can act on.</p>
        </div>
      </section>

      <section className="tool-list tools-grid" aria-busy={loading}>
        {tools.map((tool) => {
          const meta = toolMeta[tool.slug] || {
            number: "",
            category: "TOOL",
            outcome: "Get a practical result",
          };

          return (
            <article className="tool-card tool-card-large tool-card-premium" key={tool.slug}>
              <div className="tool-card-topline">
                <span className="tool-index">{meta.number}</span>
                <span className="tool-category">{meta.category}</span>
              </div>
              {tool.slug === "social-media-audit" && (
                <span className="tool-recommended">BEST PLACE TO START</span>
              )}
              <h2>{tool.name}</h2>
              <p>{tool.description}</p>
              <span className="card-outcome">{meta.outcome}</span>
              <Link className="button button-primary tool-card-cta" to={`/tools/${tool.slug}`}>
                Use it free <span>→</span>
              </Link>
            </article>
          );
        })}
      </section>

      <section className="tools-next-step">
        <div>
          <p className="eyebrow">NEED MORE THAN A TOOL?</p>
          <h2>Turn the insight into a better social presence.</h2>
          <p>Use the free tools as your starting point. If you want hands-on help with strategy, content or social media management, talk to Flayer Wings.</p>
        </div>
        <Link className="button button-secondary" to="/contact">Talk to us <span>→</span></Link>
      </section>
    </div>
  );
}
