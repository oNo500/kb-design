"""Explicit product maintenance, separate from vocabulary delivery and refresh."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import difflib
import json
import os
from pathlib import Path
import tempfile
from uuid import uuid4

import yaml

from .common import ContractError, digest, json_bytes
from .layout import (ARCHIVES, AREAS, ATTACHMENTS, INBOX, INDEXES, PARA_ROOTS, PROJECTS,
                     RESOURCES, TEMPLATES, VIEWS, VOCABULARY)
from .storage import _absolute, _read, _write, read_state, safe_path, vault_lock


CONFIG_PATHS = frozenset({'.obsidian/app.json', '.obsidian/templates.json', '.obsidian/types.json'})
INDEX_PATH = f'{INDEXES}/index.md'


def initial_files() -> dict[str, bytes]:
    index = f"""# 知识库

## 当前工作

- [[{VIEWS}/inbox.base|收件箱]]
- [[{VIEWS}/projects.base|项目]]
- [[{VIEWS}/drafts.base|草稿]]

## 内容查找

- [[{VIEWS}/article-list.base|全部笔记]]：按标题、主题和实体查找。
- [[{VIEWS}/areas.base|领域内容]] · [[{VIEWS}/resources.base|参考资料]] · [[{VIEWS}/archives.base|归档内容]]

## 最近修改

![[{VIEWS}/recently-modified.base]]
"""
    content_scope = [{'or': [f'file.inFolder("{root}")' for root in PARA_ROOTS]}, 'file.ext == "md"']
    uuid_declaration = '/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.matches(note.identifier)'
    declared = [*content_scope, 'note.identifier.isType("string")', uuid_declaration]
    properties = {'formula.title': {'displayName': '标题'}, 'note.subject': {'displayName': '主题'},
                  'note.entities': {'displayName': '实体'}, 'note.type': {'displayName': '文档类型'},
                  'note.status': {'displayName': '状态'}, 'file.folder': {'displayName': '目录'},
                  'file.mtime': {'displayName': '修改时间'}}
    columns = ['formula.title', 'note.subject', 'note.entities', 'note.type', 'file.mtime']
    definitions = {
        'article-list': ('全部笔记', content_scope),
        'inbox': ('收件箱', [f'file.inFolder("{INBOX}")', 'file.ext == "md"']),
        'drafts': ('草稿', [*declared, 'note.status == "draft"']),
        'recently-modified': ('最近修改', declared),
        'projects': ('项目', [f'file.inFolder("{PROJECTS}")', 'file.ext == "md"']),
        'areas': ('领域', [f'file.inFolder("{AREAS}")', 'file.ext == "md"']),
        'resources': ('资源', [f'file.inFolder("{RESOURCES}")', 'file.ext == "md"']),
        'archives': ('归档', [f'file.inFolder("{ARCHIVES}")', 'file.ext == "md"']),
    }
    project = """# {{title}}

一句话目标。

## 当前工作

- [ ] 下一步。

## 完成条件

- 可检查的完成结果。

## 资料入口

