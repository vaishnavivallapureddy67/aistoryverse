import json
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings

DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"

class Settings(BaseSettings):
    PROJECT_NAME: str = "AIStoryVerse"
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_storyverse.db"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = DEFAULT_GEMINI_MODEL
    DEBUG: bool = True
    ALLOWED_ORIGINS: Union[List[str], str] = ["*"]
    SECRET_KEY: str = "super-secret-production-key-change-in-production"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str) -> str:
        if not v:
            return "sqlite+aiosqlite:///./ai_storyverse.db"
        
        # Convert Neon / Heroku / Render postgres:// or postgresql:// to asyncpg
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://") and not v.startswith("postgresql+asyncpg://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        # asyncpg expects ssl=require instead of sslmode=require
        if "sslmode=" in v:
            v = v.replace("sslmode=", "ssl=")
            
        return v

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Union[List[str], str]) -> List[str]:
        if isinstance(v, str):
            v_trimmed = v.strip()
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                try:
                    return json.loads(v_trimmed)
                except Exception:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
