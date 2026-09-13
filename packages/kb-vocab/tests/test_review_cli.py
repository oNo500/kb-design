"""CLI integration: only an explicit test decision may enter a built mapping graph."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from rdflib import Graph, URIRef
from rdflib.namespace import SKOS

from kb_vocab.cli import main


class ReviewCliTests(unittest.TestCase):
    def invoke(self, *arguments, expected_status=0):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                status = main([str(argument) for argument in arguments])
            except SystemExit as exc:
                status = exc.code
        self.assertEqual(expected_status, status, stderr.getvalue())
        return json.loads(stdout.getvalue() if status == 0 else stderr.getvalue())

    def test_review_decision_controls_published_mapping(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, label in (("left", "Memory"), ("right", "Remembering")):
                (root / f"{name}.ttl").write_text(
                    '@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n'
                    f'<https://example.test/{name}/scheme> a skos:ConceptScheme .\n'
                    f'<https://example.test/{name}/concept> a skos:Concept; '
                    f'skos:inScheme <https://example.test/{name}/scheme>; '
                    f'skos:prefLabel "{label}"@en .\n', encoding="utf-8"
                )
            catalog = root / "catalog.json"
            catalog.write_text(json.dumps({"sources": [
                {"name": name, "file": f"{name}.ttl"} for name in ("left", "right")
            ]}), encoding="utf-8")
            store = root / "review"
            self.invoke("review", "scan", "--catalog", catalog, "--output", store)
            listing = self.invoke("review", "list", store)
            proposal = self.invoke(
                "review", "propose", store,
                "--subject", "https://example.test/left/concept",
                "--object", "https://example.test/right/concept",
                "--relation", "relatedMatch", "--reason", "Synthetic integration fixture",
                "--actor", "test-operator", "--expected-revision", listing["revision"],
            )
            record_id = proposal["record"]["id"]
            pending = self.invoke("review", "show", store, record_id)
            self.assertEqual("pending", pending["records"][0]["status"])
            before = root / "before-decision"
            self.invoke("review", "build", store, "--output", before)
            self.assertEqual(0, len(Graph().parse(before / "mappings.ttl", format="turtle")))
            self.invoke(
                "review", "decide", store, record_id, "--decision", "accepted",
                "--actor", "test-operator", "--authorization", "Synthetic fixture only; no production approval",
                "--reason", "Deliberate relation in this test fixture",
                "--expected-revision", proposal["revision"],
            )
            stale = self.invoke(
                "review", "decide", store, record_id, "--decision", "withdrawn",
                "--actor", "test-operator", "--authorization", "Synthetic fixture only",
                "--reason", "Stale command must not replace the accepted decision",
                "--expected-revision", proposal["revision"], expected_status=1,
            )
            self.assertTrue(stale["error"])
            output = root / "built"
            self.invoke("review", "build", store, "--output", output)
            graph = Graph().parse(output / "mappings.ttl", format="turtle")
            self.assertIn((URIRef("https://example.test/left/concept"), SKOS.relatedMatch,
                           URIRef("https://example.test/right/concept")), graph)
            current = self.invoke("review", "list", store)
            decisions_file = root / "decisions.json"
            decisions_file.write_text(json.dumps([
                {"id": record_id, "decision": "withdrawn"}
            ]), encoding="utf-8")
            self.invoke(
                "review", "decide-batch", store, "--decisions-file", decisions_file,
                "--actor", "test-operator", "--authorization", "Synthetic fixture only",
                "--reason", "Withdraw this test mapping as a batch",
                "--expected-revision", current["revision"],
            )
            withdrawn = root / "withdrawn"
            self.invoke("review", "build", store, "--output", withdrawn)
            self.assertEqual(0, len(Graph().parse(withdrawn / "mappings.ttl", format="turtle")))


if __name__ == "__main__":
    unittest.main()
