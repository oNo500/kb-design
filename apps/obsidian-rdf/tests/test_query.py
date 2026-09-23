from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest
import yaml

from kb_obsidian_rdf.common import ContractError, Delivery, digest, json_bytes
from kb_obsidian_rdf import __version__, query
from kb_obsidian_rdf.storage import initialize, state_directory


def record(kind, token, label, *, aliases=(), use="current", selectable=True, definition=None):
    identity = {"iri": "urn:" + kind + ":" + token} if kind in {"concepts", "entities"} else {"catalog": kind, "id": token}
    summary = None if definition is None else {"text": definition, "language": "zh", "predicate": "http://www.w3.org/2004/02/skos/core#definition"}
    return {"identity": identity, "kind": kind, "path": f"vocabulary/{'document-types' if kind == 'types' else kind}/{token}.md", "label": label,
            "sources": ["fixture"], "versions": ["v1"], "use": use,
            "trial_selectable": selectable, "formal_basis": None if "iri" in identity else ["fixture-approved"],
            "restrictions": [], "history": [], "entry": {"aliases": list(aliases), "summary": summary,
                "definitions": [] if summary is None else [summary], "scope_notes": [], "descriptions": [],
                "relations": {"broader": [], "narrower": [], "related": []}, "notes": [], "raw_sources": []}}


def make_vault(tmp_path, records):
    files = {"records.json": json_bytes({"format_version": 1, "records": records}),
             "projection.json": json_bytes({"format_version": 1, "entries": []})}
    pages = {}
    for item in records:
        # A genuinely long page must not be returned by the query API.
        body = "---\n" + yaml.safe_dump({"identifier": item["identity"].get("iri", item["identity"].get("id")),
                                             "title": item["label"]}, allow_unicode=True) + "---\n\n# " + item["label"] + "\n\n" + "工程信息" * 5000
        pages[item["path"]] = body.encode()
    files["manifest.json"] = json_bytes({"format_version": 2, "mode": "preview", "files": [
        {"path": path, "role": "reference", "size": len(raw), "sha256": digest(raw)} for path, raw in sorted(pages.items())],
        "state_files": [{"path": path, "role": "state", "size": len(raw), "sha256": digest(raw)}
                        for path, raw in sorted(files.items())]})
    vault = tmp_path / "vault"
    initialize(vault, Delivery(pages, files))
    return vault


@pytest.fixture
def vocab(tmp_path):
    entries = [record("concepts", "ai", "人工智能", aliases=("Artificial intelligence", "AI"), definition="研究智能系统。"),
               record("entities", "ai", "AI", aliases=("人工智能",)),
               record("concepts", "tutorial", "教程"), record("types", "tutorial", "教程"),
               record("concepts", "first", "重名"), record("concepts", "second", "重名"),
               record("concepts", "retired", "过时", use="retained", selectable=False),
               record("genres", "background", "背景"), record("references", "guide", "指南")]
    return make_vault(tmp_path, entries)


