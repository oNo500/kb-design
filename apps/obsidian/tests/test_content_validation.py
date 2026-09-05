from __future__ import annotations

import dataclasses
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

UUID_A = "123e4567-e89b-42d3-a456-426614174000"
UUID_B = "223e4567-e89b-42d3-a456-426614174001"
UUID_C = "323e4567-e89b-42d3-a456-426614174002"
UUID_V1 = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"


class ContentValidationTests(unittest.TestCase):
    """Content validation must protect identity and controlled semantics without writes."""

    def setUp(self) -> None:
        from kb_obsidian.design_source import DesignSnapshot

        self.temporary = tempfile.TemporaryDirectory()
        self.vault = Path(self.temporary.name) / "vault"
        (self.vault / "content").mkdir(parents=True)
        self.vault_gate = patch(
            "kb_obsidian.validation.verify_vault",
            return_value=self.vault.resolve(),
        )
        self.vault_gate.start()
        self.snapshot = DesignSnapshot(
            root=Path("/design"),
            commit="design-commit",
            documents={
                "topics": {
                    "concepts": (
                        {"id": "security", "status": "active"},
                        {"id": "old-topic", "status": "deprecated"},
                    )
                },
                "entities": {
                    "entities": (
                        {"id": "obsidian", "kind": "software", "status": "active"},
                        {"id": "rfc-9562", "kind": "standard", "status": "active"},
                        {"id": "metadata-paper", "kind": "publication", "status": "active"},
                    )
                },
                "sources": {"sources": ()},
                "types": {"types": ({"id": "tutorial", "status": "active"},)},
                "genres": {"genres": ({"id": "analysis", "status": "active"},)},
                "forms": {"forms": ({"id": "diagram", "status": "unassigned"},)},
            },
            input_hashes={},
        )

    def tearDown(self) -> None:
        self.vault_gate.stop()
        self.temporary.cleanup()

    def test_valid_content_parses_all_sixteen_fields_as_immutable_data(self) -> None:
        """Removing any modeled field check must not let the complete contract drift silently."""
        from kb_obsidian.validation import validate_content

        self._write_note(
            UUID_A,
            title="旧内容",
            kb_form="[[kb/forms/diagram|Diagram]]",
            kb_level="analyze",
            kb_entities=["[[kb/entities/obsidian|Obsidian]]"],
            kb_source=f"[[content/{UUID_B}|来源内容]]",
            kb_references=["[[kb/entities/rfc-9562|RFC 9562]]"],
            kb_modified="2026-09-03",
            kb_status="deprecated",
            kb_is_replaced_by=f"[[content/{UUID_C}|新内容]]",
            kb_relation=[f"[[content/{UUID_B}|相关内容]]"],
            kb_language="en",
        )
        self._write_note(UUID_B, title="来源内容", kb_relation=[f"[[content/{UUID_A}|旧内容]]"])
        self._write_note(UUID_C, title="新内容")

        result = validate_content(self.snapshot, self.vault)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual((UUID_A, UUID_B, UUID_C), tuple(record.identifier for record in result.records))
        record = result.records[0]
        self.assertEqual("旧内容", record.title)
        self.assertEqual("正文。\n", record.body)
        self.assertEqual(
            {
                "kb_id",
                "title",
                "kb_type",
                "kb_genre",
                "kb_form",
                "kb_level",
                "kb_subjects",
                "kb_entities",
                "kb_source",
                "kb_references",
                "kb_created",
                "kb_modified",
                "kb_status",
                "kb_is_replaced_by",
                "kb_relation",
                "kb_language",
            },
            set(record.properties) - {"aliases"},
        )
        with self.assertRaises(TypeError):
            record.properties["title"] = "改写"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            record.title = "改写"

    def test_title_alias_or_stem_drift_is_reported_without_rewrite(self) -> None:
        """Changing either human lookup metadata or stable path must invalidate, never repair, a note."""
        from kb_obsidian.validation import validate_content

        note = self._write_note(UUID_B, identifier=UUID_A, title="标题", aliases=["旧标题"])
        before = note.read_bytes()

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual(
            {"content.title_mismatch", "content.path_mismatch"},
            {issue.code for issue in result.issues},
        )
        self.assertEqual(before, note.read_bytes())
        self.assertFalse(result.is_valid)
        self.assertEqual((), result.valid_records)

    def test_invalid_uuid_does_not_hide_an_independent_path_mismatch(self) -> None:
        """Short-circuiting UUID format checks must not suppress separate path-drift evidence."""
        from kb_obsidian.validation import validate_content

        self._write_note(UUID_B, identifier=UUID_A.upper())

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual(
            {"content.invalid_id", "content.path_mismatch"},
            {issue.code for issue in result.issues},
        )

    def test_parser_reports_duplicate_nested_unknown_and_heading_failures_together(self) -> None:
        """Weak YAML or Markdown parsing must not accept ambiguous content records."""
        from kb_obsidian.validation import validate_content

        duplicate = self.vault / "content" / f"{UUID_A}.md"
        duplicate.write_text(
            "---\n"
            f"kb_id: {UUID_A}\n"
            "title: 重复\n"
            "title: 覆盖\n"
            "aliases: [重复]\n"
            "kb_type: '[[kb/types/tutorial]]'\n"
            "kb_genre: '[[kb/genres/analysis]]'\n"
            "kb_subjects: ['[[kb/topics/security]]']\n"
            "kb_created: 2026-09-03\n"
            "kb_status: draft\n"
            "---\n# 重复\n",
            encoding="utf-8",
        )
        self._write_note(UUID_B, kb_extra="unknown", custom={"nested": "value"})
        self._write_note(UUID_C, body="# 第二个标题\n")

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual(
            {"content.duplicate_property", "content.property_shape", "content.unknown_property", "content.heading"},
            {issue.code for issue in result.issues},
        )
        self.assertEqual((), result.valid_records)

    def test_parser_rejects_a_second_leading_frontmatter_block(self) -> None:
        """Treating a second YAML block as body text would make the property source ambiguous."""
        from kb_obsidian.validation import validate_content

        note = self._write_note(UUID_A)
        text = note.read_text(encoding="utf-8")
        note.write_text(
            text.replace("---\n# 内容\n", "---\n---\nsecond: block\n---\n# 内容\n", 1),
            encoding="utf-8",
        )

        result = validate_content(self.snapshot, self.vault)

        self.assertIn("content.frontmatter", {issue.code for issue in result.issues})
        self.assertEqual((), result.valid_records)

    def test_parser_reports_a_cyclic_yaml_alias_and_continues_with_other_files(self) -> None:
        """Recursive YAML data must become one file issue instead of aborting the vault scan."""
        from kb_obsidian.validation import validate_content

        cyclic = self._write_note(UUID_A)
        text = cyclic.read_text(encoding="utf-8")
        cyclic.write_text(
            text.replace("---\n# 内容\n", "custom: &cycle\n  - *cycle\n---\n# 内容\n", 1),
            encoding="utf-8",
        )
        self._write_note(UUID_B, title="仍可解析")

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual(
            [(Path(f"content/{UUID_A}.md"), "content.property_cycle")],
            [(issue.path, issue.code) for issue in result.issues],
        )
        self.assertEqual((UUID_B,), tuple(record.identifier for record in result.records))
        self.assertEqual((UUID_B,), tuple(record.identifier for record in result.valid_records))

    def test_heading_scan_ignores_hash_lines_inside_both_markdown_fence_kinds(self) -> None:
        """A hash line inside backtick or tilde code fences must not count as another H1."""
        from kb_obsidian.validation import validate_content

        body = (
            "正文。\n\n"
            "````markdown\n"
            "# 反引号代码中的伪标题\n"
            "```\n"
            "仍在反引号代码块内。\n"
            "````\n\n"
            "~~~~text\n"
            "# 波浪号代码中的伪标题\n"
            "~~~\n"
            "仍在波浪号代码块内。\n"
            "~~~~\n"
        )
        self._write_note(UUID_A, body=body)

        result = validate_content(self.snapshot, self.vault)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(body, result.records[0].body)

    def test_controlled_cardinality_value_and_object_kind_failures_are_all_reported(self) -> None:
        """Removing a field-specific resolver must expose the wrong cardinality, value, or object kind."""
        from kb_obsidian.validation import validate_content

        self._write_note(
            UUID_A,
            kb_type=["[[kb/types/tutorial]]"],
            kb_genre="[[kb/types/tutorial]]",
            kb_form="[[kb/genres/analysis]]",
            kb_level="invent",
            kb_subjects=["[[kb/topics/old-topic]]"],
            kb_entities=["[[kb/topics/security]]"],
            kb_references=["[[kb/entities/obsidian]]"],
        )

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual(
            {"kb_type", "kb_genre", "kb_form", "kb_level", "kb_subjects", "kb_entities", "kb_references"},
            {issue.field for issue in result.issues},
        )
        self.assertEqual((), result.valid_records)

    def test_source_distinguishes_content_and_entity_targets_and_requires_exact_links(self) -> None:
        """Treating source as an untyped ID or accepting noncanonical links must fail this test."""
        from kb_obsidian.validation import validate_content

        self._write_note(UUID_A, kb_source=f"[[content/{UUID_B}|来源]]")
        self._write_note(UUID_B, kb_source="[[kb/entities/obsidian|Obsidian]]")
        self._write_note(UUID_C, kb_source="[[kb/topics/security|安全]]")

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual([f"content/{UUID_C}.md"], [issue.path.as_posix() for issue in result.issues])
        self.assertEqual("kb_source", result.issues[0].field)
        self.assertEqual((UUID_A, UUID_B), tuple(record.identifier for record in result.valid_records))

    def test_content_reference_rejects_a_noncanonical_target_identity(self) -> None:
        """A path-resolvable target that is not canonical UUIDv4 must invalidate its referrer too."""
        from kb_obsidian.validation import validate_content

        self._write_note(UUID_A, kb_source=f"[[content/{UUID_V1}|旧身份]]")
        self._write_note(UUID_V1)

        result = validate_content(self.snapshot, self.vault)

        source_issues = [issue for issue in result.issues if issue.path == Path(f"content/{UUID_A}.md")]
        self.assertEqual(["kb_source"], [issue.field for issue in source_issues])
        self.assertNotIn(UUID_A, {record.identifier for record in result.valid_records})

    def test_all_content_reference_fields_reject_a_duplicate_identity_target(self) -> None:
        """A duplicate target identity must invalidate source, replacement, and relation referrers."""
        from kb_obsidian.validation import validate_content

        self._write_note(
            UUID_A,
            kb_source=f"[[content/{UUID_B}|来源]]",
            kb_status="deprecated",
            kb_is_replaced_by=f"[[content/{UUID_B}|替代]]",
            kb_relation=[f"[[content/{UUID_B}|相关]]"],
        )
        self._write_note(UUID_B, kb_relation=[f"[[content/{UUID_A}|相关]]"])
        self._write_note(UUID_C, identifier=UUID_B)

        result = validate_content(self.snapshot, self.vault)

        referrer_issues = [issue for issue in result.issues if issue.path == Path(f"content/{UUID_A}.md")]
        self.assertEqual(
            {"kb_source", "kb_is_replaced_by", "kb_relation"},
            {issue.field for issue in referrer_issues},
        )
        self.assertNotIn(UUID_A, {record.identifier for record in result.valid_records})

    def test_body_alias_and_index_links_never_satisfy_missing_controlled_fields(self) -> None:
        """Scanning ordinary links as metadata would wrongly make an unclassified note valid."""
        from kb_obsidian.validation import validate_content

        link_title = "[[kb/topics/security]]"
        self._write_note(
            UUID_A,
            title=link_title,
            aliases=[link_title],
            omit={"kb_subjects"},
            body="[[kb/topics/security]]\n",
        )
        (self.vault / "indexes").mkdir()
        (self.vault / "indexes" / "security.md").write_text("[[kb/topics/security]]\n", encoding="utf-8")

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual(["kb_subjects"], [issue.field for issue in result.issues])
        self.assertEqual(1, len(result.records))

    def test_dates_status_and_replacement_lifecycle_are_enforced(self) -> None:
        """Malformed dates and replacement metadata on a live record must never pass lifecycle checks."""
        from kb_obsidian.validation import validate_content

        self._write_note(
            UUID_A,
            kb_created="2026-02-30",
            kb_modified=["2026-09-03"],
            kb_status="active",
            kb_is_replaced_by=f"[[content/{UUID_B}]]",
        )
        self._write_note(UUID_B, kb_status="deprecated", body="")

        result = validate_content(self.snapshot, self.vault)

        self.assertEqual(
            {"kb_created", "kb_modified", "kb_is_replaced_by", "kb_status"},
            {issue.field for issue in result.issues},
        )
        self.assertEqual((), result.valid_records)

    def test_relation_must_resolve_and_be_reciprocal_on_both_ends(self) -> None:
        """A one-way controlled relation must report both affected records without auto-repair."""
        from kb_obsidian.validation import validate_content

        self._write_note(UUID_A, kb_relation=[f"[[content/{UUID_B}|B]]"])
        self._write_note(UUID_B)

        result = validate_content(self.snapshot, self.vault)

        reciprocal = [issue for issue in result.issues if issue.code == "content.relation_not_reciprocal"]
        self.assertEqual(
            [f"content/{UUID_A}.md", f"content/{UUID_B}.md"],
            [issue.path.as_posix() for issue in reciprocal],
        )
        self.assertEqual((), result.valid_records)

    def test_duplicate_identifier_invalidates_every_owner_and_issues_are_sorted(self) -> None:
        """Keeping the first duplicate as valid would make stable identity order-dependent."""
        from kb_obsidian.validation import validate_content

        self._write_note(UUID_A)
        self._write_note(UUID_B, identifier=UUID_A)
        self._write_note(UUID_C, title="Valid")

        result = validate_content(self.snapshot, self.vault)

        duplicate_paths = [issue.path.as_posix() for issue in result.issues if issue.code == "content.duplicate_id"]
        self.assertEqual([f"content/{UUID_A}.md", f"content/{UUID_B}.md"], duplicate_paths)
        self.assertEqual(
            list(result.issues),
            sorted(result.issues, key=lambda issue: (issue.path.as_posix(), issue.field, issue.code, issue.message)),
        )
        self.assertEqual((UUID_C,), tuple(record.identifier for record in result.valid_records))

    def test_issue_order_uses_message_to_break_equal_path_field_and_code_ties(self) -> None:
        """Reversing same-code inputs must not leak insertion or hash order into issue output."""
        from kb_obsidian.validation import validate_content

        self._write_note(
            UUID_A,
            kb_entities=[
                "[[kb/entities/z-missing|Z]]",
                "[[kb/entities/a-missing|A]]",
            ],
        )

        result = validate_content(self.snapshot, self.vault)

        messages = [issue.message for issue in result.issues]
        self.assertEqual(sorted(messages), messages)
        self.assertEqual(
            list(result.issues),
            sorted(
                result.issues,
                key=lambda issue: (issue.path.as_posix(), issue.field, issue.code, issue.message),
            ),
        )

    def test_validation_reads_only_top_level_content_markdown_and_changes_no_bytes(self) -> None:
        """Broad traversal or repair writes would cross the user-content read-only boundary."""
        from kb_obsidian.validation import validate_content

        self._write_note(UUID_A)
        nested = self.vault / "content" / "nested"
        nested.mkdir()
        (nested / "not-content.md").write_text("not a content unit\n", encoding="utf-8")
        (self.vault / "content" / "ignored.txt").write_text("not markdown\n", encoding="utf-8")
        (self.vault / "home.md").write_text("# Home\n", encoding="utf-8")
        before = self._all_file_bytes()

        result = validate_content(self.snapshot, self.vault)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual((UUID_A,), tuple(record.identifier for record in result.records))
        self.assertEqual(before, self._all_file_bytes())

    def _write_note(
        self,
        filename: str,
        *,
        identifier: str | None = None,
        title: str = "内容",
        aliases: list[str] | None = None,
        heading: str | None = None,
        body: str = "正文。\n",
        omit: set[str] | None = None,
        **overrides: object,
    ) -> Path:
        properties: dict[str, object] = {
            "kb_id": identifier or filename,
            "title": title,
            "aliases": [title] if aliases is None else aliases,
            "kb_type": "[[kb/types/tutorial|教程]]",
            "kb_genre": "[[kb/genres/analysis|分析]]",
            "kb_subjects": ["[[kb/topics/security|安全]]"],
            "kb_created": "2026-09-03",
            "kb_status": "draft",
        }
        properties.update(overrides)
        for key in omit or set():
            properties.pop(key, None)
        frontmatter = yaml.safe_dump(properties, allow_unicode=True, sort_keys=False)
        rendered_heading = title if heading is None else heading
        heading_text = f"# {rendered_heading}\n" if rendered_heading else ""
        path = self.vault / "content" / f"{filename}.md"
        path.write_text(f"---\n{frontmatter}---\n{heading_text}{body}", encoding="utf-8")
        return path

    def _all_file_bytes(self) -> dict[str, bytes]:
        return {
            path.relative_to(self.vault).as_posix(): path.read_bytes()
            for path in self.vault.rglob("*")
            if path.is_file()
        }


if __name__ == "__main__":
    unittest.main()
