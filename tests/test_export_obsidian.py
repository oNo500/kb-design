import contextlib
import datetime
import hashlib
import json
import pathlib
import re
import shutil
import tempfile
import unittest

import yaml

import scripts.export_obsidian as export_obsidian
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

    def test_topic_basis_requires_both_language_decisions(self):
        self.assert_invalid_input(
            "vocab/topics.yaml",
            "mathematics",
            "concepts[mathematics].basis.en",
            lambda document: find_record(document, "concepts", "mathematics")["basis"].pop("en"),
        )

    def test_topic_source_and_match_are_optional(self):
        baseline_files = build_content_files(ROOT)
        baseline_properties, baseline_body = split_note(
            baseline_files["KB/Topics/mathematics.md"]
        )

        cases = (
            (
                "source",
                lambda document: find_record(document, "concepts", "mathematics").pop("source"),
            ),
            (
                "match",
                lambda document: find_record(document, "concepts", "mathematics").pop("match"),
            ),
        )
        for field, mutate in cases:
            with self.subTest(field), mutated_repository(
                "vocab/topics.yaml", mutate
            ) as repo_root:
                files = build_content_files(repo_root)
                properties, body = split_note(files["KB/Topics/mathematics.md"])
                self.assertEqual(847, len(files))
                if field == "source":
                    expected_properties = dict(baseline_properties)
                    expected_properties.pop("kb_source")
                    self.assertEqual(expected_properties, properties)
                    self.assertEqual(baseline_body, body)
                else:
                    expected_body = (
                        baseline_body.split("\n## 外部映射\n", 1)[0].rstrip("\n")
                        + "\n"
                    )
                    self.assertEqual(baseline_properties, properties)
                    self.assertEqual(expected_body, body)

    def test_entity_basis_is_optional(self):
        baseline_files = build_content_files(ROOT)
        baseline_properties, baseline_body = split_note(
            baseline_files["KB/Entities/claude-code.md"]
        )

        with mutated_repository(
            "vocab/entities.yaml",
            lambda document: find_record(
                document, "entities", "claude-code"
            ).pop("basis"),
        ) as repo_root:
            files = build_content_files(repo_root)
        properties, body = split_note(files["KB/Entities/claude-code.md"])
        before_basis, after_basis = baseline_body.split("\n## 形式依据\n", 1)
        _, after_mapping = after_basis.split("\n## 外部映射\n", 1)
        expected_body = before_basis + "\n## 外部映射\n" + after_mapping

        self.assertEqual(847, len(files))
        self.assertEqual(baseline_properties, properties)
        self.assertEqual(expected_body, body)

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

    def test_write_export_is_deterministic_and_manifest_is_complete(self):
        content_files = build_content_files(ROOT)
        manifest_bytes = export_obsidian.build_manifest(ROOT, content_files)

        with tempfile.TemporaryDirectory() as temporary:
            parent = pathlib.Path(temporary)
            first = parent / "first"
            second = parent / "second"
            second.mkdir()

            first_summary = export_obsidian.write_export(ROOT, first)
            second_summary = export_obsidian.write_export(ROOT, second)

            first_paths = sorted(
                path.relative_to(first).as_posix()
                for path in first.rglob("*")
                if path.is_file()
            )
            second_paths = sorted(
                path.relative_to(second).as_posix()
                for path in second.rglob("*")
                if path.is_file()
            )
            self.assertEqual(first_paths, second_paths)
            self.assertEqual(848, len(first_paths))
            for relative_path in first_paths:
                self.assertEqual(
                    (first / relative_path).read_bytes(),
                    (second / relative_path).read_bytes(),
                    relative_path,
                )

            self.assertEqual(manifest_bytes, (first / "manifest.json").read_bytes())
            manifest = json.loads(manifest_bytes)
            self.assertEqual(
                {
                    "content_files",
                    "content_sha256",
                    "exporter_sha256",
                    "files",
                    "inputs",
                    "object_counts",
                    "schema",
                    "schema_version",
                    "total_files",
                },
                set(manifest),
            )
            self.assertEqual("kb-design-obsidian-export", manifest["schema"])
            self.assertEqual(1, manifest["schema_version"])
            self.assertEqual(
                {
                    "array": 24,
                    "entity": 61,
                    "form": 16,
                    "genre": 5,
                    "source": 31,
                    "topic": 700,
                    "type": 6,
                },
                manifest["object_counts"],
            )
            self.assertEqual(847, manifest["content_files"])
            self.assertEqual(848, manifest["total_files"])
            self.assertEqual(847, len(manifest["files"]))
            self.assertNotIn("manifest.json", {entry["path"] for entry in manifest["files"]})

            input_paths = (
                "vocab/topics.yaml",
                "vocab/entities.yaml",
                "vocab/sources.yaml",
                "vocab/types.yaml",
                "vocab/genres.yaml",
                "vocab/forms.yaml",
            )
            self.assertEqual(
                [
                    {
                        "path": path,
                        "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
                        "version": "2026.08",
                    }
                    for path in input_paths
                ],
                manifest["inputs"],
            )
            self.assertEqual(
                hashlib.sha256(pathlib.Path(export_obsidian.__file__).read_bytes()).hexdigest(),
                manifest["exporter_sha256"],
            )

            directory_objects = {
                "Arrays": "array",
                "Entities": "entity",
                "Forms": "form",
                "Genres": "genre",
                "Sources": "source",
                "Topics": "topic",
                "Types": "type",
            }
            expected_entries = []
            content_digest_input = bytearray()
            for path, content in sorted(content_files.items()):
                sha256 = hashlib.sha256(content).hexdigest()
                if path == "README.md":
                    object_kind = "index"
                elif path.endswith(".base"):
                    object_kind = "base"
                else:
                    object_kind = directory_objects[pathlib.PurePosixPath(path).parts[1]]
                expected_entries.append(
                    {
                        "id": pathlib.PurePosixPath(path).stem,
                        "object": object_kind,
                        "path": path,
                        "sha256": sha256,
                    }
                )
                content_digest_input.extend(f"{path}\0{sha256}\n".encode("utf-8"))
            self.assertEqual(expected_entries, manifest["files"])
            self.assertEqual(
                hashlib.sha256(content_digest_input).hexdigest(),
                manifest["content_sha256"],
            )
            self.assertEqual(
                json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
                + b"\n",
                manifest_bytes,
            )
            expected_summary_keys = {"content_files", "content_sha256", "output", "total_files"}
            self.assertEqual(expected_summary_keys, set(first_summary))
            self.assertEqual(expected_summary_keys, set(second_summary))
            self.assertEqual(str(first.resolve()), first_summary["output"])
            self.assertEqual(str(second.resolve()), second_summary["output"])
            self.assertEqual(manifest["content_sha256"], first_summary["content_sha256"])
            self.assertEqual(manifest["content_sha256"], second_summary["content_sha256"])

    def test_write_export_rejects_nonempty_output_without_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = pathlib.Path(temporary)
            output = parent / "nonempty"
            output.mkdir()
            sentinel = output / "sentinel.bin"
            sentinel.write_bytes(b"keep-nonempty")
            before = sorted(path.name for path in parent.iterdir())

            with self.assertRaises(ExportError):
                export_obsidian.write_export(ROOT, output)

            self.assertEqual(b"keep-nonempty", sentinel.read_bytes())
            self.assertEqual(["sentinel.bin"], sorted(path.name for path in output.iterdir()))
            self.assertEqual(before, sorted(path.name for path in parent.iterdir()))

        with tempfile.TemporaryDirectory() as temporary:
            parent = pathlib.Path(temporary)
            linked_directory = parent / "linked"
            linked_directory.mkdir()
            sentinel = linked_directory / "sentinel.bin"
            sentinel.write_bytes(b"keep-symlink")
            output = parent / "output"
            output.symlink_to(linked_directory, target_is_directory=True)
            before = sorted(path.name for path in parent.iterdir())

            with self.assertRaises(ExportError):
                export_obsidian.write_export(ROOT, output)

            self.assertTrue(output.is_symlink())
            self.assertEqual(b"keep-symlink", sentinel.read_bytes())
            self.assertEqual(before, sorted(path.name for path in parent.iterdir()))

        with mutated_repository("vocab/topics.yaml", lambda document: None) as repo_root:
            sentinel = repo_root / "vocab" / "sentinel.bin"
            sentinel.write_bytes(b"keep-forbidden")
            output = repo_root / "vocab" / "output"

            with self.assertRaises(ExportError):
                export_obsidian.write_export(repo_root, output)

            self.assertFalse(output.exists())
            self.assertEqual(b"keep-forbidden", sentinel.read_bytes())
            self.assertFalse(any(path.name.startswith(".output.tmp-") for path in output.parent.iterdir()))

    def test_write_export_rejects_dangling_reference_without_target(self):
        def mutate(document):
            find_record(document, "concepts", "security")["broader"] = ["does-not-exist"]

        with mutated_repository("vocab/topics.yaml", mutate) as repo_root:
            output = repo_root / "output"
            with self.assertRaises(ExportError):
                export_obsidian.write_export(repo_root, output)
            self.assertFalse(output.exists())
            self.assertFalse(any(path.name.startswith(".output.tmp-") for path in repo_root.iterdir()))

    def test_write_export_rejects_unknown_field_without_target(self):
        def mutate(document):
            find_record(document, "concepts", "security")["unknown_field"] = "blocked"

        with mutated_repository("vocab/topics.yaml", mutate) as repo_root:
            output = repo_root / "output"
            with self.assertRaises(ExportError):
                export_obsidian.write_export(repo_root, output)
            self.assertFalse(output.exists())
            self.assertFalse(any(path.name.startswith(".output.tmp-") for path in repo_root.iterdir()))


if __name__ == "__main__":
    unittest.main()
