"""Language-label evidence, kept separate from non-language ``basis`` fields.

Normalization preserves historical uncertainty; validation checks structure and
adoption consistency, but cannot establish independent external attestation.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
import re


LEGACY_LEVELS = {
    'gbt-13745': 1, 'lom': 1, 'rfc-1122': 1, 'wikidata': 3,
    'cs2023': 2, 'asvs': 2, 'cwe': 2, 'attack': 2, 'atlas': 2,
    'swebok': 2, 'owasp-llm-top10': 2,
}
# Existing adopted records retain the decision path from their original commit;
# moving that document does not create a new authorization.
_APPROVAL_REFERENCE = re.compile(r'design/decisions/[a-z0-9]+(?:-[a-z0-9]+)*\.md#[^\s/#?]+')
_MARKERS = {'none', 'self', 'model', 'source'}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _legacy_reference(value, record):
    if not isinstance(value, str) or value in ('none', 'self', 'model'):
        return None
    record = record if isinstance(record, dict) else {}
    raw = record.get('source') if value == 'source' else value
    if not _text(raw):
        return None
    source, separator, locator = raw.partition(':')
    if source in _MARKERS:
        return None
    if not separator:
        for match in record.get('match', []) or []:
            if isinstance(match, dict) and match.get('source') == source:
                identifier = match.get('id')
                if identifier is not None and not isinstance(identifier, bool):
                    locator = str(identifier)
                    break
    return {'source': source, 'locator': locator}


def normalize_basis(value, record, language):
    """Copy structured evidence or migrate only explicitly mapped old sources.

    Missing legacy locators remain empty, so validation can report the missing
    evidence instead of manufacturing a source location. ``language`` identifies
    the caller's label boundary and is retained in the shared API.
    """
    if isinstance(value, dict):
        return deepcopy(value)
    if isinstance(value, str):
        reference = _legacy_reference(value, record)
        if reference and reference['source'] in LEGACY_LEVELS:
            return {'level': LEGACY_LEVELS[reference['source']], 'references': [reference]}
    return {'legacy': deepcopy(value)}


def source_references(value, record=None):
    """Extract external references without ever producing model/source markers."""
    if isinstance(value, str):
        reference = _legacy_reference(value, record)
        return [reference] if reference else []
    if not isinstance(value, dict):
        return []
    level = value.get('level')
    if type(level) is not int or level not in (1, 2, 3, 4):
        return []
    references = value.get('references')
    if not isinstance(references, list):
        return []
    return [deepcopy(ref) for ref in references
            if isinstance(ref, dict) and _text(ref.get('source'))
            and ref['source'] not in _MARKERS and _text(ref.get('locator'))]


def validate_basis(value, label, record, language, sources, decisions=None, collection='topics'):
    """Return all detectable evidence/adoption errors, without modifying inputs.

    ``decisions=None`` permits standalone display/export validation. Supplying a
    mapping (including an empty one) requires exact accepted model adoption.
    ``sources=None`` checks shape only, before a source registry is loaded.
    Distinct level-4 source IDs are necessary, not proof of independence.
    """
    errors = []
    prefix = '{}: {} label.{}'.format(collection, record.get('id', '?'), language)

    def error(message):
        errors.append('{} {}'.format(prefix, message))

    normalized = normalize_basis(value, record, language)
    if 'legacy' in normalized:
        if set(normalized) != {'legacy'}:
            error('历史依据不得混合结构化字段')
        legacy = normalized['legacy']
        if not _text(legacy):
            error('历史依据必须是非空字符串')
        elif legacy == 'model':
            error('model 字符串缺少模型元数据，不是合法历史依据')
        elif legacy == 'none':
            if _text(label):
                error('历史 none 不得有标签')
        else:
            if not _text(label):
                error('依据存在但标签为空')
            if legacy == 'self':
                if record.get('status') == 'active':
                    error('历史 self 不得用于 active 标签')
            else:
                reference = _legacy_reference(legacy, record)
                if not reference or (sources is not None and reference['source'] not in sources):
                    error('历史依据来源未登记或无法解析')
        return errors

    level = normalized.get('level')
    if type(level) is not int or level not in range(1, 7):
        error('level 必须是 1 至 6 的整数，不能是布尔值')
        return errors
    if level <= 5 and not _text(label):
        error('第 1 至 5 级必须有非空标签')

    if level <= 4:
        if set(normalized) != {'level', 'references'}:
            error('外部依据含不允许的字段')
        references = normalized.get('references')
        if not isinstance(references, list) or not references:
            error('外部依据必须有非空 references 列表')
            return errors
        distinct = set()
        for ref in references:
            if not isinstance(ref, dict):
                error('reference 必须是 source 与 locator 对象')
                continue
            if set(ref) != {'source', 'locator'}:
                error('reference 仅允许 source 与 locator')
            source = ref.get('source')
            if not _text(source) or source in _MARKERS or (sources is not None and source not in sources):
                error('reference.source 必须是真实的已登记来源')
            else:
                distinct.add(source)
            if not _text(ref.get('locator')):
                error('reference.locator 必须是非空字符串')
            if level == 3 and (source != 'wikidata' or not isinstance(ref.get('locator'), str)
                               or not re.fullmatch(r'Q[1-9][0-9]*', ref['locator'])):
                error('第 3 级必须引用 Wikidata 的有效 Q 号')
            if level in (1, 2, 3) and isinstance(source, str) and source in LEGACY_LEVELS:
                if level != LEGACY_LEVELS[source]:
                    error('level 与本次已声明的来源等级不一致')
        if level == 4 and len(distinct) < 2:
            error('第 4 级至少需要两个不同的已登记来源；独立性仍需人工核对')
    elif level == 5:
        if set(normalized) != {'level', 'model'}:
            error('模型依据仅允许 level 与 model，不能含外部引用或声明')
        model = normalized.get('model')
        if not isinstance(model, dict):
            error('model 必须是元数据对象')
        else:
            if set(model) != {'name', 'date', 'rationale', 'approval'}:
                error('model 必须且仅包含 name、date、rationale、approval')
            for field in ('name', 'rationale', 'approval'):
                if not _text(model.get(field)):
                    error('model.{} 必须是非空字符串'.format(field))
            model_date = model.get('date')
            if not isinstance(model_date, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', model_date):
                error('model.date 必须是 YYYY-MM-DD 字符串')
            else:
                try:
                    date.fromisoformat(model_date)
                except ValueError:
                    error('model.date 不是有效日期')
            approval = model.get('approval')
            if not isinstance(approval, str) or not _APPROVAL_REFERENCE.fullmatch(approval):
                error('model.approval 必须是项目内 design/decisions/ 决定文件及非空锚点')
        if decisions is not None:
            key = '{}/{}/{}'.format(collection, record.get('id', '?'), language)
            adopted = decisions.get(key) if isinstance(decisions, dict) else None
            if not isinstance(adopted, dict):
                error('模型依据缺少采纳记录 {}'.format(key))
            else:
                if adopted.get('accept') is not True:
                    error('采纳记录必须明确 accept: true')
                if adopted.get('label') != label:
                    error('采纳译名与输出标签不一致')
                adopted_basis = adopted.get('basis')
                if not isinstance(adopted_basis, dict) or adopted_basis != normalized:
                    error('采纳依据与输出模型依据不一致')
                original = adopted.get('original')
                if not isinstance(original, dict) or not {'en', 'scope'} <= set(original):
                    error('采纳记录缺少原英文与 scope 快照')
                else:
                    if original['en'] != (record.get('label') or {}).get('en'):
                        error('采纳记录原英文已过期')
                    if original['scope'] != record.get('scope'):
                        error('采纳记录原 scope 已过期')
    else:
        if set(normalized) != {'level', 'reason'} or not _text(normalized.get('reason')):
            error('第 6 级必须且仅包含 level 与非空 reason')
        if _text(label):
            error('第 6 级不得有标签')
    return errors


def basis_rows(value):
    """Return plain Chinese field/value rows; rendering and escaping stay local."""
    evidence = normalize_basis(value, {}, '')
    if 'legacy' in evidence:
        return [('依据性质', '历史记录 · 未重新分级'), ('历史值', str(evidence['legacy']))]
    level = evidence.get('level')
    if type(level) is not int or level not in range(1, 7):
        return [('依据性质', '无效依据')]
    if level == 5:
        rows = [('依据性质', '模型知识 · 第 5 级，外部用法未核实')]
        model = evidence.get('model')
        if isinstance(model, dict):
            for key, title in (('name', '模型名称'), ('date', '判断日期'),
                               ('rationale', '判断理由'), ('approval', '采纳授权')):
                if key in model:
                    rows.append((title, str(model[key])))
        return rows
    if level == 6:
        return [('依据性质', '第 6 级 · 未采用'), ('未采用原因', str(evidence.get('reason', '')))]
    names = {1: '规范来源', 2: '专业来源', 3: '知识库来源', 4: '多来源用法'}
    rows = [('依据等级', '第 {} 级 · {}'.format(level, names[level]))]
    for ref in source_references(evidence):
        rows.append(('外部依据', '{} · {}'.format(ref['source'], ref['locator'])))
    if 'rationale' in evidence:
        rows.append(('依据说明', str(evidence['rationale'])))
    if level == 4:
        rows.append(('核验边界', '不同来源标识不证明来源独立性'))
    return rows
