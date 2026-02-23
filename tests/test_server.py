import json
import threading
import urllib.error
import urllib.request

from app.server import run_server


def test_server_health_generate_and_export() -> None:
    server = run_server(port=0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        health = urllib.request.urlopen(f"http://127.0.0.1:{port}/health")
        assert health.status == 200
        assert json.loads(health.read().decode("utf-8")) == {"status": "ok"}

        payload = json.dumps(
            {"prompt": "Create a dark SaaS landing page with hero pricing testimonials"}
        ).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        generated = urllib.request.urlopen(req)
        assert generated.status == 200
        body = json.loads(generated.read().decode("utf-8"))
        assert body["theme"] == "dark"
        export_id = body["export_id"]

        exported = urllib.request.urlopen(f"http://127.0.0.1:{port}/api/export/{export_id}")
        assert exported.status == 200
        assert exported.headers["Content-Type"] == "application/zip"
        assert len(exported.read()) > 100

        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api/export/does-not-exist")
            assert False, "expected 404 for missing export"
        except urllib.error.HTTPError as exc:
            assert exc.code == 404
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
