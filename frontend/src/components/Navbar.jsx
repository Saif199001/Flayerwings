import { useState } from "react";
import { Link } from "react-router-dom";

const links = [["Solutions", "/services"], ["Product", "/product"], ["Free Tools", "/tools"], ["About", "/about"]];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  return <header className="site-header"><Link className="brand" to="/" aria-label="Flayer Wings home" onClick={() => setOpen(false)}><span className="brand-mark" aria-hidden="true">FW</span><span><strong>FLAYER</strong><small>WINGS</small></span></Link><button className="menu-toggle" onClick={() => setOpen(!open)} aria-expanded={open} aria-label="Toggle navigation">☰</button><nav className={`site-nav ${open ? "is-open" : ""}`} aria-label="Primary navigation">{links.map(([label, href]) => <Link key={href} to={href} onClick={() => setOpen(false)}>{label}</Link>)}<Link className="nav-cta" to="/#contact" onClick={() => setOpen(false)}>Start a Project</Link></nav></header>;
}
