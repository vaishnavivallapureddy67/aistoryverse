import React, { useState, useEffect } from "react";
import { Navbar } from "./components/Navbar";
import { OriginalGeneratorModal } from "./components/OriginalGeneratorModal";
import { BlueprintViewer } from "./components/BlueprintViewer";
import { ReaderView } from "./components/ReaderView";
import { LibraryView } from "./components/LibraryView";
import { ClassicsView } from "./components/ClassicsView";
import { ReimagineStudio } from "./components/ReimagineStudio";
import { SurpriseMeView } from "./components/SurpriseMeView";
import { DevToolsDrawer } from "./components/DevToolsDrawer";
import { SettingsModal } from "./components/SettingsModal";
import { Sparkles, Dices, BookOpen, Library, ArrowRight, Wand2, Compass, Layers, CheckCircle } from "lucide-react";
import { api } from "./api/client";

export function App() {
  const [activeTab, setActiveTab] = useState("discover"); // discover, create, surprise, classics, reimagine, library, reader, blueprint
  const [settings, setSettings] = useState(null);
  const [devMode, setDevMode] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Active Story & Classic State
  const [currentStory, setCurrentStory] = useState(null);
  const [currentClassic, setCurrentClassic] = useState(null);

  // Loading States
  const [loadingBlueprint, setLoadingBlueprint] = useState(false);
  const [loadingAccept, setLoadingAccept] = useState(false);
  const [loadingReject, setLoadingReject] = useState(false);
  const [loadingNext, setLoadingNext] = useState(false);

  const loadSettings = () => {
    api.getSettings().then(setSettings).catch(console.error);
  };

  useEffect(() => {
    loadSettings();
  }, []);

  // Handlers
  const handleGenerateOriginalBlueprint = async (formData) => {
    setLoadingBlueprint(true);
    try {
      const story = await api.createBlueprint(formData);
      setCurrentStory(story);
      setCurrentClassic(null);
      setShowCreateModal(false);
      setActiveTab("blueprint");
    } catch (err) {
      alert(`Error generating blueprint: ${err.message}`);
    } finally {
      setLoadingBlueprint(false);
    }
  };

  const handleAcceptBlueprint = async () => {
    if (!currentStory) return;
    setLoadingAccept(true);
    try {
      const updatedStory = await api.acceptBlueprint(currentStory.id);
      setCurrentStory(updatedStory);
      setActiveTab("reader");
    } catch (err) {
      alert(`Error accepting blueprint: ${err.message}`);
    } finally {
      setLoadingAccept(false);
    }
  };

  const handleRejectBlueprint = async () => {
    if (!currentStory) return;
    setLoadingReject(true);
    try {
      const regeneratedStory = await api.rejectBlueprint(currentStory.id);
      setCurrentStory(regeneratedStory);
    } catch (err) {
      alert(`Error regenerating story: ${err.message}`);
    } finally {
      setLoadingReject(false);
    }
  };

  const handleGenerateNextChapter = async () => {
    if (!currentStory) return;
    setLoadingNext(true);
    try {
      const chapter = await api.generateNextChapter(currentStory.id);
      // Reload story
      const reloaded = await api.getStory(currentStory.id);
      setCurrentStory(reloaded);
    } catch (err) {
      alert(`Error writing next chapter: ${err.message}`);
    } finally {
      setLoadingNext(false);
    }
  };

  const handleReimagineSubmit = async (data) => {
    setLoadingBlueprint(true);
    try {
      const story = await api.createReimagined(data);
      setCurrentStory(story);
      setCurrentClassic(null);
      setActiveTab("blueprint");
    } catch (err) {
      alert(`Error creating reimagined story: ${err.message}`);
    } finally {
      setLoadingBlueprint(false);
    }
  };

  const handleSurpriseGenerate = async () => {
    setLoadingBlueprint(true);
    try {
      const story = await api.generateSurpriseStory();
      setCurrentStory(story);
      setCurrentClassic(null);
      setActiveTab("blueprint");
    } catch (err) {
      alert(`Error generating surprise story: ${err.message}`);
    } finally {
      setLoadingBlueprint(false);
    }
  };

  const handleSelectStoryFromLibrary = async (story) => {
    try {
      const details = await api.getStory(story.id);
      setCurrentStory(details);
      setCurrentClassic(null);

      if (details.status === "Draft") {
        setActiveTab("blueprint");
      } else {
        setActiveTab("reader");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectClassic = async (book) => {
    try {
      const fullBook = await api.getClassicBook(book.id);
      setCurrentClassic(fullBook);
      setCurrentStory(null);
      setActiveTab("reader");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="app-container">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        settings={settings}
        devMode={devMode}
        setDevMode={setDevMode}
        openSettings={() => setShowSettingsModal(true)}
      />

      <main className="main-content">
        {/* TAB 1: DISCOVER / HOME */}
        {activeTab === "discover" && (
          <div>
            <section className="hero-section">
              <h1 className="hero-title">AIStoryVerse</h1>
              <p className="hero-subtitle">
                Generate original AI novels chapter-by-chapter, explore public domain classics, create futuristic retellings, and build your personal reading universe.
              </p>

              <div style={{ display: "flex", justifyContent: "center", gap: "1rem", flexWrap: "wrap" }}>
                <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
                  <Sparkles size={18} /> Create AI Novel
                </button>
                <button className="btn btn-secondary" onClick={() => setActiveTab("surprise")}>
                  <Dices size={18} /> Surprise Me
                </button>
                <button className="btn btn-secondary" onClick={() => setActiveTab("classics")}>
                  <BookOpen size={18} /> Explore Classics
                </button>
              </div>
            </section>

            {/* Feature Cards Grid */}
            <div className="grid-3" style={{ marginTop: "2rem" }}>
              <div className="glass-card" onClick={() => setShowCreateModal(true)} style={{ cursor: "pointer" }}>
                <div style={{ width: 48, height: 48, borderRadius: "var(--radius-md)", background: "rgba(139, 92, 246, 0.15)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--accent-purple)", marginBottom: "1rem" }}>
                  <Wand2 size={24} />
                </div>
                <h3 style={{ fontFamily: "var(--font-heading)", fontSize: "1.3rem", marginBottom: "0.5rem" }}>Structured AI Blueprints</h3>
                <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>
                  Step 1 creates a detailed world blueprint, character profiles, and plot roadmap before writing Chapter 1.
                </p>
              </div>

              <div className="glass-card" onClick={() => setActiveTab("reimagine")} style={{ cursor: "pointer" }}>
                <div style={{ width: 48, height: 48, borderRadius: "var(--radius-md)", background: "rgba(245, 158, 11, 0.15)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--accent-gold)", marginBottom: "1rem" }}>
                  <Sparkles size={24} />
                </div>
                <h3 style={{ fontFamily: "var(--font-heading)", fontSize: "1.3rem", marginBottom: "0.5rem" }}>AI Reimagined Classics</h3>
                <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>
                  Transform timeless classics like Frankenstein, Alice in Wonderland, and Sherlock Holmes with sci-fi, cyberpunk, or alternate endings.
                </p>
              </div>

              <div className="glass-card" onClick={() => setActiveTab("library")} style={{ cursor: "pointer" }}>
                <div style={{ width: 48, height: 48, borderRadius: "var(--radius-md)", background: "rgba(6, 182, 212, 0.15)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--accent-cyan)", marginBottom: "1rem" }}>
                  <Library size={24} />
                </div>
                <h3 style={{ fontFamily: "var(--font-heading)", fontSize: "1.3rem", marginBottom: "0.5rem" }}>Persistent Story Memory</h3>
                <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>
                  Background Story Memory tracks character states, locations, and timeline to maintain 100% narrative consistency across chapters.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: CREATE NOVEL */}
        {activeTab === "create" && (
          <div style={{ textAlign: "center", padding: "3rem" }}>
            <h2 style={{ fontFamily: "var(--font-heading)", fontSize: "2rem", marginBottom: "1rem" }}>Ready to create an original AI story?</h2>
            <p style={{ color: "var(--text-secondary)", marginBottom: "2rem" }}>Configure genre, tone, style, and character options in the generator wizard.</p>
            <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
              <Sparkles size={20} /> Open Novel Generator Wizard
            </button>
          </div>
        )}

        {/* TAB 3: BLUEPRINT VIEWER */}
        {activeTab === "blueprint" && (
          <BlueprintViewer
            story={currentStory}
            onAccept={handleAcceptBlueprint}
            onReject={handleRejectBlueprint}
            loadingAccept={loadingAccept}
            loadingReject={loadingReject}
          />
        )}

        {/* TAB 4: READER VIEW */}
        {activeTab === "reader" && (
          <ReaderView
            story={currentStory}
            classicBook={currentClassic}
            onBack={() => setActiveTab("library")}
            onGenerateNext={handleGenerateNextChapter}
            loadingNext={loadingNext}
          />
        )}

        {/* TAB 5: SURPRISE ME */}
        {activeTab === "surprise" && (
          <SurpriseMeView
            onSurpriseComplete={handleSurpriseGenerate}
            loading={loadingBlueprint}
          />
        )}

        {/* TAB 6: CLASSIC COLLECTION */}
        {activeTab === "classics" && (
          <ClassicsView
            onSelectClassic={handleSelectClassic}
            onReimagineClassic={(book) => {
              setCurrentClassic(book);
              setActiveTab("reimagine");
            }}
          />
        )}

        {/* TAB 7: REIMAGINE STUDIO */}
        {activeTab === "reimagine" && (
          <ReimagineStudio
            initialBook={currentClassic}
            onReimagineComplete={handleReimagineSubmit}
            loading={loadingBlueprint}
          />
        )}

        {/* TAB 8: MY LIBRARY */}
        {activeTab === "library" && (
          <LibraryView
            onSelectStory={handleSelectStoryFromLibrary}
            onCreateNew={() => setShowCreateModal(true)}
          />
        )}
      </main>

      {/* Modals & Drawers */}
      <OriginalGeneratorModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onGenerate={handleGenerateOriginalBlueprint}
        loading={loadingBlueprint}
      />

      <SettingsModal
        isOpen={showSettingsModal}
        onClose={() => setShowSettingsModal(false)}
        settings={settings}
        onSettingsUpdated={loadSettings}
      />

      <DevToolsDrawer
        isOpen={devMode}
        onClose={() => setDevMode(false)}
        story={currentStory}
      />
    </div>
  );
}
