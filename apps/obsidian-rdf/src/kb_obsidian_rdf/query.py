"""Field-scoped vocabulary lookup over the installed, verified identity map.

Search verifies the manifest and records, not every reference file. Reading a
particular entry additionally verifies that page. Article lookup reads real
frontmatter and uses the same reference rules as article validation.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .common import ContractError, digest, json_bytes
from .content import (_REFERENCES, _References, _articles, _identity_key, _parse,
                      _report, _valid_uuid, _wikilink)
from .storage import _check_bytes, _read, read_state, safe_path, vault_lock


FIELDS = ("subject", "entities", "type", "genre", "form", "references")
_KINDS = {"concepts", "entities", "types", "genres", "forms", "references",
          "schemes", "collections", "labels", "notes"}
_SUMMARY_LIMIT = 280


class QueryError(ContractError):
    """A lookup error with reviewable candidates, never an implicit selection."""

    def __init__(self, code: str, message: str, candidates=()):
        super().__init__(message)
        self.code = code
        self.candidates = list(candidates)


def _allowed(field: str) -> set[str]:
    if field not in FIELDS:
        raise QueryError("unsupported_field", "查询字段只能是 " + "、".join(FIELDS))
    return _REFERENCES[field]


def _fast_state(vault: Path, state_root: Path | None = None) -> dict:
    """Verify external identity state without scanning every vocabulary page."""
    state = read_state(vault, state_root=state_root)
    refs = _References(state, {})
    current = set()
    for record in state["records"]["records"]:
        key = _identity_key(record["identity"])
        if record.get("kind") not in _KINDS or not isinstance(record.get("label"), str):
            raise ContractError("身份记录缺少已知对象类型或名称")
        if not isinstance(record.get("restrictions"), list):
            raise ContractError("身份记录限制必须为列表")
        if record["use"] in {"current", "retained"}:
            if key in current:
                raise ContractError("同一身份对应多个当前入口，不能确定查询结果")
            current.add(key)
        _entry(record)
    state["references"] = refs
    return state


def _entry(record: dict) -> dict | None:
    value = record.get("entry")
    if value is None:
        return None
    if not isinstance(value, dict) or not isinstance(value.get("aliases"), list):
        raise ContractError("结构化条目缺少 aliases 列表；请重新生成交付")
    if any(not isinstance(alias, str) for alias in value["aliases"]):
        raise ContractError("结构化条目 aliases 只能包含文字")
    summary = value.get("summary")
    if summary is not None and (not isinstance(summary, dict)
            or not isinstance(summary.get("text"), str)
            or not isinstance(summary.get("predicate"), str)
            or not (summary.get("language") is None or isinstance(summary["language"], str))):
        raise ContractError("条目摘要必须保留文字、语言及说明属性")
    for field in ("definitions", "scope_notes", "descriptions", "notes", "raw_sources"):
        if not isinstance(value.get(field), list):
            raise ContractError(f"结构化条目 {field} 必须为列表")
    relations = value.get("relations")
    if not isinstance(relations, dict):
        raise ContractError("结构化条目缺少关系映射")
    for field in ("broader", "narrower", "related"):
        if not isinstance(relations.get(field), list):
            raise ContractError(f"结构化条目 {field} 必须为关系列表")
        for target in relations[field]:
            if not isinstance(target, dict):
                raise ContractError("关系目标必须保留结构化身份")
            _identity_key(target.get("identity"))
    return value


def _names(record: dict) -> list[str]:
    entry = record.get("entry")
    names = [record["label"]] if record["label"] else []
    if entry is not None:
        names.extend(entry["aliases"])
    else:
        # Older records do not expose plain labels as structured entries. Keep
        # known pref/alt XL names, never hidden names or arbitrary page text.
        for item in record.get("name_records", []):
            if not isinstance(item, dict) or item.get("role") not in {"首选名", "替代名"}:
                continue
            value = item.get("value")
            if isinstance(value, dict) and isinstance(value.get("literal"), str):
                names.append(value["literal"])
    return list(dict.fromkeys(names))


def _available(record: dict) -> bool:
    if record["use"] != "current" or not record["trial_selectable"]:
        return False
    return record["kind"] not in {"types", "genres", "forms", "references"} or record.get("formal_basis") is not None


def _brief(record: dict, matched_alias: str | None = None) -> dict:
    entry = record.get("entry")
    summary = entry.get("summary") if entry else None
    if summary is not None:
        text = summary["text"]
        summary = {"text": text if len(text) <= _SUMMARY_LIMIT else text[:_SUMMARY_LIMIT] + "…",
                   "language": summary["language"], "predicate": summary["predicate"],
                   "truncated": len(text) > _SUMMARY_LIMIT}
    limitations = []
    if entry is None:
        limitations.append("旧交付没有结构化摘要，仅按名称查找；需重新生成以取得完整别名和详情")
    notices = []
    if record.get("formal_basis") is None:
        notices.append("仅预览，正式准用未确认" if record.get('mode', 'preview') == 'preview' else '未获本实例选用授权')
    if record.get('mode') == 'formal' and record['kind'] == 'entities':
        notices.append('应用使用授权不表示实体事实或语义审阅通过')
    if record["use"] != "current":
        notices.append("历史记录可供查阅，不供新的字段选择")
    return {"label": record["label"], "kind": record["kind"], "identity": record["identity"],
            "path": record["path"], "link": _wikilink(record), "summary": summary,
            "matched_alias": matched_alias, "available": _available(record),
            "fields": [field for field, kinds in _REFERENCES.items() if record["kind"] in kinds],
            "use": record["use"], "mode": record.get('mode', 'preview'), "formal_basis": record.get("formal_basis"),
            "restrictions": record["restrictions"], "limitations": limitations, "notices": notices}


def _verification(state: dict, *, page=None, articles=False) -> dict:
    return {"scope": "manifest_records_and_articles" if articles else "manifest_records_and_page" if page else "manifest_and_records",
            "manifest_sha256": state["manifest_sha256"], "records_sha256": state["state_files"]["records.json"]["sha256"],
            "page": None if page is None else {"path": page, "sha256": state["files"][page]["sha256"]},
            "all_managed_files_checked": False, "shacl_rerun": False, "formal_use_checked": state['manifest']['mode'] == 'formal',
            "formal_use_scope": 'application_use' if state['manifest']['mode'] == 'formal' else None,
            "entity_facts_checked": False, "semantic_review_checked": False}


def _match(record: dict, query: str):
    folded = query.casefold()
    matches = []
    for name in _names(record):
        compared = name.casefold()
        if not folded:
            matches.append((3, name))
        elif compared == folded:
            matches.append((0, name))
        elif compared.startswith(folded):
            matches.append((1, name))
        elif folded in compared:
            matches.append((2, name))
    return min(matches, default=None)


def search_entries(vault: Path, *, field: str, query: str = "", limit: int = 10,
                   include_unavailable: bool = False, state_root: Path | None = None) -> dict:
    """Search display names and aliases inside one article field's value domain."""
    allowed = _allowed(field)
    if not isinstance(query, str) or type(limit) is not int or not 1 <= limit <= 1000:
        raise QueryError("invalid_query", "查询文字必须为字符串，limit 必须介于 1 和 1000")
    vault = Path(vault).absolute()
    with vault_lock(vault, state_root=state_root):
        state = _fast_state(vault, state_root=state_root)
        found = []
        for record in state["records"]["records"]:
            if record["kind"] not in allowed or not include_unavailable and not _available(record):
                continue
            match = _match(record, query)
            if match is not None:
                found.append((match[0], record["label"].casefold(), _identity_key(record["identity"]),
                              record["path"], record, match[1]))
        found.sort(key=lambda row: row[:4])
        return {"ok": True, "field": field, "query": query, "total": len(found),
                "items": [_brief(row[4], row[5] if query else None) for row in found[:limit]],
                "verification": _verification(state)}


