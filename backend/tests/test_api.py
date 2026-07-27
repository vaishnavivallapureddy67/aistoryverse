import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.db.database import init_db
from scripts.seed_classics import seed

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(init_db())
    loop.run_until_complete(seed())

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["app"] == "AIStoryVerse"
    assert data["gemini_model"] == settings.GEMINI_MODEL

def test_classics_collection():
    response = client.get("/api/v1/classics")
    assert response.status_code == 200
    books = response.json()
    assert len(books) >= 4
    titles = [b["title"] for b in books]
    assert "Alice's Adventures in Wonderland" in titles
    assert "The Time Machine" in titles

def test_surprise_me_vectors():
    response = client.get("/api/v1/surprise-me/random-prompt")
    assert response.status_code == 200
    data = response.json()
    assert "genre" in data
    assert "theme" in data
    assert "world" in data
    assert "character_archetype" in data
    assert "conflict" in data
    assert "ending_style" in data

def test_original_story_blueprint_and_accept_flow():
    payload = {
        "settings": {
            "genre": "Sci-Fi",
            "tone": "Suspenseful",
            "style": "Fast-Paced",
            "difficulty": "Intermediate",
            "length": "Medium",
            "character_name": "Dr. Aris Vance",
            "custom_prompt": "A deep space radio signal turns out to be a countdown timer."
        }
    }
    response = client.post("/api/v1/stories/blueprint", json=payload)
    assert response.status_code == 201
    story = response.json()
    assert story["status"] == "Draft"
    assert story["title"] is not None
    assert story["blueprint"] is not None
    story_id = story["id"]

    # Step 2: Accept Blueprint -> Chapter 1
    acc_res = client.post(f"/api/v1/stories/{story_id}/accept")
    assert acc_res.status_code == 200
    acc_story = acc_res.json()
    assert acc_story["status"] == "Reading"
    assert len(acc_story["chapters"]) == 1
    assert acc_story["chapters"][0]["chapter_number"] == 1

    # Step 3: Generate Chapter 2
    next_res = client.post(f"/api/v1/stories/{story_id}/next-chapter")
    assert next_res.status_code == 200
    ch2 = next_res.json()
    assert ch2["chapter_number"] == 2

    # Step 4: Verify Story Memory & Stats
    st_res = client.get(f"/api/v1/stories/{story_id}")
    assert st_res.status_code == 200
    final_story = st_res.json()
    assert final_story["chapters_generated"] == 2
    assert final_story["story_memory"] is not None

    # Step 5: Test Delete Story
    del_res = client.delete(f"/api/v1/library/stories/{story_id}")
    assert del_res.status_code == 204

def test_blueprint_rejection_flow():
    payload = {
        "settings": {
            "genre": "Fantasy",
            "tone": "Dark",
            "style": "Descriptive",
            "difficulty": "Advanced",
            "length": "Short",
            "character_name": "Lady Vane"
        }
    }
    res1 = client.post("/api/v1/stories/blueprint", json=payload)
    story1 = res1.json()
    story_id = story1["id"]
    assert story1["version_number"] == 1

    # Reject Blueprint
    res2 = client.post(f"/api/v1/stories/{story_id}/reject")
    assert res2.status_code == 200
    story2 = res2.json()
    assert story2["status"] == "Draft"
    assert story2["version_number"] == 2
    assert story2["blueprint_version"] == "v2.0"
