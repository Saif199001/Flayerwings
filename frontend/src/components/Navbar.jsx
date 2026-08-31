import { useState } from "react";
import { Link } from "react-router-dom";

const links = [["Solutions", "/services"], ["Product", "/product"], ["Free Tools", "/tools"], ["About", "/about"]];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  return <header className="site-header"><Link className="brand" to="/" aria-label="Flayer Wings home" onClick={() => setOpen(false)}><img className="brand-logo" src="/flayer_wings_logo.jpeg" alt="Flayer Wings" width="44" height="44" style={{ width: 44, height: 44, objectFit: "contain", borderRadius: 10 }} /><span className="brand-wordmark"><strong>FLAYER</strong><small>WINGS</small></span></Link><button className="menu-toggle" onClick={() => setOpen(!open)} aria-expanded={open} aria-label="Toggle navigation">☰</button><nav className={`site-nav ${open ? "is-open" : ""}`} aria-label="Primary navigation">{links.map(([label, href]) => <Link key={href} to={href} onClick={() => setOpen(false)}>{label}</Link>)}<Link className="nav-cta" to="/#contact" onClick={() => setOpen(false)}>Start a Project</Link></nav></header>;
}
