import { Navigate, Route, Routes } from "react-router-dom";
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
import "./styles/hero-slice-2.css";
import "./styles/hero-premium.css";

const solutions = [
  ["01", "AI Solutions", "Practical AI experiences and automation designed around real business workflows.", "Automate repetitive work"],
  ["02", "Custom Software", "Purpose-built software for teams that have outgrown generic tools.", "Build exactly what you need"],
  ["03", "SaaS Development", "From product concept to scalable SaaS foundations and polished user experiences.", "Turn an idea into a product"],
  ["04", "Web & Mobile", "Fast, modern digital products that make your business easier to discover and use.", "Create a better digital presence"],
];

const principles = [
  ["AI-first", "Use AI where it creates a real business advantage."],
  ["Lean delivery", "Focused builds without unnecessary complexity."],
  ["Founder-led", "Direct communication from idea to execution."],
  ["Built in public", "Our own SaaS is shaped by real-world problems."],
];

function Home() {
  return <div id="top" className="app-shell"><Navbar /><main>
    <section className="hero-section">
      <div className="hero-glow" aria-hidden="true" />
      <div className="hero-stars" aria-hidden="true"><i /><i /><i /><i /><i /><i /><i /><i /></div>
      <div className="hero-content">
        <p className="eyebrow hero-eyebrow"><span aria-hidden="true">●</span> AI • SOFTWARE • SAAS</p>
        <h1>Build.<br /><span>Automate.</span><br />Grow.</h1>
        <p className="hero-copy">We build AI-powered software, SaaS products and digital solutions that help modern businesses work smarter and grow faster.</p>
        <div className="actions hero-actions">
          <a className="button button-primary" href="#contact">Start a Project <span>→</span></a>
          <a className="button button-secondary" href="/tools">Explore Free Tools <span aria-hidden="true">↗</span></a>
        </div>
        <div className="hero-trust"><span>AI-first delivery</span><span>Practical solutions</span><span>Built for growth</span></div>
      </div>
      <div className="hero-orbit" aria-hidden="true">
        <div className="orbit-ambient" />
        <div className="orbit-grid" />
        <div className="orbit-ring ring-one" />
        <div className="orbit-ring ring-two" />
        <div className="orbit-ring ring-three" />
        <div className="orbit-ring ring-four" />
        <div className="orbit-ring ring-five" />
        <div className="orbit-circuit circuit-one" />
        <div className="orbit-circuit circuit-two" />
        <div className="orbit-node node-one" />
        <div className="orbit-node node-two" />
        <div className="orbit-node node-three" />
        <div className="orbit-node node-four" />
        <div className="orbit-node node-five" />
        <div className="orbit-node node-six" />
        <div className="orbit-card orbit-card-ai"><span className="orbit-card-icon">✦</span><strong>AI</strong><small>Intelligence</small></div>
        <div className="orbit-card orbit-card-code"><span className="orbit-card-icon">&lt;/&gt;</span><strong>Development</strong><small>Build. Scale. Ship.</small></div>
        <div className="orbit-card orbit-card-data"><span className="orbit-card-icon">▮▮▮</span><strong>Data</strong><small>Analytics</small></div>
        <div className="orbit-card orbit-card-cloud"><span className="orbit-card-icon">⌁</span><strong>Cloud</strong><small>Scalable</small></div>
        <div className="orbit-logo"><span className="orbit-logo-glow" /><img src="/flayer_wings_logo.jpeg" alt="" width="150" height="150" /></div>
      </div>
    </section>

    <section className="principles-strip" aria-label="How Flayer Wings works">{principles.map(([title, copy]) => <article key={title}><strong>{title}</strong><span>{copy}</span></article>)}</section>

    <section className="section" id="solutions"><div className="section-heading-row"><div><p className="eyebrow">WHAT WE BUILD</p><h2>Technology that moves<br /><span>business forward.</span></h2></div><p className="section-intro">From automation to complete digital products, we focus on useful technology—not technology for its own sake.</p></div><div className="card-grid">{solutions.map(([number, title, copy, outcome]) => <article className="feature-card" key={title}><span>{number}</span><h3>{title}</h3><p>{copy}</p><div className="card-outcome">{outcome}</div><a href="/services">Explore <span>→</span></a></article>)}</div></section>

    <section className="section product-section" id="products"><div className="product-copy"><p className="eyebrow">BUILDING IN PUBLIC</p><h2>Our next product<br /><span>is already in motion.</span></h2><p>We are building our own SaaS platform at Flayer Wings—designed from real-world social media management challenges.</p><a className="text-link" href="/product">Explore the Product →</a></div><div className="product-card"><span className="status-pill">COMING SOON</span><div className="product-visual"><img src="/flayer_wings_logo.jpeg" alt="Flayer Wings SaaS" width="150" height="150" /><i /><i /><i /></div><h3>Flayer Wings SaaS</h3><p>Social media management, analytics and workflow—built as a modern SaaS product.</p><a href="/product">Explore product →</a></div></section>

    <section className="section tools-section" id="tools"><div className="section-heading-row"><div><p className="eyebrow">FREE TOOLS</p><h2>Useful tools.<br /><span>No paywall.</span></h2></div><p className="section-intro">Get practical insights and create better social content with tools designed to give you a useful starting point—without forcing a signup first.</p></div><div className="card-grid three"><article className="tool-card"><span className="tool-number">01</span><h3>Social Media Audit</h3><p>Get a practical starting point for improving your social presence.</p><a href="/tools/social-media-audit">Try it free →</a></article><article className="tool-card"><span className="tool-number">02</span><h3>AI Caption Generator</h3><p>Turn a topic into a ready-to-edit social caption.</p><a href="/tools/caption-generator">Try it free →</a></article><article className="tool-card"><span className="tool-number">03</span><h3>Content Ideas</h3><p>Get 10 tailored content starting points.</p><a href="/tools/content-ideas">Try it free →</a></article></div></section>

    <section className="section contact-section" id="contact"><div className="contact-copy"><p className="eyebrow">LET'S TALK</p><h2>Have an idea?<br /><span>Let's build it.</span></h2><p>Tell us what you're trying to build, automate or improve. We'll take a look and get back to you.</p><div className="contact-points"><span>✦ Clear scope</span><span>✦ Practical solutions</span><span>✦ No pressure</span></div><ContactDetails /></div><ContactForm /></section>
  </main><Footer /></div>;
}

export default function App() { return <Routes><Route path="/" element={<Home />} /><Route path="/services" element={<><Navbar /><ServicesPage /><Footer /></>} /><Route path="/about" element={<><Navbar /><AboutPage /><Footer /></>} /><Route path="/tools" element={<><Navbar /><ToolsPage /><Footer /></>} /><Route path="/tools/:slug" element={<><Navbar /><ToolPage /><Footer /></>} /><Route path="/product" element={<><Navbar /><ProductPage /><Footer /></>} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>; }
