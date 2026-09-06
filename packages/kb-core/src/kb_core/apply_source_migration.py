#!/usr/bin/env python3
import json
import re
import shutil
import subprocess
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import NamedTuple, Sequence

import yaml


class ApplyResult(NamedTuple):
    written: Sequence[str]
    blocked: Sequence[str]


PATH_TOKEN = re.compile(r"([A-Za-z_][A-Za-z0-9_-]*)|\[(\d+)\]")


def parse_field_path(value):
    tokens = []
    for key, index in PATH_TOKEN.findall(value):
        tokens.append(int(index) if index else key)
    if not tokens:
        raise ValueError(f"invalid field path: {value}")
    return tokens


def locate_parent(document, field_path):
    tokens = parse_field_path(field_path)
    current = document
    for token in tokens[:-1]:
        current = current[token]
    return current, tokens[-1]


def apply_row(document, row):
    parent, key = locate_parent(document, row["field_path"])
    actual = parent[key]
    if actual != row["old_value"]:
        raise ValueError(f"old value mismatch: {row['identity']}")
    operation = row["operation"]
    if operation == "keep":
        return False
    if operation == "set":
        parent[key] = deepcopy(row["new_value"])
    elif operation == "delete":
        del parent[key]
    elif operation == "isolate":
        if not isinstance(actual, str):
            raise ValueError(f"isolate expects scalar: {row['identity']}")
        del parent[key]
        parent["local_analysis"] = deepcopy(row["new_value"])
    else:
        raise ValueError(f"unknown operation: {operation}")
    return True


def _load_yaml_or_json(path):
    text = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _write_yaml_or_json(path, document):
    path = Path(path)
    if path.suffix == ".json":
        path.write_text(
            json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        path.write_text(
            yaml.safe_dump(document, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )


def load_and_validate_ledgers(plan_dir):
    plan_dir = Path(plan_dir)
    plan_path = plan_dir / "plan.yaml"
    if not plan_path.is_file():
        raise ValueError(f"missing migration plan: {plan_path}")
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    if not isinstance(plan, dict) or plan.get("schema_version") != 1:
        raise ValueError("invalid migration plan")
    rows = plan.get("rows")
    if not isinstance(rows, list):
        raise ValueError("invalid migration rows")
    identities = [row.get("identity") for row in rows]
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate migration identity")
    return plan


def _safe_relative(value):
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"non-formal path: {value}")
    return path


def group_rows_by_file(rows):
    grouped = {}
    seen = set()
    for row in rows:
        relative = _safe_relative(row["old_file"])
        key = (str(relative), row["field_path"])
        if key in seen:
            raise ValueError(f"duplicate migration field: {key}")
        seen.add(key)
        grouped.setdefault(str(relative), []).append(row)
    return grouped


def _apply_file_rewrites(candidate_root, rewrites, changed):
    for rewrite in rewrites:
        relative = str(_safe_relative(rewrite["path"]))
        path = candidate_root / relative
        if candidate_root.resolve() not in path.resolve().parents:
            raise ValueError(f"candidate path escapes output: {relative}")
        if "old_sha256" in rewrite:
            import hashlib
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != rewrite["old_sha256"]:
                raise ValueError(f"old file hash mismatch: {relative}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rewrite["content"], encoding="utf-8")
        changed.add(relative)


def _validate_candidate_files(candidate_root, changed):
    for relative in sorted(changed):
        path = candidate_root / relative
        if path.suffix in {".json", ".yaml", ".yml"}:
            _load_yaml_or_json(path)


def _copy_audit_inputs(root, destination, plan):
    """Copy tracked audit inputs, or explicit fixture inputs; never a working tree."""
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--', '.'],
                            capture_output=True)
    paths = (result.stdout.decode().split('\0') if result.returncode == 0 else
             [row['old_file'] for row in plan['rows']] +
             [row['path'] for row in plan.get('file_rewrites', []) if 'old_sha256' in row])
    excluded = {'.git', '.superpowers', '__pycache__', 'output', 'build', '.venv', 'node_modules'}
    for value in sorted(set(paths)):
        if not value:
            continue
        relative = _safe_relative(value)
        if excluded.intersection(relative.parts):
            continue
        source = Path(root) / relative
        if not source.is_file() or source.is_symlink() or Path(root).resolve() not in source.resolve().parents:
            raise ValueError(f'unsafe or missing audit input: {relative}')
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def write_candidate_tree(root, plan, output_root):
    blockers = sorted(
        row["identity"] for row in plan["rows"] if row.get("blocks_cutover")
    )
    if blockers:
        return ApplyResult((), tuple(blockers))
    if output_root.exists():
        raise ValueError("candidate output must be absent")
    output_root.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=output_root.name + ".building-", dir=output_root.parent))
    try:
        _copy_audit_inputs(root, temporary, plan)
        changed = set()
        for relative, rows in sorted(group_rows_by_file(plan["rows"]).items()):
            path = temporary / relative
            if temporary.resolve() not in path.resolve().parents:
                raise ValueError(f"candidate path escapes output: {relative}")
            document = _load_yaml_or_json(path)
            for row in sorted(
                rows,
                key=lambda item: (
                    item.get("old_record", ""),
                    item["field_path"],
                    item["identity"],
                ),
            ):
                if apply_row(document, row):
                    changed.add(relative)
            if relative in changed:
                _write_yaml_or_json(path, document)
        _apply_file_rewrites(
            temporary, plan.get("file_rewrites", []), changed
        )
        _validate_candidate_files(temporary, changed)
        temporary.rename(output_root)
        return ApplyResult(tuple(sorted(changed)), ())
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def apply_migration(root, plan_dir, output_root):
    root = Path(root).resolve()
    output_root = Path(output_root).resolve()
    if output_root == root or root in output_root.parents:
        raise ValueError("output_root must be outside formal root")
    plan = load_and_validate_ledgers(plan_dir)
    return write_candidate_tree(root, plan, output_root)


