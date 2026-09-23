#!/usr/bin/env python3
"""Explicit v2-to-v3 development layout migration, with a retained full backup.

Prepare while read-only; apply/resume only with the vault closed. This script
does not migrate v1 instances, change RDF identities, or rewrite raw inputs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit
from uuid import uuid4

from markdown_it import MarkdownIt

from kb_obsidian_rdf import __version__, storage
from kb_obsidian_rdf.common import ContractError, digest, json_bytes
from kb_obsidian_rdf.layout import MANIFEST_VERSION

ROOTS = {name: f'{index:02d}-{name}' for index, name in enumerate(
    ('inbox', 'projects', 'areas', 'resources', 'archives', 'vocabulary', 'views', 'templates', 'attachments'))}
move = storage._move_directory


def relocated(value: str) -> str:
    first, slash, rest = value.partition('/')
    return ROOTS.get(first, first) + slash + rest


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {name: path.read_bytes() for name, path in storage._tree(root).items()}


def fingerprints(files: dict[str, bytes], directory: Path) -> dict[str, str]:
    values = {name: digest(data) for name, data in sorted(files.items())}
    values.update({p.relative_to(directory).as_posix() + '/': ''
                   for p in directory.rglob('*') if p.is_dir()})
    return values


def verify_tree(root: Path, expected: dict) -> None:
    if fingerprints(tree_bytes(root), root) != expected:
        raise ContractError(f'文件集合或内容已经变化，保留现场：{root}')


def path_fields(value, field=''):
    if isinstance(value, dict):
        return {key: path_fields(item, key) for key, item in value.items()}
    if isinstance(value, list):
        return [path_fields(item, field) for item in value]
    if isinstance(value, str) and field in {'path', 'location', 'file', 'folder', 'lastOpenFiles',
                                          'newFileFolderPath', 'attachmentFolderPath', 'templatesFolder'}:
        return relocated(value)
    return value


def public_bytes(name: str, raw: bytes) -> bytes:
    if name.startswith('.obsidian/') and name.endswith('.json'):
        old = json.loads(raw)
        new = path_fields(old)
        return json_bytes(new) if new != old else raw
    if not name.endswith(('.md', '.base')):
        return raw
    text = raw.decode('utf-8')
    if name.endswith('.md'):
        pending = list(MarkdownIt('commonmark').parse(text))
        while pending:
            token = pending.pop()
            pending.extend(token.children or [])
            if token.type in {'fence', 'code_block', 'code_inline', 'html_inline', 'html_block'}:
                if any(relocated(m[1]) != m[1] for m in re.finditer(r'\[\[([^\]\n]+)\]\]', token.content)):
                    raise ContractError(f'示例或 HTML 中包含需区分的旧路径，请单独审阅：{name}')
            if token.type in {'link_open', 'image'}:
                href = token.attrGet('href') or token.attrGet('src') or ''
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                old = unquote(parsed.path)
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), old))
                updated = posixpath.relpath(relocated(resolved), posixpath.dirname(relocated(name)) or '.')
                if relocated(old) != old or posixpath.normpath(old) != posixpath.normpath(updated):
                    raise ContractError(f'Markdown 链接需要专项迁移，原文件保持不变：{name} → {href}')
    # Generated links and article Properties use full, vault-relative Wikilinks.
    text = re.sub(r'(?<!\\)\[\[([^\]\n]+)\]\]',
                  lambda m: '[[' + relocated(m[1]) + ']]', text)
    if name == 'home.md':
        for old, new in ROOTS.items():
            text = text.replace(f'`{old}/`', f'`{new}/`')
    if name.endswith('.base'):
        text = re.sub(r'((?:file\.inFolder|link)\()([\'"])([^\'"\n]+)\2(\))',
                      lambda m: m[1] + m[2] + relocated(m[3]) + m[2] + m[4], text)
        if any(re.search(r'[\'"]' + root + r'/', text) for root in ROOTS):
            raise ContractError(f'Base 中仍有未支持的旧路径表达式，请单独审阅：{name}')
    return text.encode('utf-8')


def prepare(vault: Path, state_root: Path | None = None) -> dict:
    vault = storage._absolute(vault)
    with storage.vault_lock(vault, state_root):
        state = storage.state_directory(vault, state_root)
        binding = storage._binding(vault, state)
        if (state / storage.RECOVERY).exists():
            raise ContractError('存在未完成操作，须先按其原计划恢复')
        if any((vault / name).exists() for name in ROOTS.values()):
            raise ContractError('编号目录已存在；不合并或覆盖已有目录')
        source = tree_bytes(vault)
        old_state = tree_bytes(state / 'current')
        raw_manifest = old_state['manifest.json']
        manifest = json.loads(raw_manifest)
        receipt = storage._json(state / 'current.json')
        if (manifest.get('format_version') != 2 or manifest.get('mode') != 'preview'
                or receipt.get('manifest_sha256') != digest(raw_manifest)
                or receipt.get('vault_id') != binding['vault_id']
                or receipt.get('target') != str(vault) or receipt.get('result') != 'installed'):
            raise ContractError('需要已绑定且完整安装的第 2 版开发库')
        managed = {r['path']: r for r in manifest['files']}
        state_rows = {r['path']: r for r in manifest['state_files']}
        if ({p for p in source if p.startswith('vocabulary/')} != managed.keys()
                or old_state.keys() != state_rows.keys() | {'manifest.json'}):
            raise ContractError('旧交付文件集合不完整或包含未知词条')
        for name, row in managed.items():
            storage._check_bytes(name, source[name], row)
        for name, row in state_rows.items():
            storage._check_bytes(name, old_state[name], row)
        public = {relocated(name): public_bytes(name, raw) for name, raw in source.items()}
        if len(public) != len(source):
            raise ContractError('目录映射导致路径冲突')
        current = dict(old_state)
        for name in ('records.json', 'projection.json'):
            current[name] = json_bytes(path_fields(json.loads(current[name])))
        manifest['format_version'] = MANIFEST_VERSION
        manifest['layout_migration'] = {'from': 2, 'to': 3, 'previous_manifest_sha256': digest(raw_manifest),
                                        'producer': {'name': 'kb-obsidian-rdf', 'version': __version__}}
        for row in manifest['files']:
            row['path'] = relocated(row['path'])
            data = public[row['path']]
            row.update(sha256=digest(data), size=len(data))
        for row in manifest['state_files']:
            data = current[row['path']]
            row.update(sha256=digest(data), size=len(data))
        current['manifest.json'] = json_bytes(manifest)
        operation_id = uuid4().hex
        operation = storage.safe_path(state, f'layout-migrations/{operation_id}')
        storage._stage_files(operation / 'candidate-vault', public)
        for path in vault.rglob('*'):
            if path.is_dir():
                storage.safe_path(operation / 'candidate-vault', relocated(path.relative_to(vault).as_posix())).mkdir(parents=True, exist_ok=True)
        storage._stage_files(operation / 'candidate-current', current)
        snapshot = storage._read_snapshot(operation / 'candidate-current')
        storage._verify_vocabulary(operation / 'candidate-vault/05-vocabulary', snapshot)
        plan = {'format_version': 1, 'operation_id': operation_id, 'vault': str(vault),
                'state_root': str(state.parent), 'state_dir': str(state), 'vault_id': binding['vault_id'],
                'old_vault': fingerprints(source, vault),
                'new_vault': fingerprints(public, operation / 'candidate-vault'),
                'old_current': fingerprints(old_state, state / 'current'),
                'new_current': fingerprints(current, operation / 'candidate-current'),
                'old_receipt_sha256': digest((state / 'current.json').read_bytes()),
                'new_manifest_sha256': digest(current['manifest.json']), 'directories': ROOTS,
                'changed_files': [name for name, data in source.items() if data != public[relocated(name)]]}
        storage._write(operation / 'before-receipt.json', (state / 'current.json').read_bytes(), exclusive=True)
        storage._write(operation / 'before-binding.json', (state / 'binding.json').read_bytes(), exclusive=True)
        storage._write(operation / 'plan.json', json_bytes(plan), exclusive=True)
        return {'status': 'prepared', 'plan': str(operation / 'plan.json'),
                'files': len(source), 'content_changes': len(plan['changed_files']), 'directories': ROOTS}


def install_part(actual, candidate, backup, old, new):
    if actual.exists():
        value = fingerprints(tree_bytes(actual), actual)
        if value == new:
            verify_tree(backup, old)
            return
        if value != old or backup.exists():
            raise ContractError(f'目标状态与迁移计划冲突：{actual}')
        verify_tree(candidate, new)
        move(actual, backup)
        verify_tree(backup, old)
    else:
        verify_tree(backup, old)
    verify_tree(candidate, new)
    move(candidate, actual)
    verify_tree(actual, new)


def apply(plan_path: Path, *, offline: bool = False) -> dict:
    if not offline:
        raise ContractError('应用或恢复前须关闭目标库、暂停其他编辑与同步，并明确 --offline')
    plan_path = storage._absolute(plan_path)
    plan = storage._json(plan_path)
    vault, root = Path(plan['vault']), Path(plan['state_root'])
    with storage.vault_lock(vault, root):
        state = storage.state_directory(vault, root)
        binding = storage._binding(vault, state)
        op_id = plan['operation_id']
        if (not re.fullmatch(r'[0-9a-f]{32}', op_id) or plan.get('format_version') != 1
                or binding['vault_id'] != plan['vault_id'] or str(state) != plan['state_dir']
                or plan_path != state / 'layout-migrations' / op_id / 'plan.json'):
            raise ContractError('迁移计划不属于该目标库')
        operation = plan_path.parent
        recovery = state / storage.RECOVERY
        receipt = storage._json(state / storage.CURRENT)
        if not recovery.exists() and receipt.get('operation_id') == op_id:
            snapshot = storage.inspect(vault, state_root=root)
            if snapshot['manifest_sha256'] != plan['new_manifest_sha256']:
                raise ContractError('目标库已更新，不能重放旧布局迁移')
            return {'status': 'already-installed', 'vault': str(vault), 'backup': str(operation / 'backup')}
        if recovery.exists():
            journal = storage._json(recovery)
            if journal != {'format_version': 1, 'operation': 'numbered-layout', 'operation_id': op_id,
                           'plan_sha256': digest(plan_path.read_bytes()), 'vault_id': binding['vault_id']}:
                raise ContractError('另一项操作未完成，不能接管恢复')
        else:
            verify_tree(vault, plan['old_vault'])
            verify_tree(state / 'current', plan['old_current'])
            if digest((state / storage.CURRENT).read_bytes()) != plan['old_receipt_sha256']:
                raise ContractError('安装凭据已变化，请重新准备')
            verify_tree(operation / 'candidate-vault', plan['new_vault'])
            verify_tree(operation / 'candidate-current', plan['new_current'])
            journal = {'format_version': 1, 'operation': 'numbered-layout', 'operation_id': op_id,
                       'plan_sha256': digest(plan_path.read_bytes()), 'vault_id': binding['vault_id']}
            storage._journal(state, journal)
        install_part(vault, operation / 'candidate-vault', operation / 'backup/vault', plan['old_vault'], plan['new_vault'])
        install_part(state / 'current', operation / 'candidate-current', operation / 'backup/current', plan['old_current'], plan['new_current'])
        snapshot = storage._read_snapshot(state / 'current', plan['new_manifest_sha256'])
        storage._verify_vocabulary(vault / '05-vocabulary', snapshot)
        verify_tree(vault, plan['new_vault'])
        storage._receipt(vault, state, binding, snapshot, 'numbered-layout', op_id)
        storage._finish_journal(state, journal, 'numbered-layout-installed')
        storage.inspect(vault, state_root=root)
        return {'status': 'installed', 'vault': str(vault), 'backup': str(operation / 'backup'),
                'manifest_sha256': snapshot['manifest_sha256']}


def main():
    parser = argparse.ArgumentParser(description='显式迁移第 2 版开发库到编号目录；备份完整保留在库外')
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--vault', type=Path, help='准备迁移，生成候选及计划，不修改原库')
    target.add_argument('--plan', type=Path, help='应用或继续指定计划')
    parser.add_argument('--state-root', type=Path)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    try:
        if args.plan:
            if not args.apply:
                raise ContractError('--plan 必须与 --apply 一起使用')
            result = apply(args.plan, offline=args.offline)
        else:
            if args.apply:
                raise ContractError('先用 --vault 准备并核对计划，再显式应用')
            result = prepare(args.vault, args.state_root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ContractError, OSError, KeyError, ValueError) as error:
        print(f'布局迁移未完成：{error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
