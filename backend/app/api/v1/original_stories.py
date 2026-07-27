from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models import Story, Chapter
from app.schemas.story import (
    StoryBlueprintCreate,
    StoryResponse,
    ChapterResponse,
    StoryStatusUpdate
)
from app.services.ai_service import ai_service

router = APIRouter(prefix="/stories", tags=["Original Stories"])

@router.post("/blueprint", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
async def create_story_blueprint(
    data: StoryBlueprintCreate,
    db: AsyncSession = Depends(get_db)
):
    """Step 1: Generate a unique story blueprint (Draft status)."""
    story = await ai_service.create_story_blueprint(
        db=db,
        generation_settings=data.settings.model_dump()
    )
    # Reload with chapters
    result = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story.id)
    )
    return result.scalar_one()

@router.post("/{story_id}/accept", response_model=StoryResponse)
async def accept_blueprint_and_start(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Step 2: Accept blueprint (Draft -> Reading) and generate Chapter 1."""
    result = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story_id)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if story.chapters:
        # Chapter 1 already exists
        return story

    story, _ = await ai_service.accept_blueprint_and_generate_chapter_1(db, story)
    
    # Reload
    res = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story_id)
    )
    return res.scalar_one()

@router.post("/{story_id}/reject", response_model=StoryResponse)
async def reject_blueprint_and_regenerate(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Step 4: Reject Chapter 1 / Blueprint. Discards draft and generates a completely new story concept."""
    result = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story_id)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    updated_story = await ai_service.reject_blueprint_and_regenerate(db, story)
    res = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == updated_story.id)
    )
    return res.scalar_one()

@router.post("/{story_id}/next-chapter", response_model=ChapterResponse)
async def generate_next_chapter(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Step 3 & 4: Generate future chapters using background Story Memory."""
    result = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story_id)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    chapter = await ai_service.generate_next_chapter(db, story)
    return chapter

@router.get("/{story_id}", response_model=StoryResponse)
async def get_story_details(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetch story with chapters, blueprint, and statistics."""
    result = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story_id)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    story.views = (story.views or 0) + 1
    await db.commit()
    return story

@router.patch("/{story_id}/status", response_model=StoryResponse)
async def update_story_status(
    story_id: str,
    data: StoryStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update story lifecycle status (Draft, Generating, Reading, Paused, Completed, Abandoned)."""
    result = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story_id)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    story.status = data.status
    await db.commit()
    return story
