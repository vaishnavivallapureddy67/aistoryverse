from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReadingProgressCreate(BaseModel):
    story_id: Optional[str] = None
    classic_book_id: Optional[int] = None
    last_read_chapter: int = 1
    scroll_position: float = 0.0

class BookmarkCreate(BaseModel):
    story_id: Optional[str] = None
    classic_book_id: Optional[int] = None
    chapter_number: int
    position_percent: float = 0.0
    note: Optional[str] = None

class BookmarkResponse(BaseModel):
    id: str
    story_id: Optional[str] = None
    classic_book_id: Optional[int] = None
    chapter_number: int
    position_percent: float
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReadingSessionCreate(BaseModel):
    story_id: str
    last_read_chapter: int = 1
    reading_time_seconds: int = 0
    device_info: Optional[str] = None
