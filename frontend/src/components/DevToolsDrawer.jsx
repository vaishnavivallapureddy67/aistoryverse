import React, { useState, useEffect } from "react";
import { X, Terminal, Brain, History, Settings, Code, FileText } from "lucide-react";
import { api } from "../api/client";

export function DevToolsDrawer({ isOpen, onClose, story }) {
  const [activeTab, setActiveTab] = useState("memory"); // memory, logs, config
  const [logs, setLogs] = useState([]);
  const [loadingLogs, setLoadingLogs] = useState(false);

  useEffect(() => {
    if (story?.id && isOpen) {
      setLoadingLogs(true);
      api.getStoryLogs(story.id)
        .then((res) => setLogs(res || []))
        .catch(console.error)
        .finally(() => setLoadingLogs(false));
    }
  }, [story?.id, isOpen]);

  return (
    <div className={`devtools-drawer ${isOpen ? "open" : ""}`}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem", borderBottom: "1px solid var(--border-color)", paddingBottom: "1rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", color: "var(--accent-purple)" }}>
          <Terminal size={20} />
          <h3 style={{ fontFamily: "var(--font-heading)", fontSize: "1.1rem" }}>Developer Mode Inspection</h3>
        </div>
        <button className="btn btn-secondary" style={{ padding: "0.3rem" }} onClick={onClose}>
          <X size={18} />
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1.5rem" }}>
        <button
          className={`btn ${activeTab === "memory" ? "btn-primary" : "btn-secondary"}`}
          style={{ padding: "0.4rem 0.75rem", fontSize: "0.8rem", flex: 1 }}
          onClick={() => setActiveTab("memory")}
        >
          <Brain size={14} /> Story Memory
        </button>

        <button
          className={`btn ${activeTab === "logs" ? "btn-primary" : "btn-secondary"}`}
          style={{ padding: "0.4rem 0.75rem", fontSize: "0.8rem", flex: 1 }}
          onClick={() => setActiveTab("logs")}
        >
          <History size={14} /> Prompt History
        </button>
      </div>

      {/* Tab 1: Story Memory Inspection */}
      {activeTab === "memory" && (
        <div>
          {!story ? (
            <div style={{ color: "var(--text-muted)", fontSize: "0.9rem", textAlign: "center", padding: "2rem" }}>
              Open an active story to inspect its internal Story Memory state.
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
              <div style={{ fontSize: "0.85rem", color: "var(--accent-gold)" }}>
                Story: <strong>{story.title}</strong> ({story.status})
              </div>

              <div>
                <h4 style={{ fontSize: "0.85rem", color: "var(--accent-purple)", marginBottom: "0.35rem" }}>Overall Summary</h4>
                <div style={{ background: "var(--bg-primary)", padding: "0.75rem", borderRadius: "var(--radius-sm)", fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                  {story.story_memory?.overall_summary || "No summary tracked."}
                </div>
              </div>

              <div>
                <h4 style={{ fontSize: "0.85rem", color: "var(--accent-cyan)", marginBottom: "0.35rem" }}>Tracked Characters ({story.story_memory?.characters?.length || 0})</h4>
                <pre style={{ background: "var(--bg-primary)", padding: "0.75rem", borderRadius: "var(--radius-sm)", fontSize: "0.75rem", color: "var(--text-primary)", overflowX: "auto" }}>
                  {JSON.stringify(story.story_memory?.characters || [], null, 2)}
                </pre>
              </div>

              <div>
                <h4 style={{ fontSize: "0.85rem", color: "var(--accent-rose)", marginBottom: "0.35rem" }}>Timeline & Events</h4>
                <pre style={{ background: "var(--bg-primary)", padding: "0.75rem", borderRadius: "var(--radius-sm)", fontSize: "0.75rem", color: "var(--text-primary)", overflowX: "auto" }}>
                  {JSON.stringify(story.story_memory?.important_events || [], null, 2)}
                </pre>
              </div>

              <div>
                <h4 style={{ fontSize: "0.85rem", color: "var(--accent-gold)", marginBottom: "0.35rem" }}>Key Locations & Objects</h4>
                <pre style={{ background: "var(--bg-primary)", padding: "0.75rem", borderRadius: "var(--radius-sm)", fontSize: "0.75rem", color: "var(--text-primary)", overflowX: "auto" }}>
                  {JSON.stringify({ locations: story.story_memory?.locations, objects: story.story_memory?.objects }, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Prompt History Logs */}
      {activeTab === "logs" && (
        <div>
          {loadingLogs ? (
            <div style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>Loading prompt audit trail...</div>
          ) : logs.length === 0 ? (
            <div style={{ color: "var(--text-muted)", fontSize: "0.85rem", textAlign: "center", padding: "2rem" }}>
              No generation logs recorded for this story yet.
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
              {logs.map((log) => (
                <div key={log.id} style={{ background: "var(--bg-primary)", padding: "0.85rem", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.75rem", color: "var(--accent-purple)", marginBottom: "0.5rem" }}>
                    <span style={{ fontWeight: 700 }}>{log.prompt_type.toUpperCase()}</span>
                    <span>{log.model_name}</span>
                  </div>

                  <div style={{ marginBottom: "0.5rem" }}>
                    <span style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>Prompt Text:</span>
                    <pre style={{ fontSize: "0.75rem", color: "var(--text-secondary)", whiteSpace: "pre-wrap", maxHeight: "120px", overflowY: "auto", background: "rgba(0,0,0,0.3)", padding: "0.5rem", borderRadius: "4px" }}>
                      {log.prompt_text}
                    </pre>
                  </div>

                  <div>
                    <span style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>Response Snippet:</span>
                    <pre style={{ fontSize: "0.75rem", color: "var(--accent-emerald)", whiteSpace: "pre-wrap", maxHeight: "100px", overflowY: "auto", background: "rgba(0,0,0,0.3)", padding: "0.5rem", borderRadius: "4px" }}>
                      {log.response_text}
                    </pre>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