def _resolve(state: dict, field: str, reference: str | None, term: str | None) -> tuple[dict, str | None]:
    allowed = _allowed(field)
    if (reference is None) == (term is None):
        raise QueryError("lookup_argument", "须明确提供 reference 或 term，且只能提供一种")
    if term is not None:
        if not isinstance(term, str) or not term:
            raise QueryError("invalid_term", "名称必须是非空文字")
        matches = [(record, next((name for name in _names(record) if name.casefold() == term.casefold()), None))
                   for record in state["records"]["records"] if record["kind"] in allowed]
        matches = [(record, name) for record, name in matches if name is not None and _available(record)]
        if len(matches) > 1:
            raise QueryError("ambiguous_term", "字段内名称对应多个对象；请明确选择身份或路径", [_brief(record, name) for record, name in matches])
        if not matches:
            raise QueryError("term_not_selectable", "字段内没有精确且可选择的名称；请先搜索候选，再明确身份")
        return matches[0]
    if not isinstance(reference, str) or not reference:
        raise QueryError("invalid_reference", "引用必须为非空身份、路径或内部链接")
    explicit = reference
    # Only mapped, explicit vault-relative paths are adapted to Wiki links.
    # Other strings remain original identities; names are never coerced.
    path = reference if reference.endswith(".md") else reference + ".md"
    if path in state["references"].paths:
        explicit = "[[" + path + "]]"
    try:
        record = state["references"].resolve(explicit, allowed)
    except ContractError as error:
        raise QueryError("unresolved_reference", str(error)) from error
    if record["kind"] not in allowed:
        raise QueryError("wrong_field", f"{field} 不能选择 {record['kind']} 对象")
    return record, None


