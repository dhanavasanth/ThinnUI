import zipfile
from pathlib import Path

from app.main import export_zip, generate_project
from app.services.prompt_parser import parse_sections


def test_parse_sections_defaults_when_no_section_keywords() -> None:
    sections = parse_sections("build me a marketing page")
    assert sections == ["hero", "features", "pricing", "testimonials", "footer"]


def test_generate_and_export_flow(tmp_path: Path) -> None:
    result = generate_project("Create a dark SaaS landing page with hero pricing testimonials")

    assert result.theme == "dark"
    assert result.export_id
    assert "app/page.tsx" in result.files

    zip_path = export_zip(result.export_id, tmp_path / "demo.zip")
    assert zip_path.exists()

    with zipfile.ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        assert "app/page.tsx" in names
        assert "app/layout.tsx" in names
        page_contents = archive.read("app/page.tsx").decode("utf-8")
        assert "Dark SaaS Hero" in page_contents
