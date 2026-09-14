"""Versioned builds with a verified, atomically replaced current symlink."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from uuid import uuid4

from .system_build import build_system


def _identifier(value):
    if not isinstance(value,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}',value):
        raise ValueError('Version ID must be a single safe directory name')
    return value


def _layout(root):
    root=Path(root).absolute()
    if root.is_symlink():raise ValueError('Publication root must be a real directory')
    root.mkdir(parents=True,exist_ok=True)
    versions=root/'versions'
    if versions.is_symlink():raise ValueError('Versions must be a real directory')
    versions.mkdir(exist_ok=True)
    current=root/'current'
    if current.is_symlink():
        target=current.resolve()
        if target.parent!=versions.resolve():raise ValueError('Current points outside the version directory')
    elif current.exists():
        raise ValueError('Current is not a symlink; refusing to replace existing data')
    return root


@contextmanager
def _lock(root):
    lock=root/'.publish-lock'
    try:lock.mkdir()
    except FileExistsError:raise ValueError('Another publisher is active; inspect a stale lock before retrying')
    try:yield
    finally:lock.rmdir()


def _verify(version_dir):
    if version_dir.is_symlink() or not version_dir.is_dir():raise ValueError('Version is not a real build directory')
    manifest_file=version_dir/'manifest.json'
    if manifest_file.is_symlink():raise ValueError('Manifest must not be a symlink')
    manifest=json.loads(manifest_file.read_bytes())
    if manifest.get('schema_version') not in (1,2,3,4,5,6,7) or not isinstance(manifest.get('files'),dict):
        raise ValueError('Unsupported build manifest')
    entries=manifest['files']
    required={'vocabulary.ttl','organization.ttl','coverage.json','provenance.json','report.json','validation.json','inputs/config.json','inputs/catalog.json'}
    if manifest['schema_version']>=2:
        required|={'normalization.json','transformation-ledger.jsonl','migration.json','inputs/shapes.ttl','shacl-report.ttl'}
    if manifest['schema_version']>=3:
        required|={'accounting.json','inputs/original-config.json','inputs/invocation-config.json','inputs/original-catalog.json'}
    if manifest['schema_version']>=4:
        required|={'version-diff.json','recovery/environment.json','recovery/requirements.txt','recovery/tool/pyproject.toml','recovery/restore.py','recovery/run.py'}
    if manifest['schema_version']>=5:
        required.add('label-provenance.json')
        paths={'file':'labels.zh.ttl','adoptions':'label-adoptions.json','bibliography':'label-bibliography.yaml'}
        required|={'inputs/'+paths[key] for key in manifest.get('inputs',{}).get('labels',{})}
    if manifest['schema_version']>=6:
        required|={'upstream.ttl','local-effects.json'}
        config=json.loads((version_dir/'inputs/original-config.json').read_bytes())
        if 'local_edits' in config:required.add('inputs/local-edits.json')
    if manifest['schema_version']>=7:required.add('source-selection.json')
    if not required.issubset(entries):raise ValueError('Build manifest is incomplete')
    actual=set()
    for path in version_dir.rglob('*'):
        if path.is_symlink():raise ValueError('Build must not contain symlinks')
        if path.is_file() and path!=manifest_file:actual.add(path.relative_to(version_dir).as_posix())
    if actual!=set(entries):raise ValueError('Build file set differs from manifest')
    for name,expected in entries.items():
        path=version_dir/name
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Unsafe manifest path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValueError(f'Build hash mismatch: {name}')
    report=json.loads((version_dir/'report.json').read_bytes())
    validation=json.loads((version_dir/'validation.json').read_bytes())
    if report.get('introduced_validation_errors')!=[] or validation.get('introduced_errors')!=[]:
        raise ValueError('Build has not passed the new-error gate')
    if manifest['schema_version']==1:
        if report.get('source_statements_preserved') is not True:
            raise ValueError('Legacy build has not passed source preservation')
    else:
        required_flags=('source_copies_preserved','source_concepts_preserved','source_accounting_complete','shacl_conforms')
        if (not all(report.get(key) is True for key in required_flags)
                or validation.get('shacl',{}).get('conforms') is not True
                or validation.get('shacl',{}).get('violations')!=[]):
            raise ValueError('Build has not passed normalization and SHACL gates')
    if manifest['schema_version']>=3:
        accounting=json.loads((version_dir/'accounting.json').read_bytes())
        if accounting.get('verified') is not True:
            raise ValueError('Build has not passed independent source accounting')
    if manifest['schema_version']>=4:
        diff=json.loads((version_dir/'version-diff.json').read_bytes())
        if diff.get('baseline') is not None and diff.get('concepts',{}).get('removed')!=[]:
            from .removal import validate_removal
            config=json.loads((version_dir/'inputs/original-config.json').read_bytes())
            if manifest['schema_version']>=6:
                from .removal import validate_maintenance_removal
                validate_maintenance_removal(diff,config,json.loads((version_dir/'local-effects.json').read_bytes()))
            else:validate_removal(diff,config.get('source_removal'),config['sources'])
    if manifest['schema_version']>=6:
        local=json.loads((version_dir/'local-effects.json').read_bytes())
        if local.get('verified') is not True or local.get('conflicts')!=[]:raise ValueError('Build has unresolved local edits')
    if manifest['schema_version']>=7:
        selection=json.loads((version_dir/'source-selection.json').read_bytes())
        if selection.get('verified') is not True or selection.get('excluded_concepts')!=local.get('selection_excluded_concepts'):
            raise ValueError('Build has not passed source selection accounting')
    return report


def _activate(root,build_id):
    version_dir=root/'versions'/build_id
    _verify(version_dir)
    # Check current again while holding the publication lock.
    _layout(root)
    current=root/'current'
    previous=os.readlink(current) if current.is_symlink() else None
    temporary=root/('.current-'+uuid4().hex)
    try:
        temporary.symlink_to(Path('versions')/build_id,target_is_directory=True)
        os.replace(temporary,current)
    finally:
        if temporary.is_symlink():temporary.unlink()
    return {'version':build_id,'output':str(version_dir),'current':str(current),'previous':previous}


def activate_version(root,build_id):
    """Activate or roll back to a complete verified build; never edit its files."""
    build_id=_identifier(build_id);root=_layout(root)
    with _lock(root):return _activate(root,build_id)


def build_versioned(config_file,root,build_id=None,*,before_activate=None):
    """Build completely before switching current. Failed builds leave it untouched."""
    build_id=_identifier(build_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+uuid4().hex[:8])
    root=_layout(root)
    with _lock(root):
        output=root/'versions'/build_id
        previous=(root/'current').resolve() if (root/'current').is_symlink() else None
        if previous:_verify(previous)
        report=build_system(config_file,output,previous/'vocabulary.ttl' if previous else None)
        if before_activate:before_activate()
        publication=_activate(root,build_id)
    return dict(report,publication=publication)
