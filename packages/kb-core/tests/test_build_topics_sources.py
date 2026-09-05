import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[3]


def basis_leaves(document):
    return {
        f"concepts[{concept['id']}].basis.{language}": value
        for concept in document["concepts"]
        for language, value in concept["basis"].items()
    }


def build_topics_in_temporary_tree():
    with tempfile.TemporaryDirectory() as tmp:
        temporary_root = pathlib.Path(tmp)
        (temporary_root / "data" / "vocab").mkdir(parents=True)
        shutil.copy2(
            ROOT / "data" / "vocab" / "sources.yaml",
            temporary_root / "data" / "vocab" / "sources.yaml",
        )
        shutil.copytree(
            ROOT / "data" / "inputs" / "topics",
            temporary_root / "data" / "inputs" / "topics",
        )
        subprocess.run(
            [sys.executable, "-m", "kb_core.build_topics"],
            cwd=temporary_root,
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "KB_DESIGN_ROOT": str(temporary_root)},
        )
        return yaml.safe_load(
            (temporary_root / "data" / "vocab" / "topics.yaml").read_text(
                encoding="utf-8"
            )
        )


class BuildTopicsSourceTests(unittest.TestCase):
    def test_regeneration_leaves_no_parent_concept_unassigned(self):
        generated = build_topics_in_temporary_tree()
        parent_ids = {
            broader
            for concept in generated["concepts"]
            for broader in concept["broader"]
        }
        unassigned_parent_ids = sorted(
            concept["id"]
            for concept in generated["concepts"]
            if concept["id"] in parent_ids and concept["status"] == "unassigned"
        )

        self.maxDiff = None
        self.assertEqual([], unassigned_parent_ids)

    def test_regeneration_preserves_all_frozen_topic_basis_values(self):
        frozen = yaml.safe_load(
            (ROOT / "data" / "vocab" / "topics.yaml").read_text(encoding="utf-8")
        )
        generated = build_topics_in_temporary_tree()

        self.assertEqual(1400, len(basis_leaves(frozen)))
        self.assertEqual(basis_leaves(frozen), basis_leaves(generated))


if __name__ == "__main__":
    unittest.main()
