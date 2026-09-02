import { Navigate, Route, Routes, Link } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ContactForm from "./components/ContactForm";
import ContactDetails from "./components/ContactDetails";
import ToolsPage from "./pages/ToolsPage";
import ToolPage from "./pages/ToolPage";
import ProductPage from "./pages/ProductPage";
import ServicesPage from "./pages/ServicesPage";
import AboutPage from "./pages/AboutPage";
import "./styles/premium.css";
import "./styles/hero-premium.css";

const principles = [
  {
    icon: "📈",
    title: "AI-first",
    copy: "Intelligent solutions that deliver real impact",
  },
  {
    icon: "⚙️",
    title: "Lean delivery",
    copy: "Ship fast with quality and continuous value",
  },
  {
    icon: "👤",
    title: "Founder-led",
    copy: "Hands-on leadership in every engagement",
  },
  {
    icon: "🚀",
    title: "Built in public",
    copy: "Transparent, accountable and community driven",
  },
];

const solutionsData = [
  {
    number: "01",
    icon: "🧠",
    title: "AI Solutions",
    copy: "Intelligent automation, AI agents and data-driven systems that simplify complex workflows.",
    accent: "cyan",
  },
  {
    number: "02",
    icon: "</>",
    title: "Custom Software",
    copy: "Robust web and mobile applications built to solve your unique business challenges.",
    accent: "blue",
  },
  {
    number: "03",
    icon: "🚀",
    title: "SaaS Development",
    copy: "Scalable SaaS products with modern architecture, analytics and subscription models.",
    accent: "violet",
  },
  {
    number: "04",
    icon: "💻",
    title: "Web & Mobile",
    copy: "High-performance websites and mobile apps that deliver exceptional user experiences.",
    accent: "magenta",
  },
];

const toolsData = [
  {
    icon: "🧾",
    title: "GST Invoice Generator",
    copy: "Create professional GST invoices with automatic tax calculations and print-ready output.",
    cta: "Create Invoice",
    link: "/tools/gst-invoice-generator",
  },
  {
    icon: "🧮",
    title: "GST Calculator",
    copy: "Add or remove GST instantly with clear CGST, SGST and IGST calculations.",
    cta: "Calculate GST",
    link: "/tools/gst-calculator",
  },
  {
    icon: "▦",
    title: "QR Code Generator",
    copy: "Create branded QR codes for links, text, payments, menus and campaigns.",
    cta: "Create QR",
    link: "/tools/qr-generator",
  },
  {
    icon: "◉",
    title: "WhatsApp Link & QR",
    copy: "Create click-to-chat WhatsApp links and QR codes with a ready-to-share message.",
    cta: "Create Link",
    link: "/tools/whatsapp-link-generator",
  },
  {
    icon: "📋",
    title: "Quotation Generator",
    copy: "Build professional quotations and estimates with GST, discounts and customer details.",
    cta: "Create Quote",
    link: "/tools/quotation-generator",
  },
  {
    icon: "🧾",
    title: "Receipt Generator",
    copy: "Create clean payment receipts with business details, payment method and printable output.",
    cta: "Create Receipt",
    link: "/tools/receipt-generator",
  },
  {
    icon: "💳",
    title: "Payment Reminder",
    copy: "Generate polite or firm payment reminders ready to copy and share with customers.",
    cta: "Create Reminder",
    link: "/tools/payment-reminder-generator",
  },
  {
    icon: "🔗",
    title: "UTM Campaign Builder",
    copy: "Build clean campaign URLs for tracking traffic from social, ads, email and more.",
    cta: "Build UTM",
    link: "/tools/utm-builder",
  },
];

