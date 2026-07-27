from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClassicChapterResponse(BaseModel):
    id: int
    classic_book_id: int
    chapter_number: int
    title: str
    content: str
    word_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class ClassicBookResponse(BaseModel):
    id: int
    title: str
    author: str
    cover_image: Optional[str] = None
    description: str
    genres: List[str] = []
    publication_year: Optional[int] = None
    chapters_count: int
    created_at: datetime
    chapters: List[ClassicChapterResponse] = []

    class Config:
        from_attributes = True
