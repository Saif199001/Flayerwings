import { Link } from "react-router-dom";

const tools = [
  { slug: "social-media-audit", title: "Social Media Audit", text: "Get a practical snapshot of your social presence and find the biggest opportunities to improve it.", tag: "LEAD TOOL" },
  { slug: "caption-generator", title: "AI Caption Generator", text: "Turn a topic, product or idea into platform-ready social captions in seconds.", tag: "AI TOOL" },
  { slug: "content-ideas", title: "Content Ideas Generator", text: "Generate useful content directions tailored to your business, audience and platform.", tag: "IDEAS" },
];

export default function FreeTools() {
  return (
    <main className="tools-page section">
      <div className="page-intro">
        <p className="eyebrow">FREE TOOLS</p>
        <h1>Useful tools for<br /><span>better growth.</span></h1>
        <p className="section-copy">No complicated setup. Use practical tools to understand your social presence and create better content.</p>
      </div>
      <div className="card-grid three tool-page-grid">
        {tools.map((tool) => (
          <article className="tool-card tool-page-card" key={tool.slug}>
            <span className="status-pill">{tool.tag}</span>
            <h2>{tool.title}</h2>
            <p>{tool.text}</p>
            <Link className="button button-primary" to={`/tools/${tool.slug}`}>Use Free Tool <span>→</span></Link>
          </article>
        ))}
      </div>
      <section className="tool-lead-banner">
        <div><p className="eyebrow">NEED HELP?</p><h2>Want a human to look at it?</h2><p>Get a free social media audit and turn the findings into a practical growth plan.</p></div>
        <a className="button button-primary" href="/#contact">Request an Audit <span>→</span></a>
      </section>
    </main>
  );
}
