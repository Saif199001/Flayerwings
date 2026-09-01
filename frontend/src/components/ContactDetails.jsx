export default function ContactDetails() {
  return (
    <div className="contact-details-box" aria-label="Flayer Wings contact details">
      <div className="contact-item">
        <span className="contact-icon" aria-hidden="true">✉</span>
        <a href="mailto:hello@flayerwings.info" className="contact-link">
          hello@flayerwings.info
        </a>
      </div>
      <div className="contact-item">
        <span className="contact-icon" aria-hidden="true">☎</span>
        <a href="tel:+917752987573" className="contact-link">
          +91 77529 87573
        </a>
      </div>
      <div className="contact-item">
        <span className="contact-icon" aria-hidden="true">📍</span>
        <address className="contact-address">
          Building No. 6, Avtar Enclave, Paschim Vihar, New Delhi – 110063
        </address>
      </div>
    </div>
  );
}
