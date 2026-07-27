import json
from typing import Dict, Any, List, Optional

class PromptBuilder:
    @staticmethod
    def build_blueprint_prompt(settings: Dict[str, Any]) -> tuple[str, str]:
        genre = settings.get("genre", "Fantasy")
        tone = settings.get("tone", "Immersive")
        style = settings.get("style", "Descriptive")
        difficulty = settings.get("difficulty", "Intermediate")
        length = settings.get("length", "Medium")
        character_name = settings.get("character_name") or "Main Character"
        custom_prompt = settings.get("custom_prompt", "")

        system_instruction = (
            "You are an expert master novelist, creative writing director, and world builder. "
            "Your task is to generate a comprehensive, highly original, structured JSON story blueprint. "
            "Do NOT reproduce copyrighted modern novels or verbatim existing texts. "
            "Produce clean, valid JSON only with NO markdown codeblock delimiters outside JSON."
        )

        user_prompt = f"""
Generate a complete, novel-length original story blueprint based on these specifications:
- Genre: {genre}
- Tone / Atmosphere: {tone}
- Writing Style: {style}
- Target Reading Level: {difficulty}
- Length Target: {length}
- Protagonist Name Idea: {character_name}
- Additional Guidance / Premise: {custom_prompt or 'Create an unforgettable premise with high stakes.'}

Return JSON with this EXACT structure:
{{
  "title": "Evocative & Catchy Book Title",
  "genre": "{genre}",
  "theme": "Core underlying thematic message",
  "world_setting": "Rich description of the setting, world rules, and atmosphere",
  "time_period": "Historical or fictional time period",
  "main_characters": [
    {{
      "name": "Character Name",
      "archetype": "Archetype (e.g. Reluctant Scholar, Maverick Pilot)",
      "personality": "Detailed traits and flaws",
      "goals": "Primary desire or motivation",
      "relationships": "Dynamic with key allies or rivals"
    }}
  ],
  "main_conflict": "Central dramatic conflict driving the plot",
  "story_goal": "Ultimate resolution goal",
  "plot_outline": [
    {{
      "chapter_number": 1,
      "chapter_title": "Inciting Incident Title",
      "objective": "What happens in this chapter",
      "key_elements": ["Key event 1", "Key mystery 2"]
    }}
  ],
  "estimated_chapters": 8,
  "ending_style": "Bittersweet, Triumphant, Mind-Bending Twist, etc.",
  "tags": ["Tag1", "Tag2", "Tag3"],
  "summary": "Compelling 3-sentence book blurb"
}}
"""
        return user_prompt.strip(), system_instruction.strip()

    @staticmethod
    def build_chapter_prompt(
        blueprint: Dict[str, Any],
        chapter_number: int,
        story_memory: Optional[Dict[str, Any]] = None,
        previous_chapters_summaries: Optional[List[str]] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> tuple[str, str]:
        title = blueprint.get("title", "Untitled Story")
        genre = blueprint.get("genre", "Fiction")
        world = blueprint.get("world_setting", "Detailed environment")
        characters = blueprint.get("main_characters", [])
        conflict = blueprint.get("main_conflict", "Central tension")
        outline = blueprint.get("plot_outline", [])
        
        # Find objective for target chapter
        ch_outline = next((ch for ch in outline if ch.get("chapter_number") == chapter_number), None)
        ch_title = ch_outline.get("chapter_title", f"Chapter {chapter_number}") if ch_outline else f"Chapter {chapter_number}"
        ch_objective = ch_outline.get("objective", "Advance the plot with dramatic narrative beats.") if ch_outline else "Advance the plot."

        style = settings.get("style", "Descriptive") if settings else "Immersive & Engaging"
        tone = settings.get("tone", "Dramatic") if settings else "Atmospheric"

        memory_context = ""
        if story_memory:
            memory_context = f"""
STORY MEMORY (Long-Term Consistency State):
- Known Characters: {json.dumps(story_memory.get('characters', []))}
- Character Relationships: {json.dumps(story_memory.get('relationships', []))}
- Key Locations: {json.dumps(story_memory.get('locations', []))}
- Story Timeline & Past Events: {json.dumps(story_memory.get('important_events', []))}
- Key Objects / Artifacts: {json.dumps(story_memory.get('objects', []))}
- Overall Story Narrative So Far: {story_memory.get('overall_summary', 'Story begins.')}
"""

        past_summaries = ""
        if previous_chapters_summaries:
            past_summaries = "PREVIOUS CHAPTERS RECAP:\n" + "\n".join(
                [f"Chapter {i+1}: {summary}" for i, summary in enumerate(previous_chapters_summaries)]
            )

        system_instruction = (
            "You are a bestselling prose novelist. Write deeply engaging, cinematic story chapters. "
            "Focus on realistic, emotional dialogue, vivid sensory world-building, proper paragraphing, "
            "flawless grammar, and compelling pacing. Always end the chapter on a captivating hook or cliffhanger."
        )

        user_prompt = f"""
Write Chapter {chapter_number} for the novel "{title}".

BOOK BLUEPRINT CONTEXT:
- Genre: {genre}
- Tone: {tone}
- Writing Style: {style}
- World & Setting: {world}
- Main Conflict: {conflict}
- Characters Roster: {json.dumps(characters)}

{memory_context}
{past_summaries}

CHAPTER {chapter_number} GOALS:
- Chapter Title: {ch_title}
- Chapter Objective: {ch_objective}

INSTRUCTIONS:
1. Write Chapter {chapter_number} in full, rich prose (between 800 to 1400 words).
2. Format paragraph breaks cleanly using double newlines.
3. Ensure natural dialogue formatting with quote marks.
4. Conclude with a strong narrative hook or cliffhanger.

Return JSON with this EXACT structure:
{{
  "chapter_number": {chapter_number},
  "chapter_title": "{ch_title}",
  "content": "Full chapter prose text here...",
  "chapter_summary": "1-2 sentence recap of major plot developments in this chapter."
}}
"""
        return user_prompt.strip(), system_instruction.strip()

    @staticmethod
    def build_memory_update_prompt(
        existing_memory: Optional[Dict[str, Any]],
        new_chapter_content: str,
        chapter_number: int
    ) -> tuple[str, str]:
        current_mem = existing_memory or {
            "characters": [],
            "relationships": [],
            "locations": [],
            "timeline": [],
            "important_events": [],
            "objects": [],
            "overall_summary": ""
        }

        system_instruction = (
            "You are an AI Narrative Continuity Director. Your job is to analyze new story chapter text "
            "and update the story's persistent memory state cleanly and accurately."
        )

        user_prompt = f"""
Analyze Chapter {chapter_number} and update the Story Memory JSON state.

CURRENT STORY MEMORY STATE:
{json.dumps(current_mem, indent=2)}

NEW CHAPTER CONTENT:
{new_chapter_content[:3000]}...

INSTRUCTIONS:
Update and return the merged JSON state:
1. "characters": Update status, secrets, or newly introduced characters.
2. "relationships": Update character dynamics or new alliances/rifts.
3. "locations": Add any new settings visited.
4. "timeline": Add timestamp/phase marker for Chapter {chapter_number}.
5. "important_events": Append 1-2 major plot turning points from this chapter.
6. "objects": Track key physical items, clues, or weapons.
7. "overall_summary": Concise updated summary of the overall narrative so far.

Return JSON with this EXACT structure:
{{
  "characters": [...],
  "relationships": [...],
  "locations": [...],
  "timeline": [...],
  "important_events": [...],
  "objects": [...],
  "overall_summary": "Updated overall narrative summary"
}}
"""
        return user_prompt.strip(), system_instruction.strip()

    @staticmethod
    def build_reimagined_prompt(
        classic_title: str,
        classic_author: str,
        classic_summary: str,
        transformation_type: str,
        twist_instructions: Optional[str] = None
    ) -> tuple[str, str]:
        system_instruction = (
            "You are an innovative literary reimagining director. "
            "You take public-domain classic literature and create completely original, creative reinterpretations."
        )

        user_prompt = f"""
Create a unique AI Reimagined Story Blueprint inspired by the classic "{classic_title}" by {classic_author}.

ORIGINAL CLASSIC OVERVIEW:
{classic_summary}

REIMAGINING ANGLE:
- Transformation Vector: {transformation_type} (e.g. Alternate Ending, Futuristic Sci-Fi, Cyberpunk, Villain POV, Modern Retelling)
- Custom Twist Guidance: {twist_instructions or 'Create an unexpected, brilliant narrative twist while honoring key thematic motifs.'}

Return JSON with this EXACT structure:
{{
  "title": "Reimagined Title (e.g., Frankenstein 2099)",
  "genre": "Reimagined Sci-Fi / Alternate History",
  "theme": "Fresh thematic lens",
  "world_setting": "New setting description",
  "time_period": "New time period",
  "main_characters": [
    {{
      "name": "Character Name",
      "archetype": "Reimagined Archetype",
      "personality": "Updated traits",
      "goals": "Motivations",
      "relationships": "Dynamic"
    }}
  ],
  "main_conflict": "New central conflict",
  "story_goal": "Goal",
  "plot_outline": [
    {{
      "chapter_number": 1,
      "chapter_title": "Chapter Title",
      "objective": "Objective",
      "key_elements": ["Element"]
    }}
  ],
  "estimated_chapters": 6,
  "ending_style": "Twist Ending",
  "tags": ["Reimagined", "Classic Twist"],
  "summary": "3-sentence blurb of this fresh reimagine concept"
}}
"""
        return user_prompt.strip(), system_instruction.strip()
