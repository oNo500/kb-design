import json
import pathlib
import unittest

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"
SCHEMA_NAMES = (
    "source-entities.schema.json",
    "source-uses.schema.json",
    "source-obligations.schema.json",
    "source-reference-index.schema.json",
    "source-probe.schema.json",
    "source-migration.schema.json",
    "decision.schema.json",
)


def load_schema(name):
    path = ROOT / "schemas" / name
    if not path.exists():
        raise AssertionError(f"schema is missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_fixture(name):
    return yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))


def errors(schema_name, fixture_name):
    return list(Draft202012Validator(
        load_schema(schema_name), format_checker=FormatChecker()
    ).iter_errors(load_fixture(fixture_name)))


def validate_definition(schema_name, definition, value):
    schema = load_schema(schema_name)
    definition_schema = {
        "$schema": schema["$schema"],
        "$defs": schema["$defs"],
        "$ref": f"#/$defs/{definition}",
    }
    return list(Draft202012Validator(
        definition_schema, format_checker=FormatChecker()
    ).iter_errors(value))


class SourceSchemaTests(unittest.TestCase):
    def test_all_seven_schemas_pass_meta_validation(self):
        for name in SCHEMA_NAMES:
            Draft202012Validator.check_schema(load_schema(name))

    def test_valid_documents_pass(self):
        cases = (
            ("source-entities.schema.json", "valid/entities.yaml"),
            ("source-uses.schema.json", "valid/sources.yaml"),
            ("source-obligations.schema.json", "valid/obligations.yaml"),
            ("decision.schema.json", "valid/decision.yaml"),
        )
        for schema_name, fixture_name in cases:
            self.assertEqual([], errors(schema_name, fixture_name), fixture_name)

    def test_basis_requires_locator(self):
        self.assertTrue(validate_definition(
            "source-entities.schema.json", "basisItem",
            load_fixture("invalid/basis-missing-locator.yaml")))

    def test_source_requires_nested_basis(self):
        self.assertTrue(validate_definition(
            "source-migration.schema.json", "source",
            load_fixture("invalid/source-missing-basis.yaml")))

    def test_match_rejects_unknown_relation(self):
        self.assertTrue(validate_definition(
            "source-migration.schema.json", "match",
            load_fixture("invalid/match-invalid-rel.yaml")))

    def test_entity_rejects_scalar_url_in_strict_schema(self):
        self.assertTrue(errors(
            "source-entities.schema.json", "invalid/entity-scalar-url.yaml"))

    def test_approved_role_requires_decision(self):
        self.assertTrue(errors(
            "source-uses.schema.json", "invalid/role-missing-decision.yaml"))

    def test_resolved_obligation_cannot_reopen(self):
        self.assertTrue(errors(
            "source-obligations.schema.json", "invalid/obligation-reopened.yaml"))

    def test_migration_rejects_unknown_disposition(self):
        self.assertTrue(errors(
            "source-migration.schema.json", "invalid/migration-unknown-disposition.yaml"))

    def test_decision_front_matter_requires_stable_id(self):
        self.assertTrue(errors(
            "decision.schema.json", "invalid/decision-missing-id.yaml"))

    def test_payload_manifest_requires_topics_after_hash(self):
        self.assertTrue(validate_definition(
            "source-migration.schema.json", "cutoverPayloadManifest",
            load_fixture("invalid/cutover-manifest-missing-topics-hash.yaml")))

    def test_payload_manifest_rejects_its_own_path(self):
        self.assertTrue(validate_definition(
            "source-migration.schema.json", "cutoverPayloadManifest",
            load_fixture("invalid/cutover-manifest-self-entry.yaml")))

    def test_valid_source_handoff_passes(self):
        self.assertEqual([], validate_definition(
            "source-migration.schema.json", "sourceCutoverHandoff",
            load_fixture("valid/source-cutover-handoff.yaml")))

    def test_source_handoff_requires_seven_schemas(self):
        self.assertTrue(validate_definition(
            "source-migration.schema.json", "sourceCutoverHandoff",
            load_fixture("invalid/source-handoff-missing-schemas.yaml")))


if __name__ == "__main__":
    unittest.main()
