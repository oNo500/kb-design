"""Pinned local input reading; this module never downloads or changes a source."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from rdflib import BNode, Graph, RDF, URIRef
from rdflib.namespace import SKOS

from .common import ContractError, digest
from . import __version__

RELATIVE_BASE = 'https://invalid.local/__kb_unresolved_relative__/'


@dataclass
class Source:
    spec: dict
    raw: bytes
    graph: Graph
    selected: set
    raw_path: str


def require(value, message):
    if not value:
        raise ContractError(message)


def absolute_iri(value):
    return isinstance(value, str) and bool(urlsplit(value).scheme) and not any(c.isspace() for c in value)


def iri_list(value, field):
    require(isinstance(value, list) and all(absolute_iri(v) for v in value), f'{field} 需要完整 IRI 列表')
    require(len(value) == len(set(value)), f'{field} 存在重复身份')
    return {URIRef(v) for v in value}


def frozen_file(spec, root, extension, files):
    require(isinstance(spec.get('path'), str), '输入缺少 path')
    path = Path(spec['path'])
    path = path if path.is_absolute() else root / path
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ContractError(f'输入无法读取：{path}：{exc}') from exc
    sha = digest(raw)
    require(spec.get('sha256') == sha, f'输入摘要不符：{path}')
    name = f'inputs/{sha}.{extension}'
    files[name] = raw
    return raw, name


def authority(value, root, files):
    require(isinstance(value, dict), '缺少预览授权 authority')
    for key in ('preview_reference', 'scope_reference'):
        require(isinstance(value.get(key), str) and bool(value[key].strip()), f'授权缺少 {key}')
    require(value.get('formal_reference') is None or isinstance(value['formal_reference'], str), '正式依据必须是引用或 null')
    # 只有显式的本地证据和摘要才冻结正文；网络引用不在导出时联网读取。
    for reference_key, hash_key in (('preview_reference', 'evidence_sha256'), ('formal_reference', 'formal_evidence_sha256')):
        if value.get(hash_key):
            require(isinstance(value.get(reference_key), str) and bool(value[reference_key]), f'{hash_key} 缺少对应依据引用')
            url = urlsplit(value[reference_key])
            require(url.scheme == 'file', f'{hash_key} 需要 file URI 授权证据')
            require(url.netloc in ('', 'localhost'), '授权证据不能是远程 file URI')
            frozen_file({'path': unquote(url.path), 'sha256': value[hash_key]}, root, 'md', files)


def source_scope(graph, spec):
    scope = spec.get('scope')
    choices = {'subject_iris', 'concept_scheme_iris', 'entity_class_iris'}
    require(isinstance(scope, dict) and len(scope) == 1 and set(scope) <= choices, 'scope 范围须选择一种明确条件')
    key = next(iter(scope))
    requested = iri_list(scope[key], 'scope 范围')
    require(requested, 'scope 范围不能为空')
    if key == 'subject_iris':
        missing = {x for x in requested if not any(graph.triples((x, None, None)))}
        selected = requested
    elif key == 'concept_scheme_iris':
        missing = {x for x in requested if not any(graph.triples((x, None, None))) and not any(graph.subjects(SKOS.inScheme, x))}
        selected = {s for x in requested for s in graph.subjects(SKOS.inScheme, x) if (s, RDF.type, SKOS.Concept) in graph}
    else:
        missing = {x for x in requested if not any(graph.subjects(RDF.type, x))}
        selected = {s for x in requested for s in graph.subjects(RDF.type, x)}
    require(not missing, f'声明范围在输入中不存在：{sorted(map(str, missing))}')
    require(all(isinstance(x, URIRef) for x in selected), '选定主体必须具有 IRI，不能使用空白节点身份')
    trial = iri_list(spec.get('trial_subjects'), 'trial_subjects')
    require(trial <= selected, f'预览试选超出授权范围：{sorted(map(str, trial - selected))}')
    return selected


def read_inputs(path):
    root = path.resolve().parent
    raw = path.read_bytes()
    try:
        spec = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise ContractError(f'输入清单不是有效 JSON：{exc}') from exc
    require(isinstance(spec, dict) and type(spec.get('format_version')) is int and spec['format_version'] == 1, '输入清单 format_version 必须为 1')
    require(spec.get('mode') == 'preview', '当前工具只接受 preview，不批准正式使用')
    require(isinstance(spec.get('sources'), list) and bool(spec['sources']), 'sources 需要非空列表')
    require(isinstance(spec.get('auxiliary', []), list), 'auxiliary 必须为列表')
    require(isinstance(spec.get('producer'), dict), '输入缺少 producer')
    require(spec['producer'].get('name') == 'kb-obsidian-rdf' and spec['producer'].get('version') == __version__, '输入导出器与当前包版本不符')
    display = spec.get('display')
    languages = display.get('languages') if isinstance(display, dict) else display
    require(isinstance(languages, list) and bool(languages) and all(isinstance(x, str) and x and '*' not in x for x in languages), 'display.languages 需要具体语言请求列表')
    spec['display'] = {'languages': languages}
    require(isinstance(spec.get('rules'), dict), '输入缺少规则选择 rules')
    files = {f'inputs/{digest(raw)}.json': raw}
    sources, auxiliaries, keys = [], [], set()
    for item in [*spec['sources'], *spec.get('auxiliary', [])]:
        require(isinstance(item, dict), '每项输入须为对象')
        require(isinstance(item.get('key'), str) and bool(item['key']) and '\0' not in item['key'], '输入需要稳定 key')
        require(item['key'] not in keys, f'输入 key 重复：{item["key"]}')
        keys.add(item['key'])
        require(isinstance(item.get('version'), (str, dict)) and bool(item['version']), f'{item["key"]} 缺少版本说明')
        authority(item.get('authority'), root, files)
    for item in spec['sources']:
        require(item.get('format') in ('turtle', 'ttl', 'nt', 'ntriples'), 'RDF 输入仅支持 Turtle 或 N-Triples')
        require(isinstance(item.get('identity'), (str, dict)) and bool(item['identity']), '来源缺少数据身份 identity')
        source_raw, raw_path = frozen_file(item, root, 'ttl' if item['format'] in ('turtle', 'ttl') else 'nt', files)
        base = item.get('base_iri')
        require(base is None or absolute_iri(base), 'base_iri 需要完整绝对 IRI')
        graph = Graph()
        try:
            graph.parse(data=source_raw, format='turtle' if item['format'] in ('turtle', 'ttl') else 'nt', publicID=base or RELATIVE_BASE)
        except Exception as exc:
            raise ContractError(f'RDF 解析失败 {item["key"]}：{exc}') from exc
        unresolved = any(isinstance(term, URIRef) and str(term).startswith(RELATIVE_BASE) for triple in graph for term in triple)
        require(not unresolved, f'{item["key"]} 相对 IRI 缺少来源 base_iri')
        require(all(absolute_iri(str(term)) for triple in graph for term in triple if isinstance(term, URIRef)), 'RDF 包含非绝对 IRI')
        sources.append(Source(item, source_raw, graph, source_scope(graph, item), raw_path))
    for item in spec.get('auxiliary', []):
        require(item.get('kind') in ('types', 'genres', 'forms', 'references'), '辅助输入 kind 不受支持')
        require(item.get('format') in ('yaml', 'yml', 'json'), '辅助输入仅支持 YAML 或 JSON')
        source_raw, raw_path = frozen_file(item, root, item['format'], files)
        try:
            data = yaml.safe_load(source_raw) if item['format'] != 'json' else json.loads(source_raw)
        except Exception as exc:
            raise ContractError(f'辅助数据解析失败：{item["key"]}：{exc}') from exc
        require(isinstance(data, dict), '辅助数据须为对象')
        require(item.get('schema_version') == data.get('schema_version') and item.get('schema_version') is not None, '辅助输入 schema_version 与源数据不符')
        require(isinstance(data.get(item['kind']), list), f'辅助数据缺少 {item["kind"]} 列表')
        auxiliaries.append((item, data, raw_path))
    return spec, digest(raw), files, sources, auxiliaries
