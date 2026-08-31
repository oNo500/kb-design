import importlib
import unittest
from pathlib import Path
from typing import List, Sequence, get_args, get_type_hints


EXPECTED_SCHEMA_IDS = {
    "source-entities.schema.json": "urn:kb-design:schema:source-entities:2",
    "source-uses.schema.json": "urn:kb-design:schema:source-uses:2",
    "source-obligations.schema.json": "urn:kb-design:schema:source-obligations:1",
    "source-reference-index.schema.json": "urn:kb-design:schema:source-reference-index:1",
    "source-probe.schema.json": "urn:kb-design:schema:source-probe:1",
    "source-migration.schema.json": "urn:kb-design:schema:source-migration:1",
    "decision.schema.json": "urn:kb-design:schema:decision:1",
}

EXPECTED_ERROR_CODES = (
    "SOURCE_SCHEMA_INVALID",
    "SOURCE_REFERENCE_KIND_INVALID",
    "SOURCE_REFERENCE_VALUE_INVALID",
    "SOURCE_ENTITY_MISSING",
    "SOURCE_USE_MISSING",
    "SOURCE_ROLE_NOT_APPROVED",
    "SOURCE_ROLE_DECISION_MISSING",
    "SOURCE_BASIS_LOCATOR_MISSING",
    "SOURCE_BASIS_CHECKED_MISSING",
    "SOURCE_SOURCE_ITEM_MISSING",
    "SOURCE_SOURCE_LOCATOR_MISSING",
    "SOURCE_SOURCE_BASIS_MISSING",
    "SOURCE_MATCH_REL_INVALID",
    "SOURCE_MATCH_BASIS_MISSING",
    "SOURCE_STABLE_ID_CHANGED",
    "SOURCE_HISTORY_NOT_APPEND_ONLY",
    "SOURCE_OBLIGATION_REOPENED",
    "SOURCE_OBLIGATION_TARGET_MISSING",
    "SOURCE_DECISION_MISSING",
    "SOURCE_LEGACY_FIELD",
    "SOURCE_INDEX_MISMATCH",
    "SOURCE_PROBE_FORMAL_WRITE",
    "SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED",
    "SOURCE_CUTOVER_MANIFEST_INVALID",
    "SOURCE_DECISION_DELIVERY_MISSING",
    "SOURCE_DECISION_PATCH_CONFLICT",
)


class SourceContractTests(unittest.TestCase):
    def source_model(self):
        try:
            return importlib.import_module("scripts.source_model")
        except ModuleNotFoundError as error:
            self.fail(f"source governance contract is missing: {error}")

    def test_public_types_have_exact_fields(self):
        model = self.source_model()
        self.assertEqual(("code", "file", "record", "field_path", "message"),
                         model.Issue._fields)
        self.assertEqual(("kind", "file", "record", "field_path", "value"),
                         model.ReferenceUse._fields)
        self.assertEqual(("identity", "field", "value", "qid"),
                         model.DecisionPatch._fields)
        self.assertEqual(("basis", "source", "match", "external_group"),
                         get_args(model.ReferenceKind))

    def test_validate_references_has_exact_signature(self):
        model = self.source_model()
        self.assertEqual({
            "root": Path,
            "references": Sequence[model.ReferenceUse],
            "return": List[model.Issue],
        }, get_type_hints(model.validate_references))

    def test_schema_ids_are_exact(self):
        self.assertEqual(EXPECTED_SCHEMA_IDS, self.source_model().SCHEMA_IDS)

    def test_role_qualifications_are_exact(self):
        self.assertEqual({
            "basis": None,
            "source": "structure",
            "match": "mapping",
            "external_group": "structure",
        }, self.source_model().ROLE_QUALIFICATIONS)

    def test_error_codes_are_exact_and_stable(self):
        self.assertEqual(EXPECTED_ERROR_CODES, self.source_model().ERROR_CODES)


if __name__ == "__main__":
    unittest.main()
