from datetime import datetime
from pathlib import Path
from typing import List

from fpdf import FPDF

from app.config import BASE_DIR
from app.models import ComicPanel


EXPORTS_DIR = BASE_DIR / "static" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _pdf_text(value: str) -> str:
    # FPDF built-in Helvetica is Latin-1 based.
    return value.encode("latin-1", "replace").decode("latin-1")


def save_pdf(layout: List[ComicPanel]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"comiccraft_{timestamp}.pdf"
    output_path = EXPORTS_DIR / filename

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 20)
        pdf.multi_cell(
            0,
            12,
            _pdf_text(f"Panel {panel.panel_number}: {panel.title}"),
        )

        image_file = BASE_DIR / panel.image_url.lstrip("/")
        if image_file.exists():
            pdf.image(str(image_file), x=15, y=35, w=180)

        pdf.ln(115)

        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(0, 7, _pdf_text(panel.scene_description))

        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, _pdf_text("Caption: " + panel.caption))

        pdf.ln(2)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, _pdf_text("Narration: " + panel.narration))

        if panel.dialogue:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 7, _pdf_text("Dialogue: " + panel.dialogue))

    pdf.output(str(output_path))
    return f"/static/exports/{filename}"
