import React, { useState, useEffect } from "react";
import { BookOpen, Sparkles, Search, Bookmark, ChevronRight } from "lucide-react";
import { api } from "../api/client";

export function ClassicsView({ onSelectClassic, onReimagineClassic }) {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    setLoading(true);
    api.getClassics(search)
      .then((res) => setBooks(res || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [search]);

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
      {/* Header */}
      <div style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
          <BookOpen className="text-amber" size={28} />
          <h1 style={{ fontFamily: "var(--font-heading)", fontSize: "2.2rem" }}>Classic Literature Collection</h1>
        </div>
        <p style={{ color: "var(--text-secondary)" }}>
          Curated timeless public-domain masterpieces. Read full books or prompt the AI to generate modern reimaginings.
        </p>
      </div>

      {/* Search */}
      <div style={{ marginBottom: "2rem", maxWidth: "450px", position: "relative" }}>
        <Search size={18} style={{ position: "absolute", left: "1rem", top: "50%", transform: "translateY(-50%)", color: "var(--text-muted)" }} />
        <input
          type="text"
          className="glass-card"
          placeholder="Search by title or author..."
          style={{ width: "100%", padding: "0.75rem 1rem 0.75rem 2.75rem", color: "var(--text-primary)" }}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Books Showcase Grid */}
      {loading ? (
        <div style={{ textAlign: "center", padding: "4rem", color: "var(--text-muted)" }}>Loading classic collection...</div>
      ) : (
        <div className="grid-3">
          {books.map((book) => (
            <div
              key={book.id}
              className="glass-card"
              style={{ display: "flex", flexDirection: "column" }}
            >
              <img
                src={book.cover_image}
                alt={book.title}
                style={{ width: "100%", height: "240px", objectFit: "cover", borderRadius: "var(--radius-md)", marginBottom: "1rem" }}
              />

              <div style={{ fontSize: "0.8rem", color: "var(--accent-gold)", fontWeight: 700, marginBottom: "0.25rem" }}>
                {book.author} ({book.publication_year})
              </div>

              <h3 style={{ fontFamily: "var(--font-heading)", fontSize: "1.3rem", marginBottom: "0.5rem" }}>{book.title}</h3>

              <p style={{ color: "var(--text-secondary)", fontSize: "0.85rem", marginBottom: "1.25rem", flex: 1, display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                {book.description}
              </p>

              <div style={{ display: "flex", gap: "0.5rem" }}>
                <button
                  className="btn btn-secondary"
                  style={{ flex: 1, fontSize: "0.85rem", padding: "0.6rem" }}
                  onClick={() => onSelectClassic(book)}
                >
                  <BookOpen size={16} /> Read Classic
                </button>
                <button
                  className="btn btn-primary"
                  style={{ flex: 1, fontSize: "0.85rem", padding: "0.6rem" }}
                  onClick={() => onReimagineClassic(book)}
                >
                  <Sparkles size={16} /> Reimagine
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