def article(vault, name, *, folder="resources", subject=None, entities=None, identifier=None, body=""):
    metadata = {"identifier": identifier or str(uuid4()), "title": name, "type": "tutorial", "genre": "background",
                "subject": subject or ["urn:concepts:ai"], "created": "2026-09-23", "status": "draft"}
    if entities is not None:
        metadata["entities"] = entities
    path = vault / folder / (name + ".md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True) + "---\n\n# " + name + "\n\n" + body)
    return path


def test_fields_aliases_and_bounded_summary_are_enforced(vocab):
    found = query.search_entries(vocab, field="subject", query="ai")
    assert found["total"] == 1
    item = found["items"][0]
    assert item["label"] == "人工智能" and item["matched_alias"] == "AI"
    assert item["identity"] == {"iri": "urn:concepts:ai"}
    assert item["summary"]["predicate"].endswith("#definition")
    assert len(json.dumps(found, ensure_ascii=False)) < 4000
    assert query.search_entries(vocab, field="entities", query="ai")["items"][0]["kind"] == "entities"
    assert query.get_entry(vocab, field="type", term="教程")["items"][0]["identity"] == {"catalog": "types", "id": "tutorial"}


def test_name_resolution_requires_exact_unique_name_and_never_picks_first(vocab):
    with pytest.raises(query.QueryError) as caught:
        query.get_entry(vocab, field="subject", term="重名")
    assert caught.value.code == "ambiguous_term"
    assert len(caught.value.candidates) == 2
    with pytest.raises(query.QueryError, match="精确"):
        query.get_entry(vocab, field="subject", term="人工")


def test_history_can_be_read_explicitly_but_is_never_new_selection(vocab):
    assert query.search_entries(vocab, field="subject", query="过时")["items"] == []
    item = query.search_entries(vocab, field="subject", query="过时", include_unavailable=True)["items"][0]
    assert not item["available"]
    with pytest.raises(query.QueryError):
        query.get_entry(vocab, field="subject", term="过时")
    detail = query.get_entry(vocab, field="subject", reference="[[vocabulary/concepts/retired]]")
    assert detail["items"][0]["use"] == "retained"
    assert not detail["items"][0]["available"]


def test_explicit_reference_keeps_identity_and_rejects_other_field(vocab):
    a = query.get_entry(vocab, field="subject", reference="urn:concepts:ai")["items"][0]
    b = query.get_entry(vocab, field="subject", reference="vocabulary/concepts/ai.md")["items"][0]
    assert a["identity"] == b["identity"]
    with pytest.raises(query.QueryError):
        query.get_entry(vocab, field="subject", reference="urn:entities:ai")
    with pytest.raises(query.QueryError):
        query.get_entry(vocab, field="subject", reference="AI")
    assert query.get_entry(vocab, field="type", reference="tutorial")["items"][0]["kind"] == "types"


@pytest.mark.parametrize("target", ["current/records.json", "current/manifest.json", "current.json"])
def test_changed_identity_map_manifest_or_receipt_cannot_feed_search(vocab, target):
    path = state_directory(vocab) / target
    data = json.loads(path.read_bytes())
    if target.endswith("current.json"):
        data["manifest_sha256"] = "0" * 64
    elif target.endswith("/records.json"):
        data["records"][0]["identity"] = {"iri": "urn:unapproved:replacement"}
    else:
        data["files"][0]["sha256"] = "0" * 64
    path.write_bytes(json_bytes(data))
    with pytest.raises(ContractError):
        query.search_entries(vocab, field="subject", query="AI")


def test_get_checks_requested_page_but_search_is_explicitly_partial(vocab):
    (vocab / "vocabulary/concepts/ai.md").write_text("changed")
    assert query.search_entries(vocab, field="subject", query="AI")["verification"]["scope"] == "manifest_and_records"
    with pytest.raises(ContractError, match="摘要|变化"):
        query.get_entry(vocab, field="subject", term="AI")


@pytest.mark.parametrize("unsafe", ["pending", "symlink"])
def test_pending_and_symlink_are_not_read_as_installed_identity(vocab, tmp_path, unsafe):
    if unsafe == "pending":
        (state_directory(vocab) / "recovery.json").write_text("{}")
    else:
        path = state_directory(vocab) / "current/records.json"
        outside = tmp_path / "outside.json"
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)
    with pytest.raises(ContractError):
        query.search_entries(vocab, field="subject", query="AI")


def test_legacy_hidden_name_is_not_a_search_alias_and_missing_summary_is_explicit(tmp_path):
    entry = record("concepts", "one", "公开名称")
    del entry["entry"]
    entry["name_records"] = [{"iri": "urn:label:hidden", "role": "隐藏名", "value": {"literal": "secret", "language": "en", "datatype": None}},
                             {"iri": "urn:label:alias", "role": "替代名", "value": {"literal": "public", "language": "en", "datatype": None}}]
    vault = make_vault(tmp_path, [entry])
    assert query.search_entries(vault, field="subject", query="secret")["items"] == []
    assert query.search_entries(vault, field="subject", query="public")["total"] == 1
    item = query.search_entries(vault, field="subject", query="公开名称")["items"][0]
    assert item["summary"] is None and item["limitations"]


