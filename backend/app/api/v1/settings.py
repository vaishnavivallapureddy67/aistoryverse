from fastapi import APIRouter
from pydantic import BaseModel
from app.core.config import settings
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/settings", tags=["System Settings"])

class SystemSettingsResponse(BaseModel):
    project_name: str
    gemini_model: str
    has_api_key: bool
    mode: str # "Live Gemini AI" or "Offline Mock AI Engine"

class ApiKeyUpdateRequest(BaseModel):
    api_key: str

@router.get("", response_model=SystemSettingsResponse)
async def get_system_settings():
    has_key = gemini_service.is_available()
    return {
        "project_name": settings.PROJECT_NAME,
        "gemini_model": settings.GEMINI_MODEL,
        "has_api_key": has_key,
        "mode": "Live Google Gemini AI" if has_key else "Offline Mock AI Engine"
    }

@router.post("/api-key")
async def update_api_key(data: ApiKeyUpdateRequest):
    key = data.api_key.strip()
    settings.GEMINI_API_KEY = key
    gemini_service.api_key = key
    has_key = gemini_service.is_available()
    return {
        "status": "success",
        "has_api_key": has_key,
        "mode": "Live Google Gemini AI" if has_key else "Offline Mock AI Engine"
    }
