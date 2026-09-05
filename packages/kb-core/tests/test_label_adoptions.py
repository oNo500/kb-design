"""Protect the authorized write set, beyond label-basis shape validation."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from kb_core.label_adoptions import apply_adoptions, load_adoptions


class LabelAdoptionTests(unittest.TestCase):
    def setUp(self):
        self.approval = "design/decisions/structured-label-basis.md#批次授权"
        self.basis = {"level": 5, "model": {
            "name": "GPT-6", "date": "2026-09-05", "rationale": "数学概念。",
            "approval": self.approval,
        }}
        self.record = {"id": "mathematics", "label": {"zh": "数学", "en": "mathematics"},
                       "scope": "数学", "status": "active", "basis": {
                           "zh": {"level": 1, "references": [{"source": "gbt-13745", "locator": "110"}]}}}
        self.adoption = {"accept": True, "label": "数学", "basis": self.basis,
                         "original": {"en": "mathematics", "scope": "数学"}}

    def test_missing_label_batch_cannot_downgrade_existing_evidence(self):
        before = copy.deepcopy(self.record)
        with self.assertRaisesRegex(ValueError, "existing.*basis"):
            apply_adoptions([self.record], "topics", {"topics/mathematics/zh": self.adoption}, {"gbt-13745"})
        self.assertEqual(before, self.record)

    def test_declared_authorization_must_match_the_supported_batch(self):
        for declared, embedded in [("design/decisions/nonexistent.md#approval", "design/decisions/nonexistent.md#approval"),
                                   (self.approval, "design/decisions/other.md#approval")]:
            with self.subTest(declared=declared, embedded=embedded), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "data/inputs/topics").mkdir(parents=True)
                adopted = copy.deepcopy(self.adoption)
                adopted["basis"]["model"]["approval"] = embedded
                (root / "data/inputs/topics/label-adoptions.json").write_text(json.dumps({
                    "authorization": declared, "records": {"topics/mathematics/zh": adopted}}))
                with self.assertRaisesRegex(ValueError, "authorization"):
                    load_adoptions(root)


if __name__ == "__main__":
    unittest.main()
