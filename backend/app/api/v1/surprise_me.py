import random
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models import Story
from app.schemas.story import StoryResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/surprise-me", tags=["Surprise Me Generator"])

GENRES = ["Cyberpunk", "Dark Fantasy", "Space Opera", "Gothic Mystery", "Cozy Romance", "High Fantasy", "Noir Detective", "Time Travel"]
THEMES = ["Identity & Memory", "The Price of Ambition", "Forbidden Knowledge", "Redemption across Stars", "Secrets of the Past", "Artificial Consciousness"]
WORLDS = ["A floating island sky-city", "Subterranean neon metropolis", "Post-apocalyptic overgrown jungle", "Deep space mining colony", "Victorian steampunk academy"]
ARCHETYPES = ["Reluctant Rogue", "Ambitious Scholar", "Exiled Guard", "Cybernetic Hacker", "Disillusioned Detective", "Royal Outcast"]
CONFLICTS = ["An ancient artifact begins awakening", "A shadowy syndicate demands double-cross", "A missing heir resurfaces with strange powers", "Time paradox loop threatening reality"]
TONES = ["Atmospheric & Suspenseful", "Witty & Fast-Paced", "Dark & Whimsical", "Epic & Cinematic", "Poetic & Melancholic"]
NARRATION_POVS = ["First Person ('I')", "Third Person Limited ('He/She')", "Third Person Omniscient"]
ENDING_STYLES = ["Mind-Bending Twist Ending", "Bittersweet Resolution", "Triumphant Victory", "Unsettling Mystery"]

@router.get("/random-prompt")
async def generate_random_prompt_vectors():
    """Generates a randomized combination of story building blocks."""
    return {
        "genre": random.choice(GENRES),
        "theme": random.choice(THEMES),
        "world": random.choice(WORLDS),
        "character_archetype": random.choice(ARCHETYPES),
        "conflict": random.choice(CONFLICTS),
        "tone": random.choice(TONES),
        "narration_pov": random.choice(NARRATION_POVS),
        "ending_style": random.choice(ENDING_STYLES)
    }

@router.post("/generate", response_model=StoryResponse)
async def generate_surprise_story(
    db: AsyncSession = Depends(get_db)
):
    """Instantly generates an original story blueprint using randomized vectors."""
    vectors = {
        "genre": random.choice(GENRES),
        "theme": random.choice(THEMES),
        "world": random.choice(WORLDS),
        "character_name": f"{random.choice(ARCHETYPES).split()[-1]} {random.choice(['Vane', 'Kovacs', 'Sinclair', 'Thorne', 'Vali'])}",
        "custom_prompt": f"Theme: {random.choice(THEMES)}. World: {random.choice(WORLDS)}. Conflict: {random.choice(CONFLICTS)}. Narration: {random.choice(NARRATION_POVS)}. Ending: {random.choice(ENDING_STYLES)}.",
        "tone": random.choice(TONES),
        "style": "Cinematic & Vivid",
        "difficulty": "Intermediate",
        "length": "Medium"
    }

    story = await ai_service.create_story_blueprint(db=db, generation_settings=vectors)
    
    res = await db.execute(
        select(Story).options(selectinload(Story.chapters)).filter(Story.id == story.id)
    )
    return res.scalar_one()
