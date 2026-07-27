# AIStoryVerse – AI Novel & Story Platform

**AIStoryVerse** is an enterprise-ready, full-stack AI-powered novel and story platform. Powered by **Google Gemini AI** (with an offline mock fallback engine), AIStoryVerse enables users to generate original novels chapter-by-chapter with persistent background **Story Memory**, read curated classic literature, create AI-reimagined classics, discover random stories via a multi-vector "Surprise Me" engine, and manage a personal reading library.

---

## 🌟 Key Features

1. **AI Original Novels & Draft Rejection**:
   - **Step 1 Blueprinting**: Generates a structured JSON story blueprint (World Setting, Character Roster, Main Conflict, Plot Roadmap, Est. Chapters, Ending Style).
   - **Step 2 Chapter 1 Generation**: Writes full cinematic chapters with realistic dialogue and cliffhangers.
   - **Draft State & Re-Roll**: Blueprints start in `Draft` state so readers can review the concept. Rejecting a blueprint re-rolls a fresh story concept using saved user settings.

2. **Persistent Background Story Memory**:
   - Maintains long-term narrative consistency across chapters by quietly updating character states, relationships, locations, timeline, important events, and objects after every chapter.

3. **Classic Literature Collection**:
   - Curated public-domain masterpieces (*Alice's Adventures in Wonderland*, *The Time Machine*, *The Adventures of Sherlock Holmes*, *Pride and Prejudice*).

4. **AI Reimagined Studio**:
   - Reimagines classic public-domain books into alternate endings, futuristic space operas, cyberpunk retellings, villain POVs, and modern adaptations.

5. **Multi-Vector "Surprise Me" Engine**:
   - Randomized combination of Genre, Theme, World, Character Archetype, Conflict, Tone, Narration POV, and Ending Style.

6. **Immersive Reader Experience**:
   - Reader Themes: Dark Mode, Light Mode, Sepia Mode, Midnight Navy.
   - Typography Controls: Font size slider (14px - 28px) & Serif / Sans-serif toggles.
   - Reading progress bar, estimated reading time, bookmarks with user notes.

7. **Developer Mode**:
   - Toggleable inspection drawer for viewing live **Story Memory** state and **GenerationLog** prompt audit history.

8. **Enterprise Production Architecture**:
   - **Alembic Database Migrations**: Full schema migration tracking.
   - **Database Independence**: Zero-config SQLite for development; seamless switch to PostgreSQL via `DATABASE_URL` in `.env`.
   - **Centralized Logging & Exception Handling**: Formatted structured logging and masked JSON error responses.

---

## 🏗️ Architecture & Technology Stack

- **Frontend**: React (SPA), Vite, Vanilla CSS Design System with CSS Custom Properties, Lucide Icons.
- **Backend Framework**: Python 3.10+, FastAPI, Pydantic v2 & `pydantic-settings`.
- **Database & ORM**: SQLAlchemy 2.0 (Async Engine), `aiosqlite` (Dev) / `asyncpg` (Production PostgreSQL), Alembic.
- **AI Layer**: Google Gemini API via dedicated `gemini_service.py`, `prompt_builder.py`, `ai_service.py`, and `mock_ai_engine.py`.

---

## 📁 Project Folder Structure

```
aistoryverse/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_initial_schema.py   # Migration scripts
│   │   └── env.py                       # Migration environment
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── original_stories.py  # Story generation & blueprint routes
│   │   │       ├── classic_stories.py   # Public domain classics routes
│   │   │       ├── reimagined_stories.py# Classic reimagining routes
│   │   │       ├── surprise_me.py       # Multi-vector randomizer routes
│   │   │       ├── library.py           # Library, search, bookmarks, dev logs
│   │   │       ├── analytics.py         # Reading sessions & statistics
│   │   │       └── settings.py          # Gemini API key & model status
│   │   ├── core/
│   │   │   ├── config.py                # Pydantic Settings & environment variables
│   │   │   ├── logging_config.py        # Centralized structured logger
│   │   │   └── exceptions.py            # Global exception handlers
│   │   ├── db/
│   │   │   ├── database.py              # Async SQLAlchemy engine
│   │   │   └── models.py                # ORM models (Story, Chapter, Bookmark, etc.)
│   │   ├── schemas/                     # Request/Response Pydantic models
│   │   ├── services/
│   │   │   ├── gemini_service.py        # Google Gemini API client
│   │   │   ├── prompt_builder.py        # Prompt construction templates
│   │   │   ├── ai_service.py            # High-level story coordinator
│   │   │   └── mock_ai_engine.py        # Offline procedural fallback engine
│   │   └── main.py                      # FastAPI app entrypoint & middleware
│   ├── scripts/
│   │   └── seed_classics.py             # Pre-seeds classic literature into DB
│   ├── tests/                           # Pytest automated test suite
│   ├── alembic.ini                      # Migration configuration
│   ├── requirements.txt                 # Backend dependencies
│   ├── .env.example                     # Environment template
│   └── .env                             # Local environment settings
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js                # Frontend API client
│   │   ├── components/                  # React UI components
│   │   ├── styles/
│   │   │   └── index.css                # CSS Design system & theme tokens
│   │   ├── App.jsx                      # Main app router & state manager
│   │   └── main.jsx                     # Vite entrypoint
│   ├── package.json
│   └── vite.config.js
└── README.md                            # Production documentation
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` inside `backend/`:

| Variable | Default Value | Description |
|---|---|---|
| `PROJECT_NAME` | `AIStoryVerse` | Application Name |
| `DATABASE_URL` | `sqlite+aiosqlite:///./ai_storyverse.db` | Database connection URI (`sqlite+aiosqlite` for Dev, `postgresql+asyncpg` for Prod) |
| `GEMINI_API_KEY` | `""` | Google Gemini API Key (If blank, uses built-in Mock Engine) |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Central Gemini Model Name |
| `DEBUG` | `True` | Debug Mode Flag |
| `ALLOWED_ORIGINS` | `["http://localhost:5173", ...]` | Allowed CORS Origins |
| `SECRET_KEY` | `super-secret-key...` | Security Secret Key |

---

## 🚀 Installation & Local Execution

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & NPM

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Database Migrations & Pre-seeding
```bash
# Run Alembic migrations
alembic upgrade head

# Seed public domain classic books
python -m scripts.seed_classics
```

### 4. Running Backend Server
```bash
python -m uvicorn app.main:app --reload --port 8000
```
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Frontend Setup & Execution
```bash
cd ../frontend
npm install
npm run dev
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## 🔮 Future Roadmap

1. **User Authentication & Authorization**:
   - JWT Auth (Registration, Login, Password Hashing, Refresh Tokens).
   - User Profiles & Personalized Libraries (`user_id` fields are pre-configured in models).
2. **AI Cover Art Generation**:
   - Automatic story cover generation using Imagen / Gemini Multimodal.
3. **AI Audiobook Synthesis**:
   - Chapter voice narration using Text-to-Speech APIs.
4. **Community Features**:
   - Story Ratings, Public Comments, Social Story Sharing & Author Showcases.
