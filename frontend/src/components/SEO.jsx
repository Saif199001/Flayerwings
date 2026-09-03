import { useEffect } from "react";

const SITE_URL = "https://flayerwings.info";
const DEFAULT_IMAGE = `${SITE_URL}/og-image.svg`;

function setMeta(attribute, key, content) {
  let node = document.head.querySelector(`meta[${attribute}="${key}"]`);
  if (!node) {
    node = document.createElement("meta");
    node.setAttribute(attribute, key);
    document.head.appendChild(node);
  }
  node.setAttribute("content", content);
}

export default function SEO({ title, description, path = "/", image = DEFAULT_IMAGE }) {
  useEffect(() => {
    const canonical = new URL(path, SITE_URL).toString();
    document.title = title;
    setMeta("name", "description", description);
    setMeta("property", "og:title", title);
    setMeta("property", "og:description", description);
    setMeta("property", "og:url", canonical);
    setMeta("property", "og:image", image);
    setMeta("name", "twitter:title", title);
    setMeta("name", "twitter:description", description);
    setMeta("name", "twitter:image", image);

    let link = document.head.querySelector('link[rel="canonical"]');
    if (!link) {
      link = document.createElement("link");
      link.setAttribute("rel", "canonical");
      document.head.appendChild(link);
    }
    link.setAttribute("href", canonical);

    return () => {
      document.title = "Flayer Wings — AI, Software & SaaS Solutions";
    };
  }, [title, description, path, image]);

  return null;
}
