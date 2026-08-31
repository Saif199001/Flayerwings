import { Navigate, Route, Routes } from "react-router-dom";

function Home() {
  return (
    <main className="page-shell">
      <section className="hero">
        <p className="eyebrow">FLAYER WINGS 2.0</p>
        <h1>Build. Automate. Grow.</h1>
        <p className="hero-copy">
          AI-powered software, SaaS products and digital solutions for modern businesses.
        </p>
        <div className="actions">
          <a className="button button-primary" href="#contact">Start a Project</a>
          <a className="button button-secondary" href="#tools">Explore Free Tools</a>
        </div>
      </section>
    </main>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