REFERENCE_FIELDS = frozenset({'source', 'match', 'external_group', 'assertions', 'local_analysis'})


def load_reference_inputs(root, path=None):
    """Read explicit field adoptions; absence is uncertainty, never a fallback."""
    path = Path(path) if path else Path(root) / 'data/inputs/topics/source-references-v2.json'
    if not path.is_file():
        return {'schema_version': 2, 'records': {}}
    document = _load_yaml_or_json(path)
    if (not isinstance(document, dict) or set(document) != {'schema_version', 'records'}
            or document.get('schema_version') != 2 or not isinstance(document.get('records'), dict)):
        raise ValueError(f'invalid v2 reference inputs: {path}')
    return document


def _field_is_adopted(decisions, identity, field, value, evidence):
    from kb_core.source_model import decision_authorizes
    return (isinstance(evidence, dict) and evidence.get('reviewed') is True
            and decision_authorizes(decisions, evidence.get('decision'), identity, field, value))


def migrate_reference_document(root, collection, document, inputs):
    """Replace reference fields only, requiring exact old values and adoptions.

    This produces a candidate document, not activation or approval of a dataset.
    Language basis, IDs and memberships are copied. Scope changes require a separate
    exact adoption and an old-value snapshot after language adoptions are applied.
    """
    from kb_core.source_model import collect_reference_uses, validate_references, _load_accepted_decisions
    if inputs.get('schema_version') != 2 or not isinstance(inputs.get('records'), dict):
        raise ValueError('invalid v2 reference inputs')
    decisions = _load_accepted_decisions(Path(root) / 'docs/decisions')
    result = deepcopy(document)
    blockers = []
    seen = set()
    for section, records in result.items():
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict) or 'id' not in record:
                continue
            identity = f'{collection}/{section}/{record["id"]}'
            seen.add(identity)
            before = {field: deepcopy(record[field]) for field in REFERENCE_FIELDS if field in record}
            if not before:
                continue
            invalid_before = []
            for field, value in before.items():
                if field == 'source':
                    valid = isinstance(value, str) and bool(value.strip())
                elif field == 'match':
                    valid = isinstance(value, list) and all(
                        isinstance(item, dict) and set(item) == {'source', 'id', 'rel'}
                        and all(isinstance(item[key], str) and bool(item[key].strip())
                                for key in ('source', 'id', 'rel'))
                        and item['rel'] in {'exactMatch', 'closeMatch', 'broadMatch', 'narrowMatch', 'relatedMatch'}
                        for item in value)
                else:
                    # This entry point only migrates v1. Existing v2 fields must
                    # never be treated as removable legacy input.
                    valid = False
                if not valid:
                    invalid_before.append(f'{identity}.{field}: expected unmigrated v1 reference field')
            if invalid_before:
                blockers.extend(invalid_before)
                continue
            entry = inputs['records'].get(identity)
            if not isinstance(entry, dict):
                blockers.extend(f'{identity}.{field}: missing reviewed migration input' for field in sorted(before))
                continue
            after = entry.get('after')
            expected_before = deepcopy(before)
            if isinstance(after, dict) and 'scope' in after:
                expected_before['scope'] = deepcopy(record.get('scope'))
            if (set(entry) != {'before', 'after', 'evidence'} or entry.get('before') != expected_before
                    or not isinstance(after, dict) or set(after) - (REFERENCE_FIELDS | {'scope'})):
                blockers.append(f'{identity}: stale or invalid reference migration input')
                continue
            errors = []
            # Isolation preserves the old object in the same accepted decision;
            # it is not an adoption of that object's external claim.
            old_matches, new_matches = before.get('match', []), after.get('match', [])
            evidence = entry.get('evidence')
            if not isinstance(evidence, dict):
                blockers.append(f'{identity}: invalid migration evidence')
                continue
            match_evidence = evidence.get('match', {})
            isolated = match_evidence.get('isolated', []) if isinstance(match_evidence, dict) else []
            if (not isinstance(isolated, list)
                    or any(type(index) is not int or not 0 <= index < len(old_matches) for index in isolated)
                    or len(set(isolated)) != len(isolated)):
                errors.append(f'{identity}.match: invalid isolation indexes')
                isolated = []
            for index in isolated:
                if not _field_is_adopted(decisions, identity, f'match[{index}].isolation',
                                         old_matches[index], match_evidence):
                    errors.append(f'{identity}.match[{index}]: missing exact isolation adoption')
            retained = [(index, old) for index, old in enumerate(old_matches) if index not in isolated]
            if (('match' in before and 'match' not in after)
                    or not isinstance(new_matches, list) or len(retained) != len(new_matches)):
                errors.append(f'{identity}.match: mapping identity or relation changed')
            else:
                for (index, old), new in zip(retained, new_matches):
                    same = (isinstance(new, dict)
                            and (old['source'], old['id'], old['rel']) ==
                            (new.get('registry'), new.get('item'), new.get('rel')))
                    if not same and not _field_is_adopted(
                            decisions, identity, f'match[{index}].correction',
                            {'before': old, 'after': new}, match_evidence):
                        errors.append(f'{identity}.match[{index}]: mapping identity or relation changed')
            old_source = before.get('source')
            if old_source == 'self':
                assertion = after.get('assertions', {}).get('source', {})
                if ('source' in after or set(assertion) != {'disposition', 'original', 'migration'}
                        or assertion.get('disposition') != 'project_assertion'
                        or assertion.get('original') != 'self' or not assertion.get('migration')):
                    errors.append(f'{identity}.source: local assertion must preserve self and audit location')
            elif isinstance(old_source, str):
                field = 'external_group' if section == 'arrays' else 'source'
                if collection == 'forms' and section == 'arrays':
                    field = 'local_analysis'
                    local = after.get(field)
                    if (not isinstance(local, dict)
                            or set(local) != {'legacy_source_label', 'state', 'decision'}
                            or local.get('legacy_source_label') != old_source
                            or local.get('state') != 'isolated'
                            or local.get('decision') != 'decision-source-0011'
                            or local.get('decision') not in decisions
                            or 'source' in after or 'external_group' in after):
                        errors.append(f'{identity}.{field}: Q16 isolation must preserve the original label and accepted decision')
                elif not isinstance(after.get(field), dict) or after[field].get('registry') != old_source:
                    errors.append(f'{identity}.{field}: original source registry must be preserved')
            for field, value in after.items():
                # Keeping an empty match creates no fact. Every other result must
                # be backed by the exact field/value in an accepted decision.
                if field == 'match' and value == [] and before.get('match', []) == []:
                    continue
                if not _field_is_adopted(decisions, identity, field, value, evidence.get(field)):
                    errors.append(f'{identity}.{field}: missing reviewed field adoption')
            if errors:
                blockers.extend(errors)
                continue
            for field in REFERENCE_FIELDS:
                record.pop(field, None)
            record.update(deepcopy(after))
    for identity in inputs['records']:
        if identity.startswith(collection + '/') and identity not in seen:
            blockers.append(f'{identity}: unknown migration target')
    if blockers:
        raise ValueError('\n'.join(sorted(blockers)))
    references = collect_reference_uses(Path(f'data/vocab/{collection}.yaml'), result)
    issues = validate_references(Path(root), references)
    if issues:
        raise ValueError('\n'.join(f'{collection}/{issue.record}.{issue.field_path}: {issue.code}' for issue in issues))
    result['schema_version'] = 2
    return result


