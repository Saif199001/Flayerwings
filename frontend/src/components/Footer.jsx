export default function Footer() {
  return (
    <footer className="site-footer" id="contact">
      <div>
        <p className="footer-brand">FLAYER WINGS</p>
        <p>AI, Software & SaaS Solutions for Modern Businesses.</p>
      </div>
      <div className="footer-links">
        <a href="mailto:hello@flayerwings.info">hello@flayerwings.info</a>
        <span>© {new Date().getFullYear()} Flayer Wings</span>
      </div>
    </footer>
  );
}
