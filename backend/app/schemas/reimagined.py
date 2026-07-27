from pydantic import BaseModel
from typing import Optional

class ReimagineRequest(BaseModel):
    classic_book_id: int
    transformation_type: str # Alternate Ending, Futuristic Sci-Fi, Cyberpunk, Villain POV, Modern Adaptation, Fantasy Retelling, What-If
    twist_instructions: Optional[str] = None
    character_name: Optional[str] = None
    tone: str = "Immersive"
    difficulty: str = "Intermediate"
