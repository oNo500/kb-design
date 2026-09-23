"""External installation state and recoverable, explicitly owned file changes.

The lock coordinates this tool only. Refresh/recovery require other writers and
sync to be paused. Two directory locations are reconciled using a prewrite
journal; this is not a cross-directory transaction or a durability guarantee.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import difflib
import fcntl
import json
import os
from pathlib import Path
import posixpath
import re
import stat
from urllib.parse import unquote, urlsplit
import unicodedata
from uuid import UUID, uuid4

import yaml
from markdown_it import MarkdownIt

from .common import ContractError, Delivery, digest, json_bytes, safe_relative
from .layout import (MANIFEST_VERSION, PARA_ROOTS, TEMPLATES, VAULT_DIRECTORIES,
                     VIEWS, VOCABULARY)

MANIFEST = "manifest.json"
CURRENT = "current.json"
RECOVERY = "recovery.json"
TOOL = "kb-obsidian-rdf"


def _absolute(path: Path) -> Path:
    path = Path(os.path.abspath(path.expanduser()))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ContractError(f"路径包含符号链接：{part}")
    return path


def safe_path(root: Path, relative: str) -> Path:
    """Locate a safe relative path in either a vault or its external state."""
    return _absolute(_absolute(root) / safe_relative(relative))


def _path_identity(path: Path) -> str:
    return unicodedata.normalize("NFC", str(path)).casefold()


def _state_root(state_root: Path | None = None) -> Path:
    default = Path(__file__).resolve().parents[4] / "output/obsidian-rdf/state"
    return _absolute(Path(state_root or os.environ.get("KB_OBSIDIAN_STATE_ROOT") or default))


def _device(path: Path) -> int:
    while not path.exists():
        path = path.parent
    return path.stat().st_dev


def state_directory(vault: Path, state_root: Path | None = None) -> Path:
    """Resolve this vault's external state without creating either location."""
    vault, root = _absolute(vault), _state_root(state_root)
    v, r = _path_identity(vault), _path_identity(root)
    if v == r or v.startswith(r.rstrip("/") + "/") or r.startswith(v.rstrip("/") + "/"):
        raise ContractError("工程状态必须位于库外，状态根目录与知识库不能重叠")
    if _device(vault) != _device(root):
        raise ContractError("当前开发版要求工程状态与知识库位于同一文件系统；请指定同卷的库外 state-root")
    return safe_path(root, digest(v.encode("utf-8")))


@contextmanager
def vault_lock(vault: Path, state_root: Path | None = None):
    """One nonblocking sibling lock, even for callers with different state roots."""
    vault = _absolute(vault)
    state_directory(vault, state_root)
    vault.parent.mkdir(parents=True, exist_ok=True)
    lock_path = _absolute(vault.parent / (".kb-obsidian-rdf-" + digest(_path_identity(vault).encode())[:24] + ".lock"))
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ContractError(f"锁路径不是普通文件：{lock_path}")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ContractError("知识库正被另一个工具操作占用") from error
        yield
    finally:
        os.close(descriptor)


def _object(data: bytes, label: str) -> dict:
    try:
        value = json.loads(data)
    except (UnicodeError, ValueError) as error:
        raise ContractError(f"JSON 无法读取：{label}") from error
    if not isinstance(value, dict):
        raise ContractError(f"需要 JSON 对象：{label}")
    return value


def _read(path: Path) -> bytes:
    path = _absolute(path)
    if not path.is_file():
        raise ContractError(f"所需普通文件缺失：{path}")
    return path.read_bytes()


def _json(path: Path) -> dict:
    return _object(_read(path), str(path))


def _tree(directory: Path) -> dict[str, Path]:
    directory = _absolute(directory)
    if not directory.is_dir():
        raise ContractError(f"所需目录缺失：{directory}")
    result = {}
    for root, dirs, names in os.walk(directory, followlinks=False):
        for name in [*dirs, *names]:
            path = _absolute(Path(root) / name)
            if not path.is_dir() and not path.is_file():
                raise ContractError(f"不支持的文件类型：{path}")
        for name in names:
            path = Path(root) / name
            result[path.relative_to(directory).as_posix()] = path
    return result


