import React, { useState, useEffect } from "react";
import { Sparkles, Wand2, RefreshCw, BookOpen } from "lucide-react";
import { api } from "../api/client";

const TRANSFORMATION_TYPES = [
  "Alternate Ending (Unpredicted Resolution)",
  "Futuristic Sci-Fi Space Opera Retelling",
  "Cyberpunk High-Tech Dystopia",
  "Villain's Perspective & POV Re-examination",
  "Modern Day Workplace / College Drama Adaptation",
  "Dark Fantasy & Magic System Overhaul",
  "What-If Multiverse Scenario"
];

export function ReimagineStudio({ initialBook, onReimagineComplete, loading }) {
  const [books, setBooks] = useState([]);
  const [selectedBookId, setSelectedBookId] = useState(initialBook?.id || "");
  const [transformationType, setTransformationType] = useState(TRANSFORMATION_TYPES[0]);
  const [twistInstructions, setTwistInstructions] = useState("");

  useEffect(() => {
    api.getClassics().then((res) => {
      setBooks(res || []);
      if (!selectedBookId && res?.length > 0) {
        setSelectedBookId(res[0].id);
      }
    });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedBookId) return;
    onReimagineComplete({
      classic_book_id: Number(selectedBookId),
      transformation_type: transformationType,
      twist_instructions: twistInstructions
    });
  };

  const selectedBook = books.find((b) => b.id === Number(selectedBookId)) || initialBook;

  return (
    <div style={{ maxWidth: "850px", margin: "0 auto" }}>
      <div className="glass-card" style={{ padding: "2.5rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "1rem" }}>
          <Sparkles className="text-amber" size={32} />
          <div>
            <h1 style={{ fontFamily: "var(--font-heading)", fontSize: "2rem" }}>AI Reimagined Stories Studio</h1>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem" }}>
              Take classic public domain literature and ask Google Gemini AI to construct a fresh, creative reinterpretation.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1.5rem", marginTop: "2rem" }}>
          {/* Select Classic */}
          <div>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600 }}>Select Classic Story</label>
            <select
              className="glass-card"
              style={{ width: "100%", padding: "0.85rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
              value={selectedBookId}
              onChange={(e) => setSelectedBookId(e.target.value)}
            >
              {books.map((b) => (
                <option key={b.id} value={b.id} style={{ background: "var(--bg-secondary)" }}>
                  {b.title} — by {b.author}
                </option>
              ))}
            </select>
          </div>

          {/* Book Preview */}
          {selectedBook && (
            <div style={{ display: "flex", gap: "1.25rem", background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <img src={selectedBook.cover_image} alt={selectedBook.title} style={{ width: "80px", height: "110px", objectFit: "cover", borderRadius: "var(--radius-sm)" }} />
              <div>
                <h4 style={{ color: "var(--accent-gold)", marginBottom: "0.25rem" }}>{selectedBook.title}</h4>
                <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                  {selectedBook.description}
                </p>
              </div>
            </div>
          )}

          {/* Transformation Vector */}
          <div>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600 }}>Transformation Vector</label>
            <select
              className="glass-card"
              style={{ width: "100%", padding: "0.85rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
              value={transformationType}
              onChange={(e) => setTransformationType(e.target.value)}
            >
              {TRANSFORMATION_TYPES.map((t) => (
                <option key={t} value={t} style={{ background: "var(--bg-secondary)" }}>
                  {t}
                </option>
              ))}
            </select>
          </div>

          {/* Twist Guidance */}
          <div>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600 }}>Custom Reimagining Guidance / Twist Instructions</label>
            <textarea
              className="glass-card"
              rows={3}
              placeholder="e.g. Set Alice in Wonderland in a 22nd century orbital station where the White Rabbit is a quantum AI glitch..."
              style={{ width: "100%", padding: "0.85rem", borderRadius: "var(--radius-md)", color: "var(--text-primary)" }}
              value={twistInstructions}
              onChange={(e) => setTwistInstructions(e.target.value)}
            />
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: "100%", padding: "1rem", marginTop: "1rem" }} disabled={loading}>
            <Wand2 size={20} />
            <span>{loading ? "Constructing Reimagined Concept..." : "Generate AI Reimagined Novel"}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
