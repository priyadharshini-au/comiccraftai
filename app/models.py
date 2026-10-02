from typing import List

from pydantic import BaseModel, Field


class ComicRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(min_length=1, max_length=100)
    setting: str = Field(min_length=1, max_length=200)
    tone: str = Field(min_length=1, max_length=100)
    art_style: str = Field(min_length=1, max_length=100)


class PanelOutline(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str


class ComicOutline(BaseModel):
    panels: List[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str


class ComicStory(BaseModel):
    panels: List[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    image_url: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str


class ComicGenerationResult(BaseModel):
    panels: List[ComicPanel]
    pdf_url: str
