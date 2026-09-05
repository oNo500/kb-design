"""Serve a read-only live view of the six working-tree vocabularies."""
from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
import json
from pathlib import Path
import threading
from urllib.parse import urlsplit

import yaml
from kb_core.repository import project_root

COLLECTIONS = {
    "topics": "concepts", "entities": "entities", "sources": "sources",
    "types": "types", "genres": "genres", "forms": "forms",
}


def _json_default(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise ValueError(f"不支持的数据类型：{type(value).__name__}")


def _json(value):
    return json.dumps(value, ensure_ascii=False, default=_json_default)


def _validate_record(record, location):
    if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"]:
        raise ValueError(f"{location}：条目必须包含非空字符串 id")
    label = record.get("label")
    if label is not None and not (isinstance(label, str) or isinstance(label, dict)
                                  and all(isinstance(v, str) for v in label.values())):
        raise ValueError(f"{location}：label 必须是名称文本或语言名称对象")
    for field in ("broader", "related", "arrays", "subjects", "role"):
        value = record.get(field)
        if value is not None and not (isinstance(value, list) and all(isinstance(v, str) for v in value)):
            raise ValueError(f"{location}：{field} 必须是字符串列表")
    for field in ("source", "entity", "form", "superordinate", "scope", "status"):
        if record.get(field) is not None and not isinstance(record[field], str):
            raise ValueError(f"{location}：{field} 必须是字符串")
    if record.get("basis") is not None and not isinstance(record["basis"], dict):
        raise ValueError(f"{location}：basis 必须是对象")
    # Check the shapes consumed by the renderer, without approving evidence,
    # source roles or language adoptions in this working-tree view.
    for language in ("zh", "en"):
        basis = (record.get("basis") or {}).get(language)
        if not isinstance(basis, dict) or "level" not in basis:
            continue
        level = basis["level"]
        if type(level) is not int or level not in range(1, 7):
            raise ValueError(f"{location}：basis.{language}.level 必须是 1–6 的整数")
        if level <= 4:
            references = basis.get("references")
            if not isinstance(references, list) or any(
                not isinstance(ref, dict) or not isinstance(ref.get("source"), str)
                for ref in references
            ):
                raise ValueError(f"{location}：basis.{language}.references 必须是来源对象列表")
        elif level == 5 and not isinstance(basis.get("model"), dict):
            raise ValueError(f"{location}：basis.{language}.model 必须是对象")
    matches = record.get("match", [])
    if not isinstance(matches, list) or any(not isinstance(m, dict) or not isinstance(m.get("source"), str) for m in matches):
        raise ValueError(f"{location}：match 必须是包含 source 的对象列表")


def _collection(name, content):
    location = f"{name}.yaml"
    try:
        source = content.decode("utf-8")
        document = yaml.safe_load(source)
        tree = yaml.compose(source)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        line = f":{mark.line + 1}" if mark else ""
        raise ValueError(f"{location}{line}：YAML 格式错误，{getattr(error, 'problem', '请检查文件')}") from error
    if not isinstance(document, dict) or not isinstance(document.get(COLLECTIONS[name]), list):
        raise ValueError(f"{location}：缺少 {COLLECTIONS[name]} 条目列表")
    keys = set()
    for key, _ in tree.value:
        if key.value in keys:
            raise ValueError(f"{location}：重复的顶层字段 {key.value}")
        keys.add(key.value)
    for group in (COLLECTIONS[name], "arrays"):
        records = document.get(group, [])
        if not isinstance(records, list):
            raise ValueError(f"{location}：{group} 必须是列表")
        seen = set()
        for record in records:
            _validate_record(record, f"{location}/{group}")
            if record["id"] in seen:
                raise ValueError(f"{location}/{group}：重复 id {record['id']}")
            seen.add(record["id"])
    lines = source.splitlines(keepends=True)
    raw = {}
    for key, sequence in tree.value:
        if key.value not in (COLLECTIONS[name], "arrays"):
            continue
        for index, item in enumerate(sequence.value):
            identifier = document[key.value][index]["id"]
            end = (sequence.value[index + 1].start_mark.line if index + 1 < len(sequence.value)
                   else item.end_mark.line + bool(item.end_mark.column))
            raw[f"{key.value}:{identifier}"] = "".join(lines[item.start_mark.line:end]).rstrip()
    # Reject YAML-only values that cannot be faithfully sent as JSON.
    normalized = json.loads(_json(document))
    return {"data": normalized, "raw": raw}


class SnapshotStore:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        self.lock = threading.Lock()
        self.snapshot = None
        self.revision = None
        self.observed = None
        self.error = None

    def _read(self):
        contents = {}
        for name in COLLECTIONS:
            try:
                contents[name] = (self.root / "data/vocab" / f"{name}.yaml").read_bytes()
            except OSError as error:
                raise ValueError(f"{name}.yaml：无法读取词表文件") from error
        return contents

    def status(self):
        with self.lock:
            try:
                contents = self._read()
                if contents != self._read():
                    raise ValueError("词表正在保存，请稍候")
                hashes = {name: hashlib.sha256(value).hexdigest() for name, value in contents.items()}
                revision = hashlib.sha256(_json(hashes).encode()).hexdigest()
                if revision != self.observed or self.error and revision == self.revision:
                    collections = {name: _collection(name, value) for name, value in contents.items()}
                    snapshot = {"generated": datetime.now().astimezone().isoformat(timespec="seconds"),
                                "repo": str(self.root), "collections": collections, "hashes": hashes}
                    self.snapshot, self.revision, self.error = snapshot, revision, None
                self.observed = revision
            except (ValueError, UnicodeError, RecursionError) as error:
                self.error = str(error)[:500]
            return {"revision": self.revision, "error": self.error, "snapshot": self.snapshot}


LIVE_SCRIPT = r"""
(() => {
  const initialRevision = __REVISION__;
  const notice = document.createElement('div');
  notice.id = 'preview-notice'; notice.setAttribute('role', 'status');
  notice.style.cssText = 'position:fixed;bottom:16px;left:16px;right:16px;z-index:1000;background:#fff3d6;color:#624500;border:1px solid #e4be62;border-radius:8px;padding:12px 16px;font:14px system-ui';
  notice.hidden = true; document.body.appendChild(notice);
  function message(value) { notice.hidden = !value; notice.textContent = value || ''; }
  message(__INITIAL_ERROR__);
  async function poll() {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    try {
      const response = await fetch('/api/status', {cache:'no-store', signal:controller.signal});
      if (!response.ok) throw new Error('读取状态失败');
      const state = await response.json();
      if (state.error) message('词表尚未更新，保留上次有效内容：' + state.error);
      else {
        message('');
        if (state.revision && state.revision !== initialRevision) location.reload();
      }
    } catch (_) { message('预览服务连接中断；恢复连接后会自动更新。'); }
    finally { clearTimeout(timeout); setTimeout(poll, 1000); }
  }
  setTimeout(poll, 1000);
})();
"""


def _safe_json(value):
    return _json(value).replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')


def _page(state):
    if state["snapshot"] is None:
        page = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>词表预览</title><body style="font:16px system-ui;padding:40px"><h1>等待有效词表</h1><p>修正 data/vocab/ 中的文件后，页面会自动更新。</p></body></html>'
    else:
        template = files("kb_vocab_preview").joinpath("template.html").read_text(encoding="utf-8")
        page = template.replace('__SNAPSHOT__', _safe_json(state["snapshot"]))
    initial_error = ("词表尚未更新，保留上次有效内容：" + state["error"]) if state["error"] else ""
    script = LIVE_SCRIPT.replace('__REVISION__', _safe_json(state["revision"])).replace('__INITIAL_ERROR__', _safe_json(initial_error))
    return page.replace('</html>', '<script>' + script + '</script></html>').encode('utf-8')


def make_server(root, port=8765):
    store = SnapshotStore(root)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self._serve(False)

        def do_HEAD(self):
            self._serve(True)

        def _serve(self, head):
            allowed = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            origin = self.headers.get("Origin")
            if self.headers.get("Host", "").lower() not in allowed or (origin and origin not in {f"http://{host}" for host in allowed}):
                self.send_error(403)
                return
            path = urlsplit(self.path).path
            if path not in ("/", "/index.html", "/api/status"):
                self.send_error(404)
                return
            state = store.status()
            if path == "/api/status":
                body = _json({"revision": state["revision"], "error": state["error"]}).encode()
                content_type = "application/json; charset=utf-8"
            else:
                body, content_type = _page(state), "text/html; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if not head:
                self.wfile.write(body)

        def log_message(self, *_):
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description="只读实时预览仓库工作区内的词表")
    parser.add_argument("--repo-root", type=Path, help="词表所在仓库，默认使用本应用所在仓库")
    parser.add_argument("--port", type=int, default=8765, help="本机端口，默认 8765")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("端口必须在 0–65535 之间")
    try:
        root = args.repo_root or project_root(Path(__file__))
        server = make_server(root, args.port)
    except (OSError, ValueError) as error:
        parser.exit(1, f"无法启动预览：{error}\n")
    print(f"词表预览：http://127.0.0.1:{server.server_port}", flush=True)
    print(f"只读工作区：{Path(root).resolve()} / data/vocab；Ctrl+C 停止", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
