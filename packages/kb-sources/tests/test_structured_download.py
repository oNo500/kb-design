"""Reject mislabeled or damaged structured sources before publishing a snapshot."""
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import yaml
from kb_sources.download import SourceError, fetch, verify


class Response(io.BytesIO):
    status = 200

    def __init__(self, body):
        super().__init__(body)
        self.headers = {"Content-Length": str(len(body))}

    def geturl(self):
        return "https://example.org/source"


def archive(body=b"source data"):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_STORED) as zipped:
        zipped.writestr("source.xml", body)
    return stream.getvalue()


class StructuredDownloadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def receive(self, kind, body):
        manifest = self.root / "manifest.yaml"
        manifest.write_text(yaml.safe_dump({
            "schema_version": 1, "id": "sample", "title": "Sample", "version": "1",
            "files": [{"id": "data", "url": "https://example.org/source",
                       "filename": "data." + kind, "format": kind}],
        }))
        with patch("kb_sources.download.build_opener") as factory:
            factory.return_value.open.return_value = Response(body)
            return fetch(manifest, self.root / "output", retries=0)

    def test_valid_structured_downloads_preserve_bytes_and_verify_offline(self):
        samples = {
            "tsv": "code\tlabel\n00\tGénéral\n".encode("cp1252"),
            "turtle": b'@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n<concept/1> a skos:Concept .',
            "xml": b'<?xml version="1.0"?><terms><term id="1">Math</term></terms>',
            "zip": archive(),
            "json": b'[["Philosophy", 10, "1", 1]]',
        }
        for kind, body in samples.items():
            with self.subTest(kind=kind):
                snapshot = self.receive(kind, body)
                self.assertEqual((snapshot / ("data." + kind)).read_bytes(), body)
                self.assertEqual(verify(snapshot)["files"][0]["format"], kind)

    def test_html_access_pages_never_publish_as_structured_sources(self):
        for kind in ("tsv", "turtle", "xml", "zip", "json"):
            with self.subTest(kind=kind), self.assertRaises(SourceError):
                self.receive(kind, b'<html><head><title>Login</title></head><body>Sign in</body></html>')
        self.assertEqual(list((self.root / "output" / "sample").iterdir()), [])

    def test_malformed_content_never_publishes(self):
        broken_zip = archive().replace(b"source data", b"broken data")
        samples = [
            ("tsv", b"a\tb\nc\td\te\n"),
            ("tsv", b"a\tb\n"),
            ("turtle", b"@prefix bad syntax"),
            ("xml", b"<terms><term></terms>"),
            ("xml", b'<!DOCTYPE terms [<!ENTITY x "injected">]><terms>&x;</terms>'),
            ("xml", '<!DOCTYPE terms [<!ENTITY x "injected">]><terms>&x;</terms>'.encode("utf-16")),
            ("zip", broken_zip),
            ("json", b'{"broken":'),
            ("json", b'{"value": NaN}'),
        ]
        for kind, body in samples:
            with self.subTest(kind=kind, body=body[:40]), self.assertRaises(SourceError):
                self.receive(kind, body)
        self.assertEqual(list((self.root / "output" / "sample").iterdir()), [])

    def test_zip_limits_apply_before_member_decompression(self):
        with patch("kb_sources.download._ZIP_MAX_UNCOMPRESSED", 2, create=True):
            with self.assertRaises(SourceError):
                self.receive("zip", archive())
        with patch("kb_sources.download._ZIP_MAX_ENTRIES", 0, create=True):
            with self.assertRaises(SourceError):
                self.receive("zip", archive())
