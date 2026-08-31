#!/usr/bin/env python3
"""动态扫描 Markdown 中可能承担命名功能的写法，只生成复核报告。"""

import dataclasses
import hashlib
import pathlib
import re
import subprocess
from collections import defaultdict
from collections.abc import Sequence
from typing import Iterator, Mapping, Optional, Tuple


FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
PATH_VALUE = re.compile(
    r"(?<![\w.-])(?:/|(?:[A-Za-z0-9_.-]+/)+)[A-Za-z0-9_.@+/-]+"
)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
PARENTHESIZED_ENGLISH = re.compile(
    r"^(?P<zh>.*[一-鿿])\s+\([A-Za-z][^()]*\)$"
)
BOLD = re.compile(r"\*\*([^*]+)\*\*")
CHINESE_QUOTE = re.compile(r"“([^”]+)”")


@dataclasses.dataclass(frozen=True)
class UsageHit:
    file: str
    line: int
    column: int
    context: str
    kind: str
    raw: str
    normalized: str
    concept_ids: Tuple[str, ...]
    severity: str
    conclusion: str
    verdict: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class UsageScan(Sequence):
    hits: Tuple[UsageHit, ...]
    manifest: Tuple[Mapping[str, object], ...]
    mode: str = "report-only"
    blocking_hits: Tuple[UsageHit, ...] = ()

    def __getitem__(self, index):
        return self.hits[index]

    def __len__(self):
        return len(self.hits)

    def __iter__(self) -> Iterator[UsageHit]:
        return iter(self.hits)


def classify_markdown_path(path):
    value = pathlib.PurePosixPath(path).as_posix()
    if value in {"AGENTS.md", "README.md"}:
        return "formal"
    if value.startswith("concepts/"):
        return "generated" if value == "concepts/glossary.md" else "formal"
    if value.startswith("design/drafts/"):
        return "draft"
    if value.startswith("design/decisions/"):
        return "history"
    if value.startswith("design/"):
        return "formal"
    if value.startswith("sources/"):
        return "source"
    if value.startswith("docs/superpowers/"):
        return "audit"
    if value.startswith("vocab/"):
        return "history"
    return "review"


def _git_markdown_paths(repo_root):
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=repo_root,
        check=True,
        capture_output=True,
    )
    return sorted(
        value.decode("utf-8")
        for value in completed.stdout.split(b"\0")
        if value
    )


def current_markdown_manifest(repo_root):
    root = pathlib.Path(repo_root)
    manifest = []
    for relative_path in _git_markdown_paths(root):
        path = root / relative_path
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            scan_state = "pending"
        else:
            digest = "missing"
            scan_state = "missing"
        manifest.append(
            {
                "path": relative_path,
                "sha256": digest,
                "classification": classify_markdown_path(relative_path),
                "scan_state": scan_state,
            }
        )
    return tuple(manifest)


def manifest_delta(previous, current, allowed):
    before = {item["path"]: item["sha256"] for item in previous}
    after = {item["path"]: item["sha256"] for item in current}
    changed = {
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    }
    return sorted(changed - set(allowed))


def _mask_matches(text, patterns):
    masked = list(text)
    for pattern in patterns:
        for match in pattern.finditer(text):
            masked[match.start() : match.end()] = " " * (match.end() - match.start())
    return "".join(masked)


def remove_inline_code_and_link_targets(line):
    return _mask_matches(line, (INLINE_CODE, LINK_TARGET, PATH_VALUE))


def scan_line(line, line_number, context):
    visible = remove_inline_code_and_link_targets(line)
    values = []
    heading = HEADING.match(visible)
    if heading:
        raw = line[heading.start(1) : heading.end(1)]
        parenthesized = PARENTHESIZED_ENGLISH.match(raw)
        normalized = parenthesized.group("zh") if parenthesized else raw
        values.append(
            (line_number, heading.start(1) + 1, context, "heading", raw,
             normalized.strip())
        )
    for kind, pattern in (("bold", BOLD), ("quote", CHINESE_QUOTE)):
        for match in pattern.finditer(visible):
            raw = line[match.start(1) : match.end(1)]
            values.append(
                (line_number, match.start(1) + 1, context, kind, raw, raw.strip())
            )
    return tuple(values)


def _term_texts(snapshot):
    concepts = snapshot.get("concepts", []) if isinstance(snapshot, Mapping) else []
    for concept in concepts:
        if not isinstance(concept, Mapping):
            continue
        concept_id = concept.get("id")
        for language in concept.get("languages", []):
            if not isinstance(language, Mapping):
                continue
            for term in language.get("terms", []):
                if not isinstance(term, Mapping):
                    continue
                text = term.get("text")
                if isinstance(concept_id, str) and isinstance(text, str):
                    yield concept_id, text


def _match_key(value):
    return re.sub(r"[`*]", "", value).strip().casefold()


def _concept_index(snapshot):
    index = defaultdict(set)
    for concept_id, text in _term_texts(snapshot):
        index[_match_key(text)].add(concept_id)
    return {key: tuple(sorted(value)) for key, value in index.items()}


def _known_forms(snapshot):
    if not isinstance(snapshot, Mapping):
        return set()
    values = snapshot.get("known_forms", [])
    return {_match_key(value) for value in values if isinstance(value, str)}


def _context_for(classification):
    if classification in {"formal", "review"}:
        return "prose"
    return "context-only"


def _diagnosis(context, concept_ids):
    if context == "context-only":
        return "info", "context-only"
    if len(concept_ids) > 1:
        return "review", "concept-context-required"
    if len(concept_ids) == 1:
        return "info", "registered-usage"
    return "review", "human-review-required"


def scan_markdown(repo_root, paths, snapshot):
    root = pathlib.Path(repo_root)
    concept_index = _concept_index(snapshot)
    known_forms = _known_forms(snapshot)
    manifest_by_path = {
        entry["path"]: dict(entry) for entry in current_markdown_manifest(root)
    }
    hits = []
    output_manifest = []
    for relative_path in paths:
        relative_path = pathlib.PurePosixPath(relative_path).as_posix()
        classification = classify_markdown_path(relative_path)
        entry = manifest_by_path.get(
            relative_path,
            {
                "path": relative_path,
                "sha256": "missing",
                "classification": classification,
                "scan_state": "missing",
            },
        )
        if classification == "generated":
            entry["scan_state"] = "classified-only"
            output_manifest.append(entry)
            continue
        path = root / relative_path
        if not path.is_file():
            output_manifest.append(entry)
            continue
        entry["scan_state"] = "scanned"
        output_manifest.append(entry)
        context = _context_for(classification)
        fence = None
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
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
            for row in scan_line(line, line_number, context):
                key = _match_key(row[5])
                if key in known_forms:
                    continue
                concept_ids = concept_index.get(key, ())
                severity, conclusion = _diagnosis(context, concept_ids)
                hits.append(
                    UsageHit(
                        file=relative_path,
                        line=row[0],
                        column=row[1],
                        context=row[2],
                        kind=row[3],
                        raw=row[4],
                        normalized=row[5],
                        concept_ids=concept_ids,
                        severity=severity,
                        conclusion=conclusion,
                    )
                )
    return UsageScan(hits=tuple(hits), manifest=tuple(output_manifest))


def hit_as_dict(hit):
    value = dataclasses.asdict(hit)
    value.pop("verdict", None)
    value["concept_ids"] = list(hit.concept_ids)
    return value
