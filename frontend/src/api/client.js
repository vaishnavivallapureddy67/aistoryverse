// Dynamic API Base: Uses production VITE_BACKEND_URL environment variable from Vercel / .env.production,
// or falls back to local dev server when running locally.
const PROD_API = import.meta.env?.VITE_BACKEND_URL;
const LOCAL_API = typeof window !== "undefined" ? `http://${window.location.hostname}:8000/api/v1` : "http://localhost:8000/api/v1";

const API_BASE = PROD_API || LOCAL_API;

export async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server error: ${response.status}`);
    }
    if (response.status === 204) return null;
    return await response.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  // System & Settings
  getSettings: () => request("/settings"),
  updateApiKey: (apiKey) => request("/settings/api-key", { method: "POST", body: JSON.stringify({ api_key: apiKey }) }),

  // Original Stories
  createBlueprint: (settings) => request("/stories/blueprint", { method: "POST", body: JSON.stringify({ settings }) }),
  acceptBlueprint: (storyId) => request(`/stories/${storyId}/accept`, { method: "POST" }),
  rejectBlueprint: (storyId) => request(`/stories/${storyId}/reject`, { method: "POST" }),
  generateNextChapter: (storyId) => request(`/stories/${storyId}/next-chapter`, { method: "POST" }),
  getStory: (storyId) => request(`/stories/${storyId}`),
  updateStoryStatus: (storyId, status) => request(`/stories/${storyId}/status`, { method: "PATCH", body: JSON.stringify({ status }) }),

  // Classics
  getClassics: (search, genre) => {
    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (genre) params.append("genre", genre);
    const q = params.toString();
    return request(`/classics${q ? `?${q}` : ""}`);
  },
  getClassicBook: (bookId) => request(`/classics/${bookId}`),

  // Reimagined Stories
  createReimagined: (data) => request("/reimagined/create", { method: "POST", body: JSON.stringify(data) }),

  // Surprise Me
  getSurpriseVectors: () => request("/surprise-me/random-prompt"),
  generateSurpriseStory: () => request("/surprise-me/generate", { method: "POST" }),

  // Library & Bookmarks
  getLibraryStories: (search, status, genre) => {
    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (status) params.append("status", status);
    if (genre) params.append("genre", genre);
    const q = params.toString();
    return request(`/library/stories${q ? `?${q}` : ""}`);
  },
  deleteStory: (storyId) => request(`/library/stories/${storyId}`, { method: "DELETE" }),
  addBookmark: (data) => request("/library/bookmarks", { method: "POST", body: JSON.stringify(data) }),
  getBookmarks: (storyId, classicId) => {
    const params = new URLSearchParams();
    if (storyId) params.append("story_id", storyId);
    if (classicId) params.append("classic_book_id", classicId);
    const q = params.toString();
    return request(`/library/bookmarks${q ? `?${q}` : ""}`);
  },
  getStoryLogs: (storyId) => request(`/library/stories/${storyId}/logs`),

  // Analytics & Sessions
  startSession: (data) => request("/analytics/session/start", { method: "POST", body: JSON.stringify(data) }),
  endSession: (sessionId, data) => request(`/analytics/session/${sessionId}/end`, { method: "POST", body: JSON.stringify(data) }),
  getAnalyticsSummary: () => request("/analytics/summary"),
};
