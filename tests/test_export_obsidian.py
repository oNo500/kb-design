import datetime
import pathlib
import re
import unittest

import yaml

from scripts.export_obsidian import build_content_files


ROOT = pathlib.Path(__file__).resolve().parents[1]
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")


def split_note(content):
    text = content.decode("utf-8")
    _, frontmatter, body = text.split("---\n", 2)
    return yaml.safe_load(frontmatter), body


class ExportObsidianTests(unittest.TestCase):
    def test_build_content_files_maps_every_formal_object(self):
        files = build_content_files(ROOT)

        self.assertEqual(847, len(files))
        self.assertEqual(
            {
                "KB/Topics": 700,
                "KB/Arrays": 24,
                "KB/Entities": 61,
                "KB/Sources": 31,
                "KB/Types": 6,
                "KB/Genres": 5,
                "KB/Forms": 16,
            },
            {
                directory: sum(
                    path.startswith(f"{directory}/") and path.endswith(".md")
                    for path in files
                )
                for directory in (
                    "KB/Topics",
                    "KB/Arrays",
                    "KB/Entities",
                    "KB/Sources",
                    "KB/Types",
                    "KB/Genres",
                    "KB/Forms",
                )
            },
        )
        self.assertEqual(
            {
                "README.md",
                "KB/Views/Topics.base",
                "KB/Views/Entities.base",
                "KB/Views/Sources.base",
            },
            set(files) - {path for path in files if path.endswith(".md") and path != "README.md"},
        )

    def test_topic_note_uses_flat_properties_and_resolvable_links(self):
        files = build_content_files(ROOT)
        properties, body = split_note(files["KB/Topics/security.md"])

        scalar_types = (str, int, float, bool, datetime.date, datetime.datetime)
        for path, content in files.items():
            if not path.startswith("KB/") or not path.endswith(".md"):
                continue
            note_properties, _ = split_note(content)
            for key, value in note_properties.items():
                is_flat = isinstance(value, scalar_types) or (
                    isinstance(value, list)
                    and all(isinstance(item, scalar_types) for item in value)
                )
                self.assertTrue(is_flat, f"nested property at {path}:{key}")

        self.assertEqual("security", properties["kb_id"])
        self.assertEqual("topic", properties["kb_object"])
        self.assertEqual("active", properties["kb_status"])
        self.assertEqual(
            ["[[KB/Topics/computing|计算机科学技术]]"],
            properties["kb_broader"],
        )
        self.assertEqual([], properties.get("kb_arrays", []))
        self.assertNotIn("aliases", properties)
        self.assertIn("| zh | none |", body)
        self.assertIn("| en | source |", body)
        self.assertIn("| cs2023 | SEC | exactMatch |", body)

        unresolved = []
        for source_path, content in files.items():
            if not source_path.endswith(".md"):
                continue
            for target in WIKILINK.findall(content.decode("utf-8")):
                if f"{target}.md" not in files:
                    unresolved.append((source_path, target))
        self.assertEqual([], unresolved)


if __name__ == "__main__":
    unittest.main()
