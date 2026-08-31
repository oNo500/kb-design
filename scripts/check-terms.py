#!/usr/bin/env python3
"""扫描 Markdown 中的术语使用位置，只输出供人工复核的报告。"""

import argparse
import collections
import json
import pathlib
import re
import sys

import yaml

from governance.check_term_usage import (
    current_markdown_manifest,
    hit_as_dict,
    scan_markdown,
)


ROOT = pathlib.Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "concepts" / "glossary.md"
VOCABULARIES = ("topics.yaml", "entities.yaml", "types.yaml")
VOCABULARY_COLLECTIONS = ("concepts", "entities", "types")
GLOSSARY_SEPARATOR = re.compile(r"\s*/\s*|、|，|,")
CHINESE_PUNCTUATION = re.compile(r"[、，。？！……：；]")
CHINESE_CHARACTER = re.compile(r"[一-鿿]")
TOO_SHORT = re.compile(r"[按由在与和或的是不有]?.{0,1}")

# 这些字符串不是登记写法，也不构成术语准入规则。
EXCLUDED_STRINGS = {
    "本库", "例", "待定", "来源", "规则", "例子", "说明", "其他", "注",
    "字段", "文件", "内容", "问题", "定义", "对象", "权威来源", "待定事项",
    "待办事项", "解决的问题", "在知识库中的用法", "在知识库中",
    "与受控词表的关系", "背景", "决定", "后果", "何时重新考虑", "文章的关系",
    "阅读顺序", "建设流程", "校验规则", "触发条件", "生命周期", "触发与动作",
    "记录", "相关", "标准",
}


def registered_form(value):
    return re.sub(r"[`*]", "", value).strip().lower()


def glossary_forms():
    forms = set()
    for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        if line.startswith("| 术语") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        for cell in cells[:2]:
            for part in GLOSSARY_SEPARATOR.split(cell):
                form = registered_form(part)
                if form:
                    forms.add(form)
    return forms


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested_value in value.values():
            yield from strings(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from strings(nested_value)


def vocabulary_forms():
    forms = set()
    for filename in VOCABULARIES:
        document = yaml.safe_load(
            (ROOT / "vocab" / filename).read_text(encoding="utf-8")
        ) or {}
        for collection_name in VOCABULARY_COLLECTIONS:
            for record in document.get(collection_name, []):
                for field_name in ("label", "alt", "hidden"):
                    for value in strings(record.get(field_name)):
                        form = registered_form(value)
                        if form:
                            forms.add(form)
    return forms


def _load_document(path):
    if path is None:
        return None
    path = pathlib.Path(path)
    value = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(value)
    return yaml.safe_load(value)


def _candidate(hit):
    value = hit.normalized.strip("：:，,。；;（）() ")
    if not CHINESE_CHARACTER.search(value):
        return False
    if value in EXCLUDED_STRINGS or TOO_SHORT.fullmatch(value):
        return False
    if hit.context != "prose":
        return False
    return not CHINESE_PUNCTUATION.search(value)


def _text_report(result, known, show_all):
    files_by_term = collections.defaultdict(set)
    for hit in result:
        if _candidate(hit):
            files_by_term[hit.normalized].add(hit.file)
    rows = sorted(files_by_term.items(), key=lambda item: (-len(item[1]), item[0]))
    lines = [
        f"已登记 {len(known)} 个写法；识别到 {len(rows)} 个"
        "待人工判断的候选字符串（按出现文件数排序）"
    ]
    minimum_files = 1 if show_all else 2
    for term, files in rows:
        if len(files) >= minimum_files:
            locations = ", ".join(sorted(files))[:90]
            lines.append(
                f"  候选字符串：{term}  出现文件数：{len(files):>2}  "
                f"文件：{locations}"
            )
    return "\n".join(lines) + "\n"


def _structured_report(result):
    return {
        "mode": result.mode,
        "blocking_count": len(result.blocking_hits),
        "manifest": {
            "count": len(result.manifest),
            "files": list(result.manifest),
        },
        "hits": [hit_as_dict(hit) for hit in result],
    }


def _render(result, known, arguments):
    if arguments.format == "text":
        return _text_report(result, known, arguments.all)
    report = _structured_report(result)
    if arguments.format == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    columns = (
        "file", "line", "column", "context", "kind", "raw", "normalized",
        "concept_ids", "severity", "conclusion",
    )
    lines = ["\t".join(columns)]
    for hit in report["hits"]:
        row = dict(hit)
        row["concept_ids"] = ",".join(row["concept_ids"])
        lines.append("\t".join(str(row[column]) for column in columns))
    return "\n".join(lines) + "\n"


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--format", choices=("text", "json", "tsv"), default="text")
    parser.add_argument("--output")
    parser.add_argument("--snapshot")
    parser.add_argument("--state")
    parser.add_argument("--decisions")
    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_args(sys.argv[1:] if argv is None else argv)
    known = glossary_forms() | vocabulary_forms()
    snapshot = _load_document(arguments.snapshot) if arguments.snapshot else {
        "known_forms": sorted(known),
        "concepts": [],
    }
    # 可选状态和人工裁定只验证输入可解析；首轮不据此自动形成违规结论。
    _load_document(arguments.state)
    _load_document(arguments.decisions)
    manifest = current_markdown_manifest(ROOT)
    paths = [entry["path"] for entry in manifest]
    result = scan_markdown(ROOT, paths, snapshot)
    rendered = _render(result, known, arguments)
    if arguments.output:
        pathlib.Path(arguments.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
