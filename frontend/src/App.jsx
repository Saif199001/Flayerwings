import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

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
            <p className="hero-copy">
              We build AI-powered software, SaaS products and digital solutions that help modern businesses work smarter and grow faster.
            </p>
            <div className="actions">
              <a className="button button-primary" href="#contact">Start a Project <span>→</span></a>
              <a className="button button-secondary" href="#tools">Explore Free Tools</a>
            </div>
            <p className="hero-note">Technology built for the next stage of your business.</p>
          </div>
          <div className="hero-orbit" aria-hidden="true"><div className="orbit-core">FW</div></div>
        </section>

        <section className="section" id="solutions">
          <p className="eyebrow">WHAT WE BUILD</p>
          <h2>Technology that moves<br /><span>business forward.</span></h2>
          <div className="card-grid">
            {["AI Solutions", "Custom Software", "SaaS Development", "Web & Mobile"].map((item, i) => (
              <article className="feature-card" key={item}><span>0{i + 1}</span><h3>{item}</h3><p>Practical technology designed around real business problems and measurable outcomes.</p><a href="#contact">Explore →</a></article>
            ))}
          </div>
        </section>

        <section className="section product-section" id="products">
          <div><p className="eyebrow">BUILDING IN PUBLIC</p><h2>Our next product<br /><span>is already in motion.</span></h2><p>We are building our own SaaS platform at Flayer Wings—designed from real-world social media management challenges.</p><a className="text-link" href="#contact">Join the journey →</a></div>
          <div className="product-card"><span className="status-pill">COMING SOON</span><div className="product-icon">FW</div><h3>Flayer Wings SaaS</h3><p>Social media management, analytics and workflow—built as a modern SaaS product.</p></div>
        </section>

        <section className="section tools-section" id="tools">
          <p className="eyebrow">FREE TOOLS</p><h2>Useful tools.<br /><span>No paywall.</span></h2><p className="section-copy">Get practical insights and create better social content with our free tools.</p>
          <div className="card-grid three"><article className="tool-card"><h3>Social Media Audit</h3><p>Discover what's holding your social presence back.</p><a href="#contact">Try it free →</a></article><article className="tool-card"><h3>AI Caption Generator</h3><p>Create platform-ready captions in seconds.</p><a href="#contact">Try it free →</a></article><article className="tool-card"><h3>Content Ideas</h3><p>Get ideas tailored to your business and audience.</p><a href="#contact">Try it free →</a></article></div>
        </section>

        <section className="section cta-section" id="about"><p className="eyebrow">FLAYER WINGS</p><h2>Have an idea?<br /><span>Let's build it.</span></h2><a className="button button-primary" href="#contact">Start a Project <span>→</span></a></section>
      </main>
      <Footer />
    </div>
  );
}

function App() { return <Routes><Route path="/" element={<Home />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>; }
export default App;
