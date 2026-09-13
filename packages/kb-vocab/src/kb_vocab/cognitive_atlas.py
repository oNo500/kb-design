"""Cognitive Atlas evaluation projection; source assertions remain auditable."""
from collections import Counter
from importlib.resources import files
import hashlib
from html import unescape
import json
import os
from pathlib import Path
import tempfile
from .identity import mint, align

from rdflib import Graph, Literal, RDF, RDFS, SKOS, DCTERMS, URIRef
from rdflib.compare import isomorphic
from kb_vocab.validation import validate_graph


def project_cognitive(data, identities=None, exclusion_policy=None):
    records = data['records']
    by_id = {row['id']: row for row in records}
    if len(by_id) != len(records) or not records:
        raise ValueError('empty or duplicate Cognitive Atlas IDs')
    if any(row['kind'] not in ('concept', 'task') for row in records):
        raise ValueError('unknown source record kind')
    if identities is None:
        scheme = mint('cognitive-atlas','__scheme__')
        ids = align('cognitive-atlas',by_id,{})
    else:
        schemes = list(identities.subjects(RDF.type, SKOS.ConceptScheme))
        if len(schemes) != 1:
            raise ValueError('identity graph needs one concept scheme')
        scheme = schemes[0]
        ids = {}
        for node, key in identities.subject_objects(DCTERMS.identifier):
            if str(key) in ids or not isinstance(node, URIRef):
                raise ValueError('duplicate or invalid source identity')
            ids[str(key)] = node
        for key,node in ids.items():
            if key in by_id and ((node,RDF.type,SKOS.Concept) in identities) != (by_id[key]['kind']=='concept'):
                raise ValueError('identity source record kind changed')
        ids=align('cognitive-atlas',by_id,ids)
    graph = Graph()
    for prefix, ns in [('skos', SKOS), ('dcterms', DCTERMS), ('rdfs', RDFS)]:
        graph.bind(prefix, ns)
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal('Cognitive Atlas cognitive concepts', lang='en')))
    graph.add((scheme, DCTERMS.source, URIRef('https://www.cognitiveatlas.org/')))
    graph.add((scheme, SKOS.note, Literal('Evaluation of source assertions, not adopted vocabulary or a complete discipline classification. Tasks are separate RDF resources. Held statements and original fields remain in mapping-ledger.json.', lang='en')))
    ledger = {'stage': 'evaluation-only', 'entries': [], 'relations': []}
    for row in records:
        node, detail, kind = ids[row['id']], row['detail'], row['kind']
        label = SKOS.prefLabel if kind == 'concept' else RDFS.label
        definition = SKOS.definition if kind == 'concept' else DCTERMS.description
        graph.add((node, RDF.type, SKOS.Concept if kind == 'concept' else RDFS.Resource))
        if kind == 'concept':
            graph.add((node, SKOS.inScheme, scheme))
        graph.add((node, DCTERMS.type, Literal(kind)))
        graph.add((node, DCTERMS.identifier, Literal(row['id'])))
        graph.add((node, label, Literal(unescape(detail['name']), lang='en')))
        graph.add((node, DCTERMS.source, URIRef(row['source_url'])))
        if detail.get('definition_text'):
            graph.add((node, definition, Literal(unescape(detail['definition_text']), lang='en')))
        # Alias fields can contain multiple expressions without a documented delimiter.
        # Preserve the original field without manufacturing individual altLabels.
        ledger['entries'].append({**row, 'resource': str(node),
                                  'unmapped_fields': sorted(set(detail) - {'id', 'name', 'definition_text', 'relationships'}),
                                  'alias_policy': 'preserved in source detail; not split into inferred labels'})
    concepts = {r['id'] for r in records if r['kind'] == 'concept'}
    edges = {(r['id'], rel.get('id'), rel.get('relationship'), rel.get('direction'))
             for r in records if r['kind'] == 'concept' for rel in r['detail']['relationships']}
    hierarchy = Graph()
    for a, b, relation, direction in edges:
        if relation == 'KINDOF' and a in concepts and b in concepts and direction in ('parent', 'child'):
            child, parent = (a, b) if direction == 'parent' else (b, a)
            hierarchy.add((ids[child], SKOS.broader, ids[parent]))
    for row in records:
        kind, identity = row['kind'], row['id']
        field = 'relationships' if kind == 'concept' else 'concepts'
        for index, relation in enumerate(row['detail'].get(field, [])):
            target, predicate, direction = relation.get('id'), relation.get('relationship'), relation.get('direction')
            reason, triple = None, None
            if kind == 'task':
                reason = 'task_assertion_requires_contrast_context'
            elif target not in concepts:
                reason = 'target_outside_concept_catalog'
            elif direction not in ('parent', 'child'):
                reason = 'unknown_direction'
            elif identity == target:
                reason = 'self_relation'
            elif predicate == 'KINDOF':
                child, parent = (identity, target) if direction == 'parent' else (target, identity)
                opposite = 'child' if direction == 'parent' else 'parent'
                if (target, identity, predicate, opposite) not in edges:
                    reason = 'missing_reciprocal'
                elif ids[child] in set(hierarchy.transitive_objects(ids[parent], SKOS.broader)):
                    reason = 'hierarchy_cycle'
                else:
                    triple = (ids[child], SKOS.broader, ids[parent])
            elif predicate == 'PARTOF':
                part, whole = (identity, target) if direction == 'parent' else (target, identity)
                triple = (ids[part], DCTERMS.isPartOf, ids[whole])
            else:
                reason = 'unmapped_source_relation'
            item = {'source_id': identity, 'field': field, 'index': index,
                    'source_relation': relation, 'status': 'emitted' if triple else 'held', 'reason': reason}
            if triple:
                graph.add(triple)
                item['triple'] = ' '.join(term.n3() for term in triple) + ' .'
            ledger['relations'].append(item)
    applied = False
    if exclusion_policy and exclusion_policy.get('source_data_sha256') == hashlib.sha256(
            json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest():
        rows = {(r['source_id'], r['field'], r['index']): r for r in ledger['relations']}
        selected = set()
        for exclusion in exclusion_policy['exclusions']:
            key = (exclusion['source_id'], exclusion['field'], exclusion['index'])
            row = rows.get(key)
            if key in selected or row is None or row['status'] != 'held' or row['reason'] != exclusion['reason']:
                raise ValueError('review exclusion does not match a held source statement')
            selected.add(key)
        for key in selected:
            rows[key]['status'] = 'excluded_by_review'
            rows[key]['review_id'] = exclusion_policy['id']
        applied = True
    ledger['applied_review'] = exclusion_policy if applied else None
    return graph, ledger


def import_cognitive(source_file, output, identity_file=None):
    source = Path(source_file).resolve()
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    receipt_raw = (source.parent / 'record.json').read_bytes()
    receipt = json.loads(receipt_raw)
    if (data.get('representation') != 'cognitive-atlas-source-transcription'
            or receipt['outputs'].get(source.name) != digest or receipt['source'] != data['source']):
        raise ValueError('source transcription hash or metadata mismatch')
    target = Path(output).absolute()
    if target.exists() or target.is_symlink() or source.parent == target.resolve() or source.parent in target.resolve().parents:
        raise ValueError('output must be a new directory outside the source transcription')
    identities, previous = None, None
    if identity_file:
        previous = Path(identity_file).read_bytes()
        manifest = json.loads((Path(identity_file).parent / 'manifest.json').read_bytes())
        if manifest['files'].get(Path(identity_file).name) != hashlib.sha256(previous).hexdigest():
            raise ValueError('identity graph differs from its source or manifest')
        identities = Graph().parse(data=previous, format='turtle')
    policy = json.loads(files('kb_vocab').joinpath('policies', 'cognitive-atlas-2026-09-13.json').read_text())
    graph, ledger = project_cognitive(data, identities, policy if policy['source_json_sha256'] == digest else None)
    validation = validate_graph(graph)
    if not validation['valid']:
        raise ValueError('projection failed SKOS/profile validation')
    report = {'stage': 'evaluation-only', 'source_json_sha256': digest,
              'concepts': len(set(graph.subjects(RDF.type, SKOS.Concept))),
              'tasks': sum(r['kind'] == 'task' for r in data['records']), 'triples': len(graph),
              'broader': len(list(graph.triples((None, SKOS.broader, None)))),
              'isPartOf': len(list(graph.triples((None, DCTERMS.isPartOf, None)))),
              'relation_dispositions': dict(Counter(r['reason'] or 'emitted' for r in ledger['relations'])),
              'validation': validation,
              'relation_statuses': dict(Counter(r['status'] for r in ledger['relations'])),
              'applied_review': ledger['applied_review']['id'] if ledger['applied_review'] else None}
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.cognitive-', dir=target.parent) as tmp:
        stage = Path(tmp) / 'result'; stage.mkdir()
        graph.serialize(destination=stage/'vocabulary.ttl', format='turtle', encoding='utf-8')
        if not isomorphic(graph, Graph().parse(stage/'vocabulary.ttl', format='turtle')):
            raise ValueError('Turtle round trip changed graph')
        for name, value in [('mapping-ledger.json', ledger), ('report.json', report), ('validation.json', validation)]:
            (stage/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
        if ledger['applied_review']:
            (stage/'review-policy.json').write_text(json.dumps(ledger['applied_review'], ensure_ascii=False, indent=2)+'\n')
        (stage/'index.md').write_text('# 认知词表评估\n\n'
            f'{report["concepts"]} 个 SKOS 概念、{report["tasks"]} 个独立任务资源。'
            f'{report["broader"]} 条上下位关系、{report["isPartOf"]} 条部分关系。\n\n'
            '[Turtle 数据](vocabulary.ttl) · [映射账本](mapping-ledger.json) · [转换报告](report.json) · [校验结果](validation.json)\n\n'
            'KINDOF 映射为 skos:broader；PARTOF 映射为 dcterms:isPartOf。任务断言及其实验对比条件、原始别名字段和分组等保留在账本中，不推断额外关系。异常的逐项处理见映射账本；只有匹配固定来源的已核记录才明确排除。\n\n'
            '本结果仅为来源评估，不代表正式词表采纳或整个认知科学的完整分类。UUID 首次分配后通过 --identities 复用；来源 ID 相同则复用，缺失旧 ID 或改变概念类型会阻止自动替换。\n')
        manifest = {'source_file': str(source), 'source_json_sha256': digest,
                    'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    'identity_source_sha256': hashlib.sha256(previous).hexdigest() if previous else None,
                    'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}}
        (stage/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
        if source.read_bytes() != raw or (source.parent/'record.json').read_bytes() != receipt_raw:
            raise ValueError('source changed during conversion')
        if identity_file and Path(identity_file).read_bytes() != previous:
            raise ValueError('identity graph changed during conversion')
        if target.exists() or target.is_symlink():
            raise ValueError('output appeared during conversion')
        os.rename(stage, target)
    return report
