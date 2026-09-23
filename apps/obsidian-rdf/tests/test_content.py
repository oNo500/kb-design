from __future__ import annotations

from datetime import date
from contextlib import contextmanager
from pathlib import Path
from uuid import UUID

import pytest
import yaml

from kb_obsidian_rdf.common import ContractError, Delivery, digest, json_bytes
from kb_obsidian_rdf.content import check_content, new_content
from kb_obsidian_rdf.storage import state_directory


def record(kind, token, *, iri=None, use="current", selectable=True):
    return {
        "identity": {"iri": iri} if iri else {"catalog": kind, "id": token},
        "kind": kind,
        "path": f"vocabulary/{'document-types' if kind == 'types' else kind}/{token}.md",
        "label": "同名",
        "sources": ["test"],
        "versions": ["v1"],
        "use": use,
        "trial_selectable": selectable,
        "formal_basis": None if iri else {"reference": "fixture-approved"},
        "restrictions": [],
        "history": [],
    }


@pytest.fixture
def vault(tmp_path, request):
    from kb_obsidian_rdf.storage import initialize

    records = [
        record("concepts", "one", iri="urn:concept:one"),
        record("concepts", "two", iri="urn:concept:two"),
        record("entities", "one", iri="urn:entity:one"),
        record("concepts", "retained", iri="urn:concept:old", use="retained", selectable=False),
        record("concepts", "denied", iri="urn:concept:denied", selectable=False),
        record("types", "tutorial"),
        record("genres", "background"),
        record("forms", "table"),
        record("references", "guide"),
    ]
    if getattr(request, "param", None) == "unapproved-type":
        next(item for item in records if item["kind"] == "types")["formal_basis"] = None
    files = {
        "records.json": json_bytes({"format_version": 1, "records": records}),
        "projection.json": json_bytes({"format_version": 1, "entries": []}),
    }
    pages = {item["path"]: b"# Reference\n" for item in records}
    files["manifest.json"] = json_bytes({
        "format_version": 2, "mode": "preview",
        "files": [{"path": path, "role": "reference", "size": len(data), "sha256": digest(data)}
                  for path, data in sorted(pages.items())],
        "state_files": [{"path": path, "role": "state", "size": len(data), "sha256": digest(data)}
                        for path, data in sorted(files.items())],
    })
    target = tmp_path / "vault"
    initialize(target, Delivery(pages, files))
    return target


def article(vault, name="一篇", *, folder="resources", **updates):
    metadata = {
        "identifier": "6894680b-09ca-4b29-bb82-206008c886ca", "title": name,
        "type": "[[vocabulary/document-types/tutorial]]", "genre": "[[vocabulary/genres/background]]",
        "subject": ["[[vocabulary/concepts/one]]"], "created": date(2026, 9, 23), "status": "draft",
    }
    metadata.update(updates)
    path = vault / folder / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
                    + "---\n\n# " + name + "\n\n正文 **保留**。\n", encoding="utf-8")
    return path


def codes(report):
    return {item["code"] for item in report["errors"]}


def test_article_scan_covers_para_and_leaves_free_capture_outside_content_model(tmp_path):
    from kb_obsidian_rdf.content import _articles

    for directory in ("projects/demo", "areas", "resources", "archives"):
        folder = tmp_path / directory
        folder.mkdir(parents=True)
        (folder / "note.md").write_text("---\nidentifier: declared\ntitle: 内容\nstatus: active\n---\n# 内容\n")
    for directory in ("inbox", "vocabulary/concepts", "views", "templates", "attachments"):
        folder = tmp_path / directory
        folder.mkdir(parents=True)
        (folder / "capture.md").write_text("没有元数据的随手记录")

    found = _articles(tmp_path)
    assert set(found) == {"projects/demo/note.md", "areas/note.md", "resources/note.md", "archives/note.md"}
    assert found["archives/note.md"].metadata["status"] == "active"
    assert not any(article.failure for article in found.values())


