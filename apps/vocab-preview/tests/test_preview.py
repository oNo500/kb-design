import hashlib
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest

import yaml

from kb_vocab_preview.server import SnapshotStore, make_server


COLLECTIONS = {
    "topics": "concepts", "entities": "entities", "sources": "sources",
    "types": "types", "genres": "genres", "forms": "forms",
    "bibliography": "references",
}


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.vocab = self.root / "data/vocab"
        self.vocab.mkdir(parents=True)
        for name, key in COLLECTIONS.items():
            document = {"schema_version": 3, "version": {"id": "fixture"}, key: []}
            if name == "entities":
                document.update(schema="urn:kb-design:data:entities", schema_version=3)
                document[key] = [{"id": "organization", "label": {"en": "Organization"}, "kind": "organization",
                                  "subjects": [], "status": "candidate", "added": "2026-09-05"}]
            if name == "sources":
                document.update(schema="urn:kb-design:data:source-uses", schema_version=3)
                document[key] = [{"id": "discovery", "reference": "standard", "history": [],
                                  "roles": [{"role": "discovery", "status": "proposed", "decision": None}]}]
            if name == "topics":
                document[key] = [{"id": "example", "label": {"zh": "原始名称"}}]
            directory = self.root / "data/references" if name == "bibliography" else self.vocab
            directory.mkdir(parents=True, exist_ok=True)
            if name == "bibliography":
                document.update(schema="urn:kb-design:data:bibliography")
                document[key] = [{"id": "standard", "label": {"en": "Standard"}, "kind": "standard", "subjects": [], "status": "candidate", "added": "2026-09-05", "tier": "archival", "version": None, "basis": {}, "review": {"checked": None, "next_due": None, "interval_months": None, "grace_days": 30, "obligations": []}, "watch": [], "replaced_by": None, "urls": [{"role": "canonical", "url": "https://example.invalid", "primary": True}], "history": [{"date": "2026-09-05", "action": "migration", "fields": ["version"], "decisions": []}]}]
            (directory / f"{name}.yaml").write_text(
                yaml.safe_dump(document, allow_unicode=True), encoding="utf-8"
            )
        self.topic = self.vocab / "topics.yaml"

    def hashes(self):
        return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob("*") if p.is_file()}

    def rename(self, title):
        document = yaml.safe_load(self.topic.read_text())
        document["concepts"][0]["label"]["zh"] = title
        self.topic.write_text(yaml.safe_dump(document, allow_unicode=True), encoding="utf-8")

    def test_working_file_change_updates_data_and_raw_yaml_without_writes(self):
        store = SnapshotStore(self.root)
        before = self.hashes()
        first = store.status()
        self.assertIsNone(first["error"])
        self.assertIsNotNone(first["revision"])
        self.assertEqual(before, self.hashes())
        self.rename("已保存的新名称")
        before = self.hashes()
        second = store.status()
        self.assertNotEqual(first["revision"], second["revision"])
        self.assertEqual("已保存的新名称", second["snapshot"]["collections"]["topics"]["data"]["concepts"][0]["label"]["zh"])
        self.assertIn("已保存的新名称", second["snapshot"]["collections"]["topics"]["raw"]["concepts:example"])
        self.assertEqual(before, self.hashes())
        self.assertEqual(second, store.status())

    def test_bibliography_updates_separately_without_writes(self):
        """Bibliography saves must refresh real reference records without merging entity identities."""
        store = SnapshotStore(self.root)
        first = store.status()
        path = self.root / "data/references/bibliography.yaml"
        document = yaml.safe_load(path.read_text())
        document["references"][0]["label"]["en"] = "Updated standard"
        path.write_text(yaml.safe_dump(document))
        before = self.hashes()
        second = store.status()
        self.assertIsNone(second["error"])
        self.assertNotEqual(first["revision"], second["revision"])
        collections = second["snapshot"]["collections"]
        self.assertIn("Updated standard", collections["bibliography"]["raw"]["references:standard"])
        self.assertEqual(first["snapshot"]["collections"]["entities"], collections["entities"])
        self.assertEqual(before, self.hashes())

    def test_invalid_save_keeps_last_good_result_and_recovers(self):
        store = SnapshotStore(self.root)
        good = store.status()
        self.assertIsNone(good["error"])
        self.topic.write_text("schema_version: 3\nconcepts: [\n", encoding="utf-8")
        failed = store.status()
        self.assertIn("topics.yaml", failed["error"])
        self.assertEqual(good["revision"], failed["revision"])
        self.assertEqual(good["snapshot"], failed["snapshot"])
        self.topic.write_text("schema_version: 3\nconcepts:\n  - id: recovered\n    label: 已恢复\n", encoding="utf-8")
        recovered = store.status()
        self.assertIsNone(recovered["error"])
        self.assertNotEqual(good["revision"], recovered["revision"])

    def test_legacy_source_reference_does_not_replace_current_snapshot(self):
        store = SnapshotStore(self.root)
        good = store.status()
        document = yaml.safe_load(self.topic.read_text())
        document["concepts"][0]["source"] = "discovery"
        self.topic.write_text(yaml.safe_dump(document))
        failed = store.status()
        self.assertIsNotNone(failed["error"])
        self.assertEqual(good["snapshot"], failed["snapshot"])
        self.assertEqual(good["revision"], failed["revision"])

    def test_invalid_record_shape_is_reported_instead_of_published(self):
        store = SnapshotStore(self.root)
        self.assertIsNone(store.status()["error"])
        for content in ("schema_version: 3\nconcepts: wrong\n", "schema_version: 3\nconcepts: [{id: a}, {id: a}]\n",
                        "schema_version: 3\nconcepts: [{id: a, broader: {wrong: shape}}]\n"):
            self.topic.write_text(content, encoding="utf-8")
            self.assertIsNotNone(store.status()["error"])

    def test_invalid_language_basis_does_not_replace_last_good_snapshot(self):
        store = SnapshotStore(self.root)
        good = store.status()
        for basis in ({"level": 1, "references": {"source": "x"}},
                      {"level": 5, "model": None}):
            document = {"schema_version": 3, "concepts": [{"id": "a", "label": {"zh": "错误依据"},
                                      "basis": {"zh": basis}}]}
            self.topic.write_text(yaml.safe_dump(document, allow_unicode=True), encoding="utf-8")
            failed = store.status()
            self.assertIsNotNone(failed["error"])
            self.assertEqual(good["revision"], failed["revision"])

    def test_duplicate_collection_keys_are_reported_and_recover(self):
        store = SnapshotStore(self.root)
        good = store.status()
        self.topic.write_text("schema_version: 3\nconcepts: [{id: a}, {id: b}]\nconcepts: [{id: c}]\n", encoding="utf-8")
        failed = store.status()
        self.assertIn("重复", failed["error"])
        self.assertEqual(good["snapshot"], failed["snapshot"])
        self.topic.write_text("schema_version: 3\nconcepts: [{id: recovered}]\n", encoding="utf-8")
        self.assertIsNone(store.status()["error"])

    def start_server(self):
        server = make_server(self.root, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server.server_address[1]

    def request(self, port, path, method="GET", headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            connection.request(method, path, headers=headers or {})
            response = connection.getresponse()
            return response.status, response.read().decode()
        finally:
            connection.close()

    def test_http_serves_updates_and_escapes_embedded_script_data(self):
        port = self.start_server()
        code, body = self.request(port, "/")
        self.assertEqual(200, code)
        self.assertIn("原始名称", body)
        code, status = self.request(port, "/api/status")
        self.assertEqual(200, code)
        revision = json.loads(status)["revision"]
        self.rename('</script><img src=x onerror="bad()">')
        _, status = self.request(port, "/api/status")
        self.assertNotEqual(revision, json.loads(status)["revision"])
        code, body = self.request(port, "/")
        self.assertEqual(200, code)
        self.assertNotIn('</script><img src=x', body)
        self.assertIn(r'\u003c/script\u003e', body)

    def test_server_exposes_no_repository_files_or_write_endpoint(self):
        secret = self.root / "private.txt"
        secret.write_text("not vocabulary", encoding="utf-8")
        port = self.start_server()
        before = self.hashes()
        for path in ("/private.txt", "/../private.txt", "/data/vocab/topics.yaml"):
            code, _ = self.request(port, path)
            self.assertEqual(404, code)
        code, _ = self.request(port, "/", method="POST")
        self.assertNotEqual(200, code)
        code, _ = self.request(port, "/api/status", headers={"Host": "untrusted.invalid"})
        self.assertEqual(403, code)
        self.assertEqual(before, self.hashes())


if __name__ == "__main__":
    unittest.main()