def test_details_are_structured_not_raw_page_and_long_summary_is_bounded(tmp_path):
    entry = record("concepts", "one", "词", definition="定义" * 2000)
    vault = make_vault(tmp_path, [entry])
    brief = query.get_entry(vault, field="subject", term="词")["items"][0]
    assert len(brief["summary"]["text"]) <= 281 and brief["summary"]["truncated"]
    detail = query.get_entry(vault, field="subject", term="词", details=True)["items"][0]
    assert detail["details"]["definitions"][0]["text"] == "定义" * 2000
    assert "工程信息" not in json.dumps(detail, ensure_ascii=False)


def test_article_lookup_uses_only_actual_field_and_retains_formal_boundary(vocab):
    chosen = article(vocab, "已标引", entities=["urn:entities:ai"])
    article(vocab, "仅提及", subject=["urn:concepts:first"], body="人工智能 [[vocabulary/concepts/ai]]")
    found = query.find_articles(vocab, field="subject", term="AI")
    assert [i["path"] for i in found["items"]] == [chosen.relative_to(vocab).as_posix()]
    assert found["target"]["formal_basis"] is None
    assert not found["verification"]["formal_use_checked"]


def test_article_lookup_spans_para_and_excludes_unclassified_captures(vocab):
    for folder in ("projects/demo", "areas", "resources", "archives/finished"):
        article(vocab, "说明", folder=folder, entities=["urn:entities:ai"])
    inbox = vocab / "inbox"
    inbox.mkdir(exist_ok=True)
    (inbox / "capture.md").write_text("AI 的未整理随手记录，没有元数据")
    article(vocab, "模板示例", folder="templates", entities=["urn:entities:ai"])

    expected = {"projects/demo/说明.md", "areas/说明.md", "resources/说明.md", "archives/finished/说明.md"}
    for field in ("subject", "entities"):
        found = query.find_articles(vocab, field=field, term="AI")
        assert found["ok"]
        assert {item["path"] for item in found["items"]} == expected
        assert found["verification"]["article_count"] == 4


def test_plain_materials_never_become_indexed_articles_and_coverage_is_explicit(vocab):
    registered = article(vocab, "已登记", entities=["urn:entities:ai"])
    plain = vocab / "resources/excerpt.md"
    plain.write_text("---\ntitle: 未登记资料\nsubject: [urn:concepts:ai]\nentities: [urn:entities:ai]\n---\n# 资料\n")
    for field in ("subject", "entities"):
        found = query.find_articles(vocab, field=field, term="AI")
        assert found["ok"] and found["total"] == 1
        assert found["items"][0]["path"] == registered.relative_to(vocab).as_posix()
        assert found["verification"]["article_count"] == 1
        assert found["verification"]["unregistered_count"] == 1
        assert found["unregistered"][0]["path"] == "resources/excerpt.md"
        assert found["unregistered"][0]["reason"]

    (vocab / "archives/broken.md").write_text("---\nidentifier: wrong\nsubject: [urn:concepts:ai]\n---\n坏记录\n")
    found = query.find_articles(vocab, field="subject", term="AI")
    assert not found["ok"] and found["total"] == 1
    assert any(item["path"] == "archives/broken.md" and item["code"] == "identifier" for item in found["issues"])


def test_descendant_lookup_traverses_edges_without_cycles_or_duplicate_article_hits(tmp_path):
    entries = [record("concepts", token, token) for token in ("a", "b", "c")]
    entries.extend([record("types", "tutorial", "教程"), record("genres", "background", "背景")])
    by_token = {e["identity"].get("iri", "").rsplit(":", 1)[-1]: e for e in entries}
    for child, parent in (("b", "a"), ("c", "a"), ("c", "b"), ("a", "c")):
        by_token[child]["entry"]["relations"]["broader"].append({"identity": by_token[parent]["identity"], "label": parent, "path": by_token[parent]["path"]})
    vault = make_vault(tmp_path, entries)
    article(vault, "多父概念", subject=["urn:concepts:b", "urn:concepts:c"])
    assert query.find_articles(vault, field="subject", term="a")["total"] == 0
    found = query.find_articles(vault, field="subject", term="a", descendants=True)
    assert found["total"] == 1 and len(found["expanded_identities"]) == 3
    with pytest.raises(query.QueryError):
        query.find_articles(vault, field="type", term="教程", descendants=True)


