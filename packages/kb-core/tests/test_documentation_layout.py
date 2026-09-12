import shutil
import tempfile
import unittest
from pathlib import Path

from kb_core.governance.check_term_usage import classify_markdown_path
from kb_core.source_model import _load_accepted_decisions
from kb_core.governance.term_validation import load_term_decisions
from test_source_v2_contract import write_fixture


class DocumentationLayoutTests(unittest.TestCase):
    def test_topic_paths_preserve_document_authority_classification(self):
        for path, expected in (
            ("docs/model/vocabulary/proposal-facet-field.md", "draft"),
            ("docs/model/sources/decision-source-approval.md", "history"),
            ("docs/model/vocabulary/reading-iso-25964.md", "source"),
            ("docs/model/vocabulary/topics.md", "formal"),
        ):
            with self.subTest(path=path):
                self.assertEqual(expected, classify_markdown_path(path))

    def test_relocated_decisions_keep_grants_and_duplicate_ids_stay_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, grant = write_fixture(root)
            legacy = root / "docs/decisions/source-approval.md"
            relocated = root / "docs/model/sources/decision-source-approval.md"
            relocated.parent.mkdir(parents=True)
            legacy.rename(relocated)
            proposal = relocated.with_name("proposal-source-other.md")
            shutil.copyfile(relocated, proposal)
            # A proposal containing copied accepted metadata cannot be a grant.
            for actual in (_load_accepted_decisions(root / "docs"), load_term_decisions(root)):
                self.assertEqual({grant["id"]: grant}, actual)
            duplicate = root / "docs/model/terminology/decision-source-copy.md"
            duplicate.parent.mkdir(parents=True)
            shutil.copyfile(relocated, duplicate)
            self.assertEqual({}, _load_accepted_decisions(root / "docs"))
            self.assertEqual({}, load_term_decisions(root))
