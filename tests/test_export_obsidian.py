import contextlib
import datetime
import pathlib
import re
import shutil
import tempfile
import unittest

import yaml

from scripts.export_obsidian import ExportError, build_content_files


ROOT = pathlib.Path(__file__).resolve().parents[1]
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")


def split_note(content):
    text = content.decode("utf-8")
    _, frontmatter, body = text.split("---\n", 2)
    return yaml.safe_load(frontmatter), body


@contextlib.contextmanager
def mutated_repository(relative_path, mutate):
    with tempfile.TemporaryDirectory() as temporary:
        repo_root = pathlib.Path(temporary)
        shutil.copytree(ROOT / "vocab", repo_root / "vocab")
        input_path = repo_root / relative_path
        document = yaml.safe_load(input_path.read_text(encoding="utf-8"))
        mutate(document)
        input_path.write_text(
            yaml.safe_dump(document, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        yield repo_root


def find_record(document, collection, object_id):
    return next(record for record in document[collection] if record["id"] == object_id)


class ExportObsidianTests(unittest.TestCase):
    def assert_invalid_input(self, relative_path, object_id, field_path, mutate):
        with mutated_repository(relative_path, mutate) as repo_root:
            with self.assertRaises(ExportError) as raised:
                build_content_files(repo_root)
        message = str(raised.exception)
        self.assertIn(relative_path, message)
        self.assertIn(f"object {object_id}", message)
        self.assertIn(field_path, message)

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

    def test_invalid_formal_field_shapes_are_blocked_with_context(self):
        cases = (
            (
                "match missing id",
                "vocab/topics.yaml",
                "security",
                "concepts[security].match[0].id",
                lambda document: find_record(document, "concepts", "security")["match"][0].pop("id"),
            ),
            (
                "match missing rel",
                "vocab/topics.yaml",
                "security",
                "concepts[security].match[0].rel",
                lambda document: find_record(document, "concepts", "security")["match"][0].pop("rel"),
            ),
            (
                "role scalar",
                "vocab/sources.yaml",
                "cs2023",
                "sources[cs2023].role",
                lambda document: find_record(document, "sources", "cs2023").update(role="mapping"),
            ),
            (
                "reference list scalar",
                "vocab/topics.yaml",
                "security",
                "concepts[security].broader",
                lambda document: find_record(document, "concepts", "security").update(broader="computing"),
            ),
            (
                "role element non-string",
                "vocab/sources.yaml",
                "cs2023",
                "sources[cs2023].role[1]",
                lambda document: find_record(document, "sources", "cs2023").update(role=["mapping", 7]),
            ),
            (
                "match scalar non-string",
                "vocab/topics.yaml",
                "security",
                "concepts[security].match[0].id",
                lambda document: find_record(document, "concepts", "security")["match"][0].update(id=7),
            ),
        )

        for name, relative_path, object_id, field_path, mutate in cases:
            with self.subTest(name):
                self.assert_invalid_input(relative_path, object_id, field_path, mutate)

    def test_form_internal_arrays_are_preserved_and_validated(self):
        readme = build_content_files(ROOT)["README.md"].decode("utf-8")
        with self.subTest("README table"):
            self.assertIn("## 载体数组", readme)
            self.assertIn("| id | superordinate | source |", readme)
            self.assertIn("| forms-presentation | forms | lom |", readme)
            self.assertIn("| forms-activity | forms | lom |", readme)

        cases = (
            (
                "source",
                "arrays[forms-presentation].source",
                lambda document: document["arrays"][0].update(source="does-not-exist"),
            ),
            (
                "superordinate",
                "arrays[forms-presentation].superordinate",
                lambda document: document["arrays"][0].update(superordinate="does-not-exist"),
            ),
        )
        for name, field_path, mutate in cases:
            with self.subTest(name):
                self.assert_invalid_input(
                    "vocab/forms.yaml",
                    "forms-presentation",
                    field_path,
                    mutate,
                )

    def test_object_notes_and_bases_expose_formal_display_labels(self):
        files = build_content_files(ROOT)
        object_paths = sorted(
            path
            for path in files
            if path.startswith("KB/") and path.endswith(".md")
        )

        with self.subTest("all object notes"):
            missing = []
            non_scalar = []
            for path in object_paths:
                properties, _ = split_note(files[path])
                if "kb_label" not in properties:
                    missing.append(path)
                elif not isinstance(properties["kb_label"], str):
                    non_scalar.append(path)
            self.assertEqual(843, len(object_paths))
            self.assertEqual([], missing)
            self.assertEqual([], non_scalar)

        expected_labels = {
            "KB/Topics/security.md": "Security",
            "KB/Arrays/security-cs2023.md": "security-cs2023",
            "KB/Entities/cs2023.md": "计算机科学课程 2023",
            "KB/Sources/cs2023.md": "cs2023",
            "KB/Types/tutorial.md": "教程",
            "KB/Forms/diagram.md": "Diagram",
        }
        for path, expected in expected_labels.items():
            with self.subTest(path):
                properties, _ = split_note(files[path])
                self.assertEqual(expected, properties["kb_label"])

        expected_orders = {
            "KB/Views/Topics.base": ["kb_id", "kb_label", "kb_status", "kb_broader"],
            "KB/Views/Entities.base": ["kb_id", "kb_label", "kb_status", "kb_kind"],
            "KB/Views/Sources.base": ["kb_id", "kb_label", "kb_entity", "kb_roles"],
        }
        for path, expected in expected_orders.items():
            with self.subTest(path):
                base = yaml.safe_load(files[path])
                self.assertEqual(expected, base["views"][0]["order"])


if __name__ == "__main__":
    unittest.main()
