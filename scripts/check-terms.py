#!/usr/bin/env python3
"""识别正文指定位置中的候选字符串，输出供人工判断的报告。

扫描 concepts/ 与 design/ 的 Markdown 标题、加粗内容和中文引号，排除
代码与链接目标。命中只表示需要人工判断，不构成项目术语、违规或准入
结论。脚本只报告，不修改文件；规则见 design/governance.md“术语准入”。
"""

import collections
import pathlib
import re
import sys

import yaml


ROOT = pathlib.Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "concepts" / "glossary.md"
VOCABULARIES = ("topics.yaml", "entities.yaml", "types.yaml")
VOCABULARY_COLLECTIONS = ("concepts", "entities", "types")

GLOSSARY_SEPARATOR = re.compile(r"\s*/\s*|、|，|,")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
BOLD = re.compile(r"\*\*([^*]{2,14})\*\*")
CHINESE_QUOTE = re.compile(r"“([^”]{2,10})”")
CHINESE_PUNCTUATION = re.compile(r"[、，。？！……：；]")
CHINESE_CHARACTER = re.compile(r"[一-鿿]")
TOO_SHORT = re.compile(r"[按由在与和或的是不有]?.{0,1}")

# 这些字符串不作为抽取结果；它们不是登记写法，也不构成术语准入规则。
EXCLUDED_STRINGS = {
    "本库",
    "例",
    "待定",
    "来源",
    "规则",
    "例子",
    "说明",
    "其他",
    "注",
    "字段",
    "文件",
    "内容",
    "问题",
    "定义",
    "对象",
    "权威来源",
    "待定事项",
    "待办事项",
    "解决的问题",
    "在知识库中的用法",
    "在知识库中",
    "与受控词表的关系",
    "背景",
    "决定",
    "后果",
    "何时重新考虑",
    "文章的关系",
    "阅读顺序",
    "建设流程",
    "校验规则",
    "触发条件",
    "生命周期",
    "触发与动作",
    "记录",
    "相关",
    "标准",
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
        document = (
            yaml.safe_load(
                (ROOT / "vocab" / filename).read_text(encoding="utf-8")
            )
            or {}
        )
        for collection_name in VOCABULARY_COLLECTIONS:
            for record in document.get(collection_name, []):
                for field_name in ("label", "alt", "hidden"):
                    for value in strings(record.get(field_name)):
                        form = registered_form(value)
                        if form:
                            forms.add(form)
    return forms


def markdown_files():
    files = list((ROOT / "concepts").glob("*.md"))
    files.extend((ROOT / "design").rglob("*.md"))
    return sorted(path for path in files if path.name != "glossary.md")


def visible_text(line):
    without_code = INLINE_CODE.sub("", line)
    return LINK_TARGET.sub("]", without_code)


def candidate_strings(line):
    text = visible_text(line)
    heading = HEADING.match(text)
    if heading:
        yield heading.group(1)
    yield from BOLD.findall(text)
    for quoted in CHINESE_QUOTE.findall(text):
        if len(quoted) <= 6 and not CHINESE_PUNCTUATION.search(quoted):
            yield quoted


def normalized_candidate(value):
    return value.strip("：:，,。；;（）() ")


def collect_candidates(known):
    hits = collections.defaultdict(set)
    for path in markdown_files():
        fence = None
        for line in path.read_text(encoding="utf-8").splitlines():
            fence_match = FENCE.match(line)
            if fence_match:
                marker = fence_match.group(1)
                if fence is None:
                    fence = (marker[0], len(marker))
                elif marker[0] == fence[0] and len(marker) >= fence[1]:
                    fence = None
                continue
            if fence is not None:
                continue
            for value in candidate_strings(line):
                candidate = normalized_candidate(value)
                if not CHINESE_CHARACTER.search(candidate):
                    continue
                if candidate.lower() in known or candidate in EXCLUDED_STRINGS:
                    continue
                if TOO_SHORT.fullmatch(candidate):
                    continue
                hits[candidate].add(str(path.relative_to(ROOT)))
    return hits


def report(hits, known):
    rows = sorted(hits.items(), key=lambda item: (-len(item[1]), item[0]))
    print(
        f"已登记 {len(known)} 个写法；识别到 {len(rows)} 个"
        "待人工判断的候选字符串（按出现文件数排序）"
    )
    minimum_files = 1 if "--all" in sys.argv else 2
    for term, files in rows:
        if len(files) >= minimum_files:
            locations = ", ".join(sorted(files))[:90]
            print(
                f"  候选字符串：{term}  出现文件数：{len(files):>2}  "
                f"文件：{locations}"
            )


def main():
    known = glossary_forms() | vocabulary_forms()
    report(collect_candidates(known), known)


if __name__ == "__main__":
    main()
