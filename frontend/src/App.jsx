import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ContactForm from "./components/ContactForm";

const solutions = [
  ["01", "AI Solutions", "Practical AI experiences and automation designed around real business workflows."],
  ["02", "Custom Software", "Purpose-built software for teams that have outgrown generic tools."],
  ["03", "SaaS Development", "From product concept to scalable SaaS foundations and polished user experiences."],
  ["04", "Web & Mobile", "Fast, modern digital products that make your business easier to discover and use."],
];

const tools = [
  ["Social Media Audit", "Discover what's holding your social presence back."],
  ["AI Caption Generator", "Create platform-ready captions in seconds."],
  ["Content Ideas", "Get practical ideas tailored to your business and audience."],
];

function Home() {
  return (
    <div id="top" className="app-shell">
      <Navbar />
      <main>
        <section className="hero-section">
          <div className="hero-glow" aria-hidden="true" />
          <div className="hero-content">
            <p className="eyebrow">AI • SOFTWARE • SAAS</p>
            <h1>Build.<br /><span>Automate.</span><br />Grow.</h1>
            <p className="hero-copy">We build AI-powered software, SaaS products and digital solutions that help modern businesses work smarter and grow faster.</p>
            <div className="actions">
              <a className="button button-primary" href="#contact">Start a Project <span>→</span></a>
              <a className="button button-secondary" href="#tools">Explore Free Tools</a>
            </div>
            <p className="hero-note">Technology built for the next stage of your business.</p>
          </div>
          <div className="hero-orbit" aria-hidden="true"><div className="orbit-ring ring-one" /><div className="orbit-ring ring-two" /><div className="orbit-core">FW</div></div>
        </section>

        <section className="section" id="solutions">
          <p className="eyebrow">WHAT WE BUILD</p>
          <h2>Technology that moves<br /><span>business forward.</span></h2>
          <div className="card-grid">
            {solutions.map(([number, title, copy]) => (
              <article className="feature-card" key={title}><span>{number}</span><h3>{title}</h3><p>{copy}</p><a href="#contact">Explore →</a></article>
            ))}
          </div>
        </section>

        <section className="section product-section" id="products">
          <div className="product-copy"><p className="eyebrow">BUILDING IN PUBLIC</p><h2>Our next product<br /><span>is already in motion.</span></h2><p>We are building our own SaaS platform at Flayer Wings—designed from real-world social media management challenges.</p><a className="text-link" href="#contact">Join the journey →</a></div>
          <div className="product-card"><span className="status-pill">COMING SOON</span><div className="product-visual"><span>FW</span><i /><i /><i /></div><h3>Flayer Wings SaaS</h3><p>Social media management, analytics and workflow—built as a modern SaaS product.</p><a href="#contact">Get early access →</a></div>
        </section>

        <section className="section tools-section" id="tools">
          <p className="eyebrow">FREE TOOLS</p><h2>Useful tools.<br /><span>No paywall.</span></h2><p className="section-copy">Get practical insights and create better social content with our free tools.</p>
          <div className="card-grid three">{tools.map(([title, copy], index) => <article className="tool-card" key={title}><span className="tool-number">0{index + 1}</span><h3>{title}</h3><p>{copy}</p><a href="#contact">Try it free →</a></article>)}</div>
        </section>

        <section className="section contact-section" id="contact">
          <div className="contact-copy"><p className="eyebrow">LET'S TALK</p><h2>Have an idea?<br /><span>Let's build it.</span></h2><p>Tell us what you're trying to build, automate or improve. We'll take a look and get back to you.</p><div className="contact-points"><span>✦ Clear scope</span><span>✦ Practical solutions</span><span>✦ No pressure</span></div></div>
          <ContactForm />
        </section>
      </main>
      <Footer />
    </div>
  );
}

function App() {
  return <Routes><Route path="/" element={<Home />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>;
}

export default App;
