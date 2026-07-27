import random
import time
from typing import Dict, Any, List, Optional

class MockAIEngine:
    GENRE_COVERS = {
        "Fantasy": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80",
        "Sci-Fi": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?auto=format&fit=crop&w=600&q=80",
        "Cyberpunk": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=600&q=80",
        "Mystery": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=600&q=80",
        "Romance": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?auto=format&fit=crop&w=600&q=80",
        "Thriller": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=600&q=80",
        "Horror": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?auto=format&fit=crop&w=600&q=80",
        "Historical": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=600&q=80",
        "Classic": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=600&q=80"
    }

    @classmethod
    def get_default_cover(cls, genre: str) -> str:
        for k, v in cls.GENRE_COVERS.items():
            if k.lower() in genre.lower():
                return v
        return cls.GENRE_COVERS["Fantasy"]

    @classmethod
    def generate_blueprint(cls, settings: Dict[str, Any]) -> Dict[str, Any]:
        genre = settings.get("genre", "Fantasy")
        char_name = settings.get("character_name") or "Kaelen Voss"
        custom_prompt = settings.get("custom_prompt", "")
        tone = settings.get("tone", "Immersive")

        title_prefixes = {
            "Fantasy": ["Chronicles of", "The Starlight", "Whispers of", "The Obsidian"],
            "Sci-Fi": ["Echoes of", "Project", "The Nebula", "Beyond"],
            "Cyberpunk": ["Neon", "Neural", "Syndicate", "Cyber"],
            "Mystery": ["The Secret of", "Shadows over", "The Last", "Silent"],
            "Romance": ["Heart of", "Summer at", "The Starlight", "Love in"],
            "Thriller": ["The Vector", "Zero Hour", "The Terminal", "Phantom"]
        }
        title_nouns = ["Aether", "Sovereign", "Horizon", "Paradox", "Citadel", "Requiem", "Protocol", "Enigma"]
        
        pref = random.choice(title_prefixes.get(genre, title_prefixes["Fantasy"]))
        noun = random.choice(title_nouns)
        title = f"{pref} {noun}"

        return {
            "title": title,
            "genre": genre,
            "theme": "The search for truth amidst deceptive illusions and high stakes.",
            "world_setting": f"A vibrant {genre.lower()} realm characterized by rich contrast, ancient lore, and soaring spires.",
            "time_period": "An era of turning tides and technological or mystical revolutions.",
            "main_characters": [
                {
                    "name": char_name,
                    "archetype": "Driven Investigator",
                    "personality": "Determined, inquisitive, prone to taking calculated risks.",
                    "goals": "To uncover the hidden truth behind the sudden disruption.",
                    "relationships": "Tethered to a mysterious informant known only as The Oracle."
                },
                {
                    "name": "Lyra Vane",
                    "archetype": "Enigmatic Ally",
                    "personality": "Sharp-witted, guarded, fiercely loyal once trust is earned.",
                    "goals": "Protect the ancient sanctuary from falling into enemy hands.",
                    "relationships": "Uneasy truce with " + char_name
                }
            ],
            "main_conflict": "A powerful artifact/code sequence has been activated, threatening to unravel the established order.",
            "story_goal": "Neutralize the threat before the lunar eclipse.",
            "plot_outline": [
                {
                    "chapter_number": 1,
                    "chapter_title": "The First Signal",
                    "objective": "Introduce protagonist and the initial anomaly.",
                    "key_elements": ["Midnight discovery", "Cryptic message"]
                },
                {
                    "chapter_number": 2,
                    "chapter_title": "Shadows in the Archive",
                    "objective": "Search for context in ancient records.",
                    "key_elements": ["Hidden vault", "Sudden ambush"]
                },
                {
                    "chapter_number": 3,
                    "chapter_title": "The Sanctuary Threshold",
                    "objective": "Rendezvous with Lyra Vane.",
                    "key_elements": ["Forbidden sanctuary", "Uneasy alliance"]
                },
                {
                    "chapter_number": 4,
                    "chapter_title": "Crossroads of Fate",
                    "objective": "Face the antagonist's lieutenant.",
                    "key_elements": ["High-stakes confrontation", "Shocking revelation"]
                },
                {
                    "chapter_number": 5,
                    "chapter_title": "The Final Reckoning",
                    "objective": "Climactic resolution at the heart of the anomaly.",
                    "key_elements": ["Ultimate sacrifice", "New dawn"]
                }
            ],
            "estimated_chapters": 5,
            "ending_style": "Bittersweet & Inspiring",
            "tags": [genre, tone, "AI Generated", "Epic Adventure"],
            "summary": f"In a world where {genre.lower()} rules, {char_name} discovers a anomaly that changes everything. Joined by unexpected allies, the journey will test resolve and reshape the future."
        }

    @classmethod
    def generate_chapter(
        cls,
        blueprint: Dict[str, Any],
        chapter_number: int,
        story_memory: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        title = blueprint.get("title", "The Legend")
        genre = blueprint.get("genre", "Fantasy")
        chars = blueprint.get("main_characters", [])
        char1 = chars[0]["name"] if chars else "The Hero"
        char2 = chars[1]["name"] if len(chars) > 1 else "The Companion"
        
        outline = blueprint.get("plot_outline", [])
        ch_outline = next((ch for ch in outline if ch.get("chapter_number") == chapter_number), None)
        ch_title = ch_outline.get("chapter_title", f"Chapter {chapter_number}") if ch_outline else f"Chapter {chapter_number}"

        p1 = f"The night sky over the city of {genre} hung heavy with silver mists. {char1} stood atop the observation balcony, watching the amber lanterns flicker in the cold wind. Every instinct honed over years of quiet vigilance screamed that something fundamental had shifted."
        p2 = f'"You shouldn\'t be out here alone," a quiet voice cut through the rustling breeze. {char2} stepped out from the archway shadows, hands folded inside high-collared robes. "The council has already sealed the lower archives. They know what was retrieved from the vault."'
        p3 = f'{char1} turned slowly, pulling out the small, humming cylinder found beneath the central plaza. "Then the council is already too late. Look at the inscriptions—these aren\'t ancient glyphs. They\'re coordinates."'
        p4 = f'A sudden low rumble resonated through the stone floor. Far in the distance, a beam of sapphire light pierced the cloud layer, illuminating the horizon in silent brilliance. Neither spoke for a long moment; the quiet agreement between them was absolute.'
        p5 = f'"If we cross the threshold tonight," {char2} whispered, checking the latch on a side holster, "there will be no turning back when dawn breaks."'
        p6 = f'{char1} tightened the grip on the cylinder, feeling its pulsing warmth beat like a second heart. "Good. Because staying here was never an option." A dark shadow glided across the moonlit roofs toward them...'

        content = f"\n\n".join([p1, p2, p3, p4, p5, p6])
        summary = f"{char1} and {char2} discover coordinates on the mysterious artifact as a sapphire light pierces the horizon."

        return {
            "chapter_number": chapter_number,
            "chapter_title": ch_title,
            "content": content,
            "chapter_summary": summary
        }

    @classmethod
    def update_memory(
        cls,
        existing_memory: Optional[Dict[str, Any]],
        new_chapter_summary: str,
        chapter_number: int
    ) -> Dict[str, Any]:
        mem = existing_memory or {
            "characters": [
                {"name": "Protagonist", "status": "Active", "notes": "Discovered mysterious artifact."}
            ],
            "relationships": [
                {"pair": "Protagonist & Companion", "dynamic": "Developing trust and shared purpose."}
            ],
            "locations": [
                {"name": "Observation Balcony", "description": "High vantage point above mist-shrouded city."}
            ],
            "timeline": [],
            "important_events": [],
            "objects": [
                {"name": "Humming Cylinder", "state": "Emitting coordinate pulses"}
            ],
            "overall_summary": "Story underway."
        }

        mem["timeline"].append({
            "phase": f"Chapter {chapter_number}",
            "event": new_chapter_summary
        })
        mem["important_events"].append(f"Chapter {chapter_number}: {new_chapter_summary}")
        mem["overall_summary"] += f" In Chapter {chapter_number}, {new_chapter_summary}"

        return mem
