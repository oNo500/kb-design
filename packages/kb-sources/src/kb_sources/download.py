"""Bounded HTTP downloads, immutable snapshots and offline byte verification."""

import csv
from datetime import datetime, timezone
import io
import hashlib
from http.client import HTTPException
from importlib.resources import files
import json
import os
from pathlib import Path
import re
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from jsonschema import Draft202012Validator, FormatChecker
import yaml

from kb_sources import __version__


class SourceError(ValueError):
    """A source could not be safely received or verified."""


class _UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise SourceError("source YAML requires unique string keys")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _validate(value, name):
    schema = json.loads(files("kb_sources").joinpath("schemas", name + ".json").read_text())
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path)
        raise SourceError(f"invalid {name} at {location or '<root>'}: {error.message}")


def _source(raw):
    if len(raw) > 1024 * 1024:
        raise SourceError("source manifest exceeds 1 MiB")
    try:
        spec = yaml.load(raw, Loader=_UniqueLoader)
    except yaml.YAMLError as exc:
        raise SourceError(f"invalid source YAML: {exc}") from exc
    _validate(spec, "source")
    ids, names = set(), {"receipt.json", "source.yaml"}
    for item in spec["files"]:
        name = item["filename"].casefold()
        if item["id"] in ids or name in names:
            raise SourceError("duplicate file id or duplicate/reserved filename")
        ids.add(item["id"])
        names.add(name)
        url = urlsplit(item["url"])
        if not url.hostname or url.username or url.password or url.fragment:
            raise SourceError("source URL must have a host and no credentials or fragment")
    return spec


class _Redirects(HTTPRedirectHandler):
    def __init__(self, url):
        self.origin = urlsplit(url)

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlsplit(newurl)
        if (target.scheme not in {"http", "https"}
                or target.hostname != self.origin.hostname
                or target.username or target.password
                or (self.origin.scheme == "https" and target.scheme != "https")):
            raise SourceError("redirect leaves the source host or downgrades HTTPS")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_ZIP_MAX_ENTRIES = 10000
_ZIP_MAX_UNCOMPRESSED = 256 * 1024 * 1024


class _NoDTD(ET.TreeBuilder):
    def doctype(self, name, pubid, system):
        raise SourceError("XML DTD and entity declarations are not allowed")


def _structured_format(path, kind, base_uri=None):
    # Validate syntax, not vocabulary semantics or source completeness.
    try:
        if kind == "zip":
            with zipfile.ZipFile(path) as archive:
                members = archive.infolist()
                if not members or len(members) > _ZIP_MAX_ENTRIES:
                    raise SourceError("ZIP member count outside limit")
                if sum(item.file_size for item in members) > _ZIP_MAX_UNCOMPRESSED:
                    raise SourceError("ZIP uncompressed size exceeds limit")
                total = 0
                for item in members:
                    if item.is_dir():
                        continue
                    with archive.open(item) as stream:
                        while chunk := stream.read(64 * 1024):
                            total += len(chunk)
                            if total > _ZIP_MAX_UNCOMPRESSED:
                                raise SourceError("ZIP uncompressed size exceeds limit")
                # Reading each member to EOF verifies CRC without extraction.
            return
        raw = path.read_bytes()
        if kind == "json":
            def reject_constant(value):
                raise SourceError(f"invalid JSON constant: {value}")
            json.loads(raw, parse_constant=reject_constant)
            return
        if kind == "xml":
            root = ET.fromstring(raw, parser=ET.XMLParser(target=_NoDTD()))
            if root.tag.rsplit("}", 1)[-1].lower() == "html":
                raise SourceError("received HTML rather than XML source data")
            return
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            if kind != "tsv":
                raise
            text = raw.decode("cp1252")
        if re.search(r"<html(?:\s|>)|<!doctype\s+html", text[:8192], re.I):
            raise SourceError("received HTML rather than structured source data")
        if kind == "tsv":
            count, width = 0, None
            for row in csv.reader(io.StringIO(text, newline=""), delimiter="\t", strict=True):
                if not row:
                    continue
                if width is None:
                    width = len(row)
                if width < 2 or len(row) != width:
                    raise SourceError("TSV requires equal-width rows with at least two columns")
                count += 1
            if count < 2:
                raise SourceError("TSV requires at least two rows")
        elif kind == "turtle":
            from rdflib import Graph
            graph = Graph().parse(data=text, format="turtle", publicID=base_uri or path.absolute().as_uri())
            if not graph:
                raise SourceError("Turtle source contains no triples")
        else:
            raise SourceError(f"unsupported source format: {kind}")
    except SourceError:
        raise
    except Exception as exc:
        raise SourceError(f"{path.name}: invalid {kind}: {exc}") from exc


