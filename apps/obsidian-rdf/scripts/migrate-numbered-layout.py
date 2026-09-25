#!/usr/bin/env python3
"""Explicit v2/v3-to-v4 navigation migration with retained external backups.

Prepare is read-only for the vault. Apply/resume requires closed vault and paused
writers. Frozen inputs and RDF identities are preserved byte-for-byte.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import parse_qsl, quote, unquote, unquote_plus, urlsplit, urlunsplit
from uuid import uuid4

from markdown_it.helpers import parseLinkDestination

from kb_obsidian_rdf import __version__, storage
from kb_obsidian_rdf.common import ContractError, digest, json_bytes, safe_relative
from kb_obsidian_rdf.layout import MANIFEST_VERSION, VOCABULARY

NAMES = ('inbox', 'projects', 'areas', 'resources', 'archives', 'vocabulary',
         'views', 'templates', 'attachments')
DESTINATIONS = ('01-inbox', '10-projects', '20-areas', '30-resources', '40-archives',
                '90-vocabulary', '91-views', '92-templates', '93-attachments')
LEGACY_ROOTS = {2: dict(zip(NAMES, DESTINATIONS)),
                3: dict(zip((f'{i:02d}-{name}' for i, name in enumerate(NAMES)), DESTINATIONS))}
move = storage._move_directory


class Relocation:
    def __init__(self, vault: Path, version: int, files: dict[str, bytes], index_notes=()):
        self.vault, self.roots, self.files = vault, LEGACY_ROOTS[version], files
        self.notes = {'home.md': '00-indexes/index.md'} if 'home.md' in files else {}
        content_roots = set(list(self.roots)[1:5])
        for value in index_notes:
            name = safe_relative(value)
            if name not in files or not name.endswith('.md') or name.split('/')[0] not in content_roots:
                raise ContractError(f'人工索引必须明确指定现有内容笔记：{name}')
            self.notes[name] = '00-indexes/' + posixpath.basename(name)

    def path(self, value: str) -> str:
        if value in self.notes:
            return self.notes[value]
        if value + '.md' in self.notes:
            return self.notes[value + '.md'].removesuffix('.md')
        first, slash, rest = value.partition('/')
        return self.roots.get(first, first) + slash + rest

    def absolute(self, value: str) -> str:
        prefix = str(self.vault) + '/'
        if value.startswith(prefix):
            return prefix + self.path(value[len(prefix):])
        return self.path(value)

    def destination(self, value: str, owner: str, *, wiki: bool = False) -> str:
        # Wikilink aliases and fragments are not paths.
        target, sep, alias = value.partition('|') if wiki else (value, '', '')
        parsed = urlsplit(target)
        if parsed.scheme == 'obsidian' and parsed.netloc == 'open':
            query = dict(parse_qsl(parsed.query))
            if query.get('vault') not in (None, self.vault.name, str(self.vault)):
                return value
            def uri_parameter(match):
                original = unquote_plus(match[3])
                updated = (self.destination(original, owner, wiki=True) if match[2] == 'file'
                           else self.absolute(original))
                return match[1] + match[2] + '=' + quote(updated, safe='') if updated != original else match[0]
            updated = re.sub(r'(^|&)(file|path)=([^&]*)', uri_parameter, parsed.query)
            return urlunsplit(parsed._replace(query=updated)) + sep + alias
        if parsed.scheme == 'file' and parsed.netloc in ('', 'localhost'):
            path = unquote(parsed.path)
            updated = self.absolute(path)
            return urlunsplit(parsed._replace(path=quote(updated, safe='/'))) + sep + alias if updated != path else value
        if parsed.scheme or parsed.netloc or not parsed.path:
            return value
        path = unquote(parsed.path)
        if path.startswith(str(self.vault) + '/'):
            updated = self.absolute(path)
        elif wiki and not path.startswith(('./', '../')):
            # Obsidian's slash-free links resolve by filename; only the explicit
            # home rename changes one. Other targets keep their lookup behavior.
            lead = '/' if path.startswith('/') else ''
            updated = lead + self.path(path.lstrip('/'))
        elif path.startswith('/'):
            updated = '/' + self.path(path.lstrip('/'))
        else:
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(owner), path))
            updated = posixpath.relpath(self.path(resolved), posixpath.dirname(self.path(owner)) or '.')
            if path.startswith('./') and not updated.startswith('.'):
                updated = './' + updated
        if updated == path:
            return value
        updated = updated if wiki and '%' not in parsed.path else quote(updated, safe='/@:+')
        return urlunsplit(parsed._replace(path=updated)) + sep + alias

    def fields(self, value, field='', *, config=False):
        if isinstance(value, dict):
            return {key: self.fields(item, key, config=config) for key, item in value.items()}
        if isinstance(value, list):
            return [self.fields(item, field, config=config) for item in value]
        if isinstance(value, str) and (config or field in {'path', 'location', 'file', 'folder'}):
            return self.absolute(value)
        return value

    def markdown_links(self, text: str, owner: str) -> str:
        # Keep original Markdown formatting. The existing Markdown parser parses
        # angle destinations, escaping and balanced URL parentheses for us.
        edits = []
        for match in re.finditer(r'\]\([ \t]*|^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*', text, re.MULTILINE):
            start = match.end()
            parsed = parseLinkDestination(text, start, len(text))
            if not parsed.ok:
                continue
            raw = text[start:parsed.pos]
            href = parsed.str
            updated = self.destination(href, owner)
            if updated != href:
                edits.append((start, parsed.pos, '<' + updated + '>' if raw.startswith('<') else updated))
        for start, end, value in reversed(edits):
            text = text[:start] + value + text[end:]
        return text

    def public(self, name: str, raw: bytes) -> bytes:
        if name.startswith('.obsidian/') and name.endswith('.json'):
            old = json.loads(raw)
            new = self.fields(old, config=True)
            return json_bytes(new) if new != old else raw
        if not name.endswith(('.md', '.base')):
            return raw
        text = raw.decode('utf-8')
        text = re.sub(r'(?<!\\)\[\[([^\]\n]+)\]\]',
                      lambda m: '[[' + self.destination(m[1], name, wiki=True) + ']]', text)
        if name.endswith('.md'):
            text = self.markdown_links(text, name)
            text = re.sub(r'((?:href|src)\s*=\s*)([\'"])([^\'"\n]+)\2',
                          lambda m: m[1] + m[2] + self.destination(m[3], name) + m[2], text)
            text = re.sub(r'obsidian://[^\s<>\'"\]\)]+',
                          lambda m: self.destination(m[0], name), text)
        else:
            # Base uses quoted vault paths both in functions and comparisons.
            text = re.sub(r'([\'"])([^\'"\n]+)\1',
                          lambda m: m[1] + self.path(m[2]) + m[1], text)
        # Approved mechanical mapping also covers documented paths in code
        # examples. External URLs and unrelated words are deliberately excluded.
        def cli_argument(match):
            mark, value = (match[2], match[3]) if match[2] else ('', match[4])
            return match[1] + mark + self.absolute(value) + mark
        text = re.sub(r'(?<!\S)((?:--)?(?:path|file|folder)=)(?:([\'"])(.*?)\2|([^\s`\'"]+))',
                      cli_argument, text)
        for old, new in self.notes.items():
            for previous, replacement in ((old, new), (old.removesuffix('.md'), new.removesuffix('.md'))):
                if '/' not in previous and not previous.endswith('.md'):
                    continue
                text = re.sub(r'(?<![\w./:=&#?%-])' + re.escape(previous)
                              + r'(?=[#|`\'"\s>\]\)]|$)', replacement, text)
            text = text.replace(str(self.vault) + '/' + old, str(self.vault) + '/' + new)
        for old, new in self.roots.items():
            text = re.sub(r'(?<![\w./:=&#?%-])' + re.escape(old) + r'(?=/|[`\'"])', new, text)
            text = text.replace(str(self.vault) + '/' + old + '/', str(self.vault) + '/' + new + '/')
        return text.encode('utf-8')


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


def _entries(manifest: dict, field: str, vocabulary: str) -> dict:
    rows = manifest.get(field)
    if not isinstance(rows, list):
        raise ContractError(f'旧交付清单缺少 {field}')
    entries, aliases = {}, set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('path'), str):
            raise ContractError('旧交付记录缺少路径')
        name = safe_relative(row['path'])
        alias = storage._path_identity(Path(name))
        if (name in entries or alias in aliases or name == 'manifest.json'
                or field == 'files' and (not name.startswith(vocabulary + '/') or not name.endswith('.md'))
                or field == 'state_files' and name.startswith(vocabulary + '/')):
            raise ContractError('旧交付文件集合重复或越过受管理范围')
        entries[name] = row
        aliases.add(alias)
    return entries


def prepare(vault: Path, state_root: Path | None = None, *, index_notes=()) -> dict:
    vault = storage._absolute(vault)
    with storage.vault_lock(vault, state_root):
        state = storage.state_directory(vault, state_root)
        binding = storage._binding(vault, state)
        if (state / storage.RECOVERY).exists():
            raise ContractError('存在未完成操作，须先按其原计划恢复')
        source, old_state = tree_bytes(vault), tree_bytes(state / 'current')
        raw_manifest = old_state['manifest.json']
        manifest = json.loads(raw_manifest)
        receipt = storage._json(state / 'current.json')
        version = manifest.get('format_version')
        if (version not in LEGACY_ROOTS or manifest.get('mode') not in {'preview', 'formal'}
                or version == 2 and manifest['mode'] != 'preview'
                or receipt.get('manifest_sha256') != digest(raw_manifest)
                or receipt.get('vault_id') != binding['vault_id']
                or receipt.get('target') != str(vault) or receipt.get('result') != 'installed'):
            raise ContractError('需要已绑定且完整安装的第 2 版开发库或第 3 版知识库')
        storage._same_mode(binding, manifest, receipt)
        relocation = Relocation(vault, version, source, index_notes)
        if any((vault / name).exists() for name in ('00-indexes', *DESTINATIONS)):
            raise ContractError('新编号目录已存在；不合并或覆盖已有目录')
        vocabulary = next(old for old, new in relocation.roots.items() if new == VOCABULARY)
        managed = _entries(manifest, 'files', vocabulary)
        state_rows = _entries(manifest, 'state_files', vocabulary)
        if ({p for p in source if p.startswith(vocabulary + '/')} != managed.keys()
                or old_state.keys() != state_rows.keys() | {'manifest.json'}
                or not {'records.json', 'projection.json'} <= state_rows.keys()):
            raise ContractError('旧交付文件集合不完整或包含未知词条')
        for name, row in managed.items():
            storage._check_bytes(name, source[name], row)
        for name, row in state_rows.items():
            storage._check_bytes(name, old_state[name], row)
        storage._formal_input(manifest, old_state.__getitem__)
        records = storage._record_object(old_state['records.json'])
        if any(row.get('mode', 'preview') != manifest['mode'] for row in records['records']):
            raise ContractError('身份记录与交付模式不一致')
        mapped = {name: relocation.path(name) for name in source}
        all_names = [storage._path_identity(Path(name)) for name in mapped.values()]
        if len(set(all_names)) != len(all_names):
            raise ContractError('目录映射导致路径冲突')
        public = {mapped[name]: relocation.public(name, raw) for name, raw in source.items()}
        current = dict(old_state)
        for name in ('records.json', 'projection.json'):
            current[name] = json_bytes(relocation.fields(json.loads(current[name])))
        manifest['format_version'] = MANIFEST_VERSION
        manifest['layout_migration'] = {'from': version, 'to': MANIFEST_VERSION,
                                        'previous_manifest_sha256': digest(raw_manifest),
                                        'producer': {'name': 'kb-obsidian-rdf', 'version': __version__}}
        for row in manifest['files']:
            row['path'] = relocation.path(row['path'])
            data = public[row['path']]
            row.update(sha256=digest(data), size=len(data))
        for row in manifest['state_files']:
            data = current[row['path']]
            row.update(sha256=digest(data), size=len(data))
        current['manifest.json'] = json_bytes(manifest)
        product = tree_bytes(state / 'product') if (state / 'product').exists() else None
        new_product = dict(product) if product is not None else None
        if product is not None and 'baseline.json' in product:
            baseline = storage._object(product['baseline.json'], 'product/baseline.json')
            if baseline.get('format_version') != 1 or not isinstance(baseline.get('files'), dict):
                raise ContractError('产物基线结构无效')
            rewritten = {}
            for name, row in baseline['files'].items():
                safe_relative(name)
                if not isinstance(row, dict):
                    raise ContractError('产物基线文件记录无效')
                target = relocation.path(name)
                if target in rewritten:
                    raise ContractError('产物基线映射冲突')
                changed = dict(row)
                # A custom file remains custom: update its path, never claim its
                # current bytes as the generated baseline.
                if name in source and row.get('sha256') == digest(source[name]):
                    changed['sha256'] = digest(public[target])
                rewritten[target] = changed
            baseline['files'] = rewritten
            new_product['baseline.json'] = json_bytes(baseline)
        operation_id = uuid4().hex
        operation = storage.safe_path(state, f'layout-migrations/{operation_id}')
        storage._stage_files(operation / 'candidate-vault', public)
        for path in vault.rglob('*'):
            if path.is_dir():
                storage.safe_path(operation / 'candidate-vault', relocation.path(path.relative_to(vault).as_posix())).mkdir(parents=True, exist_ok=True)
        for name in ('00-indexes', *DESTINATIONS):
            (operation / 'candidate-vault' / name).mkdir(exist_ok=True)
        storage._stage_files(operation / 'candidate-current', current)
        if new_product is not None:
            storage._stage_files(operation / 'candidate-product', new_product)
            for path in (state / 'product').rglob('*'):
                if path.is_dir():
                    storage.safe_path(operation / 'candidate-product', path.relative_to(state / 'product').as_posix()).mkdir(parents=True, exist_ok=True)
        snapshot = storage._read_snapshot(operation / 'candidate-current')
        storage._verify_vocabulary(operation / 'candidate-vault' / VOCABULARY, snapshot)
        plan = {'format_version': 2, 'operation_id': operation_id, 'vault': str(vault),
                'state_root': str(state.parent), 'state_dir': str(state), 'vault_id': binding['vault_id'],
                'mode': binding['mode'], 'from_version': version, 'to_version': MANIFEST_VERSION,
                'old_vault': fingerprints(source, vault),
                'new_vault': fingerprints(public, operation / 'candidate-vault'),
                'old_current': fingerprints(old_state, state / 'current'),
                'new_current': fingerprints(current, operation / 'candidate-current'),
                'old_product': fingerprints(product, state / 'product') if product is not None else None,
                'new_product': fingerprints(new_product, operation / 'candidate-product') if new_product is not None else None,
                'old_receipt_sha256': digest((state / 'current.json').read_bytes()),
                'old_binding_sha256': digest((state / 'binding.json').read_bytes()),
                'new_manifest_sha256': digest(current['manifest.json']), 'directories': relocation.roots,
                'note_moves': relocation.notes,
                'moved_files': {old: new for old, new in mapped.items() if old != new},
                'changed_files': [name for name, data in source.items() if data != public[mapped[name]]],
                'state_write_set': ['current', 'current.json', 'recovery.json', 'receipts/' + operation_id + '.json']
                                   + (['product'] if product is not None else [])}
        storage._write(operation / 'before-receipt.json', (state / 'current.json').read_bytes(), exclusive=True)
        storage._write(operation / 'before-binding.json', (state / 'binding.json').read_bytes(), exclusive=True)
        storage._write(operation / 'plan.json', json_bytes(plan), exclusive=True)
        return {'status': 'prepared', 'plan': str(operation / 'plan.json'), 'files': len(source),
                'content_changes': len(plan['changed_files']), 'directories': relocation.roots,
                'note_moves': relocation.notes}


def install_part(actual, candidate, backup, old, new):
    if actual.exists():
        value = fingerprints(tree_bytes(actual), actual)
        if value == new and backup.exists():
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
        if (not re.fullmatch(r'[0-9a-f]{32}', op_id) or plan.get('format_version') != 2
                or binding['vault_id'] != plan['vault_id'] or str(state) != plan['state_dir']
                or plan_path != state / 'layout-migrations' / op_id / 'plan.json'
                or digest((state / 'binding.json').read_bytes()) != plan['old_binding_sha256']):
            raise ContractError('迁移计划不属于该目标库或绑定已变化')
        storage._same_mode(binding, plan)
        operation = plan_path.parent
        recovery = state / storage.RECOVERY
        receipt = storage._json(state / storage.CURRENT)
        if not recovery.exists() and receipt.get('operation_id') == op_id:
            snapshot = storage.inspect(vault, state_root=root)
            if snapshot['manifest_sha256'] != plan['new_manifest_sha256']:
                raise ContractError('目标库已更新，不能重放旧布局迁移')
            return {'status': 'already-installed', 'vault': str(vault), 'backup': str(operation / 'backup')}
        journal = {'format_version': 1, 'operation': 'numbered-layout', 'operation_id': op_id,
                   'plan_sha256': digest(plan_path.read_bytes()), 'vault_id': binding['vault_id']}
        if recovery.exists():
            if storage._json(recovery) != journal:
                raise ContractError('另一项操作未完成，不能接管恢复')
            current_receipt = (state / storage.CURRENT).read_bytes()
            own_receipt = state / 'receipts' / (op_id + '.json')
            if (digest(current_receipt) != plan['old_receipt_sha256']
                    and not (own_receipt.exists() and own_receipt.read_bytes() == current_receipt
                             and receipt.get('operation_id') == op_id
                             and receipt.get('manifest_sha256') == plan['new_manifest_sha256']
                             and receipt.get('mode') == binding['mode'])):
                raise ContractError('恢复期间安装凭据已变化，保留现场')
        else:
            verify_tree(vault, plan['old_vault'])
            verify_tree(state / 'current', plan['old_current'])
            if plan['old_product'] is not None:
                verify_tree(state / 'product', plan['old_product'])
                verify_tree(operation / 'candidate-product', plan['new_product'])
            elif (state / 'product').exists():
                raise ContractError('产物状态已变化，请重新准备')
            if digest((state / storage.CURRENT).read_bytes()) != plan['old_receipt_sha256']:
                raise ContractError('安装凭据已变化，请重新准备')
            verify_tree(operation / 'candidate-vault', plan['new_vault'])
            verify_tree(operation / 'candidate-current', plan['new_current'])
            storage._journal(state, journal)
        for name, actual, old, new in [('vault', vault, plan['old_vault'], plan['new_vault']),
                                       ('current', state / 'current', plan['old_current'], plan['new_current'])]:
            install_part(actual, operation / ('candidate-' + name), operation / 'backup' / name, old, new)
        if plan['old_product'] is not None:
            install_part(state / 'product', operation / 'candidate-product', operation / 'backup/product', plan['old_product'], plan['new_product'])
        snapshot = storage._read_snapshot(state / 'current', plan['new_manifest_sha256'])
        storage._verify_vocabulary(vault / VOCABULARY, snapshot)
        verify_tree(vault, plan['new_vault'])
        storage._receipt(vault, state, binding, snapshot, 'numbered-layout', op_id)
        storage._finish_journal(state, journal, 'numbered-layout-installed')
        storage.inspect(vault, state_root=root)
        return {'status': 'installed', 'vault': str(vault), 'backup': str(operation / 'backup'),
                'manifest_sha256': snapshot['manifest_sha256']}


def main():
    parser = argparse.ArgumentParser(description='显式迁移第 2／3 版知识库到第 4 版目录；备份完整保留在库外')
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--vault', type=Path, help='准备迁移，生成候选及计划，不修改原库')
    target.add_argument('--plan', type=Path, help='应用或继续指定计划')
    parser.add_argument('--state-root', type=Path)
    parser.add_argument('--index-note', action='append', default=[], help='移入人工索引目录的现有笔记路径，可重复')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    try:
        if args.plan:
            if not args.apply or args.index_note:
                raise ContractError('--plan 必须与 --apply 一起使用；索引移动仅能在准备时指定')
            result = apply(args.plan, offline=args.offline)
        else:
            if args.apply:
                raise ContractError('先用 --vault 准备并核对计划，再显式应用')
            result = prepare(args.vault, args.state_root, index_notes=args.index_note)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ContractError, OSError, KeyError, ValueError) as error:
        print(f'布局迁移未完成：{error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
