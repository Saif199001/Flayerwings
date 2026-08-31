import { Link } from "react-router-dom";

export default function Footer() {
  return <footer className="site-footer" id="footer-contact"><div><Link className="footer-brand" to="/">FLAYER WINGS</Link><p>AI, Software & SaaS Solutions for Modern Businesses.</p></div><div className="footer-links"><strong>Explore</strong><Link to="/services">Services</Link><Link to="/product">Our SaaS</Link><Link to="/tools">Free Tools</Link><Link to="/about">About</Link></div><div className="footer-contact-info"><strong>Contact</strong><a href="tel:+917752987573">+91 77529 87573</a><a href="mailto:hello@flayerwings.info">hello@flayerwings.info</a><address>Building No. 6, Avtar Enclave, Paschim Vihar,<br />New Delhi – 110063</address></div><div className="footer-bottom"><span>© {new Date().getFullYear()} Flayer Wings</span><a href="#top">Back to top ↑</a></div></footer>;
}
