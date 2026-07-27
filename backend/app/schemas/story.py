from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class StoryGenerationSettings(BaseModel):
    genre: str = "Fantasy"
    tone: str = "Immersive"
    style: str = "Descriptive"
    difficulty: str = "Intermediate"
    length: str = "Medium" # Short, Medium, Long, Epic
    character_name: Optional[str] = None
    custom_prompt: Optional[str] = None

class StoryBlueprintCreate(BaseModel):
    settings: StoryGenerationSettings

class CharacterProfile(BaseModel):
    name: str
    archetype: str
    personality: str
    goals: str
    relationships: str

class StoryBlueprint(BaseModel):
    title: str
    genre: str
    theme: str
    world_setting: str
    time_period: str
    main_characters: List[CharacterProfile]
    main_conflict: str
    story_goal: str
    plot_outline: List[Dict[str, Any]]
    estimated_chapters: int
    ending_style: str
    tags: List[str]

class StoryMemory(BaseModel):
    characters: List[Dict[str, Any]] = Field(default_factory=list)
    relationships: List[Dict[str, Any]] = Field(default_factory=list)
    locations: List[Dict[str, Any]] = Field(default_factory=list)
    timeline: List[Dict[str, Any]] = Field(default_factory=list)
    important_events: List[Dict[str, Any]] = Field(default_factory=list)
    objects: List[Dict[str, Any]] = Field(default_factory=list)
    overall_summary: str = ""

class ChapterResponse(BaseModel):
    id: str
    story_id: str
    chapter_number: int
    title: str
    content: str
    summary: Optional[str] = None
    word_count: int
    estimated_reading_time_min: int
    created_at: datetime

    class Config:
        from_attributes = True

class StoryResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    title: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    genre: str
    tags: List[str] = Field(default_factory=list)
    blueprint: Optional[Dict[str, Any]] = None
    version_number: int
    blueprint_version: str
    status: str
    generation_settings: Optional[Dict[str, Any]] = None
    story_memory: Optional[Dict[str, Any]] = None
    views: int
    times_read: int
    chapters_generated: int
    total_words: int
    last_generated_at: Optional[datetime] = None
    is_classic: bool
    is_reimagined: bool
    original_classic_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    chapters: List[ChapterResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

class StoryStatusUpdate(BaseModel):
    status: str # Draft, Generating, Reading, Paused, Completed, Abandoned
