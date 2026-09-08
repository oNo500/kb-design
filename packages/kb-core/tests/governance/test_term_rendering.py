import copy
import json
import unittest
from pathlib import Path

from kb_core.governance.build_terms import (
    build_model_label_rows,
    canonical_snapshot,
    ordered_concepts,
    validate_glossary_layout,
)
from kb_core.governance.term_rendering import render_glossary, render_term_markdown
from kb_core.build_source_index import visit_reference_use
from kb_core.source_model import collect_reference_uses


TC1 = "tc-11111111-1111-4111-8111-111111111111"
TC2 = "tc-22222222-2222-4222-8222-222222222222"


def basis(locator):
    return [{"reference": "source-a", "locator": locator, "checked": "2026-09-06"}]


def term(term_id, text, status="preferredTerm-admn-sts", locator="term"):
    return {"id": term_id, "text": text, "administrative_status": status,
            "basis": basis(locator), "history": []}


def concept(concept_id=TC1):
    return {
        "id": concept_id,
        "subject_fields": [],
        "definitions": [
            {"language": "en", "text": "English definition.", "basis": basis("def-en")},
            {"language": "zh-Hans", "text": "中文定义。", "basis": basis("def-zh")},
        ],
        "languages": [
            {"language": "en", "terms": [
                term("tm-11111111-1111-4111-8111-111111111111", "English term", locator="term-en"),
                term("tm-33333333-3333-4333-8333-333333333333", "Old term",
                     "deprecatedTerm-admn-sts", "term-old"),
            ]},
            {"language": "zh-Hans", "terms": [
                term("tm-22222222-2222-4222-8222-222222222222", "中文术语", locator="term-zh")
            ]},
        ],
        "basis": basis("concept"), "source": None, "match": [],
        "workflow": "active", "history": [],
    }


SOURCES = {"source-a": {"id": "source-a", "label": {"zh": "甲来源", "en": "Source A"},
                         "version": "2026", "urls": [{"role": "landing", "url": "https://example.test/a", "primary": True}]}}
STATE = {"state": "active", "terms_mode": "active_editor", "consumers_enabled": True,
         "decision": "decision-publication"}


