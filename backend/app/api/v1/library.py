from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.db.database import get_db
from app.db.models import Story, UserReadingProgress, Bookmark, GenerationLog
from app.schemas.story import StoryResponse
from app.schemas.user_progress import BookmarkCreate, BookmarkResponse, ReadingProgressCreate

router = APIRouter(prefix="/library", tags=["Story Library"])

@router.get("/stories", response_model=List[StoryResponse])
async def list_library_stories(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    is_favorite: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Story).options(selectinload(Story.chapters)).order_by(Story.updated_at.desc())
    
    if status:
        query = query.filter(Story.status == status)
    if search:
        query = query.filter((Story.title.ilike(f"%{search}%")) | (Story.summary.ilike(f"%{search}%")))
    if genre:
        query = query.filter(Story.genre == genre)

    result = await db.execute(query)
    stories = result.scalars().all()
    return stories

@router.delete("/stories/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Story).filter(Story.id == story_id))
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    await db.delete(story)
    await db.commit()
    return None

@router.post("/bookmarks", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
async def add_bookmark(
    data: BookmarkCreate,
    db: AsyncSession = Depends(get_db)
):
    bookmark = Bookmark(
        story_id=data.story_id,
        classic_book_id=data.classic_book_id,
        chapter_number=data.chapter_number,
        position_percent=data.position_percent,
        note=data.note
    )
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return bookmark

@router.get("/bookmarks", response_model=List[BookmarkResponse])
async def list_bookmarks(
    story_id: Optional[str] = Query(None),
    classic_book_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Bookmark).order_by(Bookmark.created_at.desc())
    if story_id:
        query = query.filter(Bookmark.story_id == story_id)
    if classic_book_id:
        query = query.filter(Bookmark.classic_book_id == classic_book_id)

    result = await db.execute(query)
    return result.scalars().all()

@router.get("/stories/{story_id}/logs")
async def get_story_generation_logs(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Developer Mode: Returns prompt history logs for debugging story generation."""
    result = await db.execute(
        select(GenerationLog).filter(GenerationLog.story_id == story_id).order_by(GenerationLog.created_at.desc())
    )
    logs = result.scalars().all()
    return [
        {
            "id": l.id,
            "chapter_number": l.chapter_number,
            "prompt_type": l.prompt_type,
            "prompt_text": l.prompt_text,
            "response_text": l.response_text,
            "model_name": l.model_name,
            "created_at": l.created_at
        }
        for l in logs
    ]
