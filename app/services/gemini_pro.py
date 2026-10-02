from google import genai
from google.genai import types

from app.config import settings
from app.models import ComicOutline, ComicStory


def _client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(
    outline: ComicOutline,
    character_name: str,
    tone: str,
    art_style: str,
) -> ComicStory:
    outline_json = outline.model_dump_json(indent=2)

    prompt = f"""
Expand the following comic outline into a polished comic script.

Main character: {character_name}
Tone: {tone}
Art style: {art_style}

Outline:
{outline_json}

Requirements:
- Return exactly the same number of panels as the outline.
- Preserve panel order and panel numbers.
- Write concise but engaging narration.
- Add a short environmental caption.
- Add natural character dialogue.
- Keep the character, setting, and visual continuity consistent.
- Keep image_prompt suitable for a comic illustration model.
- Do not include markdown or explanations outside the requested JSON structure.
- Keep content family-friendly.
"""

    response = _client().models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
            response_schema=ComicStory,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty story.")
    return ComicStory.model_validate_json(response.text)