def write_reference_candidate(root, collection, output, inputs_path=None):
    """Write one reference-migration candidate under build, without copying a tree."""
    root, output = Path(root).resolve(), Path(output).resolve()
    if collection not in {'topics', 'entities', 'types', 'genres', 'forms'}:
        raise ValueError('unsupported reference collection')
    if root / 'build' not in output.parents:
        raise ValueError('reference candidate output must be under root/build')
    if output.exists():
        raise ValueError('reference candidate output must be absent')
    document = _load_yaml_or_json(root / f'data/vocab/{collection}.yaml')
    candidate = migrate_reference_document(root, collection, document,
                                           load_reference_inputs(root, inputs_path))
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_yaml_or_json(output, candidate)
    return output


def main(argv=None):
    import argparse
    from kb_core.repository import project_root
    parser = argparse.ArgumentParser(description='Build an explicitly adopted reference candidate; frozen v1 ledgers remain audit only.')
    parser.add_argument('--root', type=Path, default=None)
    parser.add_argument('--collection', required=True, choices=('topics', 'entities', 'types', 'genres', 'forms'))
    parser.add_argument('--references', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        output = write_reference_candidate(args.root or project_root(), args.collection, args.output, args.references)
    except ValueError as exc:
        parser.exit(1, str(exc) + '\n')
    print(f'Reference candidate: {output}; full repository validation is still required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
