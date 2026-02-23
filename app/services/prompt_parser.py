from __future__ import annotations

from app.models import SectionName

DEFAULT_SECTIONS: list[SectionName] = ["hero", "features", "pricing", "testimonials", "footer"]

SECTION_KEYWORDS: dict[SectionName, tuple[str, ...]] = {
    "hero": ("hero", "headline", "banner"),
    "features": ("features", "benefits", "feature"),
    "pricing": ("pricing", "plans", "plan"),
    "testimonials": ("testimonials", "reviews", "social proof"),
    "footer": ("footer", "contact", "copyright"),
}


def parse_sections(prompt: str) -> list[SectionName]:
    normalized = prompt.lower()
    sections: list[SectionName] = []
    for section, keywords in SECTION_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            sections.append(section)

    return sections or DEFAULT_SECTIONS


def detect_theme(prompt: str, requested_theme: str | None = None) -> str:
    if requested_theme:
        return requested_theme

    normalized = prompt.lower()
    if "dark" in normalized:
        return "dark"
    if "light" in normalized:
        return "light"
    return "dark"