class TermRenderingTests(unittest.TestCase):
    def layout_v2(self):
        return {
            "schema": "urn:kb-design:layout:glossary:2", "version": 2,
            "groups": [{"id": "one", "title": "应用与生成", "order": 1, "members": [TC1]}],
            "source_abbreviations": {"id": "sources", "title": "出处缩写", "order": 0,
                "entries": [{"id": "a", "cells": ["ISO", "ISO source"],
                             "meaning": "只作引用说明。", "source_entity_ids": ["source-a"]}]},
            "standards_appendix": {"id": "standards", "title": "引用文献", "order": 2,
                "entries": [{"id": "s", "cells": ["Standard", "Historical lead"],
                             "verification": "未升级为已核事实。"}]},
            "reference_entries": [{"id": "r", "section": "应用与生成",
                "cells": ["来源分级", "tiers", "项目规则说明", "rules.md"],
                "content_role": "reference_explanation", "scope": "不是四个术语概念。"}],
            "symbol_mappings": [{"origin_id": "o", "symbols": ["USE", "UF"],
                "concept_ids": [TC1], "role": "relationship_indicator",
                "display_note": "关系指示符，不是术语形式。"}],
            "historical_designations": [{"origin_id": "h", "forms": ["旧称"],
                "target_concept_ids": [TC1], "disposition": "withdraw",
                "reason": "名称不准确。", "display": "改用当前首选形式。",
                "effect": "已退出当前准用名称。", "approval": "decision-layout"}],
            "model_labels": {"generation_inputs": ["topics.yaml"],
                "display_rule": "按中英形式合并并保留身份。",
                "language_notice": "模型知识 · 第 5 级，外部用法未核实"},
        }

    def test_layout_v2_is_complete_and_unapproved_value_is_rejected(self):
        layout = self.layout_v2()
        self.assertEqual((), validate_glossary_layout(layout, concept_ids={TC1}))
        self.assertIn("TERM_LAYOUT_ADOPTION_MISSING",
                      validate_glossary_layout(layout, concept_ids={TC1}, accepted_decisions={}))
        grant = {
            "id": "decision-layout", "schema": "urn:kb-design:data:decision",
            "schema_version": 1, "status": "accepted", "date": "2026-09-06",
            "level": "L1", "scope": "fixture", "supersedes": [],
            "answers": [{"question": "Q01", "resolution": "recommended", "patches": [{
                "identity": "@control:terms", "field": "glossary_layout", "value": layout,
            }]}],
        }
        self.assertIn("TERM_LAYOUT_ADOPTION_MISSING", validate_glossary_layout(
            layout, concept_ids={TC1}, accepted_decisions={grant["id"]: grant},
        ))
        grant["level"] = "L3"
        self.assertEqual((), validate_glossary_layout(
            layout, concept_ids={TC1}, accepted_decisions={grant["id"]: grant},
        ))
        dropped = copy.deepcopy(layout)
        dropped["groups"][0]["members"] = []
        self.assertTrue(any("TERM_LAYOUT_MEMBER_MISSING" in issue
                            for issue in validate_glossary_layout(dropped, concept_ids={TC1})))

    def test_layout_v2_sections_and_project_basis_are_readable(self):
        value = concept()
        value["basis"] = {"project": {"approval": "decision-project",
            "origin": {"commit": "abc123", "file": "docs/design/model.md", "locator": "内容单元"},
            "rationale": "采用现行项目定义。"}}
        rendered = render_glossary({"concepts": [value], "model_labels": [{
            "zh": "模型译名", "en": "Model label", "targets": ["topics/a"],
            "target_models": [{"target": "topics/a", "model": {"name": "gpt", "date": "2026-09-06", "rationale": "r", "approval": "d"}}],
        }]}, self.layout_v2(), STATE, SOURCES)
        for expected in ("出处缩写", "ISO source", "补充说明", "来源分级", "关系符号",
                         "USE / UF", "历史名称", "旧称", "引用文献", "Historical lead",
                         "模型译名", "topics/a", "项目决定依据，不是外部来源",
                         "abc123:docs/design/model.md", "采用现行项目定义"):
            self.assertIn(expected, rendered)

    def test_layout_members_are_complete_and_ordered(self):
        document = {"concepts": [concept(TC2), concept(TC1)]}
        layout = {"groups": [
            {"id": "later", "title": "后组", "order": 2, "members": [TC2]},
            {"id": "first", "title": "前组", "order": 1, "members": [TC1]},
        ]}
        self.assertEqual((TC1, TC2), tuple(row["id"] for row in ordered_concepts(document, layout)))

        for bad, code in (
            ({"groups": [{"id": "one", "title": "一", "order": 1, "members": [TC1]}]},
             "TERM_LAYOUT_MEMBER_MISSING"),
            ({"groups": [{"id": "one", "title": "一", "order": 1, "members": [TC1, "tc-99999999-9999-4999-8999-999999999999"]},
                         {"id": "two", "title": "二", "order": 2, "members": [TC2]}]},
             "TERM_LAYOUT_MEMBER_UNKNOWN"),
            ({"groups": [{"id": "one", "title": "一", "order": 1, "members": [TC1, TC1, TC2]}]},
             "TERM_LAYOUT_MEMBER_DUPLICATE"),
        ):
            with self.subTest(code=code), self.assertRaisesRegex(ValueError, code):
                ordered_concepts(document, bad)

    def test_same_concept_can_appear_in_multiple_groups(self):
        document = {"concepts": [concept()]}
        layout = {"groups": [
            {"id": "one", "title": "应用", "order": 1, "members": [TC1]},
            {"id": "two", "title": "生成", "order": 2, "members": [TC1]},
        ]}
        rendered = render_glossary({"concepts": document["concepts"]}, layout, STATE, SOURCES)
        self.assertEqual(2, rendered.count(f"| {TC1} |"))

    def test_term_page_preserves_all_languages_definitions_and_evidence(self):
        value = concept()
        value["subject_fields"] = [{"topic_id": "computing", "basis": basis("subject") }]
        value["source"] = {"registry": "source-a", "item": "source item",
                           "locator": "source locator", "basis": basis("source-basis")}
        value["match"] = [{"registry": "source-a", "item": "matched item",
                            "rel": "exactMatch", "basis": basis("match-basis")}]
        historical = value["languages"][0]["terms"][1]
        historical["administrative_status"] = "supersededTerm-admn-sts"
        historical["replaced_by"] = value["languages"][0]["terms"][0]["id"]
        rendered = render_term_markdown(value, SOURCES)
        for expected in ("# 中文术语 (English term)", "中文定义。", "English definition.",
                         "def-zh", "def-en", "term-zh", "term-en", "term-old",
                         "甲来源", "Source A", "2026", "[甲来源 / Source A · 2026](https://example.test/a)",
                         "核对日期 2026-09-06", "### 简体中文定义", "### 英文形式"):
            self.assertIn(expected, rendered)
        for expected in ("适用学科", "computing", "subject", "概念对应", "source-basis",
                         "match-basis", "替代形式 `tm-11111111-1111-4111-8111-111111111111`"):
            self.assertIn(expected, rendered)
        self.assertNotIn("### en", rendered)
        self.assertNotIn("### zh-Hans", rendered)
        self.assertIn("历史形式", rendered)

    def test_snapshot_contains_readable_source_catalog_and_model_rows(self):
        document = {"schema": "urn:kb-design:schema:terms:1", "version": 1,
                    "concepts": [concept()]}
        snapshot = json.loads(canonical_snapshot(
            document, {"rows": []}, STATE, bibliography_references=SOURCES,
            model_labels=[{"zh": "模型名", "en": "Model name", "targets": ["topics/a"]}],
        ))
        self.assertEqual("甲来源", snapshot["bibliography_references"][0]["label"]["zh"])
        self.assertEqual("模型名", snapshot["model_labels"][0]["zh"])

    def test_model_rows_keep_distinct_chinese_identities_and_reject_stale_scope(self):
        model = {"level": 5, "model": {"name": "gpt", "date": "2026-09-06",
                 "rationale": "r", "approval": "design/decisions/structured-label-basis.md#批次授权"}}
        topics = {"concepts": [
            {"id": "a", "label": {"en": "Same", "zh": "甲"}, "scope": "scope-a", "basis": {"zh": model}},
            {"id": "b", "label": {"en": "Same", "zh": "乙"}, "scope": "scope-b", "basis": {"zh": model}},
        ]}
        adoptions = {
            "topics/a/zh": {"accept": True, "label": "甲", "basis": copy.deepcopy(model), "original": {"en": "Same", "scope": "scope-a"}},
            "topics/b/zh": {"accept": True, "label": "乙", "basis": copy.deepcopy(model), "original": {"en": "Same", "scope": "scope-b"}},
        }
        rows = build_model_label_rows(topics, {"concepts": []}, adoptions, {})
        self.assertEqual([("甲", ["topics/a"]), ("乙", ["topics/b"])],
                         [(row["zh"], row["targets"]) for row in rows])
        self.assertEqual("topics/a", rows[0]["target_models"][0]["target"])
        changed = copy.deepcopy(topics)
        changed["concepts"][0]["label"]["zh"] = "已改名"
        with self.assertRaisesRegex(ValueError, "MODEL_LABEL_ADOPTION_STALE"):
            build_model_label_rows(changed, {"concepts": []}, adoptions, {})
        unknown = copy.deepcopy(adoptions)
        unknown["topics/missing/zh"] = copy.deepcopy(unknown["topics/a/zh"])
        with self.assertRaisesRegex(ValueError, "MODEL_LABEL_TARGET_INVALID"):
            build_model_label_rows(topics, {"concepts": []}, unknown, {})
        adoptions["topics/a/zh"]["original"]["scope"] = "tampered"
        with self.assertRaisesRegex(ValueError, "原 scope 已过期"):
            build_model_label_rows(topics, {"concepts": []}, adoptions, {})

    def test_glossary_keeps_each_concepts_evidence_locations(self):
        value = concept()
        layout = {"groups": [{"id": "one", "title": "应用与生成", "order": 1,
                              "members": [TC1]}]}
        rendered = render_glossary({"concepts": [value]}, layout, STATE, SOURCES)
        for locator in ("concept", "def-en", "def-zh", "term-en", "term-zh", "term-old"):
            self.assertIn(locator, rendered)
        self.assertIn(f"**中文术语**（`{TC1}`）", rendered)
        self.assertNotIn("## 概念依据", rendered)
        self.assertNotIn("### 简体中文定义", rendered)
        self.assertIn("**概念依据**", rendered)
        self.assertIn("**简体中文定义**", rendered)

    def test_correspondence_target_and_relation_change_rendered_output(self):
        value = concept()
        value["source"] = {"registry": "source-a", "item": "source-item",
                           "locator": "source-locator", "basis": basis("same-basis")}
        value["match"] = [{"registry": "source-a", "item": "target-A",
                            "rel": "exactMatch", "basis": basis("same-basis")}]
        first = render_term_markdown(value, SOURCES)
        changed = copy.deepcopy(value)
        changed["match"][0]["item"] = "target-B"
        changed["match"][0]["rel"] = "broadMatch"
        second = render_term_markdown(changed, SOURCES)

        self.assertIn("source-item", first)
        self.assertIn("source-locator", first)
        self.assertIn("target-A", first)
        self.assertIn("exactMatch", first)
        self.assertIn("target-B", second)
        self.assertIn("broadMatch", second)
        self.assertNotEqual(first, second)

    def test_model_chinese_term_and_external_english_term_keep_distinct_evidence(self):
        value = concept()
        model = {"level": 5, "model": {
            "name": "gpt-6-astra", "date": "2026-09-06",
            "rationale": "用于现有概念的中文形式。",
            "approval": "docs/decisions/term-form-adoption.md#中文形式",
        }}
        value["languages"][0]["terms"] = value["languages"][0]["terms"][:1]
        value["languages"][1]["terms"][0]["basis"] = model
        rendered = render_term_markdown(value, SOURCES)
        self.assertIn("模型知识 · 第 5 级，外部中文用法未核实", rendered)
        for expected in model["model"].values():
            self.assertIn(expected, rendered)
        self.assertIn("term-en", rendered)
        glossary = render_glossary(
            {"concepts": [value]},
            {"groups": [{"id": "one", "title": "应用与生成", "order": 1,
                         "members": [TC1]}]}, STATE, SOURCES,
        )
        self.assertIn("模型知识 · 第 5 级，外部中文用法未核实", glossary)
        self.assertIn("term-en", glossary)

        rows = [visit_reference_use(use) for use in collect_reference_uses(
            Path("data/vocab/terms.yaml"), {"concepts": [value]})]
        self.assertNotIn("gpt-6-astra", json.dumps(rows, ensure_ascii=False))

        broken = copy.deepcopy(value)
        del broken["languages"][1]["terms"][0]["basis"]["model"]["approval"]
        with self.assertRaisesRegex(ValueError, "TERM_BASIS_INVALID"):
            render_term_markdown(broken, SOURCES)

    def test_url_locator_keeps_page_description_outside_link_target(self):
        value = concept()
        locator = (
            "https://cdn.example.test/ISO-15489-1-2016.pdf；"
            "PDF p. 10（印刷 p. 2），§3.8 disposition"
        )
        value["basis"] = [{"reference": "source-a", "locator": locator,
                           "checked": "2026-09-06"}]
        rendered = render_term_markdown(value, SOURCES)
        self.assertIn("[定位](https://cdn.example.test/ISO-15489-1-2016.pdf)", rendered)
        self.assertIn("PDF p. 10（印刷 p. 2），§3.8 disposition", rendered)
        self.assertNotIn(f"]({locator})", rendered)


if __name__ == "__main__":
    unittest.main()
