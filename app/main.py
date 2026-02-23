from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from app.models import GenerationResult
from app.services.codegen import generate_project_files
from app.services.exporter import create_zip, fetch_zip
from app.services.layout import compose_layout
from app.services.prompt_parser import detect_theme, parse_sections
from app.services.registry import query_components


def generate_project(prompt: str, theme: str | None = None) -> GenerationResult:
    sections = parse_sections(prompt)
    resolved_theme = detect_theme(prompt, theme)
    candidates = {section: query_components(section, prompt) for section in sections}
    selected = compose_layout(candidates)
    files = generate_project_files(theme=resolved_theme, selected_components=selected)
    export_id = create_zip(files)
    return GenerationResult(
        prompt=prompt,
        theme=resolved_theme,
        sections=sections,
        selected_components=selected,
        files=files,
        export_id=export_id,
    )


def export_zip(export_id: str, output_path: Path) -> Path:
    archive = fetch_zip(export_id)
    if archive is None:
        raise ValueError(f"Unknown export id: {export_id}")

    output_path.write_bytes(archive)
    return output_path


def _run_cli() -> None:
    parser = argparse.ArgumentParser(description="ThinnUI AI prototype generator")
    parser.add_argument("prompt", help="Natural-language prompt")
    parser.add_argument("--theme", choices=["dark", "light"], default=None)
    parser.add_argument("--output", default="thinnui-export.zip")
    args = parser.parse_args()

    result = generate_project(prompt=args.prompt, theme=args.theme)
    out_file = export_zip(result.export_id, Path(args.output))

    response = {
        "prompt": result.prompt,
        "theme": result.theme,
        "sections": result.sections,
        "selected_components": {
            section: asdict(component)
            for section, component in result.selected_components.items()
        },
        "files": sorted(result.files.keys()),
        "export_id": result.export_id,
        "zip_path": str(out_file),
    }
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    _run_cli()
