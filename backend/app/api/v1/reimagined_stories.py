from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models import ClassicBook, Story
from app.schemas.reimagined import ReimagineRequest
from app.schemas.story import StoryResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/reimagined", tags=["AI Reimagined Stories"])

@router.post("/create", response_model=StoryResponse)
async def create_reimagined_story(
    data: ReimagineRequest,
    db: AsyncSession = Depends(get_db)
):
    # Fetch classic book
    result = await db.execute(select(ClassicBook).filter(ClassicBook.id == data.classic_book_id))
    classic = result.scalar_one_or_none()
    if not classic:
        raise HTTPException(status_code=404, detail="Classic book not found")

    story = await ai_service.create_reimagined_story(
        db=db,
        classic_title=classic.title,
        classic_author=classic.author,
        classic_summary=classic.description,
        transformation_type=data.transformation_type,
        twist_instructions=data.twist_instructions,
        classic_id=classic.id
    )

    res = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story.id)
    )
    return res.scalar_one()
