"""Prepare two offline review dossiers; never create source data or approvals."""
from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

import yaml

from kb_core.repository import project_root


# These are retrieval recipes for the approved pilot, not vocabulary records.
RECIPES = (
    {
        'id': 'computing-gbt-520', 'title': '学科映射',
        'file': 'data/vocab/topics.yaml', 'collection': 'concepts', 'record': 'computing',
        'source': 'gbt-13745', 'item': '520', 'ledger': 'match-inventory.tsv:49',
        'basis_field': 'concepts[computing].basis.zh',
        'material': {
            'path': 'docs/references/gbt-13745.md', 'kind': 'transcription',
            'description': '项目保存的转载清单，不是本轮核对的标准原文',
            'needle': '520 计算机科学技术',
            'source_url': 'https://xkfl.xhma.com/',
        },
        'missing': ['primary_standard_and_amendments', 'adjacent_match_basis',
                    'external_status_evidence', 'mapping_role_decision', 'relation_review'],
    },
    {
        'id': 'explanation-diataxis', 'title': '类型映射',
        'file': 'data/vocab/types.yaml', 'collection': 'types', 'record': 'explanation',
        'source': 'diataxis', 'item': 'explanation', 'ledger': 'match-inventory.tsv:755',
        'basis_field': None,
        'material': {
            'path': 'docs/references/writing-guides.md', 'kind': 'reading-note',
            'description': '项目阅读记录，不是原页面快照或本轮外部核验',
            'needle': 'https://diataxis.fr/explanation/',
            'source_url': 'https://diataxis.fr/explanation/',
        },
        'missing': ['primary_page_version_and_locator', 'adjacent_match_basis',
                    'external_status_evidence', 'mapping_role_decision', 'relation_review'],
    },
)
POLICIES = ('docs/decisions/current-stage-scope.md', 'docs/decisions/source-validation-policy.md')
OUTPUT_FILES = {'evidence.json', 'evidence.md', 'changes.md', 'cache.json'}
MISSING_LABELS = {
    'primary_standard_and_amendments': '缺原始标准及适用修改单的逐值证据',
    'primary_page_version_and_locator': '缺原页面版本与具体位置的证据',
    'adjacent_match_basis': '缺拟采用的相邻映射依据',
    'external_status_evidence': '外部状态仍待证据核对',
    'mapping_role_decision': '严格 mapping 角色仍待具体决定',
    'relation_review': '双方概念范围及关系仍待人工判断',
    'adjacent_basis_review': '已填写映射依据，是否支持关系仍待人工判断',
    'mapping_decision_review': '角色账本有批准记录，仍须核对决定的范围与效力',
    'offline_material_missing': '指定离线材料缺失，未沿用缓存片段',
    'locator_not_found': '材料存在，但未找到配置的定位文本',
}


def json_text(value):
    def encode(item):
        if isinstance(item, (date, datetime)):
            return item.isoformat()
        raise TypeError(type(item).__name__)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, default=encode) + '\n'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique(rows, predicate, description):
    found = [row for row in rows if predicate(row)]
    if len(found) != 1:
        raise ValueError(f'{description}: expected one record, found {len(found)}')
    return found[0]


def extract_snippets(text: str, needle: str) -> list[dict]:
    """Return exact matching lines with their Markdown heading context, not inferred evidence."""
    headings = []
    found = []
    fenced = False
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith('```'):
            fenced = not fenced
        if not fenced and line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            if level <= 6 and line[level:level + 1] == ' ':
                headings = [(depth, name) for depth, name in headings if depth < level]
                headings.append((level, line[level:].strip()))
        if needle in line:
            found.append({'line': line_number, 'heading': ' / '.join(name for _, name in headings),
                          'text': line})
    return found


def output_path(root: Path, output: Path) -> Path:
    """Constrain replaceable artifacts to a real build subdirectory in the selected checkout."""
    path = output if output.is_absolute() else root / output
    path = Path(os.path.abspath(path))
    build = root / 'build'
    if path == build or build not in path.parents:
        raise ValueError('output must be a child of the selected root/build directory')
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink():
            raise ValueError(f'symlinked output path is not allowed: {part}')
    if path.exists():
        if not path.is_dir():
            raise ValueError(f'output is not a directory: {path}')
        for child in path.iterdir():
            if child.name not in OUTPUT_FILES or child.is_symlink() or not child.is_file():
                raise ValueError(f'refusing to replace an unrelated output entry: {child}')
    return path


