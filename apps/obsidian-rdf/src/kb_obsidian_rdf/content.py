"""Article checks use the installed identity map, never a display-label lookup."""
from __future__ import annotations

import os
import re
import string
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from uuid import UUID, uuid4

import yaml
from markdown_it import MarkdownIt
from rdflib import Literal

from .common import ContractError, digest, safe_relative
from .layout import KIND_DIRECTORIES, PARA_ROOTS, RESOURCES, VOCABULARY
from .naming import filename_stem, path_key
from .storage import inspect, safe_path, vault_lock


_REQUIRED = {"identifier", "title", "type", "genre", "subject", "created", "status"}
_MULTIPLE = {"subject", "entities", "references", "relation"}
_REFERENCES = {
    "subject": {"concepts"}, "entities": {"entities"}, "type": {"types"},
    "genre": {"genres"}, "form": {"forms"}, "references": {"references"},
    "source": {"content", "entities", "references"},
    "relation": {"content"}, "isReplacedBy": {"content"},
}
_FIELDS = _REQUIRED | set(_REFERENCES) | {"level", "modified", "language"}
_LEVELS = {"remember", "understand", "apply", "analyze", "evaluate", "create"}
_MARKDOWN = MarkdownIt("commonmark")


class _UniqueLoader(yaml.SafeLoader):
    """Keep SafeLoader parsing, but reject key replacement in metadata."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                if key in keys:
                    raise ValueError(f"重复的 YAML 字段：{key}")
                keys.add(key)
            except TypeError as error:
                raise ValueError("YAML 字段名必须是可识别的标量") from error
        return super().construct_mapping(node, deep=deep)


@dataclass
class _Article:
    path: str
    raw: bytes
    metadata: dict
    body: str
    failure: str | None = None


def _parse(path: str, raw: bytes) -> _Article:
    try:
        text = raw.decode("utf-8")
        lines = text.splitlines(keepends=True)
        if not lines or lines[0].strip() != "---":
            raise ValueError("缺少文件开头的 YAML 元数据")
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is None:
            raise ValueError("YAML 元数据缺少结束分隔线")
        metadata = yaml.load("".join(lines[1:end]), Loader=_UniqueLoader)
        if not isinstance(metadata, dict) or not all(isinstance(k, str) for k in metadata):
            raise ValueError("元数据必须是字段名到值的映射")
        return _Article(path, raw, metadata, "".join(lines[end + 1:]))
    except (UnicodeError, yaml.YAMLError, ValueError, TypeError, RecursionError) as error:
        return _Article(path, raw, {}, "", str(error))


def _declares_identifier(article: _Article) -> bool:
    """A damaged declaration stays checkable; directory placement is not identity."""
    if article.failure is None:
        return "identifier" in article.metadata
    lines = article.raw.decode("utf-8", errors="replace").splitlines(keepends=True)
    if not lines or lines[0].removeprefix("\ufeff").strip() != "---":
        return False
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), len(lines))
    frontmatter = "".join(lines[1:end])
    # YAML tokenization also recognizes quoted, tagged and explicit keys. It can
    # continue through some syntax errors that stopped the mapping parser.
    key, root_indent, collections = False, 0, []
    starts = (yaml.tokens.BlockMappingStartToken, yaml.tokens.FlowMappingStartToken,
              yaml.tokens.BlockSequenceStartToken, yaml.tokens.FlowSequenceStartToken)
    ends = (yaml.tokens.BlockEndToken, yaml.tokens.FlowMappingEndToken, yaml.tokens.FlowSequenceEndToken)
    try:
        for token in yaml.scan(frontmatter):
            if isinstance(token, starts):
                if not collections:
                    root_indent = token.start_mark.column
                collections.append(token)
                key = False
            elif isinstance(token, ends):
                if collections:
                    collections.pop()
                key = False
            elif isinstance(token, yaml.tokens.KeyToken):
                key = len(collections) == 1 and isinstance(
                    collections[0], (yaml.tokens.BlockMappingStartToken, yaml.tokens.FlowMappingStartToken))
            elif key and isinstance(token, yaml.tokens.ScalarToken):
                if token.value == "identifier":
                    return True
                key = False
            elif not isinstance(token, (yaml.tokens.TagToken, yaml.tokens.AnchorToken)):
                key = False
    except yaml.YAMLError:
        pass
    # A preceding malformed value may prevent reaching a later key. Only inspect
    # the opening metadata block, never promote a mention in the document body.
    return bool(re.search(r'''^[ ]{%d}(?:identifier|"identifier"|'identifier')[ \t]*:''' % root_indent,
                          frontmatter, flags=re.MULTILINE))


def _articles(vault: Path, *, unregistered: list[dict] | None = None) -> dict[str, _Article]:
    found = {}
    for area in PARA_ROOTS:
        directory = safe_path(vault, area)
        if not directory.exists():
            continue
        if not directory.is_dir():
            raise ContractError(f"{area} 必须是文章目录")
        for root, directories, files in os.walk(directory, followlinks=False):
            for name in directories + files:
                if (Path(root) / name).is_symlink():
                    raise ContractError(f"文章目录含符号链接：{Path(root) / name}")
            for name in sorted(files):
                if Path(name).suffix.casefold() == ".md":
                    path = Path(root) / name
                    relative = path.relative_to(vault).as_posix()
                    try:
                        article = _parse(relative, safe_path(vault, relative).read_bytes())
                        if _declares_identifier(article):
                            found[relative] = article
                        elif unregistered is not None:
                            unregistered.append({
                                "path": relative, "sha256": digest(article.raw),
                                "reason": "未确认 identifier 声明；未纳入文章字段校验，不计为通过",
                            })
                    except OSError as error:
                        raise ContractError(f"无法读取文章 {relative}：{error}") from error
    if unregistered is not None:
        unregistered.sort(key=lambda item: item["path"])
    return dict(sorted(found.items()))


def _identity_key(identity: dict) -> str:
    if not isinstance(identity, dict):
        raise ContractError("交付记录缺少结构化身份")
    if set(identity) == {"iri"} and isinstance(identity["iri"], str) and identity["iri"]:
        return identity["iri"]
    if (set(identity) == {"catalog", "id"}
            and all(isinstance(identity[k], str) and identity[k] and "\0" not in identity[k]
                    for k in ("catalog", "id"))):
        return identity["catalog"] + "\0" + identity["id"]
    raise ContractError("交付记录的身份必须为 IRI 或带目录语境的局部 ID")


def _link_path(value: str) -> str | None:
    if not (value.startswith("[[") and value.endswith("]]")):
        return None
    target = value[2:-2].split("|", 1)[0]
    if not target or any(c in target for c in "#^[]\n\r"):
        raise ContractError("字段引用须指向整篇记录，不能使用标题、块或空链接")
    safe_relative(target)
    return target if target.endswith(".md") else target + ".md"


class _References:
    def __init__(self, state: dict, articles: dict[str, _Article]):
        self.paths = {}
        self.identities = defaultdict(list)
        self.articles = articles
        self.article_ids = defaultdict(list)
        managed = {item["path"] for item in state["manifest"]["files"]}
        records = state["records"].get("records")
        if not isinstance(records, list):
            raise ContractError("交付记录必须包含 records 列表")
        for record in records:
            if not isinstance(record, dict):
                raise ContractError("交付记录条目必须是对象")
            key = _identity_key(record.get("identity"))
            path = safe_relative(record.get("path", ""))
            kind = record.get("kind")
            directory = KIND_DIRECTORIES.get(kind)
            parts = path.split("/")
            current_path = directory and len(parts) == 3 and parts[:2] == [VOCABULARY, directory]
            historical_directory = directory or ({"labels": "labels", "notes": "notes"}.get(kind))
            historical_path = (historical_directory and record.get("use") == "historical"
                               and len(parts) == 5 and parts[:2] == [VOCABULARY, "history"]
                               and parts[3] == historical_directory)
            if path not in managed or not (current_path or historical_path) or not path.endswith(".md"):
                raise ContractError(f"参考路径没有交付依据：{path}")
            if path in self.paths:
                raise ContractError(f"参考路径对应多个对象：{path}")
            if record.get("use") not in {"current", "retained", "historical"}:
                raise ContractError(f"参考页面用途不明：{path}")
            if not isinstance(record.get("trial_selectable"), bool):
                raise ContractError(f"参考记录未明确试选资格：{path}")
            self.paths[path] = record
            self.identities[key].append(record)
        for path, article in articles.items():
            value = article.metadata.get("identifier")
            if isinstance(value, str):
                self.article_ids[value].append(path)

    def resolve(self, value: str, allowed: set[str]) -> dict:
        path = _link_path(value)
        if path is not None:
            if path in self.articles:
                return {"kind": "content", "path": path,
                        "identity": {"identifier": self.articles[path].metadata.get("identifier")}}
            if path in self.paths:
                return self.paths[path]
            raise ContractError("链接目标不在已安装参考记录或文章中")
        if "content" in allowed and value in self.article_ids:
            paths = self.article_ids[value]
            if len(paths) != 1:
                raise ContractError("文章身份对应多个文件，不能确定引用目标")
            return {"kind": "content", "path": paths[0], "identity": {"identifier": value}}
        candidates = self.identities.get(value, [])
        if not candidates:
            # 只有字段限定的辅助目录可以使用其原有局部 ID。
            catalogs = allowed & {"types", "genres", "forms", "references"}
            for catalog in catalogs:
                local = value[len(catalog) + 1:] if value.startswith(catalog + ":") else value
                if len(allowed) == 1 or value.startswith(catalog + ":"):
                    candidates.extend(self.identities.get(catalog + "\0" + local, []))
        current = [r for r in candidates if r["use"] in {"current", "retained"}]
        if len(current) == 1:
            return current[0]
        if current or candidates:
            raise ContractError("身份存在歧义或仅有历史版本，请提供明确的参考页链接")
        raise ContractError("无法识别引用身份；名称文字不能代替 IRI、受控 ID 或完整内部链接")


def _valid_uuid(value) -> bool:
    try:
        parsed = UUID(value)
        return isinstance(value, str) and str(parsed) == value and parsed.version == 4
    except (ValueError, TypeError, AttributeError):
        return False


def _date(value) -> date | None:
    if isinstance(value, datetime):
        return None
    if isinstance(value, date):
        return value
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _headings(body: str) -> list[str]:
    # 只读取语法树，不渲染 HTML；代码、引用块里的示例不充当文章主标题。
    tokens = _MARKDOWN.parse(body)
    headings = []
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag == "h1" and token.level == 0:
            inline = tokens[index + 1]
            headings.append("".join(
                child.content if child.type in {"text", "code_inline", "image"}
                else "\n" if child.type in {"softbreak", "hardbreak"} else ""
                for child in inline.children or []))
    return headings


def _report(state: dict, articles: dict[str, _Article], selected: list[str], *, new=False,
            unregistered=()) -> dict:
    references = _References(state, articles)
    result = {
        "ok": True, "errors": [], "issues": [], "formal_unconfirmed": [],
        "mode": state['manifest']['mode'],
        "manifest_sha256": state["manifest_sha256"], "checked_count": len(selected),
        "unregistered": list(unregistered), "unregistered_count": len(unregistered),
        "coverage": {"roots": list(PARA_ROOTS), "identity_field": "identifier",
                     "complete": not unregistered},
        "vocabulary_validation": state["manifest"].get("validation"),
        "articles": [{"path": p, "identifier": articles[p].metadata.get("identifier"),
                      "sha256": digest(articles[p].raw)} for p in selected],
        "dependencies": [{"path": p, "sha256": digest(a.raw)}
                         for p, a in articles.items() if p not in selected],
        "not_checked": ["正文质量、主题选择与关系含义的人工审阅", "内容状态变更的正式批准",
                        "手工编辑的历史引用是否早已存在", "语言标签的 IANA 登记有效性"],
    }

    def issue(path, field, code, message, value=None, *, severity="error"):
        # 日期是 YAML 的正常值，诊断仍须能直接输出 JSON。
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        elif not isinstance(value, (str, int, float, bool, type(None))):
            value = repr(value)
        item = {"severity": severity, "code": code, "path": path,
                "field": field, "value": value, "message": message}
        result["errors" if severity == "error" else "issues"].append(item)

    def resolve(path, field, value, *, enforce=True):
        try:
            target = references.resolve(value, _REFERENCES[field])
        except ContractError as error:
            if enforce:
                issue(path, field, "unresolved_reference", str(error), value)
            return None
        if target["kind"] not in _REFERENCES[field]:
            if enforce:
                issue(path, field, "object_kind", f"字段不能引用 {target['kind']} 对象", value)
            return None
        if target["kind"] == "content":
            target_article = articles[target["path"]]
            identifier = target_article.metadata.get("identifier")
            if (not _valid_uuid(identifier) or len(references.article_ids.get(identifier, [])) != 1
                    or target_article.failure):
                if enforce:
                    issue(path, field, "content_identity", "目标文章的身份无效或不唯一", value)
                return None
            if target["path"] == path and enforce:
                issue(path, field, "self_reference", "文章不能通过该关系引用自身", value)
        elif enforce:
            historical = target["use"] in {"retained", "historical"}
            if historical and not new:
                issue(path, field, "historical_reference", "旧引用可以读取；不证明可用于新的主题标引",
                      value, severity="warning")
            elif historical or not target["trial_selectable"]:
                issue(path, field, "not_selectable", "该对象未获准本次选用，或只保留为历史入口", value)
            if (not historical and target["kind"] in {"types", "genres", "forms", "references"}
                    and target.get("formal_basis") is None):
                issue(path, field, "auxiliary_unapproved", "辅助值域仍须有具体采用依据，不能用概念试选权限代替", value)
            if target.get("formal_basis") is None:
                result["formal_unconfirmed"].append({
                    "path": path, "field": field, "identity": target["identity"],
                    "message": "仅预览，正式准用未确认" if result['mode'] == 'preview' else '该对象未获本实例选用授权',
                })
        return target

    # 全库身份扫描是所选文章的共享依赖，不以局部检查掩盖身份碰撞。
    for path, article in articles.items():
        if article.failure:
            issue(path, None, "frontmatter", article.failure)
    for path in selected:
        article = articles[path]
        if article.failure:
            continue
        data = article.metadata
        for field in sorted(_REQUIRED):
            if field not in data or data[field] in (None, "", []):
                issue(path, field, "required", "缺少必填字段或必要值", data.get(field))
        for field in sorted(_FIELDS & data.keys()):
            value = data[field]
            if field in _MULTIPLE:
                if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
                    issue(path, field, "field_type", "需要非空引用字符串组成的列表", value)
            elif field not in {"created", "modified"} and (not isinstance(value, str) or not value.strip()):
                issue(path, field, "field_type", "需要恰好一个非空文字值；可选字段无值时请省略", value)
        identifier = data.get("identifier")
        if not _valid_uuid(identifier):
            issue(path, "identifier", "identifier", "需要小写、标准连字符、无前缀的 UUIDv4", identifier)
        elif len(references.article_ids[identifier]) != 1:
            issue(path, "identifier", "duplicate_identifier", "UUID 已被其他文章使用：" +
                  "、".join(references.article_ids[identifier]), identifier)
        title = data.get("title")
        if isinstance(title, str) and _headings(article.body) != [title]:
            issue(path, "title", "heading", "正文需要恰好一个与 title 相同的主一级标题", title)
        if not isinstance(data.get("status"), str) or data.get("status") not in {"draft", "active", "deprecated"}:
            issue(path, "status", "status", "状态只能是 draft、active 或 deprecated", data.get("status"))
        if "level" in data and (not isinstance(data["level"], str) or data["level"] not in _LEVELS):
            issue(path, "level", "level", "认知活动不在允许值中", data["level"])
        if "language" in data:
            value = data["language"]
            try:
                if not isinstance(value, str) or not value:
                    raise ValueError("empty")
                Literal("", lang=value)
            except (ValueError, TypeError):
                issue(path, "language", "language", "语言标签格式无效；不会自动改写语言或文字系统", value)
        for field in ("created", "modified"):
            if field in data and _date(data[field]) is None:
                issue(path, field, "date", "需要有效的 YYYY-MM-DD 日期", data[field])
        created, modified = _date(data.get("created")), _date(data.get("modified"))
        if created and modified and modified < created:
            issue(path, "modified", "date_order", "修改日期不能早于建立日期", data["modified"])
        resolved = {}
        for field in _REFERENCES.keys() & data.keys():
            values = data[field] if field in _MULTIPLE else [data[field]]
            if not isinstance(values, list):
                continue
            resolved[field] = [target for value in values if isinstance(value, str) and value
                               if (target := resolve(path, field, value)) is not None]
        if "isReplacedBy" in data and data.get("status") != "deprecated":
            issue(path, "isReplacedBy", "replacement_status", "只有 deprecated 文章可以声明直接后继")
        if data.get("status") == "deprecated" and "isReplacedBy" not in data:
            issue(path, "isReplacedBy", "retirement_reason", "没有后继；需人工核对正文中的退出原因",
                  severity="info")
        for target in resolved.get("relation", []):
            other = articles[target["path"]].metadata.get("relation", [])
            reciprocal = isinstance(other, list) and any(
                isinstance(value, str) and (back := resolve(target["path"], "relation", value, enforce=False))
                and back["path"] == path for value in other)
            if not reciprocal:
                issue(path, "relation", "relation_not_reciprocal", "关联文章尚未反向引用本文章", target["path"])
            if any(item["path"] == target["path"] for field in ("source", "isReplacedBy")
                   for item in resolved.get(field, [])):
                issue(path, "relation", "relation_overlap", "已由来源或替代关系表达的目标不能重复作为 relation",
                      target["path"])
        seen = {path}
        cursor = path
        while isinstance(articles[cursor].metadata.get("isReplacedBy"), str):
            target = resolve(cursor, "isReplacedBy", articles[cursor].metadata["isReplacedBy"], enforce=False)
            if target is None:
                break
            cursor = target["path"]
            if cursor in seen:
                issue(path, "isReplacedBy", "replacement_cycle", "文章直接替代关系形成循环", cursor)
                break
            seen.add(cursor)
        for field in sorted(data.keys() - _FIELDS - {"tags", "aliases", "cssclasses"}):
            issue(path, field, "unrecognized_field", "该字段不属于受控内容合同；不会用于主题或实体标引",
                  severity="info")
    result["ok"] = not result["errors"]
    return result


def check_content(vault: Path, paths: list[str] | None = None, *, state_root: Path | None = None) -> dict:
    """Check article bytes against one verified reference delivery; write nothing."""
    vault = Path(vault).absolute()
    state = inspect(vault, state_root=state_root)
    unregistered = []
    articles = _articles(vault, unregistered=unregistered)
    selected = list(articles)
    if paths is not None:
        selected = []
        for value in paths:
            try:
                path = Path(value)
                relative = path.relative_to(vault).as_posix() if path.is_absolute() else value
                safe_relative(relative)
            except (ValueError, TypeError) as error:
                raise ContractError(f"检查路径不属于预览库：{value}") from error
            if relative in {item["path"] for item in unregistered}:
                continue  # Requested but not identified: report as unchecked, never passed.
            if relative not in articles:
                raise ContractError(f"检查对象不是 PARA 内容区中的既有 Markdown 文章：{relative}")
            if relative not in selected:
                selected.append(relative)
    result = _report(state, articles, selected, unregistered=unregistered)
    result["scope"] = "all" if paths is None else "selected"
    return result


def _wikilink(record: dict) -> str:
    path = record["path"][:-3]
    label = record.get("label")
    if (isinstance(label, str) and label.strip()
            and not any(c in label for c in "|[]#^\n\r") and "%%" not in label):
        return f"[[{path}|{label}]]"
    return f"[[{path}]]"


def new_content(vault: Path, *, title: str, type_id: str, genre_id: str,
                subjects: list[str], entities=(), references=(), form=None,
                level=None, language=None, folder: str = RESOURCES,
                state_root: Path | None = None) -> dict:
    """Create one validated draft without selecting by label or overwriting a note."""
    if (not isinstance(title, str) or not title.strip() or title != title.strip()
            or any(ord(c) < 32 or ord(c) == 127 for c in title)):
        raise ContractError("标题需要非空的单行文字，不能包含控制字符或首尾空白")
    if any(not isinstance(values, (list, tuple)) for values in (subjects, entities, references)):
        raise ContractError("主题、实体和参考文献参数必须为引用列表")
    if not isinstance(folder, str):
        raise ContractError("文章目录须为 PARA 内容区中的明确相对路径")
    safe_relative(folder)
    parts = folder.split("/")
    if parts[0] not in PARA_ROOTS or any(filename_stem(part) != part for part in parts):
        raise ContractError("文章目录须位于 " + "、".join(PARA_ROOTS) + "；目录名用小写与中划线")
    vault = Path(vault).absolute()
    with vault_lock(vault, state_root=state_root):
        state = inspect(vault, state_root=state_root)
        unregistered = []
        existing = _articles(vault, unregistered=unregistered)
        invalid = [a.path for a in existing.values() if a.failure or not _valid_uuid(a.metadata.get("identifier"))]
        if invalid:
            raise ContractError("既有文章身份无法完整核对：" + "、".join(invalid))
        ids = [a.metadata["identifier"] for a in existing.values()]
        if len(ids) != len(set(ids)):
            raise ContractError("既有文章存在重复 UUID，请先处理身份冲突")
        relative = safe_relative(f"{folder}/{filename_stem(title)}.md")
        destination = safe_path(vault, relative)
        if destination.exists() or (destination.parent.exists() and any(
                path_key(child.name) == path_key(destination.name) for child in destination.parent.iterdir())):
            raise ContractError(f"同名文章已存在，不会覆盖：{relative}")
        for _ in range(10):
            identifier = str(uuid4())
            if identifier not in ids:
                break
        else:
            raise ContractError("未能分配唯一 UUID")
        metadata = {"identifier": identifier, "title": title, "type": type_id,
                    "genre": genre_id, "subject": list(subjects),
                    "created": date.today(), "status": "draft"}
        for field, value in {"entities": list(entities), "references": list(references),
                             "form": form, "level": level, "language": language}.items():
            if value is not None and value != []:
                metadata[field] = value
        heading = title.translate(str.maketrans({c: "\\" + c for c in string.punctuation}))
        body = f"\n# {heading}\n\n"
        candidate = _Article(relative, b"", metadata, body)
        all_articles = {**existing, relative: candidate}
        report = _report(state, all_articles, [relative], new=True, unregistered=unregistered)
        if not report["ok"]:
            raise ContractError("文章建立失败：" + "；".join(
                f"{item['field'] or item['path']}：{item['message']}" for item in report["errors"]))
        lookup = _References(state, all_articles)
        for field in _REFERENCES.keys() & metadata.keys():
            values = metadata[field] if field in _MULTIPLE else [metadata[field]]
            links = [_wikilink(lookup.resolve(value, _REFERENCES[field])) for value in values]
            metadata[field] = links if field in _MULTIPLE else links[0]
        raw = ("---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
               + "---\n" + body).encode("utf-8")
        candidate.raw = raw
        report = _report(state, all_articles, [relative], new=True, unregistered=unregistered)
        report["scope"] = "new"
        # 写前重新核对参考交付；完整暂存后独占安装，避免暴露半篇文章。
        if inspect(vault, state_root=state_root)["manifest_sha256"] != state["manifest_sha256"]:
            raise ContractError("参考版本已变化，请重新建立文章")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination = safe_path(vault, relative)
        temporary = None
        try:
            fd, temporary = tempfile.mkstemp(prefix=".draft-", suffix=".tmp", dir=destination.parent)
            with os.fdopen(fd, "wb") as stream:
                stream.write(raw)
            destination = safe_path(vault, relative)
            os.chmod(temporary, 0o644)
            os.link(temporary, destination, follow_symlinks=False)
        except OSError as error:
            raise ContractError(f"文章没有完成安装，不会覆盖已有文件：{relative}：{error}") from error
        finally:
            if temporary is not None:
                Path(temporary).unlink(missing_ok=True)
        return {"path": relative, "identifier": identifier, "report": report}
