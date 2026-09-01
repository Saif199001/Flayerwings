const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(data.detail || "Request failed");
    error.data = data;
    throw error;
  }
  return data;
}

export function createLead(payload) { return request("/leads/", { method: "POST", body: JSON.stringify(payload) }); }
export function getProjects() { return request("/projects/"); }

export function listTools() { return request("/tools/"); }
export function getToolTemplates(slug) { return request(`/tools/templates/${slug}/`); }
export function createToolDocument(payload) { return request("/tools/documents/", { method: "POST", body: JSON.stringify(payload) }); }
export function getToolDocuments(visitorId) { return request(`/tools/documents/?visitor_id=${encodeURIComponent(visitorId)}`); }
export function trackToolEvent(payload) { return request("/tools/events/", { method: "POST", body: JSON.stringify(payload) }); }
export function getToolPdfUrl(id, visitorId) {
  const suffix = visitorId ? `?visitor_id=${encodeURIComponent(visitorId)}` : "";
  return `${API_BASE_URL}/tools/documents/${id}/pdf/${suffix}`;
}
