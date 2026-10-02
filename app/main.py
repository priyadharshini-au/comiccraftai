from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title=settings.app_name,
    description="AI comic story creator using Gemini and Stable Diffusion-compatible image generation.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "ai_mode": settings.ai_mode,
        "image_backend": settings.image_backend,
    }
