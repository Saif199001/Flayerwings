import { Link } from "react-router-dom";

const capabilities = [
  ["01", "Social Publishing", "Plan, organize and manage social content from one focused workspace."],
  ["02", "Analytics", "Turn social performance data into clear, actionable insights."],
  ["03", "Workflow", "Keep content, approvals and day-to-day social work organized."],
  ["04", "Multi-platform", "Bring supported social channels into a more consistent management workflow."],
];

export default function ProductPage() {
  return (
    <main className="section product-page">
      <Link className="back-link" to="/">← Flayer Wings</Link>
      <section className="product-hero">
        <div>
          <p className="eyebrow">BUILDING IN PUBLIC · COMING SOON</p>
          <h1>Social media management, <span>rebuilt.</span></h1>
          <p className="section-copy">We're building a modern SaaS platform at Flayer Wings to make social media management, publishing and analytics simpler for growing businesses.</p>
          <div className="actions"><a className="button button-primary" href="#early-access">Join Early Access →</a><Link className="button button-secondary" to="/tools">Try Free Tools</Link></div>
        </div>
        <div className="saas-preview" aria-label="SaaS product preview">
          <div className="preview-top"><span>FLAYER WINGS</span><i>COMING SOON</i></div>
          <div className="preview-body"><div className="preview-sidebar"><b /> <b /> <b /> <b /></div><div className="preview-main"><span className="preview-kicker">OVERVIEW</span><strong>Social performance</strong><div className="preview-chart"><i /><i /><i /><i /><i /><i /></div><div className="preview-metrics"><span>Content <b>24</b></span><span>Reach <b>18.4K</b></span><span>Engagement <b>7.8%</b></span></div></div></div>
        </div>
      </section>

      <section className="product-story">
        <p className="eyebrow">WHY WE'RE BUILDING IT</p>
        <h2>Less scattered work.<br /><span>More useful insight.</span></h2>
        <p className="section-copy">Social media management often means jumping between platforms, spreadsheets, schedulers and analytics dashboards. Our goal is to bring the important workflow into one focused product.</p>
      </section>

      <section className="capability-section">
        <p className="eyebrow">PRODUCT DIRECTION</p>
        <div className="capability-grid">{capabilities.map(([number, title, copy]) => <article key={title}><span>{number}</span><h3>{title}</h3><p>{copy}</p></article>)}</div>
      </section>

      <section className="early-access" id="early-access">
        <div><p className="eyebrow">EARLY ACCESS</p><h2>Want to see where<br /><span>this is going?</span></h2><p>Join the early-access list and be among the first to hear when the product is ready for real users.</p></div>
        <Link className="button button-primary" to="/#contact">Request Early Access →</Link>
      </section>
    </main>
  );
}
