import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    db_exception_handler,
    global_exception_handler
)
from app.db.database import init_db
from scripts.seed_classics import seed
from app.api.v1.original_stories import router as original_router
from app.api.v1.classic_stories import router as classic_router
from app.api.v1.reimagined_stories import router as reimagined_router
from app.api.v1.surprise_me import router as surprise_router
from app.api.v1.library import router as library_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.settings import router as settings_router

setup_logging()
logger = logging.getLogger("ai_storyverse.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Server Starting: {settings.PROJECT_NAME} (Model: {settings.GEMINI_MODEL})")
    logger.info(f"Database Engine initialized for URL: {settings.DATABASE_URL.split('@')[-1]}")
    await init_db()
    try:
        await seed()
    except Exception as e:
        logger.warning(f"Classics seed check notice: {e}")
    yield
    logger.info(f"Server Shutting Down: {settings.PROJECT_NAME}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Novel & Story Platform API (Google Gemini AI)",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware using settings.ALLOWED_ORIGINS
allowed_origins = settings.ALLOWED_ORIGINS if isinstance(settings.ALLOWED_ORIGINS, list) else [settings.ALLOWED_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Audit Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} ({duration_ms}ms)")
    return response

# Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, db_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# API v1 Routers
app.include_router(original_router, prefix="/api/v1")
app.include_router(classic_router, prefix="/api/v1")
app.include_router(reimagined_router, prefix="/api/v1")
app.include_router(surprise_router, prefix="/api/v1")
app.include_router(library_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "gemini_model": settings.GEMINI_MODEL,
        "docs": "/docs"
    }
