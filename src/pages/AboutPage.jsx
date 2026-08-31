import { Link } from "react-router-dom";

const principles = [
  {
    number: "01",
    title: "Useful over flashy",
    copy: "Technology should solve a real problem and make the next step clearer.",
    icon: "🎯",
  },
  {
    number: "02",
    title: "Build with purpose",
    copy: "We choose technology around the business need—not the other way around.",
    icon: "📐",
  },
  {
    number: "03",
    title: "Stay transparent",
    copy: "We show what is live, what is being built and what is still a plan.",
    icon: "🔍",
  },
  {
    number: "04",
    title: "Keep improving",
    copy: "Real feedback and real results should shape what we build next.",
    icon: "📈",
  },
];

export default function AboutPage() {
  return (
    <div className="app-shell">
      <main className="inner-page about-page">
        {/* ABOUT HERO */}
        <section className="inner-hero-section">
          <div className="inner-hero-glow" aria-hidden="true" />
          <div className="section-container">
            <div className="inner-hero-content">
              <span className="eyebrow-cyan">ABOUT FLAYER WINGS</span>
              <h1 className="inner-hero-headline">
                We build technology<br />
                <span className="hero-gradient-text">with a reason.</span>
              </h1>
              <p className="inner-hero-desc">
                Flayer Wings is a technology and digital solutions studio focused on AI, software, SaaS and practical digital execution for modern businesses.
              </p>
              <div className="actions hero-actions">
                <Link className="button button-primary hero-btn-primary" to="/services">
                  See Our Services <span className="btn-arrow" aria-hidden="true">→</span>
                </Link>
                <Link className="button button-secondary hero-btn-secondary" to="/product">
                  See What We're Building <span className="btn-arrow-diag" aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* APPROACH STORY SECTION */}
        <section className="section about-story-section">
          <div className="section-container">
            <div className="about-story-card">
              <div className="about-story-left">
                <span className="eyebrow-cyan">OUR APPROACH</span>
                <h2 className="section-title">
                  Start with the problem.<br />
                  <span className="hero-gradient-text">Then build the solution.</span>
                </h2>
              </div>
              <div className="about-story-right">
                <p className="story-paragraph">
                  We don't believe every business needs more software. We believe businesses need the right solution to the right problem.
                </p>
                <p className="story-paragraph">
                  That might be social media support today, an automation workflow tomorrow, or a complete SaaS product over time. Our role is to understand the need and build something useful around it.
                </p>
                <div className="story-stats-strip">
                  <div className="story-stat-item">
                    <strong>100%</strong>
                    <span>Practical Execution</span>
                  </div>
                  <div className="story-stat-item">
                    <strong>Founder</strong>
                    <span>Led Development</span>
                  </div>
                  <div className="story-stat-item">
                    <strong>AI-First</strong>
                    <span>Engineered Solutions</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* PRINCIPLES GRID */}
        <section className="section about-principles-section">
          <div className="section-container">
            <div className="section-header-split">
              <div className="header-left">
                <span className="eyebrow-cyan">WHAT WE BELIEVE</span>
                <h2 className="section-title">Foundational principles</h2>
              </div>
              <div className="header-right">
                <p className="header-desc">
                  Core values that shape every line of code, strategy session, and product release.
                </p>
              </div>
            </div>

            <div className="about-principles-grid">
              {principles.map((item) => (
                <article key={item.number} className="about-principle-card">
                  <div className="principle-card-top">
                    <span className="principle-number-tag">{item.number}</span>
                    <span className="principle-icon-tag" aria-hidden="true">{item.icon}</span>
                  </div>
                  <h3 className="principle-card-heading">{item.title}</h3>
                  <p className="principle-card-text">{item.copy}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* BUILDING IN PUBLIC SHOWCASE */}
        <section className="section about-building-section">
          <div className="section-container">
            <div className="building-highlight-card">
              <div className="building-highlight-info">
                <span className="eyebrow-cyan">BUILDING OUR OWN PRODUCT</span>
                <h2 className="section-title">
                  We practice what<br />
                  <span className="hero-gradient-text">we build.</span>
                </h2>
                <p className="building-highlight-desc">
                  Our upcoming social media management SaaS is being developed from the same problems we see in real workflows. We're building it in public, learning as we go and keeping the product honest about what is—and isn't—ready.
                </p>
                <Link className="button button-primary hero-btn-primary" to="/product">
                  Explore Our SaaS <span className="btn-arrow" aria-hidden="true">→</span>
                </Link>
              </div>

              <div className="building-highlight-badge">
                <div className="building-badge-inner">
                  <span className="building-badge-icon">🚀</span>
                  <strong>Built in Public</strong>
                  <p>Transparent progress, community feedback & continuous updates.</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
