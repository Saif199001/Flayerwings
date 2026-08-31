import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const links = [["Solutions", "/services"], ["Product", "/product"], ["Free Tools", "/tools"], ["About", "/about"]];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  const closeMenu = () => setOpen(false);

  return (
    <header className="site-header">
      <Link className="brand" to="/" aria-label="Flayer Wings home" onClick={closeMenu}>
        <span className="brand-logo-wrap">
          <img className="brand-logo" src="/flayer_wings_logo.jpeg" alt="Flayer Wings" width="52" height="52" />
        </span>
        <span className="brand-wordmark"><strong>FLAYER</strong><small>WINGS</small></span>
      </Link>

      <button
        className={`menu-toggle ${open ? "is-open" : ""}`}
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-controls="primary-navigation"
        aria-label={open ? "Close navigation" : "Open navigation"}
      >
        <span />
        <span />
        <span />
      </button>

      <nav id="primary-navigation" className={`site-nav ${open ? "is-open" : ""}`} aria-label="Primary navigation">
        {links.map(([label, href]) => (
          <Link
            key={href}
            className={location.pathname === href || location.pathname.startsWith(`${href}/`) ? "is-active" : ""}
            to={href}
            onClick={closeMenu}
          >
            {label}
          </Link>
        ))}
        <Link className="nav-cta" to="/#contact" onClick={closeMenu}>Start a Project <span aria-hidden="true">→</span></Link>
      </nav>
    </header>
  );
}
