import React, { useState } from "react";
import { Sparkles, Wand2, X, AlertCircle } from "lucide-react";

const GENRES = ["Fantasy", "Sci-Fi", "Cyberpunk", "Gothic Mystery", "Cozy Romance", "Thriller", "Horror", "Historical Fiction"];
const TONES = ["Immersive & Atmospheric", "Dark & Suspenseful", "Witty & Lighthearted", "Epic & Cinematic", "Poetic & Melancholic"];
const STYLES = ["Rich Descriptive Prose", "Fast-Paced Action", "Character-Driven Dialogue", "Poetic & Sensory"];
const DIFFICULTIES = ["Beginner", "Intermediate", "Advanced / Literary"];
const LENGTHS = ["Short Story (3-5 Chapters)", "Medium Novel (5-8 Chapters)", "Long Epic (8-12 Chapters)"];

export function OriginalGeneratorModal({ isOpen, onClose, onGenerate, loading }) {
  const [formData, setFormData] = useState({
    genre: "Fantasy",
    tone: "Immersive & Atmospheric",
    style: "Rich Descriptive Prose",
    difficulty: "Intermediate",
    length: "Medium Novel (5-8 Chapters)",
    character_name: "",
    custom_prompt: ""
  });

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerate(formData);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: "680px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
            <Sparkles className="text-amber" size={24} />
            <h2 style={{ fontFamily: "var(--font-heading)", fontSize: "1.5rem" }}>Create Original AI Novel</h2>
          </div>
          <button className="btn btn-secondary" style={{ padding: "0.4rem" }} onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
          <div>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
              Genre
            </label>
            <select
              className="glass-card"
              style={{ width: "100%", padding: "0.75rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
              value={formData.genre}
              onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
            >
              {GENRES.map((g) => (
                <option key={g} value={g} style={{ background: "var(--bg-secondary)" }}>
                  {g}
                </option>
              ))}
            </select>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
                Tone / Atmosphere
              </label>
              <select
                className="glass-card"
                style={{ width: "100%", padding: "0.75rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
                value={formData.tone}
                onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
              >
                {TONES.map((t) => (
                  <option key={t} value={t} style={{ background: "var(--bg-secondary)" }}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
                Writing Style
              </label>
              <select
                className="glass-card"
                style={{ width: "100%", padding: "0.75rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
                value={formData.style}
                onChange={(e) => setFormData({ ...formData, style: e.target.value })}
              >
                {STYLES.map((s) => (
                  <option key={s} value={s} style={{ background: "var(--bg-secondary)" }}>
                    {s}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
                Reading Difficulty
              </label>
              <select
                className="glass-card"
                style={{ width: "100%", padding: "0.75rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
                value={formData.difficulty}
                onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
              >
                {DIFFICULTIES.map((d) => (
                  <option key={d} value={d} style={{ background: "var(--bg-secondary)" }}>
                    {d}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
                Story Length Target
              </label>
              <select
                className="glass-card"
                style={{ width: "100%", padding: "0.75rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
                value={formData.length}
                onChange={(e) => setFormData({ ...formData, length: e.target.value })}
              >
                {LENGTHS.map((l) => (
                  <option key={l} value={l} style={{ background: "var(--bg-secondary)" }}>
                    {l}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
              Main Character Name (Optional)
            </label>
            <input
              type="text"
              className="glass-card"
              placeholder="e.g. Kaelen Voss, Elena Rostova..."
              style={{ width: "100%", padding: "0.75rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
              value={formData.character_name}
              onChange={(e) => setFormData({ ...formData, character_name: e.target.value })}
            />
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
              Custom Guidance / Story Premise
            </label>
            <textarea
              className="glass-card"
              rows={3}
              placeholder="e.g. A rogue scholar discovers an ancient clockwork device that controls seasonal weather..."
              style={{ width: "100%", padding: "0.75rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
              value={formData.custom_prompt}
              onChange={(e) => setFormData({ ...formData, custom_prompt: e.target.value })}
            />
          </div>

          <div style={{ display: "flex", justifyContent: "flex-end", gap: "1rem", marginTop: "1rem" }}>
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              <Wand2 size={18} />
              <span>{loading ? "Generating Blueprint..." : "Generate Blueprint"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
