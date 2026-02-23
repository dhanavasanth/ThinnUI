from __future__ import annotations

import io
import zipfile
from uuid import uuid4

EXPORTS: dict[str, bytes] = {}


def create_zip(files: dict[str, str]) -> str:
    export_id = str(uuid4())
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for path, contents in files.items():
            zip_file.writestr(path, contents)

    EXPORTS[export_id] = zip_buffer.getvalue()
    return export_id


def fetch_zip(export_id: str) -> bytes | None:
    return EXPORTS.get(export_id)
