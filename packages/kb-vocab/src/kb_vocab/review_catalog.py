"""Local source indexing and label-based review candidates, without adoption."""
from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import unicodedata
from urllib.parse import urlsplit
from uuid import NAMESPACE_URL, uuid5

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DCTERMS, RDF, SKOS


def read_catalog(path):
    """Read every local catalog source and check available manifest TTL hashes.

    The returned SHA describes the local bytes; a matching bundle manifest is
    an integrity check, not a statement about source authority or adoption.
    """
    catalog = Path(path).resolve()
    entries = json.loads(catalog.read_text(encoding='utf-8'))['sources']
    if not isinstance(entries, list):
        raise ValueError('Catalog sources must be a list')
    sources = {}
    for entry in entries:
        name = entry.get('name')
        if not isinstance(name, str) or not name.strip() or name in sources:
            raise ValueError(f'Invalid or duplicate source name: {name!r}')
        if ('file' in entry) == ('directory' in entry):
            raise ValueError(f'Source {name} requires exactly one file or directory')
        location = entry.get('file', entry.get('directory'))
        if not isinstance(location, str) or not location or urlsplit(location).scheme or location.startswith('//'):
            raise ValueError(f'Source {name} requires a local file path')
        ttl = catalog.parent / location
        if 'directory' in entry:
            ttl /= 'vocabulary.ttl'
        ttl = ttl.resolve()
        if not ttl.is_file():
            raise ValueError(f'Source {name} is not a local file: {ttl}')
        raw = ttl.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        manifest = ttl.parent / 'manifest.json'
        if manifest.exists():
            files = json.loads(manifest.read_text(encoding='utf-8')).get('files', {})
            expected = files.get(ttl.name)
            if isinstance(expected, dict):
                expected = expected.get('sha256')
            if not isinstance(expected, str) or expected.lower() != sha:
                raise ValueError(f'Source {name} sha256 does not match manifest: {ttl}')
        base = entry.get('base', ttl.as_uri())
        if (not isinstance(base, str) or not urlsplit(base).scheme
                or any(character.isspace() or ord(character) < 32
                       or character in '<>"{}|^`\\' for character in base)):
            raise ValueError(f'Source {name} base must be an absolute IRI')
        graph = Graph().parse(data=raw, format='turtle', publicID=base)
        sources[name] = {'name': name, 'path': str(ttl), 'sha256': sha,
                         'graph': graph, 'base': base, **({'selection':entry['selection']} if 'selection' in entry else {})}
    return dict(sorted(sources.items()))


def _texts(graph, subject, predicates):
    values = [{'value': str(value), 'language': value.language or '', 'kind': kind}
              for predicate, kind in predicates
              for value in graph.objects(subject, predicate) if isinstance(value, Literal)]
    return sorted(values, key=lambda item: (item['kind'], item['language'], item['value']))


def index_concepts(sources, *, allow_shared=False):
    """Index explicit SKOS concepts without pruning unlabelled or retired ones."""
    index = {}
    for name, source in sorted(sources.items()):
        graph = source['graph']
        for subject in sorted(set(graph.subjects(RDF.type, SKOS.Concept)), key=str):
            if not isinstance(subject, URIRef):
                raise ValueError(f'Source {name} has a concept without a stable URI: {subject}')
            uri = str(subject)
            if uri in index and allow_shared:
                index[uri]['sources'].append(name)
                continue
            if uri in index:
                raise ValueError(f'Concept URI occurs in multiple sources: {uri}')
            index[uri] = {
                'source': name, 'sources':[name],
                'labels': _texts(graph, subject, [(SKOS.prefLabel, 'prefLabel'),
                    (SKOS.altLabel, 'altLabel'), (SKOS.hiddenLabel, 'hiddenLabel')]),
                'definitions': _texts(graph, subject, [(SKOS.definition, 'definition'),
                    (SKOS.scopeNote, 'scopeNote'), (DCTERMS.description, 'description')]),
                'broader': sorted({str(value) for value in graph.objects(subject, SKOS.broader)
                                   if isinstance(value, URIRef)}),
                'related': sorted({str(value) for value in graph.objects(subject, SKOS.related)
                                   if isinstance(value, URIRef)}),
            }
    return dict(sorted(index.items()))


def candidate_pairs(index):
    """Return deterministic cross-source label coincidences for human review.

    Language tags are compared case-insensitively. Untagged labels only match
    untagged labels. No equivalence or other SKOS relation is inferred.
    """
    labels = defaultdict(list)
    for uri, concept in sorted(index.items()):
        for label in concept['labels']:
            if label['kind'] not in ('prefLabel', 'altLabel'):
                continue
            normalized = ' '.join(unicodedata.normalize('NFC', label['value']).split()).casefold()
            if normalized:
                labels[(label['language'].lower(), normalized)].append((uri, label))
    pairs = defaultdict(list)
    for (language, normalized), entries in sorted(labels.items()):
        for (left, left_label), (right, right_label) in combinations(entries, 2):
            if index[left]['source'] == index[right]['source']:
                continue
            if right < left:
                left, right, left_label, right_label = right, left, right_label, left_label
            evidence = {'language': language, 'normalized': normalized,
                        'subject_label': dict(left_label), 'object_label': dict(right_label)}
            if evidence not in pairs[(left, right)]:
                pairs[(left, right)].append(evidence)
    return [{'id': uuid5(NAMESPACE_URL, json.dumps([left, right], ensure_ascii=False,
                    separators=(',', ':'))).urn,
             'subject': left, 'object': right,
             'evidence': sorted(evidence, key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True))}
            for (left, right), evidence in sorted(pairs.items())]
