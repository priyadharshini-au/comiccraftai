from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.models import ComicRequest
from app.services.comic_service import generate_comic
from app.services.image_generator import generate_image


router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = ComicRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        layout, pdf_url = generate_comic(payload)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_url": pdf_url,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=500,
        )


@router.post("/generate-comic/json")
def generate_json(payload: ComicRequest):
    try:
        layout, pdf_url = generate_comic(payload)
        return {
            "success": True,
            "panels": [panel.model_dump() for panel in layout],
            "pdf_url": pdf_url,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/test-image")
def test_image(prompt: str = "A brave fox exploring an enchanted forest, comic book art"):
    try:
        image_url = generate_image(prompt, 999)
        return {"success": True, "image_url": image_url}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/download/{filename}")
def download(filename: str):
    safe_name = Path(filename).name
    file_path = BASE_DIR / "static" / "exports" / safe_name

    if not file_path.exists() or file_path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=404, detail="PDF not found.")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=safe_name,
    )


@router.get("/export-success", response_class=HTMLResponse)
def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={},
    )
