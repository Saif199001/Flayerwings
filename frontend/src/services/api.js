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

export function createLead(payload) {
  return request("/leads/", { method: "POST", body: JSON.stringify(payload) });
}

export function getProjects() { return request("/projects/"); }
