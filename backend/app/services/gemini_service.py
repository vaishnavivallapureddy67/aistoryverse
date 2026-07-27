import json
import logging
import httpx
from app.core.config import settings

logger = logging.getLogger("ai_storyverse.gemini")

class GeminiService:
    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        self.endpoint_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        if not self.is_available():
            raise ValueError("Gemini API key is not configured.")

        contents = []
        if system_instruction:
            contents.append({
                "role": "user",
                "parts": [{"text": f"SYSTEM INSTRUCTION:\n{system_instruction}\n\nUSER PROMPT:\n{prompt}"}]
            })
        else:
            contents.append({
                "role": "user",
                "parts": [{"text": prompt}]
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.8,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 4096,
            }
        }

        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": self.api_key
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.endpoint_url, headers=headers, params=params, json=payload)
            if response.status_code != 200:
                logger.error(f"Gemini API error ({response.status_code}): {response.text}")
                raise RuntimeError(f"Gemini API returned status {response.status_code}: {response.text}")

            data = response.json()
            try:
                candidates = data.get("candidates", [])
                if not candidates:
                    raise RuntimeError("No candidates returned from Gemini API.")
                text = candidates[0]["content"]["parts"][0]["text"]
                return text
            except (KeyError, IndexError) as e:
                logger.error(f"Failed to parse Gemini response: {data}")
                raise RuntimeError("Failed to parse response text from Gemini API.") from e

    async def generate_json(self, prompt: str, system_instruction: str | None = None) -> dict:
        raw_text = await self.generate_text(prompt, system_instruction)
        # Clean markdown backticks if present
        clean_text = raw_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode failed on Gemini output: {raw_text}")
            # Fallback attempts
            start_idx = clean_text.find("{")
            end_idx = clean_text.rfind("}")
            if start_idx != -1 and end_idx != -1:
                return json.loads(clean_text[start_idx:end_idx+1])
            raise RuntimeError(f"Could not parse valid JSON from Gemini output: {raw_text}") from e

gemini_service = GeminiService()
