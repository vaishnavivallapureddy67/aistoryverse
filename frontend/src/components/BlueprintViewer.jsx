import React from "react";
import { BookOpen, RefreshCw, CheckCircle, Users, Globe, Target, AlertTriangle, Layers } from "lucide-react";

export function BlueprintViewer({ story, onAccept, onReject, loadingAccept, loadingReject }) {
  if (!story || !story.blueprint) return null;

  const bp = story.blueprint;
  const chars = bp.main_characters || [];
  const outline = bp.plot_outline || [];

  return (
    <div className="glass-card" style={{ maxWidth: "900px", margin: "0 auto", padding: "2.5rem" }}>
      {/* Header Banner */}
      <div style={{ display: "flex", gap: "2rem", marginBottom: "2rem", alignItems: "flex-start", flexWrap: "wrap" }}>
        <img
          src={story.cover_image || "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80"}
          alt={story.title}
          style={{ width: "180px", height: "260px", objectFit: "cover", borderRadius: "var(--radius-md)", boxShadow: "0 8px 25px rgba(0,0,0,0.4)" }}
        />

        <div style={{ flex: 1, minWidth: "280px" }}>
          <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.75rem", flexWrap: "wrap" }}>
            <span className="status-pill" style={{ background: "rgba(245, 158, 11, 0.15)", color: "var(--accent-gold)", borderColor: "rgba(245, 158, 11, 0.3)" }}>
              Status: Draft Blueprint
            </span>
            <span className="status-pill" style={{ background: "rgba(139, 92, 246, 0.15)", color: "var(--accent-purple)", borderColor: "rgba(139, 92, 246, 0.3)" }}>
              {story.genre}
            </span>
            <span className="status-pill" style={{ background: "rgba(6, 182, 212, 0.15)", color: "var(--accent-cyan)", borderColor: "rgba(6, 182, 212, 0.3)" }}>
              {story.blueprint_version || "v1.0"}
            </span>
          </div>

          <h1 style={{ fontFamily: "var(--font-heading)", fontSize: "2.2rem", marginBottom: "0.75rem", lineHeight: 1.2 }}>
            {story.title}
          </h1>

          <p style={{ color: "var(--text-secondary)", fontSize: "1.05rem", lineHeight: 1.6, marginBottom: "1.5rem" }}>
            {story.summary || bp.summary}
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", fontSize: "0.9rem", color: "var(--text-muted)" }}>
            <div><strong>Theme:</strong> {bp.theme}</div>
            <div><strong>Est. Chapters:</strong> {bp.estimated_chapters || 5} Chapters</div>
            <div><strong>Ending Style:</strong> {bp.ending_style}</div>
            <div><strong>Target Level:</strong> {story.generation_settings?.difficulty || "Intermediate"}</div>
          </div>
        </div>
      </div>

      {/* Blueprint Content Sections */}
      <div style={{ display: "flex", flexDirection: "column", gap: "1.75rem" }}>
        {/* World Setting */}
        <div style={{ background: "var(--bg-tertiary)", padding: "1.25rem", borderRadius: "var(--radius-md)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem", color: "var(--accent-cyan)", fontWeight: 700 }}>
            <Globe size={18} />
            <span>World & Setting</span>
          </div>
          <p style={{ color: "var(--text-primary)", fontSize: "0.95rem" }}>{bp.world_setting}</p>
        </div>

        {/* Character Roster */}
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1rem", color: "var(--accent-gold)", fontWeight: 700 }}>
            <Users size={18} />
            <span>Main Characters Roster</span>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "1rem" }}>
            {chars.map((c, i) => (
              <div key={i} style={{ background: "var(--bg-secondary)", padding: "1rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
                <h4 style={{ color: "var(--accent-gold)", fontSize: "1.1rem", marginBottom: "0.25rem" }}>{c.name}</h4>
                <div style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginBottom: "0.5rem" }}>{c.archetype}</div>
                <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "0.5rem" }}><strong>Personality:</strong> {c.personality}</p>
                <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}><strong>Goals:</strong> {c.goals}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Central Conflict */}
        <div style={{ background: "var(--bg-tertiary)", padding: "1.25rem", borderRadius: "var(--radius-md)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem", color: "var(--accent-rose)", fontWeight: 700 }}>
            <Target size={18} />
            <span>Main Dramatic Conflict</span>
          </div>
          <p style={{ color: "var(--text-primary)", fontSize: "0.95rem" }}>{bp.main_conflict}</p>
        </div>

        {/* Chapter Roadmap Outline */}
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1rem", color: "var(--accent-purple)", fontWeight: 700 }}>
            <Layers size={18} />
            <span>Plot Roadmap Outline</span>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            {outline.map((ch, i) => (
              <div key={i} style={{ display: "flex", gap: "1rem", background: "var(--bg-secondary)", padding: "0.85rem 1.25rem", borderRadius: "var(--radius-md)", alignItems: "center" }}>
                <div style={{ fontWeight: 700, color: "var(--accent-purple)", minWidth: "32px" }}>Ch {ch.chapter_number}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 600, color: "var(--text-primary)" }}>{ch.chapter_title}</div>
                  <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>{ch.objective}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "2.5rem", paddingTop: "1.5rem", borderTop: "1px solid var(--border-color)", flexWrap: "wrap", gap: "1rem" }}>
        <button
          className="btn btn-danger"
          onClick={onReject}
          disabled={loadingReject || loadingAccept}
        >
          <RefreshCw size={18} className={loadingReject ? "spin" : ""} />
          <span>{loadingReject ? "Discarding & Re-rolling..." : "Reject & Re-roll Concept"}</span>
        </button>

        <button
          className="btn btn-primary"
          onClick={onAccept}
          disabled={loadingAccept || loadingReject}
        >
          <CheckCircle size={18} />
          <span>{loadingAccept ? "Accepting & Writing Chapter 1..." : "Accept Concept & Write Chapter 1"}</span>
        </button>
      </div>
    </div>
  );
}