function Home() {
  return (
    <div id="top" className="app-shell">
      <Navbar />
      <main>
        {/* 1. HERO SECTION */}
        <section className="hero-section" id="hero">
          <div className="hero-glow" aria-hidden="true" />
          <div className="hero-ambient-mesh" aria-hidden="true" />

          <div className="hero-content">
            <div className="eyebrow hero-eyebrow">
              <span className="hero-eyebrow-dot" aria-hidden="true" />
              <span>AI • SOFTWARE • SAAS</span>
            </div>

            <h1 className="hero-headline">
              Build.<br />
              <span className="hero-gradient-text">Automate.</span><br />
              Grow.
            </h1>

            <p className="hero-copy">
              We build AI-powered software, SaaS products and digital solutions that help modern businesses work smarter and grow faster.
            </p>

            <div className="actions hero-actions">
              <a className="button button-primary hero-btn-primary" href="#contact">
                Start a Project <span className="btn-arrow" aria-hidden="true">→</span>
              </a>
              <Link className="button button-secondary hero-btn-secondary" to="/tools">
                Explore Free Tools <span className="btn-arrow-diag" aria-hidden="true">→</span>
              </Link>
            </div>

            <div className="hero-trust-badges" aria-label="Key delivery promises">
              <span><i className="badge-bullet">⬡</i> AI-first approach</span>
              <span><i className="badge-bullet">🛡</i> Secure & Reliable</span>
              <span><i className="badge-bullet">⚡</i> Fast Delivery</span>
              <span><i className="badge-bullet">⬡</i> Scalable Solutions</span>
            </div>
          </div>

          <div className="hero-orbit" aria-hidden="true">
            <div className="orbit-ambient" />
            <div className="orbit-grid-matrix" />
            <div className="orbit-ring ring-one" />
            <div className="orbit-ring ring-two" />
            <div className="orbit-ring ring-three" />
            <div className="orbit-ring ring-four" />
            <div className="orbit-circuit circuit-one" />
            <div className="orbit-circuit circuit-two" />
            <div className="orbit-node node-one" />
            <div className="orbit-node node-two" />
            <div className="orbit-node node-three" />
            <div className="orbit-node node-four" />

            <div className="orbit-card orbit-card-ai">
              <span className="orbit-card-icon">🧠</span>
              <div className="orbit-card-text">
                <strong>AI</strong>
                <small>Intelligence</small>
              </div>
            </div>

            <div className="orbit-card orbit-card-code">
              <span className="orbit-card-icon">&lt;/&gt;</span>
              <div className="orbit-card-text">
                <strong>Code</strong>
                <small>Engineering</small>
              </div>
            </div>

            <div className="orbit-card orbit-card-data">
              <span className="orbit-card-icon">📊</span>
              <div className="orbit-card-text">
                <strong>Analytics</strong>
                <small>Data Insights</small>
              </div>
            </div>

            <div className="orbit-card orbit-card-cloud">
              <span className="orbit-card-icon">☁</span>
              <div className="orbit-card-text">
                <strong>Cloud</strong>
                <small>Scalable</small>
              </div>
            </div>

            <div className="orbit-logo">
              <span className="orbit-logo-glow" />
              <img src="/flayer_wings_logo.jpeg" alt="Flayer Wings" width="160" height="160" />
            </div>
          </div>
        </section>

        {/* 2. TRUST / PRINCIPLES STRIP */}
        <section className="principles-section" aria-label="Studio Principles">
          <div className="principles-container">
            <div className="principles-glass-card">
              {principles.map((item) => (
                <div key={item.title} className="principle-item">
                  <span className="principle-icon" aria-hidden="true">{item.icon}</span>
                  <div className="principle-info">
                    <strong>{item.title}</strong>
                    <p>{item.copy}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 3. WHAT WE BUILD (CORE CAPABILITIES) */}
        <section className="section solutions-section" id="solutions">
          <div className="section-container">
            <div className="section-header-split">
              <div className="header-left">
                <span className="eyebrow-cyan">WHAT WE BUILD</span>
                <h2 className="section-title">Solutions that power<br />your growth</h2>
              </div>
              <div className="header-right">
                <p className="header-desc">
                  From AI automation to custom platforms, we build products and systems that scale with your business.
                </p>
                <Link to="/services" className="button button-ghost header-cta">
                  View All Services <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>

            <div className="solutions-grid">
              {solutionsData.map((item) => (
                <div key={item.title} className={`solution-card accent-${item.accent}`}>
                  <div className="card-topline">
                    <span className="card-icon-box">{item.icon}</span>
                    <span className="card-index">{item.number}</span>
                  </div>
                  <h3 className="card-title">{item.title}</h3>
                  <p className="card-copy">{item.copy}</p>
                  <Link to="/services" className="card-explore-link">
                    Explore <span aria-hidden="true">→</span>
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 4. FLAYER WINGS SAAS PRODUCT SPOTLIGHT */}
        <section className="section product-spotlight-section" id="products">
          <div className="section-container">
            <div className="product-spotlight-card">
              <div className="product-info-col">
                <span className="eyebrow-cyan">OUR PRODUCT</span>
                <h2 className="product-title">Flayer Wings SaaS<br />Coming Soon</h2>
                <p className="product-desc">
                  Our own all-in-one platform to help businesses manage social media, content, analytics and automation from one powerful dashboard.
                </p>
                <Link to="/product" className="button button-ghost product-cta">
                  Join Early Access <span aria-hidden="true">→</span>
                </Link>
              </div>

              <div className="product-preview-col">
                <div className="dashboard-mockup">
                  <div className="mockup-header">
                    <div className="mockup-user-info">
                      <span className="mockup-avatar">👋</span>
                      <div>
                        <strong>Welcome back, Saif</strong>
                        <small>Here's what's happening with your workspace today.</small>
                      </div>
                    </div>
                  </div>

                  <div className="mockup-body">
                    <div className="mockup-sidebar" aria-hidden="true">
                      <span className="sidebar-tab active">◫ Dashboard</span>
                      <span className="sidebar-tab">👥 Accounts</span>
                      <span className="sidebar-tab">📊 Analytics</span>
                      <span className="sidebar-tab">📝 Content</span>
                      <span className="sidebar-tab">✉ Inbox</span>
                      <span className="sidebar-tab">📈 Reports</span>
                      <span className="sidebar-tab">⚙ Settings</span>
                    </div>

                    <div className="mockup-content">
                      <div className="mockup-metrics-grid">
                        <div className="metric-box"><small>Accounts</small><div className="metric-val-row"><strong>24</strong><span className="badge-up">+12%</span></div></div>
                        <div className="metric-box"><small>Total Reach</small><div className="metric-val-row"><strong>128.4K</strong><span className="badge-up">+18.2%</span></div></div>
                        <div className="metric-box"><small>Engagement</small><div className="metric-val-row"><strong>8.7K</strong><span className="badge-up">+22.1%</span></div></div>
                        <div className="metric-box"><small>Impressions</small><div className="metric-val-row"><strong>356.7K</strong><span className="badge-up">+16.7%</span></div></div>
                      </div>

                      <div className="mockup-charts-grid">
                        <div className="chart-panel">
                          <div className="chart-header"><span>Performance Overview</span><span className="chart-filter">This Week ▾</span></div>
                          <div className="chart-svg-wrap">
                            <svg viewBox="0 0 340 100" preserveAspectRatio="none" className="chart-svg">
                              <defs><linearGradient id="chartGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stopColor="#38bdf8" stopOpacity="0.4" /><stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.0" /></linearGradient></defs>
                              <path d="M0,80 Q50,20 100,50 T200,30 T280,60 T340,20 L340,100 L0,100 Z" fill="url(#chartGrad)" />
                              <path d="M0,80 Q50,20 100,50 T200,30 T280,60 T340,20" fill="none" stroke="#38bdf8" strokeWidth="2.5" />
                            </svg>
                          </div>
                        </div>

                        <div className="platforms-panel">
                          <span className="platforms-title">Top Platforms</span>
                          <div className="platform-row"><div className="platform-label"><span className="platform-dot dot-ig" /><span>Instagram</span></div><div className="platform-bar-wrap"><div className="platform-bar bar-ig" style={{ width: "48%" }} /></div><span className="platform-percent">48%</span></div>
                          <div className="platform-row"><div className="platform-label"><span className="platform-dot dot-fb" /><span>Facebook</span></div><div className="platform-bar-wrap"><div className="platform-bar bar-fb" style={{ width: "28%" }} /></div><span className="platform-percent">28%</span></div>
                          <div className="platform-row"><div className="platform-label"><span className="platform-dot dot-li" /><span>LinkedIn</span></div><div className="platform-bar-wrap"><div className="platform-bar bar-li" style={{ width: "16%" }} /></div><span className="platform-percent">16%</span></div>
                          <div className="platform-row"><div className="platform-label"><span className="platform-dot dot-x" /><span>X (Twitter)</span></div><div className="platform-bar-wrap"><div className="platform-bar bar-x" style={{ width: "8%" }} /></div><span className="platform-percent">8%</span></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 5. FREE TOOLS SHOWCASE */}
        <section className="section tools-showcase-section" id="tools">
          <div className="section-container">
            <div className="section-header-split">
              <div className="header-left">
                <span className="eyebrow-cyan">FREE TOOLS</span>
                <h2 className="section-title">Powerful tools. Free for everyone.</h2>
                <p className="section-subtitle">All 8 tools are free. No sign up required. Instant results.</p>
              </div>
              <div className="header-right">
                <Link to="/tools" className="button button-ghost header-cta">
                  Explore All Tools <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>

            <div className="tools-grid-three">
              {toolsData.map((item) => (
                <div key={item.title} className="tool-card-showcase">
                  <span className="tool-card-icon" aria-hidden="true">{item.icon}</span>
                  <h3 className="tool-card-title">{item.title}</h3>
                  <p className="tool-card-desc">{item.copy}</p>
                  <Link to={item.link} className="tool-card-action">
                    {item.cta} <span aria-hidden="true">→</span>
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 6. CONTACT / LET'S TALK */}
        <section className="section contact-section" id="contact">
          <div className="section-container contact-grid">
            <ContactDetails />
            <ContactForm />
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/tools" element={<><Navbar /><ToolsPage /><Footer /></>} />
      <Route path="/tools/:slug" element={<><Navbar /><ToolPage /><Footer /></>} />
      <Route path="/product" element={<><Navbar /><ProductPage /><Footer /></>} />
      <Route path="/services" element={<><Navbar /><ServicesPage /><Footer /></>} />
      <Route path="/about" element={<><Navbar /><AboutPage /><Footer /></>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
