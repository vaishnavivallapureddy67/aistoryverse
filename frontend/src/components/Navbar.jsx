import React from "react";
import { BookOpen, Sparkles, Dices, Library, Compass, Settings, Terminal } from "lucide-react";

export function Navbar({ activeTab, setActiveTab, settings, devMode, setDevMode, openSettings }) {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand-logo" onClick={() => setActiveTab("discover")}>
          <BookOpen className="brand-icon" size={28} />
          <span>AIStoryVerse</span>
        </div>

        <nav>
          <ul className="nav-links">
            <li>
              <button
                className={`nav-link ${activeTab === "discover" ? "active" : ""}`}
                onClick={() => setActiveTab("discover")}
              >
                <Compass size={18} />
                <span>Discover</span>
              </button>
            </li>
            <li>
              <button
                className={`nav-link ${activeTab === "create" ? "active" : ""}`}
                onClick={() => setActiveTab("create")}
              >
                <Sparkles size={18} />
                <span>Create Novel</span>
              </button>
            </li>
            <li>
              <button
                className={`nav-link ${activeTab === "surprise" ? "active" : ""}`}
                onClick={() => setActiveTab("surprise")}
              >
                <Dices size={18} />
                <span>Surprise Me</span>
              </button>
            </li>
            <li>
              <button
                className={`nav-link ${activeTab === "classics" ? "active" : ""}`}
                onClick={() => setActiveTab("classics")}
              >
                <BookOpen size={18} />
                <span>Classics</span>
              </button>
            </li>
            <li>
              <button
                className={`nav-link ${activeTab === "reimagine" ? "active" : ""}`}
                onClick={() => setActiveTab("reimagine")}
              >
                <Sparkles size={18} className="text-amber" />
                <span>Reimagine</span>
              </button>
            </li>
            <li>
              <button
                className={`nav-link ${activeTab === "library" ? "active" : ""}`}
                onClick={() => setActiveTab("library")}
              >
                <Library size={18} />
                <span>My Library</span>
              </button>
            </li>
          </ul>
        </nav>

        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <div className="status-pill">
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: "currentColor" }}></span>
            <span>{settings?.mode || "Google Gemini AI"}</span>
          </div>

          <button
            className={`btn btn-secondary ${devMode ? "active" : ""}`}
            style={{ padding: "0.4rem 0.75rem", fontSize: "0.85rem" }}
            onClick={() => setDevMode(!devMode)}
            title="Toggle Developer Mode (Memory & Prompt History)"
          >
            <Terminal size={16} />
            <span>Dev Tools</span>
          </button>

          <button
            className="btn btn-secondary"
            style={{ padding: "0.4rem 0.75rem" }}
            onClick={openSettings}
            title="System Settings"
          >
            <Settings size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}
