import hashlib
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import yaml

from kb_sources.download import SourceError, fetch, verify


PDF = b"%PDF-1.4\nfixture content\n%%EOF\n"
HTML = b"<!doctype html><html><head><title>Report</title></head><body>Source</body></html>"


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.responses = {
            "/paper.pdf": (200, "application/pdf", PDF),
            "/report.html": (200, "text/html", HTML),
            "/blocked.pdf": (200, "text/html", b"<html>Login required</html>"),
            "/missing": (404, "text/plain", b"not found"),
        }
        responses = self.responses
        self.requests = {}
        requests = self.requests

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests[self.path] = requests.get(self.path, 0) + 1
                if self.path == "/redirect":
                    self.send_response(302)
                    self.send_header("Location", "/paper.pdf")
                    self.end_headers()
                    return
                if self.path == "/foreign":
                    self.send_response(302)
                    self.send_header("Location", "http://localhost:1/secret")
                    self.end_headers()
                    return
                status, kind, body = responses[self.path]
                if self.path == "/flaky" and requests[self.path] == 1:
                    status = 503
                self.send_response(status)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(body) + (10 if self.path == "/short" else 0)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        self.output = self.root / "sources"
        self.spec = {
            "schema_version": 1,
            "id": "sample",
            "title": "Sample publication",
            "version": "edition-1",
            "files": [self.item("paper", "/paper.pdf", "pdf")],
        }
        self.manifest = self.root / "source.yaml"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def item(self, identifier, endpoint, format):
        return {"id": identifier, "url": self.url + endpoint,
                "filename": identifier + "." + format, "format": format}

    def run_fetch(self, **options):
        self.manifest.write_text(yaml.safe_dump(self.spec))
        return fetch(self.manifest, self.output, retries=0, **options)

    def test_snapshot_preserves_bytes_and_resolves_redirects(self):
        self.spec["files"][0]["url"] = self.url + "/redirect"
        self.spec["files"].append(self.item("report", "/report.html", "html"))
        snapshot = self.run_fetch()
        self.assertEqual(PDF, (snapshot / "paper.pdf").read_bytes())
        self.assertEqual(HTML, (snapshot / "report.html").read_bytes())
        receipt = verify(snapshot)
        self.assertEqual(self.url + "/paper.pdf", receipt["files"][0]["final_url"])
        self.assertEqual(hashlib.sha256(PDF).hexdigest(), receipt["files"][0]["sha256"])
        self.assertEqual(hashlib.sha256((snapshot / "receipt.json").read_bytes()).hexdigest(), snapshot.name)

    def test_failure_does_not_publish_partial_snapshot_or_change_previous(self):
        previous = self.run_fetch()
        before = {p.name: p.read_bytes() for p in previous.iterdir()}
        self.spec["files"].append(self.item("missing", "/missing", "pdf"))
        with self.assertRaises(SourceError):
            self.run_fetch()
        self.assertEqual([previous], list((self.output / "sample").iterdir()))
        self.assertEqual(before, {p.name: p.read_bytes() for p in previous.iterdir()})

    def test_rejects_wrong_format_truncation_size_and_expected_hash(self):
        self.responses["/short"] = (200, "application/pdf", PDF)
        scenarios = [
            ("/blocked.pdf", {}, {}),
            ("/short", {}, {}),
            ("/paper.pdf", {}, {"max_bytes": 10}),
            ("/paper.pdf", {"sha256": "0" * 64}, {}),
            ("/foreign", {}, {}),
        ]
        for endpoint, extra, options in scenarios:
            with self.subTest(endpoint=endpoint, extra=extra, options=options):
                self.spec["files"] = [{**self.item("paper", endpoint, "pdf"), **extra}]
                with self.assertRaises(SourceError):
                    self.run_fetch(**options)
                self.assertEqual([], list(self.output.rglob("receipt.json")))

    def test_retry_is_bounded_and_transient_failure_can_recover(self):
        self.responses["/flaky"] = (200, "application/pdf", PDF)
        self.spec["files"] = [self.item("paper", "/flaky", "pdf")]
        self.manifest.write_text(yaml.safe_dump(self.spec))
        snapshot = fetch(self.manifest, self.output, retries=1)
        self.assertEqual(2, self.requests["/flaky"])
        verify(snapshot)
        self.responses["/down"] = (503, "text/plain", b"unavailable")
        self.spec["files"] = [self.item("paper", "/down", "pdf")]
        self.manifest.write_text(yaml.safe_dump(self.spec))
        with self.assertRaises(SourceError):
            fetch(self.manifest, self.output, retries=1)
        self.assertEqual(2, self.requests["/down"])
        self.assertEqual([snapshot], list((self.output / "sample").iterdir()))

    def test_html_challenge_is_not_accepted_as_source(self):
        self.responses["/challenge"] = (200, "text/html", b"<html><head><title>Just a moment...</title></head></html>")
        self.spec["files"] = [self.item("report", "/challenge", "html")]
        with self.assertRaisesRegex(SourceError, "access page"):
            self.run_fetch()
        self.assertEqual([], list(self.output.rglob("receipt.json")))

    def test_rejects_unsafe_or_duplicate_filenames_before_writing(self):
        for filename in ["../outside.pdf", "receipt.json", "source.yaml", "/tmp/out.pdf"]:
            with self.subTest(filename=filename):
                self.spec["files"][0]["filename"] = filename
                with self.assertRaises(SourceError):
                    self.run_fetch()
                self.assertFalse(self.output.exists())
        self.spec["files"] = [self.item("one", "/paper.pdf", "pdf"), self.item("two", "/paper.pdf", "pdf")]
        self.spec["files"][1]["filename"] = "ONE.PDF"
        with self.assertRaises(SourceError):
            self.run_fetch()

    def test_changed_remote_content_creates_new_snapshot(self):
        first = self.run_fetch()
        replacement = PDF.replace(b"fixture", b"updated")
        self.responses["/paper.pdf"] = (200, "application/pdf", replacement)
        second = self.run_fetch()
        self.assertNotEqual(first, second)
        self.assertEqual(PDF, (first / "paper.pdf").read_bytes())
        self.assertEqual(replacement, (second / "paper.pdf").read_bytes())
        verify(first)
        verify(second)

    def test_verify_detects_file_receipt_and_manifest_tampering(self):
        for name in ["paper.pdf", "receipt.json", "source.yaml"]:
            with self.subTest(name=name):
                snapshot = self.run_fetch()
                p = snapshot / name
                p.write_bytes(p.read_bytes() + b" ")
                with self.assertRaises(SourceError):
                    verify(snapshot)

    def test_verify_rejects_missing_extra_and_symlink_files(self):
        snapshot = self.run_fetch()
        paper = snapshot / "paper.pdf"
        paper.unlink()
        with self.assertRaises(SourceError):
            verify(snapshot)
        external = self.root / "external.pdf"
        external.write_bytes(PDF)
        paper.symlink_to(external)
        with self.assertRaises(SourceError):
            verify(snapshot)
        paper.unlink()
        paper.write_bytes(PDF)
        (snapshot / "extra.txt").write_text("unexpected")
        with self.assertRaises(SourceError):
            verify(snapshot)


if __name__ == "__main__":
    unittest.main()
