"""Navigation notes retain content identity and reference safety after relocation."""
from __future__ import annotations

import json

import pytest
from kb_obsidian_rdf.common import ContractError, Delivery, digest, json_bytes
from kb_obsidian_rdf.content import check_content, new_content
from kb_obsidian_rdf.layout import VOCABULARY
from kb_obsidian_rdf.query import find_articles
from kb_obsidian_rdf.storage import initialize, inspect, refresh
from test_content import article, vault
from test_storage import delivery
from test_query import vocab


def test_index_can_be_created_queried_and_referenced_as_registered_content(vocab):
    vault = vocab
    created = new_content(vault, title="开发索引", folder="00-indexes", type_id="tutorial",
                          genre_id="background", subjects=["urn:concepts:ai"])
    assert created["path"] == "00-indexes/开发索引.md"
    article(vault, "资源笔记", source="[[00-indexes/开发索引]]", subject=["urn:concepts:ai"])
    checked = check_content(vault)
    assert checked["ok"] and checked["checked_count"] == 2
    found = find_articles(vault, field="subject", reference="urn:concepts:ai")
    assert created["path"] in {item["path"] for item in found["items"]}
    assert check_content(vault, [created["path"]])["ok"]


def test_invalid_index_identity_cannot_hide_from_content_validation(vault):
    resource = article(vault)
    article(vault, "损坏索引", folder="00-indexes", identifier="invalid")
    checked = check_content(vault)
    assert not checked["ok"]
    assert any(item["path"] == "00-indexes/损坏索引.md" and item["code"] == "identifier"
               for item in checked["errors"])
    before = resource.read_bytes()
    with pytest.raises(ContractError, match="身份"):
        new_content(vault, title="新笔记", type_id="tutorial", genre_id="background",
                    subjects=["urn:concept:one"])
    assert resource.read_bytes() == before


def test_refresh_preserves_user_index_content(tmp_path):
    vault = tmp_path / "vault"
    original = delivery()
    initialize(vault, original)
    folder = vault / "00-indexes"
    folder.mkdir(exist_ok=True)
    home = folder / "index.md"
    home.write_text("# 总入口\n\n用户精选内容。\n")
    topic = folder / "开发.md"
    topic.write_text(f"# 开发\n\n[[{VOCABULARY}/concepts/one]]\n")
    before = {path: path.read_bytes() for path in (home, topic)}
    result = refresh(vault, delivery("after"), apply=True, offline=True)
    assert result["status"] == "installed"
    assert all(path.read_bytes() == raw for path, raw in before.items())


def test_refresh_refuses_removing_vocabulary_referenced_only_by_manual_index(tmp_path):
    vault = tmp_path / "vault"
    original = delivery()
    initialize(vault, original)
    folder = vault / "00-indexes"
    folder.mkdir(exist_ok=True)
    index = folder / "开发.md"
    index.write_text(f"# 开发\n\n[[{VOCABULARY}/concepts/one]]\n")
    candidate = delivery("after")
    pages = {path: raw for path, raw in candidate.vault_files.items()
             if path != f"{VOCABULARY}/concepts/one.md"}
    files = dict(candidate.state_files)
    manifest = json.loads(files["manifest.json"])
    manifest["files"] = []
    files["manifest.json"] = json_bytes(manifest)
    before = inspect(vault)["manifest_sha256"]
    with pytest.raises(ContractError, match="引用"):
        refresh(vault, Delivery(pages, files), apply=True, offline=True)
    assert inspect(vault)["manifest_sha256"] == before
    assert f"[[{VOCABULARY}/concepts/one]]" in index.read_text()


@pytest.mark.parametrize("version", [2, 3])
def test_legacy_delivery_requires_explicit_layout_migration(tmp_path, version):
    original = delivery()
    files = dict(original.state_files)
    manifest = json.loads(files["manifest.json"])
    manifest["format_version"] = version
    files["manifest.json"] = json_bytes(manifest)
    with pytest.raises(ContractError, match="迁移"):
        initialize(tmp_path / "vault", Delivery(original.vault_files, files))


@pytest.mark.parametrize("note", [
    "---\nentities: ['[[90-vocabulary/entities/node.js|Node.js]]']\n---\n# 工程约定\n",
    "# 工程约定\n\n[[90-vocabulary/entities/node.js#简介|Node.js]]\n",
])
def test_refresh_resolves_dotted_wiki_names_without_weakening_missing_reference_check(tmp_path, note):
    vault = tmp_path / "vault"

    def named_delivery(text, previous=None, *, missing=False):
        value = delivery(text)
        pages = dict(value.vault_files)
        data = pages.pop(f"{VOCABULARY}/concepts/one.md")
        if not missing:
            pages[f"{VOCABULARY}/entities/node.js.md"] = data
        files = dict(value.state_files)
        manifest = json.loads(files["manifest.json"])
        manifest["files"] = ([] if missing else [{
            "path": f"{VOCABULARY}/entities/node.js.md", "role": "reference",
            "size": len(data), "sha256": digest(data),
        }])
        if previous:
            manifest["previous_delivery"] = {"sha256": previous}
        files["manifest.json"] = json_bytes(manifest)
        return Delivery(pages, files)

    initialize(vault, named_delivery("before"))
    index = vault / "00-indexes/工程约定.md"
    index.write_text(note)
    initial = inspect(vault)["manifest_sha256"]
    result = refresh(vault, named_delivery("after", initial), apply=True, offline=True)
    assert result["status"] == "installed"
    assert (vault / f"{VOCABULARY}/entities/node.js.md").read_text() == "after"
    assert index.read_text() == note
    installed = inspect(vault)["manifest_sha256"]
    with pytest.raises(ContractError, match="引用"):
        refresh(vault, named_delivery("after", installed, missing=True), apply=True, offline=True)
    assert inspect(vault)["manifest_sha256"] == installed
    assert index.read_text() == note