def load_cache(output: Path) -> dict:
    try:
        cache = json.loads((output / 'cache.json').read_text())
        return cache['items'] if cache.get('format') == 1 and isinstance(cache.get('items'), dict) else {}
    except (OSError, ValueError, TypeError, AttributeError):
        return {}


def render(items: list[dict], root: Path, changed_only=False) -> str:
    title = '来源证据变化' if changed_only else '离线来源证据'
    lines = [f'# {title}', '', '本报告只整理待审材料，不批准来源、角色、关系或正式切换。完整字段见同目录 evidence.json。', '']
    if not items:
        lines.extend(['输入未变化，没有需要重新展开的条目。旧结果仍待人工审阅。', ''])
    for item in items:
        current = item['current']
        record = current['record']
        match = current['selected_match']
        old = item['previous']
        lines.extend([f"## {item['title']}", '', f"对象：`{item['id']}`；状态：待审。", '',
                      f"当前位置：`{current['file']}` 的 `{current['field']}`。", '',
                      f"当前映射：`{record['id']}` → `{match['source']}:{match['id']}`，关系 `{match['rel']}`。", '',
                      f"本地范围：{record.get('scope') or '记录未填写 scope'}。", '',
                      f"旧账本：`{old['match']['identity']}`；结论 `{old['match'].get('disposition')}`；"
                      f"切换阻断 `{old['match'].get('blocks_cutover')}`。", ''])
        if 'basis' in record:
            lines.extend(['当前依据字段：', '', '```json', json_text(record['basis']).rstrip(), '```', ''])
        for basis in old['basis']:
            lines.extend([f"旧依据：`{basis.get('old_value')}`；结论 `{basis.get('disposition')}`。", ''])
        roles = ', '.join(f"{row.get('new_role')}: {row.get('new_status')}" for row in old['roles'])
        lines.extend([f"角色账本：{roles or '未找到'}（仅转录历史状态）。", ''])
        for material in item['materials']:
            lines.extend([f"材料：`{material['path']}`。{material['description']}。", '',
                          f"SHA-256：`{material['sha256'] or '缺失'}`；登记版本：`{item['source_entity'].get('version', '未记录')}`（不等于材料快照版本）。", '',
                          f"[原记录入口]({material['source_url']})（未联网）。", ''])
            for snippet in material['snippets']:
                target = (root / material['path']).as_posix().replace('>', '%3E').replace('<', '%3C')
                lines.extend([f"位置：[{material['path']}:{snippet['line']}](<{target}:{snippet['line']}>)；章节：{snippet['heading']}。", '',
                              '> ' + snippet['text'], ''])
        lines.extend(['待核条件：', ''])
        lines.extend('- ' + MISSING_LABELS[condition] for condition in item['missing_conditions'])
        lines.extend(['', '条件按本批审阅范围保留；命中不证明材料支持关系，程序不自动关闭语义门禁。', ''])
    return '\n'.join(lines)


def publish(output: Path, files: dict[str, str]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f'.{output.name}-', dir=output.parent))
    backup = staging / 'previous'
    new = staging / 'new'
    new.mkdir()
    published = False
    try:
        for name, text in files.items():
            (new / name).write_text(text, encoding='utf-8')
        if output.exists():
            os.replace(output, backup)
        try:
            os.replace(new, output)
            published = True
        except BaseException:
            if backup.exists():
                os.replace(backup, output)
            raise
    finally:
        # If restoration itself failed, retain the only prior output copy.
        if published or not backup.exists():
            shutil.rmtree(staging)


