import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getTools } from "../services/api";

const fallbackTools = [
  { slug: "social-media-audit", name: "Social Media Audit", description: "Get a practical assessment of your social presence and the biggest opportunities to improve it." },
  { slug: "caption-generator", name: "AI Caption Generator", description: "Create platform-ready captions from your topic, audience and preferred tone." },
  { slug: "content-ideas", name: "Social Media Content Ideas", description: "Generate practical content ideas tailored to your business and audience." },
];

export default function ToolsPage() {
  const [tools, setTools] = useState(fallbackTools);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTools().then(setTools).catch(() => {}).finally(() => setLoading(false));
  }, []);

  return (
    <div className="page-shell page-content">
      <section className="page-hero">
        <p className="eyebrow">FREE TOOLS</p>
        <h1>Useful tools.<br /><span>No paywall.</span></h1>
        <p className="hero-copy">Practical tools from Flayer Wings to help you improve your social presence and create better content.</p>
      </section>
      <section className="tool-list" aria-busy={loading}>
        {tools.map((tool) => (
          <article className="tool-card tool-card-large" key={tool.slug}>
            <span className="tool-index">TOOL</span>
            <h2>{tool.name}</h2>
            <p>{tool.description}</p>
            <Link className="button button-primary" to={`/tools/${tool.slug}`}>Use it free <span>→</span></Link>
          </article>
        ))}
      </section>
    </div>
  );
}
