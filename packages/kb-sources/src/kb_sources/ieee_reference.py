"""Read third-party IEEE reference files without adopting their semantics.

These input versions are the repository's cleaned 2023 Thesaurus CSV and
2025 Taxonomy text, not the 2025 complete Thesaurus. Taxonomy IDs identify
occurrences in a source file; identical labels are deliberately not merged.
"""

import csv
import copy
import hashlib
import io
from pathlib import Path


def compare_reference(entries: list[dict], reference: dict) -> dict:
    """Compare separate source versions without adding or rewriting entries.

    Exact matching has priority. Whitespace-only matching is diagnostic: it
    does not establish identity or merge names. Case and punctuation remain
    significant. Taxonomy comparison covers names, not parent relationships.
    """
    def whitespace(value: str) -> str:
        return ' '.join(value.split())

    exact_relations, spaced_relations = {}, {}
    exact_names, spaced_names = {}, {}
    for entry_index, entry in enumerate(entries):
        name = entry['name']
        match = {'entry_index': entry_index, 'name': name}
        exact_names.setdefault(name, []).append(match)
        spaced_names.setdefault(whitespace(name), []).append(match)
        for relation_index, relation in enumerate(entry['relations']):
            predicate, target = relation['predicate'], relation['target']
            match = {
                'entry_index': entry_index,
                'relation_index': relation_index,
                'name': name, 'predicate': predicate, 'target': target,
            }
            exact_relations.setdefault((name, predicate, target), []).append(match)
            spaced_relations.setdefault(
                (whitespace(name), predicate, whitespace(target)), []
            ).append(match)

    def grouped(rows, exact_index, spaced_index, key, normalized_key):
        groups = {'exact': [], 'whitespace_only': [], 'unmatched': []}
        for row in rows:
            exact = exact_index.get(key(row), [])
            spaced = [] if exact else spaced_index.get(normalized_key(row), [])
            category = 'exact' if exact else 'whitespace_only' if spaced else 'unmatched'
            groups[category].append({
                'reference': copy.deepcopy(row),
                'matches': copy.deepcopy(exact or spaced),
            })
        return {
            'counts': {category: len(rows) for category, rows in groups.items()},
            **groups,
        }

    thesaurus = grouped(
        reference['thesaurus']['relations'], exact_relations, spaced_relations,
        lambda row: (row['subject'], row['predicate'], row['object']),
        lambda row: (whitespace(row['subject']), row['predicate'], whitespace(row['object'])),
    )
    taxonomy = grouped(
        reference['taxonomy']['occurrences'], exact_names, spaced_names,
        lambda row: row['label'], lambda row: whitespace(row['label']),
    )
    return {
        'schema_version': 1,
        'notes': [
            'The 2023 Thesaurus and 2025 Taxonomy are separate reference versions; neither is the 2025 July complete Thesaurus.',
            'Unmatched reference rows do not by themselves prove extraction errors: versions and coverage differ.',
            'Whitespace-only matches are review suggestions, not approved identity matches. Case and punctuation are not normalized.',
            'Taxonomy comparison checks entry names only, not hierarchy; no relations are added and no names are merged.',
            'Matching indices are zero-based positions in the supplied entries and their relations.',
        ],
        'thesaurus': {
            'source': copy.deepcopy(reference['thesaurus']['source']),
            **thesaurus,
        },
        'taxonomy': {
            'source': copy.deepcopy(reference['taxonomy']['source']),
            **taxonomy,
        },
    }


def _source(path: Path, raw: bytes, version: str) -> dict:
    return {
        'path': str(path.resolve()),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'version': version,
        'version_basis': 'caller-selected input; not independently verified from file content',
        'representation': 'third-party cleaned transcription',
    }


def load_reference(csv_path: Path, taxonomy_path: Path) -> dict:
    """Load cleaned 2023 CSV and 2025 dot-indented text with source locators.

    Reject malformed structure rather than silently inventing relationships.
    Values are preserved as parsed by CSV; TXT removes only the indentation
    prefix and line terminator. No whitespace/case normalization is applied.
    """
    csv_path, taxonomy_path = Path(csv_path), Path(taxonomy_path)
    csv_raw, taxonomy_raw = csv_path.read_bytes(), taxonomy_path.read_bytes()
    reader = csv.reader(io.StringIO(csv_raw.decode('utf-8-sig'), newline=''), strict=True)
    if next(reader, None) != ['subject', 'predicate', 'object']:
        raise ValueError('Expected CSV header subject,predicate,object')
    relations = []
    while True:
        start = reader.line_num + 1
        try:
            row = next(reader)
        except StopIteration:
            break
        if not row:
            continue
        if len(row) != 3 or any(not value.strip() for value in row):
            raise ValueError(f'Invalid CSV relation at line {start}: expected three nonempty values')
        relations.append({
            'subject': row[0], 'predicate': row[1], 'object': row[2],
            'line': start, 'end_line': reader.line_num,
        })

    occurrences, stack = [], []
    for line_number, raw_line in enumerate(taxonomy_raw.decode('utf-8-sig').splitlines(), 1):
        if not raw_line.strip():
            continue
        dots = len(raw_line) - len(raw_line.lstrip('.'))
        depth = dots // 4
        if dots % 4 or depth > len(stack) or not raw_line[dots:].strip():
            raise ValueError(f'Invalid taxonomy indentation or label at line {line_number}')
        stack = stack[:depth]
        occurrence_id = f'line-{line_number}'
        occurrences.append({
            'id': occurrence_id,
            'parent': stack[-1] if stack else None,
            'depth': depth,
            'label': raw_line[dots:],
            'line': line_number,
            'raw': raw_line,
        })
        stack.append(occurrence_id)

    return {
        'schema_version': 1,
        'thesaurus': {
            'source': _source(csv_path, csv_raw, '2023'),
            'relations': relations,
        },
        'taxonomy': {
            'source': _source(taxonomy_path, taxonomy_raw, '2025'),
            'occurrences': occurrences,
        },
    }
