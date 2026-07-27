# Production Deployment Guide: AIStoryVerse (Vercel + Render + Neon PostgreSQL)

This guide provides a step-by-step checklist to deploy **AIStoryVerse** to production using **Vercel** for the React Frontend, **Render** for the FastAPI Backend, and **Neon** for the PostgreSQL Database.

---

## 📋 Deployment Overview Matrix

| Component | Host / Provider | Build Command | Start Command | Config File |
|---|---|---|---|---|
| **Frontend** | Vercel | `npm run build` | Static Dist | `frontend/vercel.json` |
| **Backend** | Render | `pip install -r requirements.txt && alembic upgrade head` | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | `backend/render.yaml` |
| **Database** | Neon PostgreSQL | Auto-provisioned | Persistent PostgreSQL | `DATABASE_URL` in Render |

---

## Step 1: Push Code to GitHub

1. Create a new GitHub repository named `aistoryverse`.
2. Initialize and push your project code:
```bash
git init
git add .
git commit -m "Production deployment ready"
git branch -M main
git remote add origin https://github.com/your-username/aistoryverse.git
git push -u origin main
```

---

## Step 2: Set Up Neon PostgreSQL Database

1. Sign up / Log in to [Neon.tech](https://neon.tech).
2. Create a new Project named `aistoryverse-db`.
3. Copy your Connection String from the Neon dashboard:
   - Example format: `postgres://alex:secretpass@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require`
4. Note: AIStoryVerse automatically translates `postgres://` or `postgresql://` into `postgresql+asyncpg://` internally.

---

## Step 3: Deploy Backend to Render

1. Sign up / Log in to [Render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository (`aistoryverse`).
4. Select the `backend` directory as the Root Directory (or use `render.yaml`).
5. Configure Environment Variables in Render:

| Environment Variable | Recommended Value |
|---|---|
| `PROJECT_NAME` | `AIStoryVerse` |
| `DATABASE_URL` | *Paste your Neon PostgreSQL Connection String* |
| `GEMINI_API_KEY` | *Paste your Google AI Studio Gemini API Key* |
| `GEMINI_MODEL` | `gemini-1.5-flash` |
| `DEBUG` | `False` |
| `ALLOWED_ORIGINS` | `["https://aistoryverse.vercel.app"]` (Update with your actual Vercel URL) |
| `SECRET_KEY` | *Generate a random secure key* |

6. Click **Deploy Web Service**.
7. Render will build the environment, run `alembic upgrade head`, seed classic books, and start the FastAPI service.
8. Copy your Render Backend URL (e.g., `https://aistoryverse-backend.onrender.com`).

---

## Step 4: Deploy Frontend to Vercel

1. Sign up / Log in to [Vercel.com](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import your GitHub repository (`aistoryverse`).
4. Set the **Root Directory** to `frontend`.
5. Under **Environment Variables**, add:

| Key | Value |
|---|---|
| `VITE_BACKEND_URL` | `https://aistoryverse-backend.onrender.com/api/v1` |

6. Click **Deploy**.
7. Vercel will build the React SPA bundle and assign your live production link (e.g. `https://aistoryverse.vercel.app`).

---

## Step 5: Post-Deployment CORS Update

1. Once Vercel finishes deploying, copy your live frontend domain (e.g., `https://aistoryverse.vercel.app`).
2. Go back to Render Dashboard -> Environment -> Update `ALLOWED_ORIGINS` to:
   ```json
   ["https://aistoryverse.vercel.app"]
   ```
3. Save changes in Render to trigger a zero-downtime reload.

---

## 🔍 Verification Checklist

- [ ] Vercel Frontend loads cleanly without console errors.
- [ ] Backend status check returns `200 OK` at `https://aistoryverse-backend.onrender.com/docs`.
- [ ] Original story blueprint generation works.
- [ ] Background Story Memory updates correctly in Neon PostgreSQL.
- [ ] Classics library loads pre-seeded books.
- [ ] Reimagined studio successfully constructs reimagined concepts.
