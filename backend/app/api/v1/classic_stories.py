from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.db.database import get_db
from app.db.models import ClassicBook
from app.schemas.classic import ClassicBookResponse

router = APIRouter(prefix="/classics", tags=["Classic Collection"])

@router.get("", response_model=List[ClassicBookResponse])
async def list_classic_books(
    genre: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(ClassicBook).options(selectinload(ClassicBook.chapters))
    if search:
        query = query.filter(
            (ClassicBook.title.ilike(f"%{search}%")) | (ClassicBook.author.ilike(f"%{search}%"))
        )
    result = await db.execute(query)
    books = result.scalars().all()

    if genre:
        books = [b for b in books if any(genre.lower() in g.lower() for g in (b.genres or []))]

    return books

@router.get("/{book_id}", response_model=ClassicBookResponse)
async def get_classic_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ClassicBook).options(selectinload(ClassicBook.chapters)).filter(ClassicBook.id == book_id)
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Classic book not found")
    return book
