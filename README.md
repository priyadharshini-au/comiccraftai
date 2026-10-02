Comic craft Ai demo link : https://drive.google.com/file/d/1gB5WXcRIScXHnOeawOvEJeSj3C4AQVA5/view?usp=sharing
# ComicCraft - AI Comic Story Creator

ComicCraft is a FastAPI + Jinja2 web application that turns a user story idea into a five-panel comic.

## Features

- Story prompt, character, setting, tone, and art-style inputs
- Gemini Flash outline generation
- Gemini Pro narration/dialogue generation
- Hugging Face text-to-image generation
- Mock mode for testing without API keys
- Five-panel comic preview
- PDF export with FPDF2
- JSON API
- Image test endpoint
- FastAPI Swagger documentation

## 1. Create the environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate
```

## 2. Test without API keys

Keep:

```env
AI_MODE=mock
IMAGE_BACKEND=mock
```

Run:

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## 3. Enable Gemini + Hugging Face

Put your credentials in `.env`:

```env
AI_MODE=live

GEMINI_API_KEY=your_key
GEMINI_FLASH_MODEL=gemini-2.5-flash
GEMINI_PRO_MODEL=gemini-2.5-pro

IMAGE_BACKEND=hf
HF_TOKEN=your_huggingface_token
HF_IMAGE_MODEL=stabilityai/stable-diffusion-2-1
```

Restart Uvicorn after changing `.env`.

## API

### POST /generate-comic/json

Example JSON:

```json
{
  "story_prompt": "A brave fox exploring an enchanted forest.",
  "character_name": "Luna",
  "setting": "Enchanted Forest",
  "tone": "Funny",
  "art_style": "Comic Book"
}
```

### GET /test-image

Example:

```text
http://127.0.0.1:8000/test-image?prompt=A%20brave%20fox%20in%20an%20enchanted%20forest
```

### GET /health

Returns the current application and AI mode.

## Run tests

```powershell
pytest
```
