export default function Footer() {
  return (
    <footer className="site-footer" id="footer-contact">
      <div>
        <p className="footer-brand">FLAYER WINGS</p>
        <p>AI, Software & SaaS Solutions for Modern Businesses.</p>
      </div>
      <div className="footer-contact-info">
        <a href="tel:+917752987573">+91 77529 87573</a>
        <a href="mailto:hello@flayerwings.info">hello@flayerwings.info</a>
        <address>Building No. 6, Avtar Enclave, Paschim Vihar,<br />New Delhi – 110063</address>
        <span>© {new Date().getFullYear()} Flayer Wings</span>
      </div>
    </footer>
  );
}
