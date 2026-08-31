import { Link } from "react-router-dom";

const services = [
  {
    number: "01",
    title: "Social Media Management",
    tag: "IMMEDIATE FOCUS",
    badgeType: "cyan",
    icon: "📱",
    copy: "Practical day-to-day social media support for businesses that need a consistent presence without building a full in-house team.",
    points: [
      "Content planning & calendars",
      "Platform-ready posts & captions",
      "Publishing & workflow support",
      "Performance review & recommendations",
    ],
  },
  {
    number: "02",
    title: "AI & Automation",
    tag: "EFFICIENCY",
    badgeType: "blue",
    icon: "🧠",
    copy: "Automate repetitive workflows and introduce practical AI where it can save time, improve consistency or unlock new capabilities.",
    points: [
      "Workflow automation",
      "AI-assisted processes",
      "Business-specific AI solutions",
      "Integration planning",
    ],
  },
  {
    number: "03",
    title: "Custom Software",
    tag: "BUILD",
    badgeType: "purple",
    icon: "</>",
    copy: "Purpose-built software for businesses with a workflow or problem that off-the-shelf tools don't solve well.",
    points: [
      "Web applications",
      "Internal business tools",
      "API-first systems",
      "Scalable foundations",
    ],
  },
  {
    number: "04",
    title: "SaaS Development",
    tag: "PRODUCT",
    badgeType: "pink",
    icon: "🚀",
    copy: "From product architecture to polished interfaces, we build SaaS foundations designed to grow with the product.",
    points: [
      "Product architecture",
      "Django + React development",
      "API design",
      "MVP-to-scale planning",
    ],
  },
];

const methodology = [
  {
    step: "01",
    title: "Understand",
    desc: "We start with the business problem, not a pre-selected technology.",
  },
  {
    step: "02",
    title: "Build",
    desc: "We keep solutions focused, useful and practical.",
  },
  {
    step: "03",
    title: "Improve",
    desc: "We use real feedback and results to decide what comes next.",
  },
];

export default function ServicesPage() {
  return (
    <div className="app-shell">
      <main className="inner-page services-page">
        {/* SERVICES HERO */}
        <section className="inner-hero-section">
          <div className="inner-hero-glow" aria-hidden="true" />
          <div className="section-container">
            <div className="inner-hero-content">
              <span className="eyebrow-cyan">WHAT WE DO</span>
              <h1 className="inner-hero-headline">
                Technology that solves<br />
                <span className="hero-gradient-text">real business problems.</span>
              </h1>
              <p className="inner-hero-desc">
                We combine software, AI and practical execution to help businesses build, automate and grow. Right now, our social media service is our fastest path to helping businesses directly.
              </p>
              <div className="actions hero-actions">
                <a className="button button-primary hero-btn-primary" href="#contact">
                  Discuss Your Business <span className="btn-arrow" aria-hidden="true">→</span>
                </a>
                <Link className="button button-secondary hero-btn-secondary" to="/tools">
                  Try Free Tools <span className="btn-arrow-diag" aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* SERVICES GRID */}
        <section className="section services-grid-section">
          <div className="section-container">
            <div className="section-header-split">
              <div className="header-left">
                <span className="eyebrow-cyan">CAPABILITIES</span>
                <h2 className="section-title">End-to-end digital solutions</h2>
              </div>
              <div className="header-right">
                <p className="header-desc">
                  Focused engineering and strategy tailored to your exact operational requirements.
                </p>
              </div>
            </div>

            <div className="services-cards-grid">
              {services.map((service) => (
                <article
                  key={service.number}
                  className={`service-card ${service.number === "01" ? "service-card-featured" : ""}`}
                >
                  <div className="service-card-header">
                    <div className="service-icon-box" aria-hidden="true">
                      {service.icon}
                    </div>
                    <div className="service-meta-tags">
                      <span className="service-number">{service.number}</span>
                      <span className={`status-pill pill-${service.badgeType}`}>
                        {service.tag}
                      </span>
                    </div>
                  </div>

                  <h3 className="service-card-title">{service.title}</h3>
                  <p className="service-card-copy">{service.copy}</p>

                  <div className="service-deliverables">
                    <span className="deliverables-label">Key Deliverables</span>
                    <ul className="deliverables-list">
                      {service.points.map((point) => (
                        <li key={point}>
                          <span className="check-bullet" aria-hidden="true">✓</span>
                          <span>{point}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="service-card-footer">
                    <a className="button button-ghost service-action-link" href="#contact">
                      Talk to us <span aria-hidden="true">→</span>
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* HOW WE WORK / METHODOLOGY */}
        <section className="section methodology-section">
          <div className="section-container">
            <div className="methodology-card">
              <div className="methodology-header">
                <span className="eyebrow-cyan">HOW WE WORK</span>
                <h2 className="section-title">A practical, disciplined process</h2>
                <p className="section-subtitle">
                  We strip away agency overhead to deliver direct value with maximum speed.
                </p>
              </div>

              <div className="methodology-grid">
                {methodology.map((item) => (
                  <div key={item.step} className="methodology-item">
                    <span className="methodology-step-number">{item.step}</span>
                    <h3 className="methodology-item-title">{item.title}</h3>
                    <p className="methodology-item-desc">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* DIRECT CONTACT STRIP */}
        <section className="section contact-showcase-section" id="contact">
          <div className="section-container">
            <div className="contact-glass-container">
              <div className="contact-info-column">
                <span className="eyebrow-cyan">READY WHEN YOU ARE</span>
                <h2 className="contact-main-heading">
                  Let's talk about<br />
                  <span className="hero-gradient-text">your next step.</span>
                </h2>
                <p className="contact-main-desc">
                  No complicated pitch. Tell us what you need help with and we'll start from there.
                </p>

                <div className="direct-cta-wrap">
                  <a className="button button-primary hero-btn-primary" href="tel:+917752987573">
                    Call +91 77529 87573 <span className="btn-arrow" aria-hidden="true">→</span>
                  </a>
                  <p className="direct-address">
                    Building No. 6, Avtar Enclave,<br />
                    Paschim Vihar, New Delhi – 110063
                  </p>
                </div>
              </div>

              <div className="contact-form-column">
                <div className="contact-direct-card">
                  <h3>Direct Inquiry</h3>
                  <p>Or send us a message directly and we'll reply within 24 business hours.</p>
                  <div className="contact-item">
                    <span className="contact-icon" aria-hidden="true">✉</span>
                    <a href="mailto:hello@flayerwings.info" className="contact-link">
                      hello@flayerwings.info
                    </a>
                  </div>
                  <div className="contact-item">
                    <span className="contact-icon" aria-hidden="true">☎</span>
                    <a href="tel:+917752987573" className="contact-link">
                      +91 77529 87573
                    </a>
                  </div>
                  <div className="contact-item">
                    <span className="contact-icon" aria-hidden="true">📍</span>
                    <address className="contact-address">
                      Building No. 6, Avtar Enclave, Paschim Vihar, New Delhi – 110063
                    </address>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
