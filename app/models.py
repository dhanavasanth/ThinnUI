from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SectionName = Literal["hero", "features", "pricing", "testimonials", "footer"]
ThemeName = Literal["dark", "light"]


@dataclass(slots=True)
class Component:
    id: str
    name: str
    section: SectionName
    description: str
    tags: list[str]
    source: str


@dataclass(slots=True)
class GenerationResult:
    prompt: str
    theme: ThemeName
    sections: list[SectionName]
    selected_components: dict[SectionName, Component]
    files: dict[str, str]
    export_id: str
