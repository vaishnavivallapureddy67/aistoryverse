import React, { useState, useEffect } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Bookmark as BookmarkIcon,
  Sun,
  Moon,
  BookOpen,
  PlusCircle,
  FileText,
  Clock,
  CheckCircle2,
  Share2
} from "lucide-react";
import { api } from "../api/client";

export function ReaderView({ story, classicBook, onBack, onGenerateNext, loadingNext }) {
  const [currentChapterIndex, setCurrentChapterIndex] = useState(0);
  const [theme, setTheme] = useState("dark"); // dark, light, sepia, midnight
  const [fontSize, setFontSize] = useState(18); // px
  const [fontFamily, setFontFamily] = useState("serif"); // serif, sans
  const [bookmarks, setBookmarks] = useState([]);
  const [showBookmarkModal, setShowBookmarkModal] = useState(false);
  const [bookmarkNote, setBookmarkNote] = useState("");

  const isClassic = Boolean(classicBook);
  const chapters = isClassic ? classicBook?.chapters || [] : story?.chapters || [];
  const title = isClassic ? classicBook?.title : story?.title;
  const author = isClassic ? classicBook?.author : "AI Master Novelist";
  const currentChapter = chapters[currentChapterIndex] || null;

  // Apply theme to body
  useEffect(() => {
    document.body.className = "";
    if (theme !== "dark") {
      document.body.classList.add(`theme-${theme}`);
    }
    return () => {
      document.body.className = "";
    };
  }, [theme]);

  // Load bookmarks
  useEffect(() => {
    if (story?.id || classicBook?.id) {
      api.getBookmarks(story?.id, classicBook?.id)
        .then((res) => setBookmarks(res || []))
        .catch(console.error);
    }
  }, [story, classicBook]);

  const handleAddBookmark = async () => {
    if (!currentChapter) return;
    try {
      const bm = await api.addBookmark({
        story_id: story?.id,
        classic_book_id: classicBook?.id,
        chapter_number: currentChapter.chapter_number,
        position_percent: 0.5,
        note: bookmarkNote.trim() || `Bookmark at Chapter ${currentChapter.chapter_number}`
      });
      setBookmarks([bm, ...bookmarks]);
      setBookmarkNote("");
      setShowBookmarkModal(false);
    } catch (err) {
      alert("Failed to save bookmark");
    }
  };

  if (!currentChapter && !loadingNext) {
    return (
      <div style={{ textAlign: "center", padding: "4rem" }}>
        <h2>No chapters available yet</h2>
        <button className="btn btn-secondary" style={{ marginTop: "1rem" }} onClick={onBack}>
          <ChevronLeft size={18} /> Back to Library
        </button>
      </div>
    );
  }

  const wordCount = currentChapter?.word_count || currentChapter?.content?.split(" ")?.length || 0;
  const estReadTime = Math.max(1, Math.round(wordCount / 200));
  const progressPercent = chapters.length > 0 ? Math.round(((currentChapterIndex + 1) / chapters.length) * 100) : 100;

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", paddingBottom: "4rem" }}>
      {/* Reader Top Bar */}
      <div className="reader-toolbar" style={{ background: "var(--bg-card)", padding: "1rem 1.5rem", borderRadius: "var(--radius-lg)" }}>
        <button className="btn btn-secondary" style={{ padding: "0.5rem 1rem" }} onClick={onBack}>
          <ChevronLeft size={18} /> Back
        </button>

        <div style={{ display: "flex", alignItems: "center", gap: "1rem", flexWrap: "wrap" }}>
          {/* Themes */}
          <div style={{ display: "flex", background: "var(--bg-secondary)", borderRadius: "var(--radius-md)", padding: "3px" }}>
            <button
              className={`btn ${theme === "dark" ? "btn-primary" : "btn-secondary"}`}
              style={{ padding: "0.3rem 0.6rem" }}
              onClick={() => setTheme("dark")}
              title="Dark Mode"
            >
              <Moon size={16} />
            </button>
            <button
              className={`btn ${theme === "light" ? "btn-primary" : "btn-secondary"}`}
              style={{ padding: "0.3rem 0.6rem" }}
              onClick={() => setTheme("light")}
              title="Light Mode"
            >
              <Sun size={16} />
            </button>
            <button
              className={`btn ${theme === "sepia" ? "btn-primary" : "btn-secondary"}`}
              style={{ padding: "0.3rem 0.6rem" }}
              onClick={() => setTheme("sepia")}
              title="Sepia Mode"
            >
              <BookOpen size={16} />
            </button>
          </div>

          {/* Font Controls */}
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>Font:</span>
            <button
              className="btn btn-secondary"
              style={{ padding: "0.2rem 0.5rem", fontSize: "0.85rem" }}
              onClick={() => setFontSize(Math.max(14, fontSize - 2))}
            >
              A-
            </button>
            <span style={{ fontSize: "0.85rem", width: "24px", textAlign: "center" }}>{fontSize}</span>
            <button
              className="btn btn-secondary"
              style={{ padding: "0.2rem 0.5rem", fontSize: "0.85rem" }}
              onClick={() => setFontSize(Math.min(28, fontSize + 2))}
            >
              A+
            </button>
          </div>

          {/* Font Family */}
          <button
            className="btn btn-secondary"
            style={{ padding: "0.3rem 0.75rem", fontSize: "0.85rem" }}
            onClick={() => setFontFamily(fontFamily === "serif" ? "sans" : "serif")}
          >
            {fontFamily === "serif" ? "Serif" : "Sans-Serif"}
          </button>

          {/* Bookmark Button */}
          <button
            className="btn btn-secondary"
            style={{ padding: "0.3rem 0.75rem", fontSize: "0.85rem" }}
            onClick={() => setShowBookmarkModal(true)}
          >
            <BookmarkIcon size={16} />
            <span>Note</span>
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{ background: "var(--bg-tertiary)", height: "4px", width: "100%", borderRadius: "2px", margin: "1rem 0 2rem" }}>
        <div style={{ background: "var(--accent-purple)", height: "100%", width: `${progressPercent}%`, transition: "width 0.3s ease" }} />
      </div>

      {/* Chapter Reader Frame */}
      <div className="reader-container">
        {/* Book Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <div style={{ fontSize: "0.85rem", color: "var(--accent-gold)", textTransform: "uppercase", letterSpacing: "1.5px", fontWeight: 700, marginBottom: "0.5rem" }}>
            {isClassic ? "Classic Literature" : story?.genre}
          </div>
          <h1 style={{ fontFamily: "var(--font-heading)", fontSize: "2.2rem", marginBottom: "0.5rem" }}>{title}</h1>
          <div style={{ color: "var(--text-secondary)", fontSize: "0.95rem" }}>By {author}</div>

          <div style={{ display: "flex", justifyContent: "center", gap: "1.5rem", marginTop: "1rem", fontSize: "0.85rem", color: "var(--text-muted)" }}>
            <span style={{ display: "flex", alignItems: "center", gap: "0.35rem" }}><FileText size={14} /> {wordCount} words</span>
            <span style={{ display: "flex", alignItems: "center", gap: "0.35rem" }}><Clock size={14} /> ~{estReadTime} min read</span>
            <span style={{ display: "flex", alignItems: "center", gap: "0.35rem" }}><CheckCircle2 size={14} /> Ch {currentChapterIndex + 1} of {chapters.length}</span>
          </div>
        </div>

        {/* Chapter Title */}
        <h2 style={{ fontFamily: "var(--font-heading)", fontSize: "1.6rem", marginBottom: "1.75rem", color: "var(--accent-purple)", textAlign: "center" }}>
          {currentChapter?.title || `Chapter ${currentChapterIndex + 1}`}
        </h2>

        {/* Chapter Content */}
        <div
          className="reader-body"
          style={{
            fontSize: `${fontSize}px`,
            fontFamily: fontFamily === "serif" ? "var(--font-serif)" : "var(--font-ui)",
          }}
        >
          {currentChapter?.content?.split("\n\n").map((para, i) => (
            <p key={i}>{para}</p>
          ))}
        </div>

        {/* Saved User Notes/Bookmarks for this Chapter */}
        {bookmarks.filter(b => b.chapter_number === currentChapter?.chapter_number).length > 0 && (
          <div style={{ marginTop: "3rem", padding: "1.25rem", background: "var(--bg-tertiary)", borderRadius: "var(--radius-md)" }}>
            <h4 style={{ display: "flex", alignItems: "center", gap: "0.5rem", color: "var(--accent-gold)", marginBottom: "0.75rem" }}>
              <BookmarkIcon size={16} /> Reader Notes for Chapter {currentChapter.chapter_number}
            </h4>
            {bookmarks.filter(b => b.chapter_number === currentChapter?.chapter_number).map((bm) => (
              <div key={bm.id} style={{ fontSize: "0.9rem", color: "var(--text-secondary)", marginBottom: "0.5rem", fontStyle: "italic" }}>
                "{bm.note}"
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Chapter Navigation Bar */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "2rem" }}>
        <button
          className="btn btn-secondary"
          disabled={currentChapterIndex === 0}
          onClick={() => setCurrentChapterIndex(currentChapterIndex - 1)}
        >
          <ChevronLeft size={18} /> Previous Chapter
        </button>

        {/* Chapter Selector Dropdown */}
        <select
          className="glass-card"
          style={{ padding: "0.5rem 1rem", color: "var(--text-primary)", borderRadius: "var(--radius-md)" }}
          value={currentChapterIndex}
          onChange={(e) => setCurrentChapterIndex(Number(e.target.value))}
        >
          {chapters.map((ch, idx) => (
            <option key={idx} value={idx} style={{ background: "var(--bg-secondary)" }}>
              Ch {idx + 1}: {ch.title}
            </option>
          ))}
        </select>

        {currentChapterIndex < chapters.length - 1 ? (
          <button className="btn btn-secondary" onClick={() => setCurrentChapterIndex(currentChapterIndex + 1)}>
            Next Chapter <ChevronRight size={18} />
          </button>
        ) : !isClassic ? (
          <button className="btn btn-primary" onClick={onGenerateNext} disabled={loadingNext}>
            <Sparkles size={18} />
            <span>{loadingNext ? "Writing Next Chapter..." : "Generate Next Chapter"}</span>
          </button>
        ) : (
          <button className="btn btn-secondary" disabled>
            End of Book
          </button>
        )}
      </div>

      {/* Add Bookmark Modal */}
      {showBookmarkModal && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: "450px" }}>
            <h3 style={{ marginBottom: "1rem", fontFamily: "var(--font-heading)" }}>Add Reader Note / Bookmark</h3>
            <textarea
              className="glass-card"
              rows={4}
              placeholder="Write your note or theory here (e.g. 'I think the king is hiding something...')"
              style={{ width: "100%", padding: "0.75rem", color: "var(--text-primary)", marginBottom: "1.25rem" }}
              value={bookmarkNote}
              onChange={(e) => setBookmarkNote(e.target.value)}
            />
            <div style={{ display: "flex", justifyContent: "flex-end", gap: "0.75rem" }}>
              <button className="btn btn-secondary" onClick={() => setShowBookmarkModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleAddBookmark}>Save Note</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