def _format(path, kind, *, base_uri=None):
    if kind not in {"pdf", "html"}:
        return _structured_format(path, kind, base_uri)
    # Signature checks only: do not claim PDF parsing or semantic validation.
    with path.open("rb") as stream:
        head = stream.read(8192)
        stream.seek(max(0, path.stat().st_size - 2048))
        tail = stream.read()
    if kind == "pdf":
        if not head.startswith(b"%PDF-") or b"%%EOF" not in tail:
            raise SourceError(f"{path.name}: missing PDF signature or end marker")
    else:
        text = head.decode("utf-8-sig", errors="replace").lower().lstrip()
        if "<html" not in text and "<!doctype html" not in text:
            raise SourceError(f"{path.name}: not an HTML document")
        title = re.search(r"<title[^>]*>(.*?)</title>", text, re.S)
        if title and any(word in title.group(1) for word in (
                "access denied", "just a moment", "sign in", "log in", "login",
                "captcha", "one moment, please")):
            raise SourceError(f"{path.name}: received an access page rather than source material")


def _download(item, path, timeout, max_bytes, retries):
    for attempt in range(retries + 1):
        try:
            request = Request(item["url"], headers={
                "User-Agent": "kb-sources/" + __version__, "Accept-Encoding": "identity",
            })
            with build_opener(_Redirects(item["url"])).open(request, timeout=timeout) as response:
                if response.status != 200:
                    raise SourceError(f"{item['id']}: expected HTTP 200, got {response.status}")
                length = response.headers.get("Content-Length")
                expected = int(length) if length is not None else None
                if expected is not None and (expected < 1 or expected > max_bytes):
                    raise SourceError(f"{item['id']}: Content-Length outside size limit")
                size, digest = 0, hashlib.sha256()
                with path.open("wb") as target:
                    while chunk := response.read(64 * 1024):
                        size += len(chunk)
                        if size > max_bytes:
                            raise SourceError(f"{item['id']}: download exceeds size limit")
                        target.write(chunk)
                        digest.update(chunk)
                if size == 0 or (expected is not None and size != expected):
                    raise SourceError(f"{item['id']}: empty or truncated download")
                checksum = digest.hexdigest()
                if item.get("sha256") and checksum != item["sha256"]:
                    raise SourceError(f"{item['id']}: expected SHA-256 does not match")
                _format(path, item["format"], base_uri=response.geturl())
                return {
                    **{key: item[key] for key in ("id", "filename", "format", "url")},
                    "final_url": response.geturl(), "size": size, "sha256": checksum,
                    "content_type": response.headers.get("Content-Type", ""),
                }
        except (OSError, URLError, HTTPException) as exc:
            retryable = not isinstance(exc, HTTPError) or exc.code in {408, 429, 500, 502, 503, 504}
            if not retryable or attempt == retries:
                raise SourceError(f"{item['id']}: download failed: {exc}") from exc
            time.sleep(min(2 ** attempt, 4))
    raise AssertionError("unreachable")


