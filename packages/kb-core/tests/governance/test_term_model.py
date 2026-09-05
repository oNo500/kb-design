import copy
import unittest
from pathlib import Path

import yaml

from kb_core.governance.term_model import (
    build_terms_schema,
    exported_reference_uris,
    parse_terms,
    schema_issues,
    validate_terms,
)
from kb_core.source_model import SCHEMA_IDS
from source_governance_helpers import materialized_current_layout


ROOT = Path(__file__).resolve().parents[4]
FIXTURES = ROOT / "tests" / "fixtures" / "terminology"
SOURCE_FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "source-governance" / "valid"


def load_yaml(relative):
    return yaml.safe_load((FIXTURES / relative).read_text(encoding="utf-8"))


class TermModelTests(unittest.TestCase):
    def setUp(self):
        self.valid_value = load_yaml("valid/minimal-active.yaml")
        self.topic_ids = frozenset({"computing"})
        self.source_tree = materialized_current_layout(SOURCE_FIXTURE_ROOT)
        self.source_root = self.source_tree.__enter__()

    def tearDown(self):
        self.source_tree.__exit__(None, None, None)

    def test_exact_top_level_keys(self):
        value = copy.deepcopy(self.valid_value)
        value["payload"] = {}

        paths = {issue.path for issue in schema_issues(value)}

        self.assertIn("$", paths)

    def test_rejects_duplicate_ids(self):
        value = copy.deepcopy(self.valid_value)
        duplicate = copy.deepcopy(value["concepts"][0])
        duplicate["definitions"][0]["text"] = "A second concept record."
        duplicate["languages"][0]["terms"][0]["text"] = "Duplicate identity"
        value["concepts"].append(duplicate)

        issues = validate_terms(
            parse_terms(value), self.source_root, self.topic_ids,
        )

        self.assertEqual(
            {"TERM_CONCEPT_ID_DUPLICATE", "TERM_ID_DUPLICATE"},
            {issue.code for issue in issues},
        )

    def test_basis_fields_are_nonempty_arrays(self):
        cases = (
            ("concept", lambda value: value["concepts"][0].update(basis=[])),
            ("subject field", lambda value: value["concepts"][0]["subject_fields"][0].update(basis=[])),
            ("definition", lambda value: value["concepts"][0]["definitions"][0].update(basis=[])),
            ("term", lambda value: value["concepts"][0]["languages"][0]["terms"][0].update(basis=[])),
        )
        for label, mutate in cases:
            with self.subTest(label=label):
                value = copy.deepcopy(self.valid_value)
                mutate(value)
                self.assertTrue(schema_issues(value))
        self.assertTrue(schema_issues(load_yaml("invalid/legacy-reference-values.yaml")))

    def test_schema_refs_match_source_model(self):
        refs = exported_reference_uris()
        schema = build_terms_schema()

        self.assertEqual(
            SCHEMA_IDS["source-entities.schema.json"] + "#/$defs/basisItem",
            refs["basis"],
        )
        self.assertEqual(
            SCHEMA_IDS["source-migration.schema.json"] + "#/$defs/source",
            schema["$defs"]["source_reference"]["$ref"],
        )
        self.assertEqual(
            SCHEMA_IDS["source-migration.schema.json"] + "#/$defs/match",
            schema["$defs"]["match_reference"]["$ref"],
        )

    def test_source_issue_code_and_path_are_preserved(self):
        value = copy.deepcopy(self.valid_value)
        value["concepts"][0]["definitions"][0]["basis"][0]["entity"] = "missing"

        issues = validate_terms(
            parse_terms(value), self.source_root, self.topic_ids,
        )
        source_issue = next(issue for issue in issues if issue.origin == "source")

        self.assertEqual(
            "TERM_SOURCE_CONTRACT_SOURCE_ENTITY_MISSING", source_issue.code,
        )
        self.assertEqual(
            "concepts[0].definitions[0].basis[0]", source_issue.path,
        )
        self.assertIn("definitions", source_issue.message)

    def test_accepts_only_v1_language_tags(self):
        cases = (
            ("definition", lambda value: value["concepts"][0]["definitions"][0].update(language="zh-CN")),
            ("language", lambda value: value["concepts"][0]["languages"][0].update(language="zh-CN")),
        )
        for label, mutate in cases:
            with self.subTest(label=label):
                value = copy.deepcopy(self.valid_value)
                mutate(value)
                self.assertTrue(schema_issues(value))
        self.assertFalse(schema_issues(load_yaml("valid/two-language.yaml")))

    def test_subject_fields_resolve_to_current_topics(self):
        document = parse_terms(self.valid_value)
        self.assertNotIn(
            "TERM_SUBJECT_FIELD_UNKNOWN",
            {issue.code for issue in validate_terms(document, self.source_root, self.topic_ids)},
        )

        issues = validate_terms(document, self.source_root, frozenset())
        self.assertEqual(
            ["TERM_SUBJECT_FIELD_UNKNOWN"],
            [issue.code for issue in issues],
        )

    def test_active_definition_conflicts_fail(self):
        value = copy.deepcopy(self.valid_value)
        conflicting = copy.deepcopy(value["concepts"][0]["definitions"][0])
        conflicting["text"] = "A conflicting active definition."
        value["concepts"][0]["definitions"].append(conflicting)

        issues = validate_terms(
            parse_terms(value), self.source_root, self.topic_ids,
        )

        self.assertIn("TERM_ACTIVE_DEFINITION_CONFLICT", {issue.code for issue in issues})


if __name__ == "__main__":
    unittest.main()