def test_same_article_uuid_is_not_counted_twice_and_collision_is_reported(vocab):
    identifier = str(uuid4())
    article(vocab, "第一路径", identifier=identifier)
    article(vocab, "第二路径", identifier=identifier)
    found = query.find_articles(vocab, field="subject", term="AI")
    assert found["total"] == 1 and len(found["items"][0]["paths"]) == 2
    assert not found["ok"]
    assert any(i["code"] == "duplicate_identifier" for i in found["issues"])


def test_historical_page_never_uses_current_hierarchy_when_identity_is_still_current(tmp_path):
    current = record("concepts", "a", "当前概念")
    historical = record("concepts", "a", "旧版概念", use="historical", selectable=False)
    historical["path"] = "vocabulary/history/v1/concepts/a.md"
    child = record("concepts", "b", "当前下位")
    child["entry"]["relations"]["broader"].append({"identity": current["identity"], "label": current["label"], "path": current["path"]})
    vault = make_vault(tmp_path, [current, historical, child, record("types", "tutorial", "教程"), record("genres", "background", "背景")])
    article(vault, "当前下位文章", subject=["urn:concepts:b"])
    reference = "[[vocabulary/history/v1/concepts/a]]"
    assert query.find_articles(vault, field="subject", reference=reference)["total"] == 0
    assert query.find_articles(vault, field="subject", reference="urn:concepts:a", descendants=True)["total"] == 1
    with pytest.raises(query.QueryError) as caught:
        query.find_articles(vault, field="subject", reference=reference, descendants=True)
    assert caught.value.code == "historical_hierarchy"


def test_query_consumes_real_generated_entry_and_preserves_note_subject(tmp_path):
    from kb_obsidian_rdf.build import build_delivery

    raw = b'''@prefix ex: <https://example.org/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xl: <http://www.w3.org/2008/05/skos-xl#> .
ex:concept a skos:Concept; skos:prefLabel "AI"@en;
  skos:altLabel "Artificial intelligence"@en; skos:hiddenLabel "AII"@en;
  xl:prefLabel ex:name; skos:scopeNote "Concept scope"@en .
ex:name a xl:Label; xl:literalForm "AI"@en; skos:definition "Name description only"@en .
'''
    (tmp_path / "source.ttl").write_bytes(raw)
    spec = {"format_version": 1, "mode": "preview", "sources": [{"key": "fixture", "path": "source.ttl", "format": "turtle",
            "sha256": digest(raw), "identity": "fixture-source", "version": "v1",
            "scope": {"subject_iris": ["https://example.org/concept"]}, "trial_subjects": ["https://example.org/concept"],
            "authority": {"preview_reference": "fixture trial", "scope_reference": "fixture scope", "formal_reference": None}}],
            "auxiliary": [], "display": ["zh", "en"], "rules": {"shacl_profiles": ["structure"]},
            "producer": {"name": "kb-obsidian-rdf", "version": __version__}, "previous_delivery": None}
    config = tmp_path / "input.json"
    config.write_bytes(json_bytes(spec))
    files = build_delivery(config)
    vault = tmp_path / "real"
    initialize(vault, files)
    item = query.get_entry(vault, field="subject", term="artificial intelligence", details=True)["items"][0]
    assert item["summary"]["text"] == "Concept scope"
    assert item["summary"]["predicate"].endswith("#scopeNote")
    assert item["details"]["definitions"] == []
    assert any(note["identity"] == {"iri": "https://example.org/name"} and note["text"] == "Name description only" for note in item["details"]["notes"])
    assert query.search_entries(vault, field="subject", query="AII")["items"] == []
