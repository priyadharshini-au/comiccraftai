import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.config import BASE_DIR, settings


PANELS_DIR = BASE_DIR / "static" / "panels"
PANELS_DIR.mkdir(parents=True, exist_ok=True)


def _safe_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_")
    return value[:80] or "panel"


def _font(size: int):
    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _create_mock_image(prompt: str, output_path: Path) -> None:
    image = Image.new(
        "RGB",
        (settings.image_width, settings.image_height),
        (244, 238, 226),
    )
    draw = ImageDraw.Draw(image)

    title_font = _font(42)
    body_font = _font(22)

    draw.rectangle(
        (24, 24, settings.image_width - 24, settings.image_height - 24),
        outline=(25, 25, 25),
        width=8,
    )
    draw.text((55, 55), "COMICCRAFT", font=title_font, fill=(25, 25, 25))

    # Simple placeholder illustration.
    cx = settings.image_width // 2
    cy = settings.image_height // 2
    draw.ellipse((cx - 120, cy - 150, cx + 120, cy + 90), outline=(25, 25, 25), width=7)
    draw.ellipse((cx - 65, cy - 65, cx - 35, cy - 35), fill=(25, 25, 25))
    draw.ellipse((cx + 35, cy - 65, cx + 65, cy - 35), fill=(25, 25, 25))
    draw.arc((cx - 65, cy - 20, cx + 65, cy + 55), 10, 170, fill=(25, 25, 25), width=6)

    text = "Mock image mode\nReplace AI_MODE=mock with live mode."
    draw.multiline_text(
        (55, settings.image_height - 180),
        text,
        font=body_font,
        fill=(45, 45, 45),
        spacing=8,
    )

    image.save(output_path, "PNG")


def generate_image(image_prompt: str, panel_number: int) -> str:
    filename = f"panel_{panel_number}_{_safe_filename(image_prompt[:40])}.png"
    output_path = PANELS_DIR / filename

    if settings.ai_mode.lower() == "mock" or settings.image_backend.lower() == "mock":
        _create_mock_image(image_prompt, output_path)
        return f"/static/panels/{filename}"

    if settings.image_backend.lower() != "hf":
        raise RuntimeError("IMAGE_BACKEND must be 'mock' or 'hf'.")

    if not settings.hf_token:
        raise RuntimeError("HF_TOKEN is not configured.")

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        api_key=settings.hf_token,
        provider="auto",
    )

    image = client.text_to_image(
        prompt=image_prompt,
        negative_prompt="blurry, low quality, distorted, extra limbs, text, watermark",
        height=settings.image_height,
        width=settings.image_width,
        num_inference_steps=25,
        guidance_scale=7.0,
        model=settings.hf_image_model,
    )
    image.save(output_path)
    return f"/static/panels/{filename}"
