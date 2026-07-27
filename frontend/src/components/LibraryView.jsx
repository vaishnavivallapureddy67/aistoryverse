import React, { useState, useEffect } from "react";
import { BookOpen, Search, Trash2, Play, Sparkles, Filter, CheckCircle, Clock } from "lucide-react";
import { api } from "../api/client";

export function LibraryView({ onSelectStory, onCreateNew }) {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  const loadLibrary = () => {
    setLoading(true);
    const filterStatus = statusFilter === "all" ? null : statusFilter;
    api.getLibraryStories(search, filterStatus)
      .then((res) => setStories(res || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadLibrary();
  }, [search, statusFilter]);

  const handleDelete = async (storyId, title, e) => {
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to delete "${title}"?`)) return;
    try {
      await api.deleteStory(storyId);
      setStories(stories.filter((s) => s.id !== storyId));
    } catch (err) {
      alert("Failed to delete story.");
    }
  };

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
      {/* Library Title & Controls */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem", flexWrap: "wrap", gap: "1rem" }}>
        <div>
          <h1 style={{ fontFamily: "var(--font-heading)", fontSize: "2.2rem", marginBottom: "0.25rem" }}>My Personal Library</h1>
          <p style={{ color: "var(--text-secondary)" }}>Your collection of generated AI novels, drafts, and reading progress.</p>
        </div>

        <button className="btn btn-primary" onClick={onCreateNew}>
          <Sparkles size={18} /> Create New Novel
        </button>
      </div>

      {/* Search & Filters */}
      <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: "260px", position: "relative" }}>
          <Search size={18} style={{ position: "absolute", left: "1rem", top: "50%", transform: "translateY(-50%)", color: "var(--text-muted)" }} />
          <input
            type="text"
            className="glass-card"
            placeholder="Search stories by title or summary..."
            style={{ width: "100%", padding: "0.75rem 1rem 0.75rem 2.75rem", color: "var(--text-primary)" }}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Status Filters */}
        <div style={{ display: "flex", gap: "0.5rem" }}>
          {["all", "Draft", "Reading", "Completed"].map((st) => (
            <button
              key={st}
              className={`btn ${statusFilter === st ? "btn-primary" : "btn-secondary"}`}
              style={{ padding: "0.5rem 1rem", fontSize: "0.85rem" }}
              onClick={() => setStatusFilter(st)}
            >
              {st === "all" ? "All Stories" : st}
            </button>
          ))}
        </div>
      </div>

      {/* Stories Grid */}
      {loading ? (
        <div style={{ textAlign: "center", padding: "4rem", color: "var(--text-muted)" }}>Loading your library...</div>
      ) : stories.length === 0 ? (
        <div className="glass-card" style={{ textAlign: "center", padding: "4rem" }}>
          <BookOpen size={48} className="text-muted" style={{ marginBottom: "1rem", opacity: 0.5 }} />
          <h3>No stories found in library</h3>
          <p style={{ color: "var(--text-secondary)", margin: "0.5rem 0 1.5rem" }}>Generate your first AI novel or start reading a classic!</p>
          <button className="btn btn-primary" onClick={onCreateNew}>
            <Sparkles size={18} /> Create Original Novel
          </button>
        </div>
      ) : (
        <div className="grid-3">
          {stories.map((story) => (
            <div
              key={story.id}
              className="glass-card"
              style={{ display: "flex", flexDirection: "column", cursor: "pointer", position: "relative" }}
              onClick={() => onSelectStory(story)}
            >
              <div style={{ position: "relative", height: "220px", marginBottom: "1rem", borderRadius: "var(--radius-md)", overflow: "hidden" }}>
                <img
                  src={story.cover_image || "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80"}
                  alt={story.title}
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
                <span
                  className="status-pill"
                  style={{
                    position: "absolute",
                    top: "0.75rem",
                    right: "0.75rem",
                    background: story.status === "Draft" ? "rgba(245,158,11,0.9)" : "rgba(139,92,246,0.9)",
                    color: "#fff",
                    border: "none",
                    fontWeight: 700
                  }}
                >
                  {story.status}
                </span>

                {story.is_reimagined && (
                  <span className="status-pill" style={{ position: "absolute", top: "0.75rem", left: "0.75rem", background: "rgba(6,182,212,0.9)", color: "#fff" }}>
                    Reimagined
                  </span>
                )}
              </div>

              <h3 style={{ fontFamily: "var(--font-heading)", fontSize: "1.25rem", marginBottom: "0.5rem" }}>{story.title}</h3>
              <p style={{ color: "var(--text-secondary)", fontSize: "0.85rem", marginBottom: "1rem", flex: 1, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                {story.summary || "No summary generated."}
              </p>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: "0.8rem", color: "var(--text-muted)", borderTop: "1px solid var(--border-color)", paddingTop: "0.75rem" }}>
                <span>{story.chapters_generated || 0} Chapters</span>
                <span>{story.total_words || 0} Words</span>
                <button
                  className="btn btn-danger"
                  style={{ padding: "0.25rem 0.5rem", fontSize: "0.75rem" }}
                  onClick={(e) => handleDelete(story.id, story.title, e)}
                  title="Delete Story"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
