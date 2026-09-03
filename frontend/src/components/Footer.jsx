import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="site-footer-premium" id="footer-contact">
      <div className="footer-container">
        <div className="footer-grid">
          <div className="footer-brand-col">
            <Link className="footer-brand-lockup" to="/">
              <img className="footer-logo-img" src="/flayer_wings_logo.jpeg" alt="Flayer Wings" width="130" height="52" />
            </Link>
            <p className="footer-tagline">
              Building AI-powered software and SaaS products for the future.
            </p>
          </div>

          <div className="footer-nav-col">
            <h4>Company</h4>
            <Link to="/about">About Us</Link>
            <Link to="/services">Our Process</Link>
            <Link to="/about">Company Updates</Link>
          </div>

          <div className="footer-nav-col">
            <h4>Resources</h4>
            <Link to="/tools">Free Tools</Link>
            <Link to="/product">Products</Link>
            <Link to="/#contact">Contact Us</Link>
          </div>

          <div className="footer-nav-col">
            <h4>Legal</h4>
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/terms">Terms of Service</Link>
          </div>

          <div className="footer-connect-col">
            <h4>Connect</h4>
            <p className="footer-tagline">Follow Flayer Wings through our official channels as they become available.</p>
          </div>
        </div>

        <div className="footer-bottom-row">
          <span>© {new Date().getFullYear()} Flayer Wings Technologies. All rights reserved.</span>
          <span className="footer-made-in">Made with <span className="heart-icon">❤️</span> in India</span>
        </div>
      </div>
    </footer>
  );
}
