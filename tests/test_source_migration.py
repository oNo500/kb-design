import hashlib
import json
import pathlib
import tempfile
import unittest

from scripts.apply_source_migration import ApplyResult, apply_migration
from scripts.plan_source_migration import build_migration_plan
from scripts.source_model import load_decision_patches


ROOT = pathlib.Path(__file__).resolve().parents[1]
FROZEN_FIXTURE_ROOT = (
    ROOT / "tests" / "fixtures" / "governance-frozen-2026-08-31"
)
INPUT = FROZEN_FIXTURE_ROOT
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"
DECISIONS = FIXTURES / "decisions"
BLOCKED_PLAN = FIXTURES / "blocked-plan"
REPLACEMENT = FIXTURES / "replacement-decisions"


def all_plan_rows(plan):
    return [
        row
        for name in sorted(plan["ledgers"])
        for row in plan["ledgers"][name]["rows"]
    ]


def value_sha256(value):
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def expected_patch_signatures(directory):
    patches = load_decision_patches(sorted(directory.glob("source-*.md")))
    return sorted(
        (row.qid, row.identity, row.field, value_sha256(row.value))
        for row in patches
    )


def actual_patch_signatures(plan):
    signatures = []
    for row in all_plan_rows(plan):
        for trace in row["decision_trace"]:
            signatures.append(
                (trace["qid"], row["identity"], trace["field"], trace["value_sha256"])
            )
    for identity, control in plan["controls"].items():
        for trace in control["decision_trace"]:
            signatures.append(
                (trace["qid"], identity, trace["field"], trace["value_sha256"])
            )
    return sorted(signatures)


class SourceMigrationTests(unittest.TestCase):
    def plan(self):
        return build_migration_plan(FROZEN_FIXTURE_ROOT, INPUT, DECISIONS)

    def test_all_eighteen_input_hashes_are_verified(self):
        self.assertEqual(18, self.plan()["verified_hash_count"])

    def test_frozen_identity_counts_are_exact(self):
        self.assertEqual(
            {
                "entities": 138,
                "uses": 47,
                "basis": 1501,
                "source": 726,
                "match": 756,
                "origin": 19,
            },
            self.plan()["counts"],
        )

    def test_entity_inventory_keeps_31_and_107_separate(self):
        self.assertEqual((31, 107), tuple(self.plan()["entity_partitions"]))

    def test_source_inventory_keeps_692_24_8_2_separate(self):
        self.assertEqual((692, 24, 8, 2), tuple(self.plan()["source_partitions"]))

    def test_identity_ambiguities_are_not_merged(self):
        self.assertEqual(16, self.plan()["blocked_identity_ambiguities"])

    def test_blocked_decision_patches_prevent_any_candidate_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = pathlib.Path(tmp) / "candidate"
            result = apply_migration(ROOT, BLOCKED_PLAN, output)
            self.assertTrue(result.blocked)
            self.assertFalse(output.exists())

    def test_missing_decision_stops_before_output_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = pathlib.Path(tmp) / "plan"
            with self.assertRaisesRegex(
                ValueError, "SOURCE_DECISION_DELIVERY_MISSING"
            ):
                build_migration_plan(
                    FROZEN_FIXTURE_ROOT,
                    INPUT,
                    FIXTURES / "missing-decisions",
                    output,
                )
            self.assertFalse(output.exists())

    def test_recommended_patches_are_consumed_once(self):
        self.assertEqual(
            expected_patch_signatures(DECISIONS),
            actual_patch_signatures(self.plan()),
        )

    def test_replacement_patches_rebuild_fields_without_duplicate_rows(self):
        plan = build_migration_plan(FROZEN_FIXTURE_ROOT, INPUT, REPLACEMENT)
        self.assertEqual(
            expected_patch_signatures(REPLACEMENT), actual_patch_signatures(plan)
        )
        self.assertEqual(3187, len(all_plan_rows(plan)))
        self.assertNotEqual(
            actual_patch_signatures(self.plan()), actual_patch_signatures(plan)
        )

    def test_duplicate_identity_field_patch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_PATCH_CONFLICT"):
            build_migration_plan(
                FROZEN_FIXTURE_ROOT,
                INPUT,
                FIXTURES / "duplicate-field-decisions",
            )

    def test_q_field_ownership_violation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_PATCH_CONFLICT"):
            build_migration_plan(
                FROZEN_FIXTURE_ROOT,
                INPUT,
                FIXTURES / "wrong-field-decisions",
            )

    def test_q_identity_domain_violation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_PATCH_CONFLICT"):
            build_migration_plan(
                FROZEN_FIXTURE_ROOT,
                INPUT,
                FIXTURES / "wrong-domain-decisions",
            )

    def test_all_qids_are_covered_by_patches(self):
        qids = {signature[0] for signature in actual_patch_signatures(self.plan())}
        self.assertEqual({f"Q{number:02d}" for number in range(1, 26)}, qids)

    def test_plan_is_deterministic(self):
        self.assertEqual(self.plan(), self.plan())

    def test_apply_rejects_output_inside_formal_root(self):
        with self.assertRaises(ValueError):
            apply_migration(ROOT, BLOCKED_PLAN, ROOT / "vocab")

    def test_apply_returns_one_apply_result_and_uses_absent_child_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = pathlib.Path(tmp) / "candidate"
            result = apply_migration(
                FIXTURES / "candidate-input", FIXTURES / "candidate-plan", output
            )
            self.assertIsInstance(result, ApplyResult)
            self.assertTrue(output.is_dir())
            self.assertTrue(all(isinstance(path, str) for path in result.written))


if __name__ == "__main__":
    unittest.main()
