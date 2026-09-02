from __future__ import annotations

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


FIRST_UUID = "123e4567-e89b-42d3-a456-426614174000"
SECOND_UUID = "223e4567-e89b-42d3-a456-426614174001"


class CreateContentTests(unittest.TestCase):
    """Creation must publish only one validated draft with a stable identity."""

    def setUp(self) -> None:
        from kb_obsidian.design_source import DesignSnapshot

        self.temporary = tempfile.TemporaryDirectory()
        self.vault = Path(self.temporary.name) / "vault"
        (self.vault / "Content").mkdir(parents=True)
        self.snapshot = DesignSnapshot(
            root=Path("/design"),
            commit="design-commit",
            documents={
                "topics": {
                    "concepts": (
                        {"id": "controlled-vocabulary", "label": {"zh": "受控词表", "en": "Controlled vocabulary"}, "status": "active"},
                        {"id": "old-topic", "label": {"zh": "旧主题", "en": "Old topic"}, "status": "deprecated"},
                    )
                },
                "entities": {
                    "entities": (
                        {"id": "obsidian", "label": {"zh": "Obsidian", "en": "Obsidian"}, "kind": "software", "status": "active"},
                        {"id": "rfc-9562", "label": {"zh": "RFC 9562", "en": "RFC 9562"}, "kind": "standard", "status": "active"},
                    )
                },
                "sources": {"sources": ()},
                "types": {"types": ({"id": "explanation", "label": {"zh": "解释", "en": "Explanation"}, "status": "active"},)},
                "genres": {"genres": ({"id": "analysis", "label": {"zh": "分析", "en": "Analysis"}, "status": "active"},)},
                "forms": {"forms": ({"id": "diagram", "label": {"zh": "图示", "en": "Diagram"}, "status": "unassigned"},)},
            },
            input_hashes={},
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_creates_uuid_path_title_alias_and_controlled_links(self) -> None:
        """Dropping the UUID, title metadata, or a target label must invalidate the new note."""
        from kb_obsidian.create_content import create_content

        path = create_content(
            self.snapshot,
            self.vault,
            title="主题目录",
            type_id="explanation",
            genre_id="analysis",
            subjects=["controlled-vocabulary"],
            form="diagram",
            level="analyze",
            entities=["obsidian"],
            references=["rfc-9562"],
            today=lambda: dt.date(2026, 9, 3),
            uuid_factory=lambda: UUID(FIRST_UUID),
        )

        self.assertEqual(self.vault.resolve() / "Content" / f"{FIRST_UUID}.md", path)
        properties, heading = self._read_note(path)
        self.assertEqual(FIRST_UUID, properties["kb_id"])
        self.assertEqual("主题目录", properties["title"])
        self.assertEqual(["主题目录"], properties["aliases"])
        self.assertEqual("[[KB/Types/explanation|解释]]", properties["kb_type"])
        self.assertEqual("[[KB/Genres/analysis|分析]]", properties["kb_genre"])
        self.assertEqual(["[[KB/Topics/controlled-vocabulary|受控词表]]"], properties["kb_subjects"])
        self.assertEqual("[[KB/Forms/diagram|图示]]", properties["kb_form"])
        self.assertEqual(["[[KB/Entities/obsidian|Obsidian]]"], properties["kb_entities"])
        self.assertEqual(["[[KB/Entities/rfc-9562|RFC 9562]]"], properties["kb_references"])
        self.assertEqual("2026-09-03", properties["kb_created"])
        self.assertEqual("draft", properties["kb_status"])
        self.assertEqual("zh", properties["kb_language"])
        self.assertEqual("主题目录", heading)

    def test_retries_a_colliding_uuid_without_overwriting_the_existing_note(self) -> None:
        """Publishing over an existing identity would destroy a user-owned content unit."""
        from kb_obsidian.create_content import create_content

        existing = self.vault / "Content" / f"{FIRST_UUID}.md"
        existing.write_bytes(b"do not replace\n")
        identifiers = iter((UUID(FIRST_UUID), UUID(SECOND_UUID)))

        path = create_content(
            self.snapshot,
            self.vault,
            title="主题目录",
            type_id="explanation",
            genre_id="analysis",
            subjects=["controlled-vocabulary"],
            uuid_factory=lambda: next(identifiers),
        )

        self.assertEqual(self.vault.resolve() / "Content" / f"{SECOND_UUID}.md", path)
        self.assertEqual(b"do not replace\n", existing.read_bytes())

    def test_rejects_invalid_arguments_and_unsafe_vault_before_writing(self) -> None:
        """Accepting bad controlled input or a non-vault target would create an invalid user file."""
        from kb_obsidian.create_content import create_content
        from kb_obsidian.errors import ApplicationError

        invalid_requests = (
            {"title": ""},
            {"type_id": "missing"},
            {"genre_id": "missing"},
            {"subjects": []},
            {"subjects": ["old-topic"]},
            {"form": "missing"},
            {"level": "invent"},
            {"entities": ["missing"]},
            {"references": ["obsidian"]},
            {"language": "fr"},
        )
        before = self._content_bytes()
        for overrides in invalid_requests:
            with self.subTest(overrides=overrides), self.assertRaises(ApplicationError):
                request = {
                    "title": "主题目录",
                    "type_id": "explanation",
                    "genre_id": "analysis",
                    "subjects": ["controlled-vocabulary"],
                    "uuid_factory": lambda: UUID(FIRST_UUID),
                }
                request.update(overrides)
                create_content(
                    self.snapshot,
                    self.vault,
                    **request,
                )
            self.assertEqual(before, self._content_bytes())

        non_vault = Path(self.temporary.name) / "not-a-vault"
        non_vault.mkdir()
        with self.assertRaises(ApplicationError):
            create_content(
                self.snapshot,
                non_vault,
                title="主题目录",
                type_id="explanation",
                genre_id="analysis",
                subjects=["controlled-vocabulary"],
                uuid_factory=lambda: UUID(FIRST_UUID),
            )
        self.assertEqual([], list(non_vault.iterdir()))

    def test_removes_its_temporary_file_when_task_four_readback_fails(self) -> None:
        """A readback failure must not leave a final or temporary content file behind."""
        from kb_obsidian.create_content import create_content
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.validation import ValidationResult

        with patch("kb_obsidian.create_content.validate_content", return_value=ValidationResult((), ())) as readback:
            with self.assertRaisesRegex(ApplicationError, "readback"):
                create_content(
                    self.snapshot,
                    self.vault,
                    title="主题目录",
                    type_id="explanation",
                    genre_id="analysis",
                    subjects=["controlled-vocabulary"],
                    uuid_factory=lambda: UUID(FIRST_UUID),
                )

        self.assertTrue(readback.called)
        self.assertEqual({}, self._content_bytes())

    def test_removes_the_final_link_when_atomic_replace_fails(self) -> None:
        """A failed final rename must not leave the newly linked draft visible in Content."""
        from kb_obsidian.create_content import create_content
        from kb_obsidian.errors import ApplicationError

        with patch("kb_obsidian.create_content.os.replace", side_effect=OSError("blocked")):
            with self.assertRaisesRegex(ApplicationError, "finalize"):
                create_content(
                    self.snapshot,
                    self.vault,
                    title="主题目录",
                    type_id="explanation",
                    genre_id="analysis",
                    subjects=["controlled-vocabulary"],
                    uuid_factory=lambda: UUID(FIRST_UUID),
                )

        self.assertEqual({}, self._content_bytes())

    def _read_note(self, path: Path) -> tuple[dict[str, object], str]:
        text = path.read_text(encoding="utf-8")
        _, frontmatter, markdown = text.split("---\n", 2)
        properties = yaml.safe_load(frontmatter)
        self.assertIsInstance(properties, dict)
        return properties, markdown.removeprefix("# ").splitlines()[0]

    def _content_bytes(self) -> dict[str, bytes]:
        return {
            path.name: path.read_bytes()
            for path in (self.vault / "Content").iterdir()
            if path.is_file()
        }


if __name__ == "__main__":
    unittest.main()
