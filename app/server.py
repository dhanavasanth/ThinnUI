from __future__ import annotations

import json
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from app.main import generate_project
from app.services.exporter import fetch_zip


class ThinnUIHandler(BaseHTTPRequestHandler):
    server_version = "ThinnUIHTTP/0.1"

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json({"status": "ok"})
            return

        if parsed.path.startswith("/api/export/"):
            export_id = parsed.path.split("/api/export/", 1)[1]
            archive = fetch_zip(export_id)
            if archive is None:
                self._send_json({"detail": "Export not found"}, status=HTTPStatus.NOT_FOUND)
                return

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f"attachment; filename=thinnui-{export_id}.zip")
            self.send_header("Content-Length", str(len(archive)))
            self.end_headers()
            self.wfile.write(archive)
            return

        self._send_json({"detail": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/generate":
            self._send_json({"detail": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        try:
            content_len = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(content_len)) if content_len else {}
        except (ValueError, json.JSONDecodeError):
            self._send_json({"detail": "Invalid JSON payload"}, status=HTTPStatus.BAD_REQUEST)
            return

        prompt = (data.get("prompt") or "").strip()
        theme = data.get("theme")

        if len(prompt) < 5:
            self._send_json({"detail": "prompt must be at least 5 characters"}, status=HTTPStatus.BAD_REQUEST)
            return

        if theme is not None and theme not in {"dark", "light"}:
            self._send_json({"detail": "theme must be dark or light"}, status=HTTPStatus.BAD_REQUEST)
            return

        result = generate_project(prompt=prompt, theme=theme)
        payload = {
            "prompt": result.prompt,
            "theme": result.theme,
            "sections": result.sections,
            "selected_components": {
                section: asdict(component)
                for section, component in result.selected_components.items()
            },
            "files": result.files,
            "export_id": result.export_id,
        }
        self._send_json(payload, status=HTTPStatus.OK)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), ThinnUIHandler)


def main() -> None:
    server = run_server()
    print("ThinnUI API server running on http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
