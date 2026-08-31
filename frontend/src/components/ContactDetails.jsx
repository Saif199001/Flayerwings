export default function ContactDetails() {
  return (
    <div className="contact-details" aria-label="Flayer Wings contact details">
      <div className="contact-detail">
        <span className="detail-label">CALL / WHATSAPP</span>
        <a href="tel:+917752987573">+91 77529 87573</a>
      </div>
      <div className="contact-detail">
        <span className="detail-label">VISIT US</span>
        <address>Building No. 6, Avtar Enclave,<br />Paschim Vihar, New Delhi – 110063</address>
      </div>
      <div className="contact-detail">
        <span className="detail-label">EMAIL</span>
        <a href="mailto:hello@flayerwings.info">hello@flayerwings.info</a>
      </div>
    </div>
  );
}
