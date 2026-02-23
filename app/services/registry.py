from __future__ import annotations

import json
from pathlib import Path

from app.models import Component, SectionName

_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "components.json"


def load_components() -> list[Component]:
    with _DATA_FILE.open("r", encoding="utf-8") as file:
        raw_components = json.load(file)
    return [Component(**component) for component in raw_components]


def query_components(section: SectionName, prompt: str, limit: int = 3) -> list[Component]:
    words = set(prompt.lower().split())
    scored: list[tuple[int, Component]] = []
    for component in load_components():
        if component.section != section:
            continue
        haystack = f"{component.name} {component.description} {' '.join(component.tags)}".lower()
        score = sum(word in haystack for word in words)
        scored.append((score, component))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [component for _, component in scored[:limit]]