- 相关资料链接。
"""
    files = {INDEX_PATH: index.encode(),
             f'{TEMPLATES}/article.md': '## 正文\n\n## 参考资料\n\n'.encode(),
             f'{TEMPLATES}/project.md': project.encode()}
    for name, (label, filters) in definitions.items():
        view = {'type': 'table', 'name': label, 'order': list(columns),
                'sort': [{'property': 'file.mtime', 'direction': 'DESC'}]}
        base = {'filters': {'and': filters},
                'formulas': {'title': 'file.asLink(if(note.title, note.title, file.name))'},
                'properties': properties, 'views': [view]}
        files[f'{VIEWS}/{name}.base'] = yaml.safe_dump(base, allow_unicode=True, sort_keys=False).encode()
    types = {name: 'text' for name in ('identifier', 'title', 'type', 'genre', 'status', 'form',
                                     'level', 'source', 'language', 'isReplacedBy')}
    types.update({name: 'multitext' for name in ('subject', 'entities', 'references', 'relation')})
    types.update({'aliases': 'aliases', 'created': 'date', 'modified': 'date'})
    files.update({'.obsidian/app.json': json_bytes({'attachmentFolderPath': ATTACHMENTS, 'alwaysUpdateLinks': True}),
                  '.obsidian/templates.json': json_bytes({'folder': TEMPLATES}),
                  '.obsidian/types.json': json_bytes({'types': types})})
    return files


def record_initial_baseline(state_dir: Path, files: dict[str, bytes]):
    """Remember generated user-file bytes outside the vocabulary manifest."""
    values = {name: {'sha256': digest(raw)} for name, raw in files.items()
              if name in initial_files()}
    _write(safe_path(state_dir, 'product/baseline.json'),
           json_bytes({'format_version': 1, 'files': values}), exclusive=True)


def _configuration(raw: bytes | None, wanted: bytes):
    target = json.loads(wanted)
    current = {} if raw is None else json.loads(raw)
    if not isinstance(current, dict):
        raise ValueError('配置不是 JSON 对象')
    merged, preserved = deepcopy(current), []

    def fill(existing, desired, prefix=''):
        for key, value in desired.items():
            name = prefix + key
            if key not in existing:
                existing[key] = value
            elif isinstance(value, dict) and isinstance(existing[key], dict):
                fill(existing[key], value, name + '.')
            elif existing[key] != value or type(existing[key]) is not type(value):
                preserved.append({'property': name, 'current': existing[key], 'suggested': value})

    fill(merged, target)
    return (raw if raw is not None and merged == current else json_bytes(merged)), preserved


def _equivalent(relative: str, old: bytes, new: bytes) -> bool:
    if relative.endswith('.base'):
        try:
            return yaml.safe_load(old) == yaml.safe_load(new)
        except (ValueError, UnicodeError, yaml.YAMLError):
            return False
    return False


def _publish_new_file(target: Path, data: bytes):
    """Publish only complete bytes, without replacing a newly appeared file."""
    target = _absolute(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix='.product-', suffix='.tmp', dir=target.parent)
    temporary = Path(name)
    os.close(descriptor)
    try:
        _write(temporary, data)
        if _read(temporary) != data:
            raise ContractError(f'维护临时文件内容不完整：{target}')
        os.chmod(temporary, 0o644)
        os.link(temporary, _absolute(target), follow_symlinks=False)
    finally:
        temporary.unlink(missing_ok=True)


def maintain(vault: Path, *, apply: bool = False, offline: bool = False,
             state_root: Path | None = None) -> dict:
    """Plan or apply an explicit, file-by-file maintenance operation.

    Each retry reads actual files again. Completed writes remain in place; any
    newly edited preference is preserved. Reports and original bytes are never
    replaced by the retry, and this operation never writes vocabulary or current.
    """
    if apply and not offline:
        raise ContractError('维护前须关闭知识库并暂停同步和其他编辑，再明确确认 offline')
    vault = _absolute(vault)
    with vault_lock(vault, state_root):
        state = read_state(vault, state_root)
        state_dir = Path(state['state_dir'])
        baseline_path = safe_path(state_dir, 'product/baseline.json')
        baseline_raw = _read(baseline_path) if baseline_path.exists() else None
        baseline = json.loads(baseline_raw) if baseline_raw is not None else {'format_version': 1, 'files': {}}
        if not isinstance(baseline, dict) or baseline.get('format_version') != 1 or not isinstance(baseline.get('files'), dict):
            raise ContractError('产物基准格式不符，不会接管用户文件')
        operation = safe_path(state_dir, f'product/operations/{uuid4().hex}')
        report_path = operation / 'report.json'
        changes, writes, originals = [], {}, {}
        for relative, wanted in sorted(initial_files().items()):
            path = safe_path(vault, relative)
            current = _read(path) if path.exists() else None
            originals[relative] = current
            row = {'path': relative, 'before_sha256': digest(current) if current is not None else None,
                   'suggested_sha256': digest(wanted), 'action': 'unchanged', 'preserved': []}
            candidate = wanted
            if relative in CONFIG_PATHS:
                try:
                    candidate, row['preserved'] = _configuration(current, wanted)
                    row['action'] = ('create' if current is None else 'merge') if candidate != current else ('preserve' if row['preserved'] else 'unchanged')
                except (ValueError, UnicodeError):
                    row.update(action='preserve', reason='配置无法按 JSON 对象合并，保留原文件')
            elif current is None:
                row['action'] = 'create'
            elif current == wanted:
                pass
            elif _equivalent(relative, current, wanted):
                row['action'] = 'equivalent'
            elif relative == INDEX_PATH and digest(current) == baseline['files'].get(relative, {}).get('sha256'):
                row.update(action='update', reason='总入口符合该路径的已知生成基准')
            else:
                row.update(action='preserve', reason='已有用户文件保留；候选仅供审阅')
            row['candidate_sha256'] = digest(candidate)
            row['diff'] = ''.join(difflib.unified_diff(
                (current or b'').decode('utf-8', errors='replace').splitlines(keepends=True),
                candidate.decode('utf-8').splitlines(keepends=True), fromfile=relative, tofile='candidate/' + relative))
            if candidate != current:
                candidate_path = safe_path(operation, 'candidate/' + relative)
                _write(candidate_path, candidate, exclusive=True)
                row['candidate'] = str(candidate_path)
            if row['action'] in {'create', 'merge', 'update'}:
                writes[relative] = candidate
                if current is not None:
                    backup = safe_path(operation, 'backup/' + relative)
                    _write(backup, current, exclusive=True)
                    row['backup'] = str(backup)
            changes.append(row)
        result = {'status': 'preview', 'vault': str(vault), 'state_dir': str(state_dir),
                  'report_path': str(report_path), 'time': datetime.now(timezone.utc).isoformat(),
                  'write_set': sorted(writes), 'written': [], 'changes': changes,
                  'state_write_set': [], 'vocabulary_manifest_sha256': state['manifest_sha256']}
        if apply and writes:
            result['state_write_set'].append(str(baseline_path))
            if baseline_raw is not None:
                _write(operation / 'baseline-before.json', baseline_raw, exclusive=True)
        result['state_write_set'].extend(sorted([str(report_path),
            *(str(path) for path in operation.rglob('*') if path.is_file())]))
        _write(report_path, json_bytes(result), exclusive=True)
        if not apply:
            return result
        try:
            for relative, data in writes.items():
                target = safe_path(vault, relative)
                actual = _read(target) if target.exists() else None
                if actual != originals[relative]:
                    raise ContractError(f'维护准备后文件发生变化，保留现有内容：{relative}')
                if actual is None:
                    _publish_new_file(target, data)
                else:
                    _write(target, data)
                if _read(target) != data:
                    raise ContractError(f'维护写入后核对不符：{relative}')
                baseline['files'][relative] = {'sha256': digest(data)}
                _write(baseline_path, json_bytes(baseline))
            result['status'] = 'maintained' if writes else 'unchanged'
        except (OSError, ContractError) as error:
            result.update(status='failed', error=str(error))
        finally:
            for row in changes:
                path = safe_path(vault, row['path'])
                actual = _read(path) if path.exists() else None
                row['actual_sha256'] = digest(actual) if actual is not None else None
                if row['path'] in writes and actual == writes[row['path']]:
                    result['written'].append(row['path'])
            _write(report_path, json_bytes(result))
        if result['status'] == 'failed':
            raise ContractError(f'维护未完成；已有写入与备份保留，修复原因后重试同一 maintain 命令。report：{report_path}；原因：{result["error"]}')
        return result