def test_new_preserves_identity_despite_identical_labels_and_does_not_overwrite(vault):
    result = new_content(vault, title="排序与来源", type_id="tutorial", genre_id="background",
                         subjects=["urn:concept:two"], entities=["urn:entity:one"],
                         references=["guide"], form="table", language="zh-Hant", level="apply")
    path = vault / result["path"]
    metadata = yaml.safe_load(path.read_text().split("---", 2)[1])
    assert UUID(metadata["identifier"]).version == 4
    assert metadata["language"] == "zh-Hant"
    assert metadata["status"] == "draft"
    assert "vocabulary/concepts/two" in metadata["subject"][0]
    assert "vocabulary/entities/one" in metadata["entities"][0]
    assert "vocabulary/references/guide" in metadata["references"][0]
    before = path.read_bytes()
    with pytest.raises(ContractError):
        new_content(vault, title="排序与来源", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:one"])
    assert path.read_bytes() == before
    assert check_content(vault)["ok"]
    assert check_content(vault)["formal_unconfirmed"]


def test_plain_materials_do_not_become_articles_or_block_new_content(vault):
    path = article(vault)
    plain = vault / "resources/excerpt.md"
    plain.write_text("# 普通摘录\n\n保留来源原文，没有内容单元元数据。\n")
    described = vault / "areas/reading.md"
    described.write_text("---\ntitle: 阅读材料\nsubject: [urn:concept:one]\n---\n正文\n")
    before = {str(item): item.read_bytes() for item in (plain, described)}

    checked = check_content(vault)
    assert checked["ok"] and checked["checked_count"] == 1
    assert [item["path"] for item in checked["articles"]] == [path.relative_to(vault).as_posix()]
    assert {item["path"] for item in checked["unregistered"]} == {"resources/excerpt.md", "areas/reading.md"}
    assert all(item["reason"] for item in checked["unregistered"])
    assert checked["unregistered_count"] == 2
    assert checked["coverage"]["complete"] is False
    only_material = check_content(vault, ["resources/excerpt.md"])
    assert only_material["checked_count"] == 0 and only_material["unregistered_count"] == 2
    assert only_material["articles"] == []

    created = new_content(vault, title="新增文章", type_id="tutorial", genre_id="background",
                          subjects=["urn:concept:one"])
    assert (vault / created["path"]).exists()
    assert created["report"]["unregistered_count"] == 2
    assert all(Path(name).read_bytes() == raw for name, raw in before.items())


def test_removing_article_identifier_reports_unchecked_file_and_breaks_controlled_reference(vault):
    path = article(vault)
    article(vault, "引用者", identifier="4c70ccf5-0b4a-45ac-a645-611f2f65755d", source="[[resources/一篇]]")
    path.write_text(path.read_text().replace("identifier: 6894680b-09ca-4b29-bb82-206008c886ca\n", ""))
    checked = check_content(vault)
    assert not checked["ok"] and checked["checked_count"] == 1
    assert checked["unregistered_count"] == 1 and checked["coverage"]["complete"] is False
    assert checked["unregistered"][0]["path"] == "resources/一篇.md"
    assert "unresolved_reference" in codes(checked)


@pytest.mark.parametrize("frontmatter", [
    "identifier: invalid\ntitle: 坏身份\n",
    "identifier: null\ntitle: 空身份\n",
    "identifier: valid-before-error\nsubject: [broken\n",
    "title: [broken\nidentifier: value-after-error\n",
    '"identifier": quoted-before-error\nsubject: [broken\n',
    '{identifier: flow-before-error, subject: [broken\n',
])
def test_declared_but_invalid_or_damaged_identity_still_fails(vault, frontmatter):
    article(vault)
    broken = vault / "archives/broken.md"
    broken.write_text("---\n" + frontmatter + "---\n\n# 坏记录\n")
    checked = check_content(vault)
    assert not checked["ok"]
    assert any(item["path"] == "archives/broken.md" for item in checked["errors"])
    assert "archives/broken.md" not in {item["path"] for item in checked["unregistered"]}
    with pytest.raises(ContractError):
        new_content(vault, title="未建立", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:one"])
    assert not (vault / "resources/未建立.md").exists()


def test_unregistered_file_cannot_supply_controlled_content_reference(vault):
    plain = vault / "resources/excerpt.md"
    plain.write_text("# 资料\n正文普通链接可以使用这份资料。\n")
    article(vault, source="[[resources/excerpt]]")
    checked = check_content(vault)
    assert "unresolved_reference" in codes(checked)
    assert any(item["field"] == "source" for item in checked["errors"])


@pytest.mark.parametrize("text", [
    "# 随手记录\nidentifier: 只是正文示例\n",
    "---\ntitle: 示例\n---\nidentifier: 只是正文示例\n",
    "---\nexample:\n  identifier: 嵌套对象\nexample: 重复字段\n---\n正文\n",
    "---\nexample: |\n  identifier: 字符串示例\nbroken: [\n---\n正文\n",
])
def test_identifier_mentions_do_not_promote_unregistered_files(vault, text):
    path = vault / "resources/example.md"
    path.write_text(text)
    checked = check_content(vault)
    assert checked["ok"] and checked["checked_count"] == 0
    assert checked["unregistered_count"] == 1
    assert checked["coverage"]["complete"] is False
    assert checked["unregistered"][0]["path"] == "resources/example.md"


def test_new_uses_selected_para_folder_and_preserves_title_and_identity(vault):
    result = new_content(vault, title="JavaScript 数组_Sort", folder="projects/js-notes",
                         type_id="tutorial", genre_id="background", subjects=["urn:concept:one"])
    assert result["path"] == "projects/js-notes/javascript-数组-sort.md"
    path = vault / result["path"]
    metadata = yaml.safe_load(path.read_text().split("---", 2)[1])
    assert metadata["title"] == "JavaScript 数组_Sort"
    assert metadata["identifier"] == result["identifier"]
    assert check_content(vault)["ok"]
    with pytest.raises(ContractError, match="同名|冲突"):
        new_content(vault, title="javascript 数组-sort", folder="projects/js-notes",
                    type_id="tutorial", genre_id="background", subjects=["urn:concept:two"])
    archived = vault / "archives/js-notes"
    archived.mkdir(parents=True)
    moved = archived / path.name
    path.rename(moved)
    checked = check_content(vault)
    assert checked["ok"]
    assert checked["articles"][0]["identifier"] == result["identifier"]
    assert yaml.safe_load(moved.read_text().split("---", 2)[1])["status"] == "draft"


@pytest.mark.parametrize("folder", ["inbox", "vocabulary", "notes", "../resources", "/resources",
                                  "projects/../areas", "projects//demo", "Projects", "areas/My Area",
                                  "resources/my_notes", "resources/..", "archives/"])
def test_new_rejects_unmanaged_or_ambiguous_content_folders(vault, folder):
    with pytest.raises(ContractError):
        new_content(vault, title="不得建立", folder=folder,
                    type_id="tutorial", genre_id="background", subjects=["urn:concept:one"])
    assert not list(vault.glob("**/不得建立.md"))


@pytest.mark.parametrize("field,value", [
    ("subject", ["urn:entity:one"]), ("subject", ["同名"]),
    ("type", "urn:concept:one"), ("references", ["urn:entity:one"]),
    ("source", "urn:concept:one"),
])
def test_content_never_coerces_wrong_object_kind_or_display_text(vault, field, value):
    article(vault, **{field: value})
    report = check_content(vault)
    assert not report["ok"]
    assert any(issue["field"] == field for issue in report["errors"])


def test_old_reference_remains_readable_but_cannot_be_selected_for_new_content(vault):
    article(vault, subject=["[[vocabulary/concepts/retained]]"])
    report = check_content(vault)
    assert report["ok"]
    assert any(item["code"] == "historical_reference" for item in report["issues"])
    with pytest.raises(ContractError):
        new_content(vault, title="错误新标引", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:old"])
    article(vault, subject=["urn:concept:denied"])
    assert "not_selectable" in codes(check_content(vault))


def test_subset_check_still_detects_duplicate_uuid_elsewhere(vault):
    article(vault)
    article(vault, "另一篇")
    report = check_content(vault, ["resources/一篇.md"])
    assert "duplicate_identifier" in codes(report)
    assert report["manifest_sha256"] == digest((state_directory(vault) / "current/manifest.json").read_bytes())
    assert report["articles"][0]["sha256"] == digest((vault / "resources/一篇.md").read_bytes())


def test_cross_article_relations_require_reciprocity_and_replacement_cannot_cycle(vault):
    first = article(vault, folder="projects/demo", relation=["[[archives/另一篇]]"])
    article(vault, "另一篇", folder="archives", identifier="4c70ccf5-0b4a-45ac-a645-611f2f65755d")
    assert "relation_not_reciprocal" in codes(check_content(vault, [str(first.relative_to(vault))]))
    article(vault, "另一篇", folder="archives", identifier="4c70ccf5-0b4a-45ac-a645-611f2f65755d",
            relation=["[[projects/demo/一篇]]"])
    assert check_content(vault)["ok"]
    article(vault, folder="projects/demo", status="deprecated", isReplacedBy="[[archives/另一篇]]")
    article(vault, "另一篇", folder="archives", identifier="4c70ccf5-0b4a-45ac-a645-611f2f65755d",
            status="deprecated", isReplacedBy="[[projects/demo/一篇]]")
    assert "replacement_cycle" in codes(check_content(vault))


@pytest.mark.parametrize("update,expected", [
    ({"subject": "[[vocabulary/concepts/one]]"}, "field_type"),
    ({"subject": []}, "required"), ({"created": "2026-02-31"}, "date"),
    ({"modified": "2026-09-22"}, "date_order"),
    ({"identifier": "6894680B-09CA-4B29-BB82-206008C886CA"}, "identifier"),
    ({"language": "zh_Hant"}, "language"),
    ({"form": None}, "field_type"), ({"status": "published"}, "status"),
    ({"isReplacedBy": "[[resources/一篇]]"}, "replacement_status"),
])
def test_field_failures_are_reported_without_modifying_content(vault, update, expected):
    path = article(vault, **update)
    before = path.read_bytes()
    assert expected in codes(check_content(vault))
    assert path.read_bytes() == before


def test_duplicate_yaml_key_does_not_silently_replace_controlled_value(vault):
    path = article(vault)
    text = path.read_text()
    path.write_text(text.replace("status: draft", "status: draft\nsubject: []"))
    assert "frontmatter" in codes(check_content(vault))


def test_new_refuses_managed_file_tampering_and_symlink_content_area(vault, tmp_path):
    managed = vault / "vocabulary/concepts/one.md"
    managed.write_text("changed identity")
    with pytest.raises(ContractError):
        new_content(vault, title="不得写入", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:one"])
    assert not (vault / "resources/不得写入.md").exists()
    managed.write_bytes(b"# Reference\n")
    outside = tmp_path / "outside"
    outside.mkdir()
    (vault / "resources").rmdir()
    (vault / "resources").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ContractError):
        new_content(vault, title="越界", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:one"])
    assert list(outside.iterdir()) == []


def test_failed_article_write_never_installs_a_partial_draft(vault, monkeypatch):
    from kb_obsidian_rdf import content

    fdopen = content.os.fdopen

    @contextmanager
    def interrupted(*args, **kwargs):
        with fdopen(*args, **kwargs) as stream:
            class Writer:
                def write(self, data):
                    stream.write(data[:20])
                    stream.flush()
                    raise OSError("simulated exhausted disk")
            yield Writer()

    monkeypatch.setattr(content.os, "fdopen", interrupted)
    with pytest.raises(ContractError):
        new_content(vault, title="不完整文章", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:one"])
    assert not (vault / "resources/不完整文章.md").exists()


@pytest.mark.parametrize("body,valid", [
    ("<!-- 说明 -->\n\n一篇\n====\n\n正文", True),
    ("# **一篇**\n\n正文", True),
    ("```md\n# 一篇\n```\n\n正文", False),
    ("# 一篇\n\n# 多出的一级标题\n", False),
    ("# 一篇\n\n```md\n# 这是代码\n```\n", True),
    ("<!--\n# 隐藏注释\n-->\n\n# 一篇\n\n> # 引文中的标题\n", True),
])
def test_heading_validation_uses_markdown_structure(vault, body, valid):
    path = article(vault)
    frontmatter = path.read_text().split("---", 2)[1]
    path.write_text("---" + frontmatter + "---\n\n" + body)
    report = check_content(vault)
    assert ("heading" not in codes(report)) is valid


def test_new_title_text_is_not_accidentally_interpreted_as_markdown(vault):
    result = new_content(vault, title="参数 _name_ 的含义", type_id="tutorial", genre_id="background",
                         subjects=["urn:concept:one"])
    path = vault / result["path"]
    assert yaml.safe_load(path.read_text().split("---", 2)[1])["title"] == "参数 _name_ 的含义"
    assert check_content(vault)["ok"]


@pytest.mark.parametrize("vault", ["unapproved-type"], indirect=True)
def test_preview_permission_does_not_approve_an_auxiliary_document_type(vault):
    with pytest.raises(ContractError):
        new_content(vault, title="未批准的类型", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:one"])
    article(vault)
    assert "auxiliary_unapproved" in codes(check_content(vault))
