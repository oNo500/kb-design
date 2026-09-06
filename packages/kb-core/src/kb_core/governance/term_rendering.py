"""Readable Markdown views of captured terminology records."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping, Sequence

from kb_core.governance.term_model import term_basis_kind


PREFERRED = "preferredTerm-admn-sts"
ADMITTED = "admittedTerm-admn-sts"
HISTORICAL = {"deprecatedTerm-admn-sts", "supersededTerm-admn-sts"}
LANGUAGE_ORDER = {"zh-Hans": 0, "zh-Hant": 1, "en": 2}
LANGUAGE_TITLES = {"zh-Hans": "简体中文", "zh-Hant": "繁体中文", "en": "英文"}
READ_ONLY_DECLARATION = (
    "本文件只读。概念、定义和术语形式由 `data/vocab/terms.yaml` 管理；"
    "章节编排、说明、关系符号和历史名称展示由 "
    "`data/inputs/terminology/glossary-layout.yaml` 管理；模型标签继续由各自现行编辑源"
    "（`data/inputs/topics/`、`data/vocab/forms.yaml`）及 "
    "`data/inputs/topics/label-adoptions.json` 的既有采纳记录管理。"
)


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(_plain(value), ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode()


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _source_rows(references: Sequence[Mapping[str, object]], source_entities):
    rows = []
    for reference in references:
        entity_id = reference.get("entity", "?")
        entity = source_entities.get(entity_id, {}) if isinstance(source_entities, Mapping) else {}
        label = entity.get("label", {}) if isinstance(entity, Mapping) else {}
        names = " / ".join(str(label[key]) for key in ("zh", "en") if label.get(key))
        name = names or str(entity_id)
        version = entity.get("version")
        urls = [row.get("url") for row in entity.get("urls", [])
                if isinstance(row, Mapping) and row.get("url")]
        description = name + ((" · " + str(version)) if version else "")
        if urls:
            description = f"[{description}]({urls[0]})"
        locator = reference.get("locator")
        if locator:
            locator_text = str(locator)
            match = re.fullmatch(r"(https?://[^\s；]+)(?:[；\s]+(.+))?", locator_text)
            if match:
                description += f" · [定位]({match.group(1)})"
                if match.group(2):
                    description += " · " + match.group(2)
            else:
                description += " · " + locator_text
        checked = reference.get("checked")
        if checked:
            description += " · 核对日期 " + str(checked)
        rows.append(description)
    return rows


def _evidence_lines(basis, source_entities):
    if isinstance(basis, Mapping):
        kind = term_basis_kind(basis)
        if kind == "project" or (set(basis) == {"project"} and isinstance(basis["project"], Mapping)):
            project = basis["project"]
            origin = project.get("origin", {})
            return [
                "项目决定依据，不是外部来源",
                "采纳决定：" + str(project.get("approval", "—")),
                "项目原文：`" + str(origin.get("commit", "—")) + ":"
                + str(origin.get("file", "—")) + "` · " + str(origin.get("locator", "—")),
                "采用理由：" + str(project.get("rationale", "—")),
            ]
        if kind != "model":
            raise ValueError("TERM_BASIS_INVALID")
        model = basis["model"]
        return [
            "模型知识 · 第 5 级，外部中文用法未核实",
            "模型名称：" + model["name"],
            "判断日期：" + model["date"],
            "判断理由：" + model["rationale"],
            "采纳授权：" + model["approval"],
        ]
    rows = _source_rows(basis or (), source_entities)
    return rows or ["未登记。"]


def _preferred(concept):
    result = {}
    for language in concept.get("languages", []):
        terms = [term for term in language.get("terms", [])
                 if term.get("administrative_status") == PREFERRED]
        if len(terms) != 1:
            raise ValueError(f"TERM_PREFERRED_TERM_COUNT {concept['id']} {language.get('language')}")
        result[language["language"]] = terms[0]["text"]
    return result


def _concept_layout_rows(concept_id, layout):
    symbols = [row for row in (layout or {}).get("symbol_mappings", [])
               if concept_id in row.get("concept_ids", [])]
    historical = [row for row in (layout or {}).get("historical_designations", [])
                  if concept_id in row.get("target_concept_ids", [])]
    return symbols, historical


def render_term_markdown(concept, source_entities, *, layout=None) -> str:
    """Render one concept body, including every language and evidence layer."""
    preferred = _preferred(concept)
    chinese = preferred.get("zh-Hans") or preferred.get("zh-Hant")
    english = preferred.get("en")
    title = chinese or english or concept["id"]
    if chinese and english:
        title += f" ({english})"
    lines = [f"# {title}", "", f"概念 ID：`{concept['id']}`。", "", "## 概念依据", ""]
    lines.extend(f"- {row}" for row in _evidence_lines(concept.get("basis"), source_entities))
    lines.extend(["", "## 定义", ""])
    definitions = sorted(concept.get("definitions", []),
                         key=lambda row: (LANGUAGE_ORDER.get(row.get("language"), 99), row.get("text", "")))
    if not definitions:
        lines.append("无。")
    for definition in definitions:
        lines.extend([f"### {LANGUAGE_TITLES.get(definition['language'], '其他语言')}定义", "", definition["text"], "", "依据："])
        lines.extend(f"- {row}" for row in _evidence_lines(definition.get("basis"), source_entities))
        lines.append("")
    subject_fields = concept.get("subject_fields", [])
    if subject_fields:
        lines.extend(["## 适用学科", ""])
        for field in subject_fields:
            lines.append(f"- {field['topic_id']}")
            lines.extend(f"  - 依据：{row}" for row in _evidence_lines(field.get("basis"), source_entities))
        lines.append("")
    if concept.get("source") or concept.get("match"):
        lines.extend(["## 概念对应", ""])
        for kind, values in (("来源", [concept.get("source")] if concept.get("source") else []),
                             ("映射", concept.get("match", []))):
            for value in values:
                identity = value.get("registry") or value.get("entity") or value.get("id") or "未标识"
                details = [str(identity)]
                if value.get("item"):
                    details.append("目标项 " + str(value["item"]))
                if value.get("rel"):
                    details.append("关系 " + str(value["rel"]))
                if value.get("locator"):
                    locator = str(value["locator"])
                    details.append(
                        f"[来源定位]({locator})"
                        if locator.startswith(("http://", "https://"))
                        else "来源定位 " + locator
                    )
                lines.append(f"- {kind}：" + " · ".join(details))
                lines.extend(f"  - 依据：{row}" for row in _evidence_lines(value.get("basis"), source_entities))
        lines.append("")
    lines.extend(["## 术语形式", ""])
    historical = []
    for language in sorted(concept.get("languages", []),
                           key=lambda row: LANGUAGE_ORDER.get(row.get("language"), 99)):
        lines.extend([f"### {LANGUAGE_TITLES.get(language['language'], '其他语言')}形式", ""])
        for term in language.get("terms", []):
            status = term["administrative_status"]
            if status in HISTORICAL:
                historical.append((language["language"], term))
                continue
            lines.append(f"- {term['text']}（`{term['id']}`；{status}）")
            lines.extend(f"  - 依据：{row}" for row in _evidence_lines(term.get("basis"), source_entities))
        lines.append("")
    lines.extend(["## 历史形式", ""])
    if historical:
        for language, term in historical:
            replacement = f"；替代形式 `{term['replaced_by']}`" if term.get("replaced_by") else ""
            lines.append(f"- {LANGUAGE_TITLES.get(language, '其他语言')}：{term['text']}（`{term['id']}`；{term['administrative_status']}{replacement}）")
            lines.extend(f"  - 依据：{row}" for row in _evidence_lines(term.get("basis"), source_entities))
    else:
        lines.append("无。")
    symbols, historical_designations = _concept_layout_rows(concept["id"], layout)
    if symbols:
        lines.extend(["", "## 关系符号", ""])
        for row in symbols:
            lines.append("- " + " / ".join(row["symbols"]) + "：" + row["display_note"])
    if historical_designations:
        lines.extend(["", "## 历史名称", ""])
        for row in historical_designations:
            lines.append("- " + " / ".join(row["forms"]) + "：已退出所列概念的当前准用名称。")
            lines.append("  - " + row["display"])
            lines.append("  - 原因：" + row["reason"])
            lines.append("  - 效力：" + row["effect"])
            lines.append("  - 采纳决定：" + row["approval"])
    return "\n".join(lines).rstrip() + "\n"


def _layout_entry_lines(entry):
    lines = ["- " + "｜".join(entry["cells"])]
    for key, title in (("meaning", "性质"), ("scope_note", "范围"),
                       ("scope", "范围"), ("basis_note", "依据"),
                       ("verification", "核验"), ("display_notice", "说明")):
        if entry.get(key):
            lines.append("  - " + title + "：" + entry[key])
    return lines


def _summary_row(concept):
    preferred = _preferred(concept)
    chinese = "；".join(preferred[tag] for tag in ("zh-Hans", "zh-Hant") if tag in preferred) or "—"
    english = preferred.get("en", "—")
    definitions = "；".join(f"{row['language']}：{row['text']}" for row in
                           sorted(concept.get("definitions", []), key=lambda row: LANGUAGE_ORDER.get(row["language"], 99))) or "—"
    admitted = []
    for language in concept.get("languages", []):
        admitted.extend(f"{language['language']}：{term['text']}" for term in language.get("terms", [])
                        if term["administrative_status"] == ADMITTED)
    return "| " + " | ".join(map(_cell, (chinese, english, definitions, "；".join(admitted) or "—", concept["id"]))) + " |"


def render_glossary(snapshot, layout, state, source_entities=None) -> str:
    if not state.get("consumers_enabled") or state.get("terms_mode") != "active_editor" or state.get("state") != "active":
        raise ValueError("TERM_CONSUMERS_DISABLED")
    concepts = {row["id"]: row for row in snapshot.get("concepts", []) if row.get("workflow") == "active"}
    covered = set()
    for group in layout.get("groups", []):
        members = group.get("members", [])
        if len(members) != len(set(members)):
            raise ValueError("TERM_LAYOUT_MEMBER_DUPLICATE " + group.get("id", "?"))
        unknown = sorted(set(members) - set(concepts))
        if unknown:
            raise ValueError("TERM_LAYOUT_MEMBER_UNKNOWN " + " ".join(unknown))
        covered.update(members)
    missing = sorted(set(concepts) - covered)
    if missing:
        raise ValueError("TERM_LAYOUT_MEMBER_MISSING " + " ".join(missing))
    lines = ["# 术语表 (Glossary)", READ_ONLY_DECLARATION, "",
             "本页按应用章节编排，并由同一已校验快照确定生成。", "",
             "快照 SHA-256：`" + hashlib.sha256(_canonical_json(snapshot)).hexdigest() + "`。"]
    abbreviation_section = layout.get("source_abbreviations", {})
    if abbreviation_section.get("entries"):
        lines.extend(["", "## " + abbreviation_section["title"], ""])
        for entry in abbreviation_section["entries"]:
            lines.extend(_layout_entry_lines(entry))
    for group in sorted(layout["groups"], key=lambda row: (row["order"], row["id"])):
        lines.extend(["", "## " + group["title"], "",
                      "| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |",
                      "|---|---|---|---|---|"])
        lines.extend(_summary_row(concepts[concept_id]) for concept_id in group["members"])
        for concept_id in group["members"]:
            concept = concepts[concept_id]
            preferred = _preferred(concept)
            name = (preferred.get("zh-Hans") or preferred.get("zh-Hant")
                    or preferred.get("en") or concept_id)
            lines.extend(["", f"**{name}**（`{concept_id}`）", ""])
            detail = render_term_markdown(concept, source_entities or {}).splitlines()[2:]
            for line in detail:
                if line.startswith("概念 ID："):
                    continue
                if line.startswith("### "):
                    lines.append("**" + line[4:] + "**")
                elif line.startswith("## "):
                    lines.append("**" + line[3:] + "**")
                else:
                    lines.append(line)
    if layout.get("reference_entries"):
        lines.extend(["", "## 补充说明", ""])
        for entry in layout["reference_entries"]:
            lines.extend(_layout_entry_lines(entry))
    if layout.get("symbol_mappings"):
        lines.extend(["", "## 关系符号", ""])
        for row in layout["symbol_mappings"]:
            lines.append("- " + " / ".join(row["symbols"]) + "：" + row["display_note"]
                         + " 参见 " + "、".join(f"`{item}`" for item in row["concept_ids"]) + "。")
    if layout.get("historical_designations"):
        lines.extend(["", "## 历史名称", ""])
        for row in layout["historical_designations"]:
            lines.append("- " + " / ".join(row["forms"]) + "：已退出所列概念的当前准用名称。")
            lines.append("  - " + row["display"])
            lines.append("  - 原因：" + row["reason"])
            lines.append("  - 效力：" + row["effect"])
            lines.append("  - 目标：" + "、".join(f"`{item}`" for item in row["target_concept_ids"]))
    appendix = layout.get("standards_appendix", {})
    if appendix.get("entries"):
        lines.extend(["", "## " + appendix["title"], ""])
        for entry in appendix["entries"]:
            lines.extend(_layout_entry_lines(entry))
    lines.extend(["", "## 来源目录", ""])
    catalog = source_entities or {row["id"]: row for row in snapshot.get("source_entities", [])}
    if catalog:
        for entity_id in sorted(catalog):
            entity = catalog[entity_id]
            labels = " / ".join(entity.get("label", {}).values())
            urls = [row.get("url") for row in entity.get("urls", []) if row.get("url")]
            display = f"[{labels}]({urls[0]})" if urls else labels
            lines.append(f"- {entity_id}：{display}")
    else:
        lines.append("当前没有已编排术语成员，因此没有术语引用的来源目录。")
    lines.extend(["", "## 模型译名", ""])
    for row in snapshot.get("model_labels", []):
        lines.append(f"- {row.get('zh', '—')} / {row.get('en', '—')}：{', '.join(row.get('targets', []))}")
        for target_model in row.get("target_models", []):
            model = target_model["model"]
            lines.append(
                f"  - {target_model['target']}：模型知识 · 第 5 级，外部用法未核实；"
                f"{model.get('name', '—')}；{model.get('date', '—')}；"
                f"{model.get('rationale', '—')}；{model.get('approval', '—')}"
            )
    if not snapshot.get("model_labels"):
        lines.append("无。")
    return "\n".join(lines) + "\n"
