from __future__ import annotations

from app.models import Component, SectionName


def compose_layout(candidates: dict[SectionName, list[Component]]) -> dict[SectionName, Component]:
    selected: dict[SectionName, Component] = {}
    for section, components in candidates.items():
        if not components:
            raise ValueError(f"No candidates found for section: {section}")
        selected[section] = components[0]
    return selected
