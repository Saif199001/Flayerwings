import SEO from "../components/SEO";

const CONTENT = {
  privacy: {
    title: "Privacy Policy",
    description: "How Flayer Wings handles information submitted through this website and its free tools.",
    heading: "Privacy Policy",
    sections: [
      ["Information we collect", "Flayer Wings may receive information you voluntarily submit through the contact form, such as your name, email address, company details and project information. Our free tools may also use a browser-generated visitor identifier and local browser storage to support anonymous tool history and usage continuity."],
      ["How we use information", "We use submitted information to respond to enquiries, provide requested services, improve our website and tools, understand aggregate usage, and protect the service from abuse. We do not require a public user account to use the free tools."],
      ["Cookies and local storage", "The website may use essential browser storage and similar technologies for functionality, analytics or attribution. You can control storage through your browser settings, although disabling it may affect some tool functionality."],
      ["Third-party services", "Some website infrastructure or integrations may be provided by third-party service providers. Information shared with such providers is limited to what is necessary for the relevant service and handled according to applicable agreements and laws."],
      ["Data retention and requests", "We retain information only for as long as reasonably necessary for the purpose for which it was collected, legal obligations, dispute resolution or legitimate business needs. You may contact us to request access, correction or deletion where applicable."],
      ["Updates", "We may update this policy when the website, tools or applicable requirements change. The latest version will be published on this page."]
    ]
  },
  terms: {
    title: "Terms of Service",
    description: "Terms governing use of the Flayer Wings website and free tools.",
    heading: "Terms of Service",
    sections: [
      ["Use of the website", "You may use this website and its free tools for lawful business or personal purposes. You must not misuse, disrupt, overload, reverse engineer or attempt to gain unauthorized access to the service or its infrastructure."],
      ["Free tools", "Our generators and calculators are provided as practical tools. You are responsible for reviewing generated information before relying on it, especially for invoices, tax calculations, payment communications, quotations or other business records."],
      ["No professional or legal guarantee", "Tool output is not a substitute for professional tax, legal, accounting or financial advice. Flayer Wings does not guarantee that generated output is suitable for every jurisdiction, transaction or business situation."],
      ["Intellectual property", "Flayer Wings and its website, branding, software and original content remain protected by applicable intellectual-property laws. You retain rights to information and content you provide, subject to any third-party rights and the permissions required to operate the service."],
      ["Availability", "We aim to keep the website and tools useful and available, but functionality may change, be temporarily unavailable, or be discontinued as the product evolves."],
      ["Changes", "We may update these terms as the website and services develop. Continued use after an update constitutes acceptance of the revised terms where permitted by applicable law."]
    ]
  }
};

export default function LegalPage({ type }) {
  const page = CONTENT[type] || CONTENT.privacy;
  return (
    <>
      <SEO title={`${page.title} — Flayer Wings`} description={page.description} path={`/${type}`} />
      <main className="section legal-page">
        <div className="section-container">
          <div className="section-header">
            <span className="eyebrow-cyan">LEGAL</span>
            <h1 className="section-title">{page.heading}</h1>
            <p className="section-subtitle">Last updated: September 2026</p>
          </div>
          <article className="legal-content">
            {page.sections.map(([heading, copy]) => (
              <section key={heading}>
                <h2>{heading}</h2>
                <p>{copy}</p>
              </section>
            ))}
          </article>
        </div>
      </main>
    </>
  );
}
