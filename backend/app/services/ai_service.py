import logging
from datetime import datetime
from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.gemini_service import gemini_service
from app.services.prompt_builder import PromptBuilder
from app.services.mock_ai_engine import MockAIEngine
from app.db.models import Story, Chapter, StoryVersion, GenerationLog

logger = logging.getLogger("ai_storyverse.service")

class AIService:
    async def create_story_blueprint(
        self,
        db: AsyncSession,
        generation_settings: Dict[str, Any],
        user_id: str | None = None
    ) -> Story:
        use_gemini = gemini_service.is_available()
        user_prompt, system_instruction = PromptBuilder.build_blueprint_prompt(generation_settings)
        
        blueprint_data = None
        model_used = settings.GEMINI_MODEL if use_gemini else "MockAIEngine"

        if use_gemini:
            try:
                logger.info(f"Generating blueprint with Gemini ({settings.GEMINI_MODEL})...")
                blueprint_data = await gemini_service.generate_json(user_prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Gemini API blueprint generation failed ({e}). Falling back to Mock Engine.")
                blueprint_data = MockAIEngine.generate_blueprint(generation_settings)
                model_used = "MockAIEngine (Fallback)"
        else:
            logger.info("No Gemini API key found. Using Mock AI Engine.")
            blueprint_data = MockAIEngine.generate_blueprint(generation_settings)

        genre = blueprint_data.get("genre", generation_settings.get("genre", "Fantasy"))
        cover_image = MockAIEngine.get_default_cover(genre)

        initial_memory = {
            "characters": blueprint_data.get("main_characters", []),
            "relationships": [],
            "locations": [{"name": blueprint_data.get("world_setting", "Main Realm")}],
            "timeline": [],
            "important_events": [],
            "objects": [],
            "overall_summary": blueprint_data.get("summary", "")
        }

        story = Story(
            user_id=user_id,
            title=blueprint_data.get("title", "Untitled Novel"),
            summary=blueprint_data.get("summary"),
            cover_image=cover_image,
            genre=genre,
            tags=blueprint_data.get("tags", []),
            blueprint=blueprint_data,
            version_number=1,
            blueprint_version="v1.0",
            status="Draft", # Draft state until accepted
            generation_settings=generation_settings,
            story_memory=initial_memory,
            views=1,
            times_read=0,
            chapters_generated=0,
            total_words=0,
            is_classic=False,
            is_reimagined=False
        )

        db.add(story)
        await db.commit()
        await db.refresh(story)

        # Log prompt history
        log = GenerationLog(
            story_id=story.id,
            chapter_number=None,
            prompt_type="blueprint",
            prompt_text=user_prompt,
            response_text=str(blueprint_data),
            model_name=model_used
        )
        db.add(log)

        # Record initial version
        version = StoryVersion(
            story_id=story.id,
            version_number=1,
            blueprint=blueprint_data,
            chapter_1_content=None
        )
        db.add(version)
        await db.commit()

        return story

    async def accept_blueprint_and_generate_chapter_1(
        self,
        db: AsyncSession,
        story: Story
    ) -> Tuple[Story, Chapter]:
        story.status = "Reading"
        story.last_generated_at = datetime.utcnow()

        chapter = await self._generate_chapter_internal(db, story, chapter_number=1)
        story.chapters_generated = 1
        story.total_words = chapter.word_count

        await db.commit()
        await db.refresh(story)
        return story, chapter

    async def reject_blueprint_and_regenerate(
        self,
        db: AsyncSession,
        story: Story
    ) -> Story:
        # Increment version number
        new_version_num = story.version_number + 1
        gen_settings = story.generation_settings or {"genre": story.genre}

        use_gemini = gemini_service.is_available()
        user_prompt, system_instruction = PromptBuilder.build_blueprint_prompt(gen_settings)
        model_used = settings.GEMINI_MODEL if use_gemini else "MockAIEngine"

        if use_gemini:
            try:
                new_blueprint = await gemini_service.generate_json(user_prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Gemini API rejection regenerate failed ({e}). Using Mock Engine.")
                new_blueprint = MockAIEngine.generate_blueprint(gen_settings)
                model_used = "MockAIEngine (Fallback)"
        else:
            new_blueprint = MockAIEngine.generate_blueprint(gen_settings)

        story.title = new_blueprint.get("title", "Untitled Novel")
        story.summary = new_blueprint.get("summary")
        story.genre = new_blueprint.get("genre", story.genre)
        story.cover_image = MockAIEngine.get_default_cover(story.genre)
        story.tags = new_blueprint.get("tags", [])
        story.blueprint = new_blueprint
        story.version_number = new_version_num
        story.blueprint_version = f"v{new_version_num}.0"
        story.status = "Draft"
        story.story_memory = {
            "characters": new_blueprint.get("main_characters", []),
            "relationships": [],
            "locations": [],
            "timeline": [],
            "important_events": [],
            "objects": [],
            "overall_summary": new_blueprint.get("summary", "")
        }

        # Save new version snapshot
        version = StoryVersion(
            story_id=story.id,
            version_number=new_version_num,
            blueprint=new_blueprint,
            chapter_1_content=None
        )
        db.add(version)

        # Log prompt
        log = GenerationLog(
            story_id=story.id,
            chapter_number=None,
            prompt_type="blueprint_reject_regenerate",
            prompt_text=user_prompt,
            response_text=str(new_blueprint),
            model_name=model_used
        )
        db.add(log)

        await db.commit()
        await db.refresh(story)
        return story

    async def generate_next_chapter(
        self,
        db: AsyncSession,
        story: Story
    ) -> Chapter:
        next_ch_num = (story.chapters_generated or 0) + 1
        chapter = await self._generate_chapter_internal(db, story, chapter_number=next_ch_num)
        
        story.chapters_generated = next_ch_num
        story.total_words = (story.total_words or 0) + chapter.word_count
        story.last_generated_at = datetime.utcnow()
        if story.status == "Draft":
            story.status = "Reading"

        await db.commit()
        return chapter

    async def _generate_chapter_internal(
        self,
        db: AsyncSession,
        story: Story,
        chapter_number: int
    ) -> Chapter:
        use_gemini = gemini_service.is_available()
        
        prev_summaries = [ch.summary for ch in story.chapters if ch.summary]
        user_prompt, system_instruction = PromptBuilder.build_chapter_prompt(
            blueprint=story.blueprint or {},
            chapter_number=chapter_number,
            story_memory=story.story_memory,
            previous_chapters_summaries=prev_summaries,
            settings=story.generation_settings
        )

        ch_data = None
        model_used = settings.GEMINI_MODEL if use_gemini else "MockAIEngine"

        if use_gemini:
            try:
                ch_data = await gemini_service.generate_json(user_prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Gemini API chapter {chapter_number} failed ({e}). Using Mock Engine.")
                ch_data = MockAIEngine.generate_chapter(story.blueprint or {}, chapter_number, story.story_memory)
                model_used = "MockAIEngine (Fallback)"
        else:
            ch_data = MockAIEngine.generate_chapter(story.blueprint or {}, chapter_number, story.story_memory)

        content = ch_data.get("content", "").strip()
        ch_title = ch_data.get("chapter_title", f"Chapter {chapter_number}")
        ch_summary = ch_data.get("chapter_summary", f"Recap of chapter {chapter_number}")

        word_count = len(content.split())
        est_min = max(1, round(word_count / 200))

        chapter = Chapter(
            story_id=story.id,
            chapter_number=chapter_number,
            title=ch_title,
            content=content,
            summary=ch_summary,
            word_count=word_count,
            estimated_reading_time_min=est_min
        )
        db.add(chapter)

        # Quietly update persistent background Story Memory
        await self._quietly_update_story_memory(db, story, chapter_number, content, ch_summary, use_gemini)

        # Save prompt history log
        log = GenerationLog(
            story_id=story.id,
            chapter_number=chapter_number,
            prompt_type="chapter",
            prompt_text=user_prompt,
            response_text=content[:500] + "...",
            model_name=model_used
        )
        db.add(log)

        return chapter

    async def _quietly_update_story_memory(
        self,
        db: AsyncSession,
        story: Story,
        chapter_number: int,
        content: str,
        summary: str,
        use_gemini: bool
    ):
        if use_gemini:
            try:
                user_prompt, system_instruction = PromptBuilder.build_memory_update_prompt(
                    story.story_memory, content, chapter_number
                )
                updated_mem = await gemini_service.generate_json(user_prompt, system_instruction)
                story.story_memory = updated_mem
                return
            except Exception as e:
                logger.warning(f"Failed to update story memory with Gemini ({e}). Using mock memory update.")

        # Fallback quiet update
        story.story_memory = MockAIEngine.update_memory(story.story_memory, summary, chapter_number)

    async def create_reimagined_story(
        self,
        db: AsyncSession,
        classic_title: str,
        classic_author: str,
        classic_summary: str,
        transformation_type: str,
        twist_instructions: str | None = None,
        classic_id: int | None = None,
        user_id: str | None = None
    ) -> Story:
        use_gemini = gemini_service.is_available()
        user_prompt, system_instruction = PromptBuilder.build_reimagined_prompt(
            classic_title, classic_author, classic_summary, transformation_type, twist_instructions
        )

        blueprint_data = None
        model_used = settings.GEMINI_MODEL if use_gemini else "MockAIEngine"

        if use_gemini:
            try:
                blueprint_data = await gemini_service.generate_json(user_prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Reimagine with Gemini failed ({e}). Using Mock Engine.")
                blueprint_data = MockAIEngine.generate_blueprint({
                    "genre": transformation_type,
                    "custom_prompt": f"Reimagine {classic_title}: {twist_instructions or transformation_type}"
                })
                model_used = "MockAIEngine (Fallback)"
        else:
            blueprint_data = MockAIEngine.generate_blueprint({
                "genre": transformation_type,
                "custom_prompt": f"Reimagine {classic_title}: {twist_instructions or transformation_type}"
            })

        genre = blueprint_data.get("genre", "Reimagined Classic")
        cover_image = MockAIEngine.get_default_cover(genre)

        story = Story(
            user_id=user_id,
            title=blueprint_data.get("title", f"{classic_title} (Reimagined)"),
            summary=blueprint_data.get("summary"),
            cover_image=cover_image,
            genre=genre,
            tags=["Reimagined", classic_title, transformation_type],
            blueprint=blueprint_data,
            version_number=1,
            blueprint_version="v1.0",
            status="Draft",
            generation_settings={
                "transformation_type": transformation_type,
                "twist_instructions": twist_instructions,
                "original_classic": classic_title
            },
            story_memory={
                "characters": blueprint_data.get("main_characters", []),
                "relationships": [],
                "locations": [],
                "timeline": [],
                "important_events": [],
                "objects": [],
                "overall_summary": blueprint_data.get("summary", "")
            },
            is_classic=False,
            is_reimagined=True,
            original_classic_id=classic_id
        )

        db.add(story)
        await db.commit()
        await db.refresh(story)

        log = GenerationLog(
            story_id=story.id,
            chapter_number=None,
            prompt_type="reimagine",
            prompt_text=user_prompt,
            response_text=str(blueprint_data),
            model_name=model_used
        )
        db.add(log)
        await db.commit()

        return story

ai_service = AIService()