def _verify_page(vault: Path, state: dict, record: dict):
    path = record["path"]
    raw = _read(safe_path(vault, path))
    _check_bytes(path, raw, state["files"][path])
    page = _parse(path, raw)
    identity = record["identity"]
    expected = identity.get("iri", identity.get("id"))
    if page.failure or page.metadata.get("identifier") != expected:
        raise ContractError("条目页面身份与已核对的记录不一致：" + path)


def get_entry(vault: Path, *, field: str, reference: str | None = None,
              term: str | None = None, details: bool = False,
              state_root: Path | None = None) -> dict:
    """Resolve an exact selection and return a compact, identity-preserving entry."""
    _allowed(field)
    vault = Path(vault).absolute()
    with vault_lock(vault, state_root=state_root):
        state = _fast_state(vault, state_root=state_root)
        record, matched = _resolve(state, field, reference, term)
        _verify_page(vault, state, record)
        item = _brief(record, matched)
        if details:
            if record.get("entry") is None:
                raise QueryError("entry_missing", "旧交付缺少结构化详情，请重新生成；不会返回整页工程信息")
            item["details"] = record["entry"]
        return {"ok": True, "field": field, "total": 1, "items": [item],
                "verification": _verification(state, page=record["path"])}


def _expanded(state: dict, target: dict, descendants: bool) -> set[str]:
    root = _identity_key(target["identity"])
    if not descendants:
        return {root}
    children = defaultdict(set)
    current = {_identity_key(row["identity"]): row for row in state["records"]["records"]
               if row["kind"] == "concepts" and row["use"] == "current"}
    if target["use"] != "current" or root not in current:
        raise QueryError("historical_hierarchy", "历史目标不能按当前层级展开；请直接查询其原有引用")
    for key, record in current.items():
        entry = record.get("entry")
        if entry is None:
            raise QueryError("hierarchy_missing", "交付缺少结构化层级，请重新生成后再查下位概念")
        for parent in entry["relations"]["broader"]:
            parent_key = _identity_key(parent["identity"])
            if parent_key in current:
                children[parent_key].add(key)
        for child in entry["relations"]["narrower"]:
            child_key = _identity_key(child["identity"])
            if child_key in current:
                children[key].add(child_key)
    visited, pending = set(), [root]
    while pending:
        key = pending.pop()
        if key not in visited:
            visited.add(key)
            pending.extend(children[key] - visited)
    return visited


def find_articles(vault: Path, *, field: str, reference: str | None = None,
                  term: str | None = None, descendants: bool = False,
                  state_root: Path | None = None) -> dict:
    """Find actual article metadata references; body text is never indexing data."""
    allowed = _allowed(field)
    if descendants and field != "subject":
        raise QueryError("unsupported_descendants", "下位概念展开只适用于 subject 字段")
    vault = Path(vault).absolute()
    with vault_lock(vault, state_root=state_root):
        state = _fast_state(vault, state_root=state_root)
        target, matched = _resolve(state, field, reference, term)
        _verify_page(vault, state, target)
        wanted = _expanded(state, target, descendants)
        unregistered = []
        articles = _articles(vault, unregistered=unregistered)
        refs = _References(state, articles)
        report = _report(state, articles, list(articles), unregistered=unregistered)
        found = {}
        for path, article in articles.items():
            identifier = article.metadata.get("identifier")
            if article.failure or not _valid_uuid(identifier):
                continue
            values = article.metadata.get(field, [])
            if field in {"subject", "entities", "references"}:
                if not isinstance(values, list):
                    continue
            else:
                values = [values] if isinstance(values, str) else []
            hits = []
            for value in values:
                if not isinstance(value, str):
                    continue
                try:
                    record = refs.resolve(value, allowed)
                except ContractError:
                    continue
                if record["kind"] not in allowed or _identity_key(record["identity"]) not in wanted:
                    continue
                hit = {"identity": record["identity"], "path": record["path"], "use": record["use"]}
                if hit not in hits:
                    hits.append(hit)
            if not hits:
                continue
            if identifier in found:
                item = found[identifier]
                item["paths"].append(path)
                item["matched_references"].extend(hit for hit in hits if hit not in item["matched_references"])
                continue
            found[identifier] = {"identifier": identifier, "title": article.metadata.get("title"),
                                 "path": path, "paths": [path], "matched_references": hits}
        identities = {key: record["identity"] for key, group in refs.identities.items() for record in group}
        verification = _verification(state, page=target["path"], articles=True)
        verification.update({"article_count": len(articles),
                             "unregistered_count": len(unregistered),
                             "article_snapshot_sha256": digest(json_bytes(report["articles"]))})
        return {"ok": report["ok"], "field": field, "target": _brief(target, matched),
                "descendants": descendants, "match_by": "identity", "expanded_identities": [identities[key] for key in sorted(wanted)],
                "total": len(found), "items": list(found.values()), "issues": report["errors"] + report["issues"],
                "unregistered": report["unregistered"], "unregistered_count": len(unregistered),
                "coverage": report["coverage"],
                "verification": verification}
