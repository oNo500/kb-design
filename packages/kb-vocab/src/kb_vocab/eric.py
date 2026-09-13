"""Project ERIC XML into an explicitly bounded SKOS evaluation graph."""
from collections import Counter, defaultdict
import hashlib
import io
import zipfile

from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException
from rdflib import DCTERMS, Graph, Literal, RDF, SKOS, URIRef

from .validation import validate_graph

_LIMIT = 128 * 1024 * 1024


def project_eric(raw: bytes, source: dict, identities=None):
    """Preserve every XML record; only unambiguous active statements enter SKOS."""
    member = None
    if zipfile.is_zipfile(io.BytesIO(raw)):
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members = [i for i in archive.infolist() if not i.is_dir()]
            if len(members) != 1 or not members[0].filename.lower().endswith('.xml'):
                raise ValueError('ERIC archive must contain exactly one XML member')
            item = members[0]
            if item.file_size > _LIMIT:
                raise ValueError('ERIC XML exceeds size limit')
            member = item.filename
            raw = archive.read(item)
    if len(raw) > _LIMIT:
        raise ValueError('ERIC XML exceeds size limit')
    try:
        root = ElementTree.fromstring(raw, forbid_dtd=True, forbid_entities=True, forbid_external=True)
    except (ElementTree.ParseError, DefusedXmlException) as exc:
        raise ValueError(f'Unsafe or invalid ERIC XML: {exc}') from exc
    elements = root.findall('./Terms/Term')
    if root.tag != 'Nstein' or not elements:
        raise ValueError('Expected populated Nstein/Terms/Term ERIC export')
    records, by_name = [], {}
    for ordinal, element in enumerate(elements, 1):
        name = element.findtext('Name')
        if not name or name != name.strip() or name in by_name:
            raise ValueError(f'Missing, padded or duplicate ERIC name at record {ordinal}')
        attrs = defaultdict(list)
        for attr in element.findall('./Attributes/Attribute'):
            attrs[attr.get('name')].append(attr.text or '')
        if len(attrs.get('RecType', [])) != 1:
            raise ValueError(f'Invalid RecType at record {ordinal}')
        relationships = [{'type': rel.get('type'), 'targets': [target.text or '' for target in rel.findall('Is')]}
                         for rel in element.findall('./Relationships/Relationship')]
        record = {'ordinal': ordinal, 'name': name, 'attributes': dict(attrs),
                  'variations': [{'attributes': dict(v.attrib), 'text': v.text or ''} for v in element.findall('./Variations/Variation')],
                  'relationships': relationships, 'raw_xml': ElementTree.tostring(element, encoding='unicode'),
                  'record_type': attrs['RecType'][0]}
        records.append(record)
        by_name[name] = record
    digest = hashlib.sha256(raw).hexdigest()
    from .identity import align, mint
    active_names={r['name'] for r in records if r['record_type']=='Main'
                  and r['attributes'].get('Active',['True'])==['True']
                  and not r['attributes'].get('DeathDate') and not r['attributes'].get('Status')}
    previous={}
    scheme=mint('eric','__scheme__')
    if identities is not None:
        schemes=list(identities.subjects(RDF.type,SKOS.ConceptScheme))
        if len(schemes)!=1 or not any(str(v).startswith('ERIC Thesaurus') for v in identities.objects(schemes[0],SKOS.prefLabel)):
            raise ValueError('identity source must be an ERIC projection')
        scheme=schemes[0]
        for node in identities.subjects(RDF.type,SKOS.Concept):
            names=[str(v) for v in identities.objects(node,SKOS.prefLabel) if v.language=='en']
            if len(names)!=1 or names[0] in previous:raise ValueError('identity source has ambiguous ERIC names')
            previous[names[0]]=node
    stable=align('eric',active_names,previous)
    graph = Graph()
    graph.bind('skos', SKOS); graph.bind('dcterms', DCTERMS)
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal('ERIC Thesaurus evaluation', lang='en')))
    nodes = {}
    for record in records:
        attrs = record['attributes']
        active = attrs.get('Active', ['True']) == ['True']
        # Unknown status and composite declarations remain audit material.
        if record['record_type'] == 'Main' and active and not attrs.get('DeathDate') and not attrs.get('Status'):
            node = stable[record['name']]
            nodes[record['name']] = node
            record.update(disposition='concept', uri=str(node))
            graph.add((node, RDF.type, SKOS.Concept)); graph.add((node, SKOS.inScheme, scheme))
            graph.add((node, SKOS.prefLabel, Literal(record['name'], lang='en')))
            graph.add((node, DCTERMS.identifier, Literal(record['name'])))
            for note in attrs.get('ScopeNote', []):
                graph.add((node, SKOS.scopeNote, Literal(note, lang='en')))
            for ref in attrs.get('Refnum', []):
                graph.add((node, DCTERMS.identifier, Literal(ref)))
        else:
            record['disposition'] = 'retired_record' if record['record_type'] == 'Dead' else 'isolated_status'
    isolated, relations = [], []
    for record in records:
        uses = list(dict.fromkeys(t for rel in record['relationships'] if rel['type'] in ('U', 'USE') for t in rel['targets']))
        attrs = record['attributes']
        if record['record_type'] == 'Synonym':
            if attrs.get('Active', ['True']) != ['True'] or attrs.get('DeathDate') or attrs.get('Status'):
                record['disposition'] = 'isolated_status'
            elif attrs.get('USEAND') or attrs.get('UFA') or len(uses) > 1:
                record['disposition'] = 'isolated_multi_target_use'
            elif len(uses) == 1 and uses[0] in nodes and record['name'] not in nodes:
                graph.add((nodes[uses[0]], SKOS.altLabel, Literal(record['name'], lang='en')))
                record.update(disposition='alternative_label', target_uri=str(nodes[uses[0]]))
            else:
                record['disposition'] = 'isolated_use_target'
        for rel in record['relationships']:
            for target in rel['targets']:
                assertion = {'record': record['ordinal'], 'source': record['name'], 'type': rel['type'], 'target': target}
                kind = rel['type']
                if kind in ('BT', 'NT', 'RT') and record['name'] in nodes and target in nodes:
                    a,b = nodes[record['name']],nodes[target]
                    predicate = SKOS.related if kind == 'RT' else SKOS.broader
                    if kind == 'NT': a,b = b,a
                    graph.add((a,predicate,b))
                    if kind == 'RT': graph.add((b,predicate,a))
                    assertion.update(disposition='relation', triple=[str(a),str(predicate),str(b)])
                elif kind in ('U','USE') and record['disposition'] == 'alternative_label':
                    assertion['disposition'] = 'alternative_label'
                elif kind == 'UF' and target in by_name and by_name[target].get('record_type') == 'Synonym':
                    candidate = by_name[target]
                    candidate_uses = {t for r in candidate['relationships'] if r['type'] in ('U','USE') for t in r['targets']}
                    # UF alone never asserts equivalence; corroborating unambiguous U is required.
                    if candidate_uses == {record['name']} and not any(candidate['attributes'].get(k) for k in ('USEAND','UFA','Status','DeathDate')) and candidate['attributes'].get('Active',['True']) == ['True'] and record['name'] in nodes:
                        assertion['disposition'] = 'corroborating_uf'
                    else:
                        assertion['disposition'] = 'isolated_uf'
                else:
                    assertion['disposition'] = 'isolated_target_or_relation'
                if assertion['disposition'].startswith('isolated'):
                    isolated.append(assertion)
                relations.append(assertion)
    preliminary = validate_graph(graph)
    conflicts = [e for e in preliminary['errors'] if e['code'] == 'skos.S27.related_hierarchy']
    conflict_pairs = set()
    for conflict in conflicts:
        a,b = URIRef(conflict['subject']),URIRef(conflict['object'])
        graph.remove((a,SKOS.related,b)); graph.remove((b,SKOS.related,a))
        conflict_pairs.add(frozenset((str(a),str(b))))
    for assertion in relations:
        triple = assertion.get('triple')
        if triple and triple[1] == str(SKOS.related) and frozenset((triple[0],triple[2])) in conflict_pairs:
            assertion['disposition'] = 'isolated_s27'
            isolated.append(assertion)
    validation = validate_graph(graph)
    report = {'source_type': 'ERIC XML', 'source_records': len(records), 'concepts': len(nodes),
              'alternative_labels': len(list(graph.triples((None,SKOS.altLabel,None)))),
              'record_types': dict(Counter(r['record_type'] for r in records)),
              'record_dispositions': dict(Counter(r['disposition'] for r in records)),
              'source_relations': len(relations), 's27_isolated_pairs': len(conflicts),
              'unresolved_target_names': sorted({a['target'] for a in relations if a['target'] not in by_name}),
              'isolated_relations': len(isolated), 'validation': validation,
              'limitations': ['Evaluation only; no official URI or cross-source mapping is asserted.',
                             'Exact source names reuse prior identities; missing names block automatic identity replacement.',
                             'Multiple USE targets, invalid descriptors and unrecognized statuses remain in ledger.',
                             'S27-related edges are isolated in this evaluation projection; source assertions remain unchanged.',
                             'GroupCode, historical date suffixes and variations remain verbatim; no inferred categories or cleaned labels.']}
    ledger = {'schema_version': 1, 'source': source, 'xml_sha256': digest, 'archive_member': member,
              'identity_policy': 'Exact-name continuity with verified prior Turtle; additions use deterministic local UUID5; missing prior keys block',
              'records': records, 'relations': relations, 'isolated_relations': isolated,
              's27_conflicts': conflicts}
    return graph, report, ledger


def import_eric(source_file, output, identity_file=None):
    from .bundles import publish_bundle, read_source
    raw, source = read_source(source_file)
    from .identity import load_verified
    identities,identity_raw=load_verified(identity_file) if identity_file else (None,None)
    graph, report, ledger = project_eric(raw, source, identities)
    if identity_file:
        from pathlib import Path
        if Path(identity_file).read_bytes()!=identity_raw:raise ValueError('identity source changed during import')
        report['identity_source_sha256']=hashlib.sha256(identity_raw).hexdigest()
        ledger['identity_source']={'path':str(Path(identity_file).resolve()),'sha256':report['identity_source_sha256']}
    return publish_bundle(output, graph, report, ledger, source)
