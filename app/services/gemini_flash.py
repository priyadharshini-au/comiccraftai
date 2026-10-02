from google import genai
from google.genai import types

from app.config import settings
from app.models import ComicOutline


def _client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> ComicOutline:
    prompt = f"""
Create a coherent {settings.panel_count}-panel comic outline.

User story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Requirements:
- Return exactly {settings.panel_count} panels.
- Keep the same main character consistent across every panel.
- Make the story have a clear beginning, middle, turning point, and ending.
- scene_description should describe what happens visually.
- image_prompt should be detailed enough for a text-to-image model.
- Do not put dialogue in image_prompt.
- Keep all content family-friendly.
"""

    response = _client().models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
            response_schema=ComicOutline,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty outline.")
    return ComicOutline.model_validate_json(response.text)
