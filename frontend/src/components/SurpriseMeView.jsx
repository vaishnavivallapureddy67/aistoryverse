import React, { useState } from "react";
import { Dices, Sparkles, RefreshCw, Wand2, Shield, Compass, Zap } from "lucide-react";
import { api } from "../api/client";

export function SurpriseMeView({ onSurpriseComplete, loading }) {
  const [vectors, setVectors] = useState(null);
  const [rolling, setRolling] = useState(false);

  const fetchRandomVectors = async () => {
    setRolling(true);
    try {
      const data = await api.getSurpriseVectors();
      setVectors(data);
    } catch (err) {
      console.error(err);
    } finally {
      setRolling(false);
    }
  };

  const handleGenerateStory = async () => {
    onSurpriseComplete();
  };

  return (
    <div style={{ maxWidth: "850px", margin: "0 auto" }}>
      <div className="glass-card" style={{ padding: "2.5rem", textAlign: "center" }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: "1rem" }}>
          <div style={{ width: 64, height: 64, borderRadius: "50%", background: "rgba(245, 158, 11, 0.15)", display: "flex", alignItems: "center", justifyContent: "center", border: "1px solid rgba(245, 158, 11, 0.3)" }}>
            <Dices className="text-amber" size={36} />
          </div>
        </div>

        <h1 style={{ fontFamily: "var(--font-heading)", fontSize: "2.2rem", marginBottom: "0.5rem" }}>
          Surprise Me Story Generator
        </h1>
        <p style={{ color: "var(--text-secondary)", maxWidth: "600px", margin: "0 auto 2rem" }}>
          Let the AI randomly combine unique narrative building blocks across genre, world, archetype, conflict, tone, and ending style!
        </p>

        {/* Vector Card Cards */}
        {vectors ? (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "1rem", marginBottom: "2.5rem", textAlign: "left" }}>
            <div style={{ background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-purple)", textTransform: "uppercase", fontWeight: 700 }}>Genre</div>
              <div style={{ fontWeight: 700, fontSize: "1.1rem", marginTop: "0.25rem" }}>{vectors.genre}</div>
            </div>

            <div style={{ background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-cyan)", textTransform: "uppercase", fontWeight: 700 }}>Theme</div>
              <div style={{ fontWeight: 600, fontSize: "0.95rem", marginTop: "0.25rem" }}>{vectors.theme}</div>
            </div>

            <div style={{ background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-gold)", textTransform: "uppercase", fontWeight: 700 }}>World Setting</div>
              <div style={{ fontWeight: 600, fontSize: "0.95rem", marginTop: "0.25rem" }}>{vectors.world}</div>
            </div>

            <div style={{ background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-rose)", textTransform: "uppercase", fontWeight: 700 }}>Character Archetype</div>
              <div style={{ fontWeight: 600, fontSize: "0.95rem", marginTop: "0.25rem" }}>{vectors.character_archetype}</div>
            </div>

            <div style={{ background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--accent-emerald)", textTransform: "uppercase", fontWeight: 700 }}>Central Conflict</div>
              <div style={{ fontWeight: 600, fontSize: "0.95rem", marginTop: "0.25rem" }}>{vectors.conflict}</div>
            </div>

            <div style={{ background: "var(--bg-tertiary)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)", textTransform: "uppercase", fontWeight: 700 }}>Narration & Ending</div>
              <div style={{ fontWeight: 600, fontSize: "0.95rem", marginTop: "0.25rem" }}>{vectors.narration_pov} • {vectors.ending_style}</div>
            </div>
          </div>
        ) : (
          <div style={{ padding: "3rem", background: "var(--bg-tertiary)", borderRadius: "var(--radius-md)", marginBottom: "2.5rem" }}>
            <Compass size={40} className="text-muted" style={{ marginBottom: "1rem", opacity: 0.6 }} />
            <h3 style={{ color: "var(--text-secondary)" }}>Ready to roll the dice?</h3>
            <p style={{ fontSize: "0.9rem", color: "var(--text-muted)", marginTop: "0.5rem" }}>Click below to spin the multi-vector randomizer!</p>
          </div>
        )}

        {/* Buttons */}
        <div style={{ display: "flex", justifyContent: "center", gap: "1rem", flexWrap: "wrap" }}>
          <button className="btn btn-secondary" onClick={fetchRandomVectors} disabled={rolling || loading}>
            <RefreshCw size={18} className={rolling ? "spin" : ""} />
            <span>{rolling ? "Rolling Dice..." : "Roll Random Vectors"}</span>
          </button>

          <button className="btn btn-primary" onClick={handleGenerateStory} disabled={loading}>
            <Sparkles size={18} />
            <span>{loading ? "Generating Surprise Novel..." : "Instant Generate Novel"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
