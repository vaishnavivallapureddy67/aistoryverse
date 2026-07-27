import uuid
from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, Boolean, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Story(Base):
    __tablename__ = "stories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    genre: Mapped[str] = mapped_column(String(100), nullable=False, default="Fantasy")
    tags: Mapped[dict | list | None] = mapped_column(JSON, nullable=True, default=list)
    
    # Blueprint & Settings
    blueprint: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    blueprint_version: Mapped[str] = mapped_column(String(50), default="v1.0")
    generation_settings: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    # Lifecycle Status: Draft, Generating, Reading, Paused, Completed, Abandoned
    status: Mapped[str] = mapped_column(String(50), default="Draft", index=True)
    
    # Persistent Background Story Memory (Internal AI State)
    story_memory: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Analytics & Statistics
    views: Mapped[int] = mapped_column(Integer, default=0)
    times_read: Mapped[int] = mapped_column(Integer, default=0)
    chapters_generated: Mapped[int] = mapped_column(Integer, default=0)
    total_words: Mapped[int] = mapped_column(Integer, default=0)
    last_generated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Reimagining & Classic links
    is_classic: Mapped[bool] = mapped_column(Boolean, default=False)
    is_reimagined: Mapped[bool] = mapped_column(Boolean, default=False)
    original_classic_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chapters: Mapped[list["Chapter"]] = relationship("Chapter", back_populates="story", cascade="all, delete-orphan", order_by="Chapter.chapter_number")
    versions: Mapped[list["StoryVersion"]] = relationship("StoryVersion", back_populates="story", cascade="all, delete-orphan")
    sessions: Mapped[list["StorySession"]] = relationship("StorySession", back_populates="story", cascade="all, delete-orphan")
    logs: Mapped[list["GenerationLog"]] = relationship("GenerationLog", back_populates="story", cascade="all, delete-orphan")

class StoryVersion(Base):
    __tablename__ = "story_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    story_id: Mapped[str] = mapped_column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    blueprint: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    chapter_1_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    story: Mapped["Story"] = relationship("Story", back_populates="versions")

class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    story_id: Mapped[str] = mapped_column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    estimated_reading_time_min: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    story: Mapped["Story"] = relationship("Story", back_populates="chapters")

class ClassicBook(Base):
    __tablename__ = "classic_books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    cover_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    genres: Mapped[dict | list | None] = mapped_column(JSON, nullable=True, default=list)
    publication_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chapters_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    chapters: Mapped[list["ClassicChapter"]] = relationship("ClassicChapter", back_populates="classic_book", cascade="all, delete-orphan", order_by="ClassicChapter.chapter_number")

class ClassicChapter(Base):
    __tablename__ = "classic_chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    classic_book_id: Mapped[int] = mapped_column(Integer, ForeignKey("classic_books.id", ondelete="CASCADE"), nullable=False)
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    classic_book: Mapped["ClassicBook"] = relationship("ClassicBook", back_populates="chapters")

class UserReadingProgress(Base):
    __tablename__ = "user_reading_progress"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    story_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=True)
    classic_book_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("classic_books.id", ondelete="CASCADE"), nullable=True)
    
    last_read_chapter: Mapped[int] = mapped_column(Integer, default=1)
    scroll_position: Mapped[float] = mapped_column(Float, default=0.0)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    is_saved: Mapped[bool] = mapped_column(Boolean, default=True)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    story_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=True)
    classic_book_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("classic_books.id", ondelete="CASCADE"), nullable=True)
    
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    position_percent: Mapped[float] = mapped_column(Float, default=0.0)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class StorySession(Base):
    __tablename__ = "story_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    story_id: Mapped[str] = mapped_column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_read_chapter: Mapped[int] = mapped_column(Integer, default=1)
    reading_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    device_info: Mapped[str | None] = mapped_column(String(255), nullable=True)

    story: Mapped["Story"] = relationship("Story", back_populates="sessions")

class GenerationLog(Base):
    __tablename__ = "generation_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    story_id: Mapped[str] = mapped_column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prompt_type: Mapped[str] = mapped_column(String(50), nullable=False) # blueprint, chapter, memory, reimagine
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    story: Mapped["Story"] = relationship("Story", back_populates="logs")
