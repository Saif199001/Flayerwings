import { useState } from "react";

const links = [
  ["Solutions", "#solutions"],
  ["Products", "#products"],
  ["Free Tools", "#tools"],
  ["About", "#about"],
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="site-header">
      <a className="brand" href="#top" aria-label="Flayer Wings home">
        <span className="brand-mark" aria-hidden="true">FW</span>
        <span><strong>FLAYER</strong><small>WINGS</small></span>
      </a>
      <button className="menu-toggle" onClick={() => setOpen(!open)} aria-expanded={open} aria-label="Toggle navigation">☰</button>
      <nav className={`site-nav ${open ? "is-open" : ""}`} aria-label="Primary navigation">
        {links.map(([label, href]) => <a key={href} href={href} onClick={() => setOpen(false)}>{label}</a>)}
        <a className="nav-cta" href="#contact" onClick={() => setOpen(false)}>Start a Project</a>
      </nav>
    </header>
  );
}