def _manifest_entries(manifest: dict, field: str = "files") -> dict[str, dict]:
    if manifest.get("format_version") != MANIFEST_VERSION or manifest.get("mode") != "preview":
        raise ContractError(f"只接受第 {MANIFEST_VERSION} 版 preview 交付清单；旧库需另行迁移")
    rows = manifest.get(field)
    if not isinstance(rows, list):
        raise ContractError(f"交付清单 {field} 必须为列表")
    entries, filesystem_names = {}, set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise ContractError("交付文件记录缺少路径")
        path = safe_relative(row["path"])
        alias = unicodedata.normalize("NFC", path).casefold()
        if (path in entries or alias in filesystem_names or path == MANIFEST
                or (field == "files" and (not path.startswith(VOCABULARY + "/") or not path.endswith(".md")))
                or (field == "state_files" and path.startswith(VOCABULARY + "/"))):
            raise ContractError(f"交付文件重复或越过受管理范围：{path}")
        if (not isinstance(row.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"])
                or type(row.get("size")) is not int or row["size"] < 0):
            raise ContractError(f"交付文件摘要或长度无效：{path}")
        entries[path] = row
        filesystem_names.add(alias)
    if field == "state_files" and not {"records.json", "projection.json"} <= entries.keys():
        raise ContractError("交付清单缺少身份或投影记录")
    return entries


def _check_bytes(path: str, data: bytes, entry: dict):
    if len(data) != entry.get("size") or digest(data) != entry.get("sha256"):
        raise ContractError(f"受管理文件发生变化或摘要不符：{path}")


def _delivery(delivery: Delivery) -> tuple[dict, str]:
    if not isinstance(delivery, Delivery) or MANIFEST not in delivery.state_files:
        raise ContractError("交付需要 Delivery 及库外 manifest.json")
    for path, data in delivery.vault_files.items():
        safe_relative(path)
        allowed = (path == "home.md"
                   or path.startswith((VOCABULARY + "/", TEMPLATES + "/")) and path.endswith(".md")
                   or path.startswith(VIEWS + "/") and path.endswith((".base", ".md")))
        if not allowed or not isinstance(data, bytes):
            raise ContractError(f"初建文件超出允许范围或不是字节内容：{path}")
    for path, data in delivery.state_files.items():
        safe_relative(path)
        if not isinstance(data, bytes):
            raise ContractError(f"工程文件不是字节内容：{path}")
    manifest = _object(delivery.state_files[MANIFEST], MANIFEST)
    for field, supplied in (("files", delivery.vault_files), ("state_files", delivery.state_files)):
        entries = _manifest_entries(manifest, field)
        actual = ({path for path in supplied if path.startswith(VOCABULARY + "/")} if field == "files"
                  else supplied.keys() - {MANIFEST})
        if actual != entries.keys():
            raise ContractError(f"交付文件集合与 {field} 清单不一致")
        for path, entry in entries.items():
            _check_bytes(path, supplied[path], entry)
    return manifest, digest(delivery.state_files[MANIFEST])


def _record_object(raw: bytes) -> dict:
    records = _object(raw, "records.json")
    if (records.get("format_version") != 1 or not isinstance(records.get("records"), list)
            or any(not isinstance(row, dict) or not isinstance(row.get("identity"), dict)
                   for row in records["records"])):
        raise ContractError("身份记录结构无效")
    return records


def _read_snapshot(directory: Path, expected: str | None = None, *, full: bool = True) -> dict:
    raw = _read(safe_path(directory, MANIFEST))
    manifest_hash = digest(raw)
    if expected is not None and manifest_hash != expected:
        raise ContractError("manifest 与安装凭据或恢复记录不符")
    manifest = _object(raw, str(directory / MANIFEST))
    files, state_files = _manifest_entries(manifest), _manifest_entries(manifest, "state_files")
    if full:
        actual = _tree(directory)
        if actual.keys() != state_files.keys() | {MANIFEST}:
            raise ContractError("外部状态文件集合冲突")
        for path, entry in state_files.items():
            _check_bytes(path, _read(actual[path]), entry)
    records_raw = _read(safe_path(directory, "records.json"))
    _check_bytes("records.json", records_raw, state_files["records.json"])
    return {"manifest": manifest, "manifest_sha256": manifest_hash, "records": _record_object(records_raw),
            "files": files, "state_files": state_files}


def _verify_vocabulary(directory: Path, snapshot: dict):
    actual = _tree(directory)
    entries = snapshot["files"]
    prefix = VOCABULARY + "/"
    expected = {path.removeprefix(prefix) for path in entries}
    if actual.keys() != expected:
        raise ContractError(f"词条文件集合冲突；未知文件：{sorted(actual.keys() - expected)}；缺失文件：{sorted(expected - actual.keys())}")
    for path, entry in entries.items():
        _check_bytes(path, _read(actual[path.removeprefix(prefix)]), entry)


def _binding(vault: Path, state_dir: Path) -> dict:
    binding = _json(safe_path(state_dir, "binding.json"))
    try:
        valid_id = str(UUID(binding.get("vault_id", ""))) == binding.get("vault_id")
    except (ValueError, TypeError, AttributeError):
        valid_id = False
    if (binding.get("tool") != TOOL or binding.get("format_version") != 1 or not valid_id
            or not isinstance(binding.get("vault"), str)
            or _path_identity(Path(binding["vault"])) != _path_identity(vault)
            or binding.get("state_dir") != str(state_dir)):
        raise ContractError("外部状态绑定与目标知识库不一致，不会接管或自动迁移")
    return binding


def _current(vault: Path, state_root: Path | None, allow_pending: bool, *, full: bool) -> dict:
    vault = _absolute(vault)
    state_dir = state_directory(vault, state_root)
    binding = _binding(vault, state_dir)
    pending_path = safe_path(state_dir, RECOVERY)
    pending = _json(pending_path) if pending_path.exists() else None
    if pending is not None and not allow_pending:
        raise ContractError("知识库存在未完成操作，请先执行 recover 恢复")
    if not vault.is_dir():
        raise ContractError("已绑定的知识库目录缺失，不会自动重新绑定或迁移")
    receipt = _json(safe_path(state_dir, CURRENT))
    if (receipt.get("vault_id") != binding["vault_id"] or receipt.get("result") != "installed"
            or receipt.get("target") != binding["vault"]
            or not isinstance(receipt.get("manifest_sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", receipt["manifest_sha256"])):
        raise ContractError("安装凭据不属于该知识库或尚未完成")
    snapshot = _read_snapshot(safe_path(state_dir, "current"), receipt["manifest_sha256"], full=full)
    if full:
        _verify_vocabulary(safe_path(vault, VOCABULARY), snapshot)
    return {**snapshot, "vault": str(vault), "state_dir": str(state_dir), "receipt": receipt, "pending": pending}


def read_state(vault: Path, state_root: Path | None = None) -> dict:
    """Read identity/index state, checking hashes without scanning all pages."""
    return _current(vault, state_root, False, full=False)


def inspect(vault: Path, allow_pending: bool = False, state_root: Path | None = None) -> dict:
    """Verify all managed vocabulary and state files; writers hold vault_lock."""
    return _current(vault, state_root, allow_pending, full=True)


def _write(path: Path, data: bytes, *, exclusive: bool = False):
    path = _absolute(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if exclusive:
        with path.open("xb") as output:
            output.write(data)
        return
    temporary = path.with_name("." + path.name + "." + uuid4().hex)
    try:
        with temporary.open("xb") as output:
            output.write(data)
        _absolute(path)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _receipt(vault: Path, state_dir: Path, binding: dict, snapshot: dict, operation: str, operation_id: str) -> dict:
    receipt = {"format_version": 1, "vault_id": binding["vault_id"], "target": binding["vault"],
               "operation": operation, "operation_id": operation_id, "result": "installed",
               "manifest_sha256": snapshot["manifest_sha256"],
               "input_sha256": snapshot["manifest"].get("input_sha256"),
               "written": sorted(snapshot["files"]),
               "state_written": [MANIFEST, *sorted(snapshot["state_files"])],
               "time": datetime.now(timezone.utc).isoformat()}
    raw = json_bytes(receipt)
    _write(safe_path(state_dir, f"receipts/{operation_id}.json"), raw)
    _write(safe_path(state_dir, CURRENT), raw)
    return receipt


def _move_directory(source: Path, target: Path):
    source, target = _absolute(source), _absolute(target)
    if target.exists():
        raise ContractError(f"目录切换目标已经存在：{target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    os.rename(source, target)


def _journal(state_dir: Path, value: dict):
    raw = json_bytes(value)
    _write(safe_path(state_dir, RECOVERY), raw)
    if _read(safe_path(state_dir, RECOVERY)) != raw:
        raise ContractError("恢复记录写入后核验失败")


def _finish_journal(state_dir: Path, journal: dict, resolution: str):
    _write(safe_path(state_dir, f"receipts/{journal['operation_id']}-operation.json"),
           json_bytes({**journal, "stage": "completed", "resolution": resolution}))
    safe_path(state_dir, RECOVERY).unlink()


def _stage_files(root: Path, files: dict[str, bytes]):
    root.mkdir(parents=True, exist_ok=False)
    for path, data in files.items():
        _write(safe_path(root, path), data, exclusive=True)


def initialize(vault: Path, files: Delivery, state_root: Path | None = None) -> dict:
    manifest, manifest_hash = _delivery(files)
    vault = _absolute(vault)
    state_dir = state_directory(vault, state_root)
    with vault_lock(vault, state_root):
        if vault.exists() and (not vault.is_dir() or any(vault.iterdir())):
            raise ContractError("初始化目标非空，不会覆盖已有库")
        if state_dir.exists():
            raise ContractError("外部状态实例已存在；先恢复未完成操作，不会覆盖或重新绑定")
        state_dir.mkdir(parents=True, exist_ok=False)
        binding = {"format_version": 1, "tool": TOOL, "vault_id": str(uuid4()), "mode": "preview",
                   "vault": str(vault), "state_dir": str(state_dir)}
        _write(state_dir / "binding.json", json_bytes(binding), exclusive=True)
        operation_id = uuid4().hex
        candidate = f"staging/{operation_id}"
        journal = {"format_version": 2, "operation": "init", "vault_id": binding["vault_id"],
                   "operation_id": operation_id, "candidate": candidate, "backup": None,
                   "old_manifest_sha256": None, "new_manifest_sha256": manifest_hash,
                   "write_set": ["vault", "current"], "stage": "preparing",
                   "initial_files": [{"path": path, "size": len(data), "sha256": digest(data)}
                                     for path, data in sorted(files.vault_files.items())]}
        _journal(state_dir, journal)
        try:
            candidate_root = safe_path(state_dir, candidate)
            _stage_files(candidate_root / "vault", files.vault_files)
            for folder in VAULT_DIRECTORIES:
                safe_path(candidate_root / "vault", folder).mkdir(exist_ok=True)
            _stage_files(candidate_root / "current", files.state_files)
            snapshot = _read_snapshot(candidate_root / "current", manifest_hash)
            _verify_vocabulary(candidate_root / "vault" / VOCABULARY, snapshot)
            for folder in ("reports", "receipts", "backups"):
                safe_path(state_dir, folder).mkdir(exist_ok=True)
            journal["stage"] = "prepared"
            _journal(state_dir, journal)
            if vault.exists():
                if not vault.is_dir() or any(vault.iterdir()):
                    raise ContractError("初始化目标在生成期间变为非空")
                vault.rmdir()
            _move_directory(candidate_root / "vault", vault)
            _move_directory(candidate_root / "current", state_dir / "current")
            _verify_vocabulary(vault / VOCABULARY, snapshot)
            _read_snapshot(state_dir / "current", manifest_hash)
            receipt = _receipt(vault, state_dir, binding, snapshot, "init", operation_id)
            _finish_journal(state_dir, journal, "new_installed")
            return {"status": "initialized", "vault": str(vault), "state_dir": str(state_dir),
                    "manifest_sha256": manifest_hash, "receipt": receipt, "mode": "preview"}
        except (OSError, ContractError) as error:
            raise ContractError(f"初始化未完成，库外候选和恢复记录已保留；请执行 recover 恢复。原因：{error}") from error


def _article_links(text: str, parser: MarkdownIt) -> tuple[dict, list[tuple[str, str]]]:
    """Read actual Markdown links and Wiki links outside code/escaped text."""
    front = {}
    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|\Z)", text, re.S)
    if match:
        try:
            front = yaml.safe_load(match[1]) or {}
        except yaml.YAMLError as error:
            raise ContractError("无法核对文章引用，frontmatter 无法解析") from error
        if not isinstance(front, dict):
            raise ContractError("无法核对文章引用，frontmatter 必须是映射")
        text = text[match.end():]
    elif re.match(r"\A---[ \t]*\r?\n", text):
        raise ContractError("无法核对文章引用，frontmatter 缺少结束标记")
    links = []
    for field in ("subject", "entities", "type", "genre", "form", "source", "references", "relation", "isReplacedBy"):
        value = front.get(field, [])
        for item in value if isinstance(value, list) else [value]:
            if isinstance(item, str) and (wiki := re.fullmatch(r"\[\[([^\[\]\n]+)\]\]", item)):
                links.append(("wiki", wiki[1]))
    for token in parser.parse(text):
        if token.type != "inline":
            continue
        prose = []
        link_depth = 0
        for child in token.children or []:
            if child.type == "link_open":
                links.append(("markdown", child.attrGet("href") or ""))
                link_depth += 1
            elif child.type == "link_close":
                link_depth -= 1
            elif child.type == "image":
                links.append(("markdown", child.attrGet("src") or ""))
            elif child.type == "text" and not link_depth:
                prose.append(child.content)
                continue
            elif child.type in {"em_open", "em_close", "strong_open", "strong_close"} and not link_depth:
                continue  # Formatting in a Wiki alias does not change its target.
            elif child.type in {"softbreak", "hardbreak"}:
                prose.append("\n")
                continue
            # Keep code_inline, text_special (escaped punctuation), HTML and
            # Markdown link labels apart, rather than joining fake Wiki syntax.
            prose.append("\0")
        links.extend(("wiki", item) for item in re.findall(r"\[\[([^\[\]\n\0]+)\]\]", "".join(prose)))
    return front, links


def _reference_destination(kind: str, link: str, article: str) -> str | None:
    destination = link.split("|", 1)[0] if kind == "wiki" else link
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None  # External URLs and fragments are not vault file dependencies.
    decoded = unquote(parsed.path)
    base = "" if kind == "wiki" else posixpath.dirname(article)
    target = posixpath.normpath(posixpath.join(base, decoded))
    safe_relative(target)  # Reject absolute paths, NUL, backslash and vault escape.
    if not target.startswith(VOCABULARY + "/"):
        return None
    if not posixpath.splitext(target)[1]:
        target += ".md"
    return target


def _dependencies(vault: Path, target: dict, alternate: dict | None = None):
    """Refuse replacement/rollback when existing articles need absent data."""
    paths = set(_manifest_entries(target["manifest"]))
    known = {json.dumps(row.get("identity"), sort_keys=True)
             for row in target["records"]["records"]}
    removed = set()
    if alternate:
        removed = {row.get("identity", {}).get("iri") for row in alternate["records"]["records"]
                   if json.dumps(row.get("identity"), sort_keys=True) not in known}
        removed.discard(None)
    # Retain escape tokens; the default text_join pass would turn an escaped
    # opening bracket back into apparent Wiki-link syntax.
    parser = MarkdownIt("commonmark").disable("text_join")
    articles = {}
    for root in PARA_ROOTS:
        directory = safe_path(vault, root)
        if directory.exists():
            articles.update({f"{root}/{relative}": path for relative, path in _tree(directory).items()})
    for relative, path in articles.items():
        if not relative.endswith(".md"):
            continue
        text = _read(path).decode("utf-8")
        front, links = _article_links(text, parser)
        for kind, link in links:
            target_path = _reference_destination(kind, link, relative)
            if target_path is not None and target_path not in paths:
                raise ContractError(f"文章引用在目标版本不存在，拒绝切换或恢复：{relative} → {target_path}")
        if removed:
            for field in ("subject", "entities", "type", "genre", "form", "source", "references"):
                value = front.get(field, [])
                values = value if isinstance(value, list) else [value]
                if any(isinstance(item, str) and item in removed for item in values):
                    raise ContractError(f"文章原身份引用依赖将丢失：{relative} 的 {field}")


def _user_suggestions(vault: Path, state_dir: Path, files: dict[str, bytes]) -> list[dict]:
    """Keep alternatives outside the vault; never rewrite user-owned files."""
    report = f"reports/{uuid4().hex}"
    changes = []
    for relative, data in sorted(files.items()):
        if relative.startswith(VOCABULARY + "/"):
            continue
        path = safe_path(vault, relative)
        current = _read(path) if path.exists() else b""
        if current == data:
            continue
        candidate = safe_path(state_dir, f"{report}/suggested/{relative}")
        _write(candidate, data, exclusive=True)
        changes.append({"path": relative, "candidate": str(candidate),
                        "current_sha256": digest(current) if path.exists() else None,
                        "candidate_sha256": digest(data),
                        "diff": "".join(difflib.unified_diff(
                            current.decode("utf-8", errors="replace").splitlines(keepends=True),
                            data.decode("utf-8", errors="replace").splitlines(keepends=True),
                            fromfile=relative, tofile=str(candidate)))})
    if changes:
        _write(safe_path(state_dir, f"{report}/user-file-changes.json"), json_bytes(changes), exclusive=True)
    return changes


def refresh(vault: Path, files: Delivery, *, apply: bool = False,
            offline: bool = False, state_root: Path | None = None) -> dict:
    manifest, manifest_hash = _delivery(files)
    vault = _absolute(vault)
    with vault_lock(vault, state_root):
        state = inspect(vault, state_root=state_root)
        state_dir = Path(state["state_dir"])
        previous = manifest.get("previous_delivery")
        if not isinstance(previous, dict) or previous.get("sha256") != state["manifest_sha256"]:
            raise ContractError("候选的上一交付基准与当前安装版本不一致，请重新生成候选")
        old, new = state["files"], _manifest_entries(manifest)
        changes = {"added": sorted(new.keys() - old.keys()), "removed": sorted(old.keys() - new.keys()),
                   "changed": sorted(path for path in old.keys() & new.keys() if old[path]["sha256"] != new[path]["sha256"])}
        result = {"status": "preview", "vault": str(vault), "state_dir": str(state_dir), "changes": changes,
                  "old_manifest_sha256": state["manifest_sha256"], "manifest_sha256": manifest_hash}
        candidate_state = {"manifest": manifest, "records": _record_object(files.state_files["records.json"]),
                           "files": new, "state_files": _manifest_entries(manifest, "state_files")}
        _dependencies(vault, candidate_state, state)
        result["user_file_changes"] = _user_suggestions(vault, state_dir, files.vault_files)
        if not apply:
            return result
        if not offline:
            raise ContractError("切换前须关闭知识库并暂停同步和其他编辑，再明确确认 offline")
        if manifest_hash == state["manifest_sha256"]:
            return {**result, "status": "unchanged"}
        binding = _binding(vault, state_dir)
        operation_id = uuid4().hex
        candidate, backup = f"staging/{operation_id}", f"backups/{operation_id}"
        candidate_root, backup_root = safe_path(state_dir, candidate), safe_path(state_dir, backup)
        vocabulary_files = {path.removeprefix(VOCABULARY + "/"): data for path, data in files.vault_files.items()
                            if path.startswith(VOCABULARY + "/")}
        _stage_files(candidate_root / VOCABULARY, vocabulary_files)
        _stage_files(candidate_root / "current", files.state_files)
        snapshot = _read_snapshot(candidate_root / "current", manifest_hash)
        _verify_vocabulary(candidate_root / VOCABULARY, snapshot)
        journal = {"format_version": 2, "operation": "refresh", "vault_id": binding["vault_id"],
                   "operation_id": operation_id, "old_manifest_sha256": state["manifest_sha256"],
                   "new_manifest_sha256": manifest_hash, "candidate": candidate, "backup": backup,
                   "write_set": [VOCABULARY, "current"], "stage": "prepared"}
        _journal(state_dir, journal)
        try:
            inspect(vault, allow_pending=True, state_root=state_root)
            _dependencies(vault, candidate_state, state)
            _move_directory(vault / VOCABULARY, backup_root / VOCABULARY)
            _verify_vocabulary(backup_root / VOCABULARY, state)
            _move_directory(state_dir / "current", backup_root / "current")
            _read_snapshot(backup_root / "current", state["manifest_sha256"])
            _verify_vocabulary(candidate_root / VOCABULARY, snapshot)
            _move_directory(candidate_root / VOCABULARY, vault / VOCABULARY)
            _verify_vocabulary(vault / VOCABULARY, snapshot)
            _move_directory(candidate_root / "current", state_dir / "current")
            journal["stage"] = "candidate_installed"
            _journal(state_dir, journal)
            _read_snapshot(state_dir / "current", manifest_hash)
            _verify_vocabulary(vault / VOCABULARY, snapshot)
            _verify_vocabulary(backup_root / VOCABULARY, state)
            _dependencies(vault, candidate_state, state)
            receipt = _receipt(vault, state_dir, binding, snapshot, "refresh", operation_id)
            _finish_journal(state_dir, journal, "new_installed")
            return {**result, "status": "installed", "receipt": receipt, "backup": str(backup_root)}
        except (OSError, ContractError) as error:
            raise ContractError(f"刷新未完成，库外目录和恢复记录已保留；请执行 recover 恢复。原因：{error}") from error


def _validated_journal(state_dir: Path, binding: dict) -> dict:
    journal = _json(safe_path(state_dir, RECOVERY))
    operation_id, operation = journal.get("operation_id"), journal.get("operation")
    if (not isinstance(operation_id, str) or not re.fullmatch(r"[0-9a-f]{32}", operation_id)
            or journal.get("format_version") != 2 or journal.get("vault_id") != binding["vault_id"]
            or operation not in {"init", "refresh"} or journal.get("candidate") != f"staging/{operation_id}"
            or journal.get("backup") != (f"backups/{operation_id}" if operation == "refresh" else None)
            or journal.get("write_set") != ([VOCABULARY, "current"] if operation == "refresh" else ["vault", "current"])):
        raise ContractError("恢复记录不属于该知识库或写集不合法")
    for key in (["old_manifest_sha256", "new_manifest_sha256"] if operation == "refresh" else ["new_manifest_sha256"]):
        if not isinstance(journal.get(key), str) or not re.fullmatch(r"[0-9a-f]{64}", journal[key]):
            raise ContractError("恢复记录缺少可核验的版本摘要")
    return journal


def _initial_recovery(vault: Path, state_dir: Path, binding: dict, journal: dict) -> dict:
    candidate = safe_path(state_dir, journal["candidate"])
    expected = journal["new_manifest_sha256"]
    if journal.get("stage") in {"preparing", "initialization_aborted"}:
        if (state_dir / "current").exists() or (vault.exists() and (not vault.is_dir() or any(vault.iterdir()))):
            raise ContractError("初始化准备记录与实际目录不符，保留现场，不覆盖内容")
        # No target mutation is allowed before the prepared journal. Preserve
        # incomplete files outside the binding slot, so a fresh init can retry.
        journal["stage"] = "initialization_aborted"
        _journal(state_dir, journal)
        preserved = state_dir.with_name(f"{state_dir.name}-failed-{journal['operation_id']}")
        _move_directory(state_dir, preserved)
        _finish_journal(preserved, journal, "initialization_aborted")
        return {"status": "recovered", "vault": str(vault), "resolution": "initialization_aborted",
                "preserved_state": str(preserved), "state_dir": str(state_dir)}
    state_source = state_dir / "current" if (state_dir / "current").exists() else candidate / "current"
    snapshot = _read_snapshot(state_source, expected)
    staged_vault = candidate / "vault"
    if staged_vault.exists():
        # Nothing may replace a user's nonempty target, even after an interruption.
        if vault.exists() and (not vault.is_dir() or any(vault.iterdir())):
            raise ContractError("初始化恢复目标非空，保留现场，不接管新增内容")
        _verify_vocabulary(staged_vault / VOCABULARY, snapshot)
        initial = journal.get("initial_files")
        if not isinstance(initial, list):
            raise ContractError("初始化恢复缺少初建写集")
        for entry in initial:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                raise ContractError("初始化恢复写集无效")
            _check_bytes(entry["path"], _read(safe_path(staged_vault, entry["path"])), entry)
        if vault.exists():
            vault.rmdir()
        _move_directory(staged_vault, vault)
    else:
        _verify_vocabulary(vault / VOCABULARY, snapshot)
        # Already installed user files may have changed; they are not rewritten.
    _dependencies(vault, snapshot)
    if state_source != state_dir / "current":
        _move_directory(state_source, state_dir / "current")
    _read_snapshot(state_dir / "current", expected)
    _verify_vocabulary(vault / VOCABULARY, snapshot)
    receipt = _receipt(vault, state_dir, binding, snapshot, "recover-init", uuid4().hex)
    _finish_journal(state_dir, journal, "new_installed")
    return {"status": "recovered", "vault": str(vault), "state_dir": str(state_dir),
            "resolution": "new_installed", "manifest_sha256": expected, "receipt": receipt}


def _refresh_recovery(vault: Path, state_dir: Path, binding: dict, journal: dict) -> dict:
    old_hash, new_hash = journal["old_manifest_sha256"], journal["new_manifest_sha256"]
    candidate = safe_path(state_dir, journal["candidate"])
    backup = safe_path(state_dir, journal["backup"])
    states = {}
    for path in (state_dir / "current", backup / "current", candidate / "current"):
        if not path.exists():
            continue
        snapshot = _read_snapshot(path)
        version = snapshot["manifest_sha256"]
        if version not in {old_hash, new_hash}:
            raise ContractError("当前或保留工程状态已变化，不覆盖未知版本")
        states[path] = snapshot
    old = next((value for value in states.values() if value["manifest_sha256"] == old_hash), None)
    new = next((value for value in states.values() if value["manifest_sha256"] == new_hash), None)
    if not old or not new:
        raise ContractError("旧版或候选工程状态缺失，无法核对依赖；保留恢复记录")
    # Always check both preserved copies. A late external edit must survive and
    # prevent success, even when the new directory is already in its destination.
    if (backup / VOCABULARY).exists():
        _verify_vocabulary(backup / VOCABULARY, old)
    if (candidate / VOCABULARY).exists():
        _verify_vocabulary(candidate / VOCABULARY, new)
    current = vault / VOCABULARY
    current_version = None
    if current.exists():
        matches, errors = set(), []
        for version, snapshot in ((old_hash, old), (new_hash, new)):
            try:
                _verify_vocabulary(current, snapshot)
                matches.add(version)
            except ContractError as error:
                errors.append(error)
        if not matches:
            raise ContractError(f"当前词条目录发生变化，保留现场，不覆盖未知内容：{errors[-1]}")
        installed_state = states.get(state_dir / "current", {}).get("manifest_sha256")
        # A source/record-only update can leave exactly the same knowledge pages.
        # Inspect both locations and candidate presence to identify what moved.
        if new_hash in matches and (installed_state == new_hash or (
                (backup / VOCABULARY).exists() and not (candidate / VOCABULARY).exists())):
            current_version = new_hash
        elif old_hash in matches:
            current_version = old_hash
        else:
            raise ContractError("词条和工程状态不属于可解释的安装阶段，保留现场")
    if current_version == new_hash:
        if not (backup / VOCABULARY).exists():
            raise ContractError("新版已安装但旧词条目录缺失，无法核对恢复依据")
        selected, other, resolution = new, old, "new_installed"
    else:
        if not (candidate / VOCABULARY).exists():
            raise ContractError("候选词条目录缺失，无法核对新引用依赖；保留恢复记录")
        if current_version is None and not (backup / VOCABULARY).exists():
            raise ContractError("旧版与已安装新版均不可核验，保留现场")
        selected, other, resolution = old, new, "old_restored"
    _dependencies(vault, selected, other)
    journal["stage"] = "recovering"
    _journal(state_dir, journal)
    if not current.exists():
        _move_directory(backup / VOCABULARY, current)
    state_target = state_dir / "current"
    if state_target in states and states[state_target]["manifest_sha256"] != selected["manifest_sha256"]:
        preserved = backup / "current" if resolution == "new_installed" else candidate / "current"
        if preserved.exists():
            raise ContractError("恢复时工程状态的保留位置已占用，不覆盖已有副本")
        _move_directory(state_target, preserved)
    if not state_target.exists():
        source = next(path for path, value in states.items()
                      if value["manifest_sha256"] == selected["manifest_sha256"] and path.exists())
        _move_directory(source, state_target)
    _read_snapshot(state_target, selected["manifest_sha256"])
    _verify_vocabulary(current, selected)
    _dependencies(vault, selected, other)
    receipt = _receipt(vault, state_dir, binding, selected, "recover", uuid4().hex)
    _finish_journal(state_dir, journal, resolution)
    return {"status": "recovered", "vault": str(vault), "state_dir": str(state_dir),
            "resolution": resolution, "manifest_sha256": selected["manifest_sha256"], "receipt": receipt}


def recover(vault: Path, *, offline: bool = False, state_root: Path | None = None) -> dict:
    vault = _absolute(vault)
    with vault_lock(vault, state_root):
        state_dir = state_directory(vault, state_root)
        binding = _binding(vault, state_dir)
        if not offline:
            raise ContractError("恢复前须关闭知识库并暂停同步和其他编辑，再明确确认 offline")
        if not safe_path(state_dir, RECOVERY).exists():
            inspect(vault, state_root=state_root)
            return {"status": "nothing_to_recover", "vault": str(vault), "state_dir": str(state_dir)}
        journal = _validated_journal(state_dir, binding)
        try:
            if journal["operation"] == "init":
                return _initial_recovery(vault, state_dir, binding, journal)
            return _refresh_recovery(vault, state_dir, binding, journal)
        except OSError as error:
            raise ContractError(f"恢复未完成，所有目录和记录继续保留：{error}") from error
