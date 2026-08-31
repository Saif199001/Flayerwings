import { Link } from "react-router-dom";

const capabilities = [
  {
    number: "01",
    title: "Social Publishing",
    icon: "📅",
    copy: "Plan, organize and schedule social content from one focused, multi-channel workspace.",
    points: ["Cross-platform calendar", "Visual asset staging", "Drafting & instant review"],
  },
  {
    number: "02",
    title: "Unified Analytics",
    icon: "📊",
    copy: "Turn raw social performance data into clear, actionable business insights.",
    points: ["Cross-network reach", "Engagement breakdown", "Growth trajectory tracking"],
  },
  {
    number: "03",
    title: "Team Workflow",
    icon: "⚡",
    copy: "Keep content approvals, revisions and day-to-day social execution organized.",
    points: ["Role-based approvals", "Comment threads", "Publishing audit log"],
  },
  {
    number: "04",
    title: "Multi-Platform Sync",
    icon: "🔗",
    copy: "Bring all your supported social channels into one cohesive management cockpit.",
    points: ["Instagram, LinkedIn, X & FB", "Single login hub", "Custom audience tagging"],
  },
];

export default function ProductPage() {
  return (
    <div className="app-shell">
      <main className="inner-page product-page">
        {/* PRODUCT HERO */}
        <section className="inner-hero-section product-hero-section">
          <div className="inner-hero-glow" aria-hidden="true" />
          <div className="section-container">
            <div className="product-hero-grid">
              <div className="product-hero-text">
                <div className="eyebrow product-status-pill">
                  <span className="hero-eyebrow-dot" aria-hidden="true" />
                  <span>BUILDING IN PUBLIC · COMING SOON</span>
                </div>
                <h1 className="product-main-headline">
                  Social media management,<br />
                  <span className="hero-gradient-text">rebuilt for clarity.</span>
                </h1>
                <p className="product-hero-copy">
                  We're building an all-in-one SaaS platform at Flayer Wings to make social publishing, multichannel analytics and client approvals fast, unified and intuitive.
                </p>
                <div className="actions hero-actions">
                  <a className="button button-primary hero-btn-primary" href="#early-access">
                    Join Early Access <span className="btn-arrow" aria-hidden="true">→</span>
                  </a>
                  <Link className="button button-secondary hero-btn-secondary" to="/tools">
                    Try Free Tools <span className="btn-arrow-diag" aria-hidden="true">→</span>
                  </Link>
                </div>
              </div>

              {/* SAAS DASHBOARD INTERACTIVE PREVIEW */}
              <div className="product-preview-wrap">
                <div className="dashboard-mockup">
                  {/* Dashboard Header Bar */}
                  <div className="mockup-header">
                    <div className="mockup-user-info">
                      <span className="mockup-avatar">⚡</span>
                      <div>
                        <strong>Flayer Wings SaaS Workspace</strong>
                        <small>Multichannel Production Dashboard · v0.9 Beta</small>
                      </div>
                    </div>
                    <span className="status-pill pill-cyan">Live Preview</span>
                  </div>

                  <div className="mockup-body">
                    {/* Mockup Sidebar */}
                    <div className="mockup-sidebar" aria-hidden="true">
                      <span className="sidebar-tab active">◫ Dashboard</span>
                      <span className="sidebar-tab">👥 Accounts</span>
                      <span className="sidebar-tab">📊 Analytics</span>
                      <span className="sidebar-tab">📝 Content</span>
                      <span className="sidebar-tab">✉ Inbox</span>
                      <span className="sidebar-tab">📈 Reports</span>
                      <span className="sidebar-tab">⚙ Settings</span>
                    </div>

                    {/* Mockup Main View */}
                    <div className="mockup-content">
                      {/* Metric Cards Row */}
                      <div className="mockup-metrics-grid">
                        <div className="metric-box">
                          <small>Active Channels</small>
                          <div className="metric-val-row">
                            <strong>8</strong>
                            <span className="badge-up">Synced</span>
                          </div>
                        </div>
                        <div className="metric-box">
                          <small>Total Audience</small>
                          <div className="metric-val-row">
                            <strong>142.8K</strong>
                            <span className="badge-up">+24.5%</span>
                          </div>
                        </div>
                        <div className="metric-box">
                          <small>Avg Engagement</small>
                          <div className="metric-val-row">
                            <strong>6.8%</strong>
                            <span className="badge-up">+1.4%</span>
                          </div>
                        </div>
                        <div className="metric-box">
                          <small>Scheduled Posts</small>
                          <div className="metric-val-row">
                            <strong>34</strong>
                            <span className="badge-up">Queued</span>
                          </div>
                        </div>
                      </div>

                      {/* Performance Chart & Platforms Row */}
                      <div className="mockup-charts-grid">
                        <div className="chart-panel">
                          <div className="chart-header">
                            <span>Reach & Impression Velocity</span>
                            <span className="chart-filter">Last 30 Days ▾</span>
                          </div>
                          <div className="chart-svg-wrap">
                            <svg viewBox="0 0 340 100" preserveAspectRatio="none" className="chart-svg">
                              <defs>
                                <linearGradient id="productChartGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                  <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.4" />
                                  <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.0" />
                                </linearGradient>
                              </defs>
                              <path
                                d="M0,80 Q50,20 100,50 T200,30 T280,60 T340,20 L340,100 L0,100 Z"
                                fill="url(#productChartGrad)"
                              />
                              <path
                                d="M0,80 Q50,20 100,50 T200,30 T280,60 T340,20"
                                fill="none"
                                stroke="#38bdf8"
                                strokeWidth="2.5"
                              />
                            </svg>
                          </div>
                        </div>

                        <div className="platforms-panel">
                          <span className="platforms-title">Audience Distribution</span>
                          <div className="platform-row">
                            <div className="platform-label">
                              <span className="platform-dot dot-ig" />
                              <span>Instagram</span>
                            </div>
                            <div className="platform-bar-wrap">
                              <div className="platform-bar bar-ig" style={{ width: "52%" }} />
                            </div>
                            <span className="platform-percent">52%</span>
                          </div>

                          <div className="platform-row">
                            <div className="platform-label">
                              <span className="platform-dot dot-li" />
                              <span>LinkedIn</span>
                            </div>
                            <div className="platform-bar-wrap">
                              <div className="platform-bar bar-li" style={{ width: "26%" }} />
                            </div>
                            <span className="platform-percent">26%</span>
                          </div>

                          <div className="platform-row">
                            <div className="platform-label">
                              <span className="platform-dot dot-x" />
                              <span>X (Twitter)</span>
                            </div>
                            <div className="platform-bar-wrap">
                              <div className="platform-bar bar-x" style={{ width: "14%" }} />
                            </div>
                            <span className="platform-percent">14%</span>
                          </div>

                          <div className="platform-row">
                            <div className="platform-label">
                              <span className="platform-dot dot-fb" />
                              <span>Facebook</span>
                            </div>
                            <div className="platform-bar-wrap">
                              <div className="platform-bar bar-fb" style={{ width: "8%" }} />
                            </div>
                            <span className="platform-percent">8%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* WHY WE'RE BUILDING IT */}
        <section className="section product-why-section">
          <div className="section-container">
            <div className="product-story-card">
              <span className="eyebrow-cyan">WHY WE'RE BUILDING IT</span>
              <h2 className="section-title">
                Less scattered work.<br />
                <span className="hero-gradient-text">More useful insight.</span>
              </h2>
              <p className="product-story-copy">
                Social media management often means jumping between disconnected platform native tools, spreadsheets, disparate schedulers and complex analytics dashboards. Our goal is to bring the vital daily workflow into one fast, beautifully structured product.
              </p>
            </div>
          </div>
        </section>

        {/* PRODUCT CAPABILITIES GRID */}
        <section className="section product-capabilities-section">
          <div className="section-container">
            <div className="section-header-split">
              <div className="header-left">
                <span className="eyebrow-cyan">PRODUCT ARCHITECTURE</span>
                <h2 className="section-title">Core capabilities</h2>
              </div>
              <div className="header-right">
                <p className="header-desc">
                  Engineered from ground up to support solopreneurs, growing agencies and brand marketing teams.
                </p>
              </div>
            </div>

            <div className="product-caps-grid">
              {capabilities.map((item) => (
                <article key={item.title} className="product-cap-card">
                  <div className="cap-card-header">
                    <span className="cap-icon-box" aria-hidden="true">{item.icon}</span>
                    <span className="cap-number">{item.number}</span>
                  </div>
                  <h3 className="cap-title">{item.title}</h3>
                  <p className="cap-copy">{item.copy}</p>

                  <ul className="cap-points-list">
                    {item.points.map((pt) => (
                      <li key={pt}>
                        <span className="check-bullet" aria-hidden="true">✓</span>
                        <span>{pt}</span>
                      </li>
                    ))}
                  </ul>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* EARLY ACCESS CTA SECTION */}
        <section className="section early-access-section" id="early-access">
          <div className="section-container">
            <div className="early-access-card">
              <div className="early-access-content">
                <span className="eyebrow-cyan">VIP EARLY ACCESS</span>
                <h2 className="early-access-heading">
                  Want to be among the first<br />
                  <span className="hero-gradient-text">to experience Flayer Wings?</span>
                </h2>
                <p className="early-access-desc">
                  Join our early access list. Get priority onboarding, early feature previews, and direct input into the product roadmap.
                </p>
                <div className="early-access-actions">
                  <Link className="button button-primary hero-btn-primary" to="/#contact">
                    Request Early Access <span className="btn-arrow" aria-hidden="true">→</span>
                  </Link>
                  <Link className="button button-secondary hero-btn-secondary" to="/services">
                    Explore Studio Services <span className="btn-arrow-diag" aria-hidden="true">→</span>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
