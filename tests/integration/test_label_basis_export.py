"""Shared-interface checks: preserve provenance and reject fake model evidence."""
import copy
import pathlib
import unittest

import yaml

from kb_obsidian import exporter


ROOT = pathlib.Path(__file__).resolve().parents[2]


class LabelBasisExportTests(unittest.TestCase):
    def setUp(self):
        document = yaml.safe_load((ROOT / "data/vocab/topics.yaml").read_text())
        self.record = copy.deepcopy(next(r for r in document["concepts"] if r["id"] == "software-engineering"))
        self.record["basis"]["zh"] = {
            "level": 5,
            "model": {
                "name": "GPT-6",
                "date": "2026-09-05",
                "rationale": "既有概念的软件工程语境。",
                "approval": "design/decisions/structured-label-basis.md#批次授权",
            },
        }

    def test_model_basis_is_readable_without_becoming_an_external_source(self):
        exporter._validate_record("topics", "data/vocab/topics.yaml", "concepts", self.record)
        body = "\n".join(exporter._common_body(self.record))
        self.assertIn("外部用法未核实", body)
        self.assertIn("GPT-6", body)
        self.assertIn("2026-09-05", body)
        self.assertNotIn("[[kb/sources/model", body)

    def test_model_cannot_carry_external_evidence_in_the_same_basis(self):
        self.record["basis"]["zh"]["references"] = [{"source": "wikidata", "locator": "Q80993"}]
        with self.assertRaises(exporter.ExportError):
            exporter._validate_record("topics", "data/vocab/topics.yaml", "concepts", self.record)

    def test_invalid_level_is_not_accepted_as_an_arbitrary_string(self):
        self.record["basis"]["zh"] = {"level": True, "references": [{"source": "wikidata", "locator": "Q80993"}]}
        with self.assertRaises(exporter.ExportError):
            exporter._validate_record("topics", "data/vocab/topics.yaml", "concepts", self.record)

    def test_bare_model_marker_cannot_bypass_metadata_validation(self):
        self.record["basis"]["zh"] = "model"
        with self.assertRaises(exporter.ExportError):
            exporter._validate_record("topics", "data/vocab/topics.yaml", "concepts", self.record)


if __name__ == "__main__":
    unittest.main()