def fetch(manifest, output, *, timeout=30, max_bytes=64 * 1024 * 1024, retries=1):
    """Publish a new snapshot only after all files in the manifest are received."""
    if timeout <= 0 or max_bytes <= 0 or not 0 <= retries <= 3:
        raise SourceError("timeout and max_bytes must be positive; retries must be 0..3")
    raw = Path(manifest).read_bytes()
    spec = _source(raw)
    root = Path(output).expanduser().resolve()
    source_root = root / spec["id"]
    if source_root.is_symlink():
        raise SourceError("source directory must not be a symlink")
    source_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".receiving-", dir=source_root) as temporary:
        stage = Path(temporary)
        payload = stage / "snapshot"
        payload.mkdir()
        received = []
        for item in spec["files"]:
            received.append(_download(item, payload / item["filename"], timeout, max_bytes, retries))
        receipt = {
            "schema_version": 1,
            "source": {"id": spec["id"], "title": spec["title"], "requested_version": spec["version"]},
            "acquired_at": datetime.now(timezone.utc).isoformat(),
            "request_sha256": hashlib.sha256(raw).hexdigest(),
            "tool": {"name": "kb-sources", "version": __version__},
            "files": received,
        }
        _validate(receipt, "receipt")
        encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode()
        snapshot = source_root / hashlib.sha256(encoded).hexdigest()
        if snapshot.exists() or snapshot.is_symlink():
            raise SourceError("snapshot already exists; refusing to replace it")
        (payload / "source.yaml").write_bytes(raw)
        (payload / "receipt.json").write_bytes(encoded)
        os.rename(payload, snapshot)
    return snapshot


def verify(snapshot):
    """Verify a fixed snapshot offline; this does not approve its semantic contents."""
    root = Path(snapshot).absolute()
    if root.is_symlink() or not root.is_dir():
        raise SourceError("snapshot must be a real directory")
    try:
        for name in ("receipt.json", "source.yaml"):
            if (root / name).is_symlink() or not (root / name).is_file():
                raise SourceError(f"missing or symlinked {name}")
        raw_receipt = (root / "receipt.json").read_bytes()
        if hashlib.sha256(raw_receipt).hexdigest() != root.name:
            raise SourceError("receipt SHA-256 does not match snapshot identity")
        receipt = json.loads(raw_receipt)
        _validate(receipt, "receipt")
        raw_source = (root / "source.yaml").read_bytes()
        if hashlib.sha256(raw_source).hexdigest() != receipt["request_sha256"]:
            raise SourceError("source manifest SHA-256 mismatch")
        spec = _source(raw_source)
        if receipt["source"] != {"id": spec["id"], "title": spec["title"], "requested_version": spec["version"]}:
            raise SourceError("source identity differs from requested source")
        expected_files = {"receipt.json", "source.yaml"} | {x["filename"] for x in spec["files"]}
        if {p.name for p in root.iterdir()} != expected_files:
            raise SourceError("snapshot file set differs from manifest")
        if len(receipt["files"]) != len(spec["files"]):
            raise SourceError("receipt does not cover every requested file")
        for requested, received in zip(spec["files"], receipt["files"]):
            if any(requested[k] != received[k] for k in ("id", "filename", "format", "url")):
                raise SourceError("receipt file differs from requested file")
            path = root / received["filename"]
            if path.is_symlink() or not path.is_file():
                raise SourceError(f"missing or symlinked {path.name}")
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                while chunk := stream.read(64 * 1024):
                    digest.update(chunk)
            if path.stat().st_size != received["size"] or digest.hexdigest() != received["sha256"]:
                raise SourceError(f"{path.name}: size or SHA-256 mismatch")
            if requested.get("sha256") and digest.hexdigest() != requested["sha256"]:
                raise SourceError(f"{path.name}: expected SHA-256 mismatch")
            _format(path, received["format"], base_uri=received["final_url"])
        return receipt
    except (OSError, json.JSONDecodeError) as exc:
        raise SourceError(f"cannot verify snapshot: {exc}") from exc
