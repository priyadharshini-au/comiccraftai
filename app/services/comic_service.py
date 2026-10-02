from app.config import settings
from app.models import ComicRequest
from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout


def _mock_outline(request: ComicRequest):
    from app.models import ComicOutline, PanelOutline

    panels = []
    for number in range(1, settings.panel_count + 1):
        panels.append(
            PanelOutline(
                panel_number=number,
                title=f"Adventure Panel {number}",
                scene_description=(
                    f"{request.character_name} continues the adventure in "
                    f"{request.setting}."
                ),
                image_prompt=(
                    f"{request.character_name}, in {request.setting}, "
                    f"{request.art_style} comic illustration, panel {number}, "
                    f"{request.tone} mood, cinematic composition"
                ),
            )
        )
    return ComicOutline(panels=panels)


def _mock_story(outline, request: ComicRequest):
    from app.models import ComicStory, PanelStory

    panels = []
    for panel in outline.panels:
        panels.append(
            PanelStory(
                panel_number=panel.panel_number,
                title=panel.title,
                scene_description=panel.scene_description,
                caption=f"Meanwhile, in {request.setting}...",
                narration=(
                    f"{request.character_name} takes another step toward the "
                    f"heart of the adventure."
                ),
                dialogue=f"{request.character_name}: Let's see what happens next!",
                image_prompt=panel.image_prompt,
            )
        )
    return ComicStory(panels=panels)


def generate_comic(request: ComicRequest):
    if settings.ai_mode.lower() == "mock":
        outline = _mock_outline(request)
        story = _mock_story(outline, request)
    else:
        outline = generate_outline(
            request.story_prompt,
            request.character_name,
            request.setting,
            request.tone,
            request.art_style,
        )
        story = generate_story(
            outline,
            request.character_name,
            request.tone,
            request.art_style,
        )

    image_urls = [
        generate_image(panel.image_prompt, panel.panel_number)
        for panel in story.panels
    ]

    layout = build_comic_layout(story, image_urls)
    pdf_url = save_pdf(layout)

    return layout, pdf_url
