import { Link } from "react-router-dom";

const principles = [
  ["01", "Useful over flashy", "Technology should solve a real problem and make the next step clearer."],
  ["02", "Build with purpose", "We choose technology around the business need—not the other way around."],
  ["03", "Stay transparent", "We show what is live, what is being built and what is still a plan."],
  ["04", "Keep improving", "Real feedback and real results should shape what we build next."],
];

export default function AboutPage() {
  return <main className="section about-page">
    <section className="page-hero"><p className="eyebrow">ABOUT FLAYER WINGS</p><h1>We build technology<br /><span>with a reason.</span></h1><p className="section-copy">Flayer Wings is a technology and digital solutions studio focused on AI, software, SaaS and practical digital execution for modern businesses.</p><div className="actions"><Link className="button button-primary" to="/services">See Our Services →</Link><Link className="button button-secondary" to="/product">See What We're Building</Link></div></section>
    <section className="about-story"><div><p className="eyebrow">OUR APPROACH</p><h2>Start with the problem.<br /><span>Then build the solution.</span></h2></div><div><p>We don't believe every business needs more software. We believe businesses need the right solution to the right problem.</p><p>That might be social media support today, an automation workflow tomorrow, or a complete SaaS product over time. Our role is to understand the need and build something useful around it.</p></div></section>
    <section className="principles"><p className="eyebrow">WHAT WE BELIEVE</p><div className="principle-grid">{principles.map(([number, title, copy]) => <article key={number}><span>{number}</span><h3>{title}</h3><p>{copy}</p></article>)}</div></section>
    <section className="building-note"><div><p className="eyebrow">BUILDING OUR OWN PRODUCT</p><h2>We practice what<br /><span>we build.</span></h2><p>Our upcoming social media management SaaS is being developed from the same problems we see in real workflows. We're building it in public, learning as we go and keeping the product honest about what is—and isn't—ready.</p></div><Link className="button button-primary" to="/product">Explore Our SaaS →</Link></section>
  </main>;
}