def prepare(root: Path, output: Path | None = None) -> dict:
    supplied_root = Path(root).absolute()
    root = supplied_root.resolve(strict=True)
    if output is not None and Path(output).is_absolute():
        # macOS /var is an alias of /private/var. Normalize the selected root,
        # while still rejecting symlinks in the writable build subtree.
        try:
            output = Path(output).relative_to(supplied_root)
        except ValueError:
            pass
    output = output_path(root, Path(output) if output is not None else root / 'build/source-evidence')
    # Capture each input once; verify bytes again before publishing the dossier.
    inputs: dict[str, bytes | None] = {}
    def read(relative, optional=False):
        if relative not in inputs:
            path = root / relative
            if path.is_symlink():
                raise ValueError(f'input symlink is not allowed: {relative}')
            try:
                inputs[relative] = path.read_bytes()
            except FileNotFoundError:
                if not optional:
                    raise ValueError(f'required input is missing: {relative}')
                inputs[relative] = None
        return inputs[relative]
    def document(relative):
        value = yaml.safe_load(read(relative))
        if not isinstance(value, dict):
            raise ValueError(f'expected a YAML mapping: {relative}')
        return value

    entities = document('data/vocab/entities.yaml')['entities']
    sources = document('data/vocab/sources.yaml')['sources']
    matches = document('data/audit/migrations/source-v1/match.yaml')['rows']
    bases = document('data/audit/migrations/source-v1/basis.yaml')['rows']
    roles = document('data/audit/migrations/source-v1/uses.yaml')['roles']
    policies = {path: digest(read(path)) for path in POLICIES}
    implementation = digest(Path(__file__).read_bytes())
    cache = load_cache(output)
    cached_items, items, changed = {}, [], []
    reused = 0
    for recipe in RECIPES:
        record = unique(document(recipe['file'])[recipe['collection']],
                        lambda row: row['id'] == recipe['record'], recipe['record'])
        match = unique(record.get('match', []),
                       lambda row: row.get('source') == recipe['source'] and row.get('id') == recipe['item'],
                       recipe['id'] + ' match')
        entity = unique(entities, lambda row: row['id'] == recipe['source'], recipe['source'])
        use = unique(sources, lambda row: row['id'] == recipe['source'], recipe['source'] + ' use')
        previous = {
            'match': unique(matches, lambda row: row['identity'] == recipe['ledger'], recipe['ledger']),
            'basis': [row for row in bases if recipe['basis_field'] and row.get('field_path') == recipe['basis_field']],
            'roles': [row for row in roles if row['use_id'] == recipe['source']],
        }
        material = dict(recipe['material'])
        raw = read(material['path'], optional=True)
        material['sha256'] = digest(raw) if raw is not None else None
        current = {'file': recipe['file'], 'field': f"{recipe['collection']}[{recipe['record']}].match",
                   'record': record, 'selected_match': match}
        fingerprint = digest(json_text([implementation, recipe, current, entity, use,
                                        previous, material['sha256'], policies]).encode())
        old = cache.get(recipe['id'], {})
        if (isinstance(old, dict) and old.get('fingerprint') == fingerprint
                and isinstance(old.get('payload'), dict)
                and old['payload'].get('review_state') == 'review_required'
                and old.get('payload_sha256') == digest(json_text(old['payload']).encode())):
            item = old['payload']
            reused += 1
        else:
            material['availability'] = 'available' if raw is not None else 'missing'
            material['snippets'] = extract_snippets(raw.decode('utf-8'), material['needle']) if raw is not None else []
            missing = list(recipe['missing'])
            if match.get('basis'):
                missing[missing.index('adjacent_match_basis')] = 'adjacent_basis_review'
            if any(row.get('new_role') == 'mapping' and row.get('new_status') == 'approved'
                   and row.get('decision') for row in previous['roles']):
                missing[missing.index('mapping_role_decision')] = 'mapping_decision_review'
            if raw is None:
                missing.append('offline_material_missing')
            elif not material['snippets']:
                missing.append('locator_not_found')
            item = {'id': recipe['id'], 'title': recipe['title'], 'review_state': 'review_required',
                    'current': current, 'source_entity': entity, 'source_use': use,
                    'previous': previous, 'materials': [material], 'missing_conditions': missing,
                    'policy_hashes': policies}
            changed.append(recipe['id'])
        items.append(item)
        cached_items[recipe['id']] = {'fingerprint': fingerprint, 'payload': item,
                                      'payload_sha256': digest(json_text(item).encode())}
    for relative, captured in inputs.items():
        path = root / relative
        now = path.read_bytes() if path.exists() else None
        if path.is_symlink() or now != captured:
            raise ValueError(f'input changed during preparation: {relative}; no output published')
    # Recheck ownership immediately before replacing previously generated output.
    output_path(root, output)
    report = {'scope': 'offline-review-only', 'items': items}
    publish(output, {
        'evidence.json': json_text(report),
        'evidence.md': render(items, root),
        'changes.md': render([item for item in items if item['id'] in changed], root, True),
        'cache.json': json_text({'format': 1, 'items': cached_items}),
    })
    return {'output': str(output), 'items': len(items), 'reused': reused, 'changed': changed,
            'review_required': len(items)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, help='input checkout; defaults to the owning checkout')
    parser.add_argument('--output', type=Path, help='generated output below the selected root/build')
    args = parser.parse_args(argv)
    try:
        result = prepare(args.root or project_root(), args.output)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        parser.exit(1, f'cannot prepare offline source evidence: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
