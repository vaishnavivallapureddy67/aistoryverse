from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.database import get_db
from app.db.models import StorySession, Story, Chapter
from app.schemas.user_progress import ReadingSessionCreate

router = APIRouter(prefix="/analytics", tags=["Analytics & Sessions"])

@router.post("/session/start")
async def start_reading_session(
    data: ReadingSessionCreate,
    db: AsyncSession = Depends(get_db)
):
    session = StorySession(
        story_id=data.story_id,
        started_at=datetime.utcnow(),
        last_read_chapter=data.last_read_chapter,
        device_info=data.device_info
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return {"session_id": session.id, "status": "started"}

@router.post("/session/{session_id}/end")
async def end_reading_session(
    session_id: str,
    data: ReadingSessionCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(StorySession).filter(StorySession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.ended_at = datetime.utcnow()
    session.last_read_chapter = data.last_read_chapter
    session.reading_time_seconds = data.reading_time_seconds

    # Update story times_read count
    st_res = await db.execute(select(Story).filter(Story.id == session.story_id))
    story = st_res.scalar_one_or_none()
    if story:
        story.times_read = (story.times_read or 0) + 1

    await db.commit()
    return {"session_id": session.id, "reading_time_seconds": session.reading_time_seconds, "status": "completed"}

@router.get("/summary")
async def get_overall_reading_stats(
    db: AsyncSession = Depends(get_db)
):
    stories_res = await db.execute(select(func.count(Story.id)))
    total_stories = stories_res.scalar() or 0

    chapters_res = await db.execute(select(func.count(Chapter.id)))
    total_chapters = chapters_res.scalar() or 0

    words_res = await db.execute(select(func.sum(Story.total_words)))
    total_words = words_res.scalar() or 0

    sessions_res = await db.execute(select(func.sum(StorySession.reading_time_seconds)))
    total_reading_time = sessions_res.scalar() or 0

    return {
        "total_stories": total_stories,
        "total_chapters": total_chapters,
        "total_words": total_words,
        "total_reading_time_minutes": round(total_reading_time / 60, 1)
    }
