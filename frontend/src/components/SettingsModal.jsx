import React, { useState } from "react";
import { Settings, Key, X, CheckCircle, Shield } from "lucide-react";
import { api } from "../api/client";

export function SettingsModal({ isOpen, onClose, settings, onSettingsUpdated }) {
  const [apiKey, setApiKey] = useState("");
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");

  if (!isOpen) return null;

  const handleSaveKey = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMsg("");
    try {
      const res = await api.updateApiKey(apiKey);
      setMsg(`API Key updated successfully! Mode: ${res.mode}`);
      onSettingsUpdated();
    } catch (err) {
      setMsg(`Error updating key: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: "550px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <Settings className="text-purple" size={24} />
            <h2 style={{ fontFamily: "var(--font-heading)", fontSize: "1.4rem" }}>System Settings</h2>
          </div>
          <button className="btn btn-secondary" style={{ padding: "0.3rem" }} onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {/* Info */}
        <div style={{ background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)", marginBottom: "1.5rem" }}>
          <div style={{ fontSize: "0.85rem", color: "var(--text-muted)", marginBottom: "0.25rem" }}>Primary AI Provider</div>
          <div style={{ fontWeight: 700, fontSize: "1.1rem", color: "var(--accent-gold)" }}>Google Gemini AI</div>
          <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginTop: "0.5rem" }}>
            Model Configured: <code>{settings?.gemini_model || "gemini-1.5-flash"}</code>
          </div>
          <div style={{ fontSize: "0.85rem", color: "var(--accent-emerald)", marginTop: "0.25rem", fontWeight: 600 }}>
            Current Status: {settings?.mode || "Live Google Gemini AI"}
          </div>
        </div>

        {/* API Key Form */}
        <form onSubmit={handleSaveKey} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <div>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600, fontSize: "0.9rem" }}>
              Google Gemini API Key
            </label>
            <input
              type="password"
              className="glass-card"
              placeholder="Enter your AIStudio / Gemini API Key..."
              style={{ width: "100%", padding: "0.75rem", color: "var(--text-primary)" }}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <p style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.35rem" }}>
              Key is saved in memory and `.env`. If left empty, the application automatically uses the rich Offline Mock AI Engine.
            </p>
          </div>

          {msg && (
            <div style={{ padding: "0.75rem", background: "rgba(16, 185, 129, 0.15)", color: "var(--accent-emerald)", borderRadius: "var(--radius-sm)", fontSize: "0.85rem" }}>
              {msg}
            </div>
          )}

          <div style={{ display: "flex", justifyContent: "flex-end", gap: "0.75rem", marginTop: "0.5rem" }}>
            <button type="button" className="btn btn-secondary" onClick={onClose}>Close</button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              <Key size={16} />
              <span>{saving ? "Saving..." : "Save API Key"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
