"""Portable local replay inputs with unchanged original configuration evidence."""
import hashlib
import json
from pathlib import Path


def _semantic_config(config):
    result={key: value for key, value in config.items()
            if key not in {'catalog', 'shapes', 'replay_origin','labels','local_edits'}}
    if 'labels' in config:result['labels']=sorted(config['labels'])
    if 'local_edits' in config:result['local_edits']=True
    return result


def configuration_origin(config_file: Path, config_raw: bytes, config: dict) -> bytes:
    """Return verified original bytes, allowing only archive path rebasing."""
    if 'replay_origin' not in config:
        return config_raw
    metadata = config['replay_origin']
    if not isinstance(metadata, dict) or set(metadata) != {'file', 'sha256'}:
        raise ValueError('Invalid replay_origin metadata')
    filename = metadata['file']
    if (not isinstance(filename, str) or not filename or filename in {'.', '..'}
            or '/' in filename or '\\' in filename or ':' in filename):
        raise ValueError('replay_origin file must be a sibling filename')
    path = Path(config_file).resolve().parent / filename
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != metadata['sha256']:
        raise ValueError('replay_origin sha256 does not match original configuration')
    origin = json.loads(raw)
    if not isinstance(origin, dict):
        raise ValueError('Original configuration must be an object')
    if 'replay_origin' in origin:
        raise ValueError('Original configuration cannot contain recursive replay_origin metadata')
    if _semantic_config(config) != _semantic_config(origin):
        raise ValueError('Replay configuration differs from original configuration')
    return raw


def write_replay_inputs(stage: Path, config_raw: bytes, catalog_raw: bytes,
                        shapes_raw: bytes, sources: dict, origin_raw: bytes, label_raw=None, edits_raw=None) -> dict:
    """Write portable inputs; the caller copies pinned sources into sources/."""
    inputs = Path(stage) / 'inputs'
    inputs.mkdir(parents=True, exist_ok=True)
    config = json.loads(config_raw)
    origin = json.loads(origin_raw)
    if not isinstance(origin, dict) or 'replay_origin' in origin:
        raise ValueError('Original configuration cannot contain recursive replay_origin metadata')
    if _semantic_config(config) != _semantic_config(origin):
        raise ValueError('Replay configuration differs from original configuration')
    origin_sha = hashlib.sha256(origin_raw).hexdigest()
    config.update(catalog='catalog.json', shapes='shapes.ttl',
                  replay_origin={'file': 'original-config.json', 'sha256': origin_sha})
    if 'labels' in config:
        filenames={'file':'labels.zh.ttl','adoptions':'label-adoptions.json','bibliography':'label-bibliography.yaml'}
        if set(label_raw or {})!=set(config['labels']):raise ValueError('Missing label replay inputs')
        for key,raw in label_raw.items():(inputs/filenames[key]).write_bytes(raw)
        config['labels']={key:filenames[key] for key in label_raw}
    if 'local_edits' in config:
        if edits_raw is None:raise ValueError('Missing local edit replay input')
        (inputs/'local-edits.json').write_bytes(edits_raw)
        config['local_edits']='local-edits.json'
    catalog = {'sources': [
        {'name': name,
         'file': '../sources/' + hashlib.sha256(name.encode()).hexdigest()[:12] + '.ttl',
         'base': source.get('base') or Path(source['path']).resolve().as_uri(),
         **({'selection':source['selection']} if 'selection' in source else {})}
        for name, source in sorted(sources.items())]}
    for filename, raw in [('original-config.json', origin_raw),
                          ('invocation-config.json', config_raw),
                          ('original-catalog.json', catalog_raw),
                          ('shapes.ttl', shapes_raw)]:
        (inputs / filename).write_bytes(raw)
    for filename, data in [('config.json', config), ('catalog.json', catalog)]:
        (inputs / filename).write_text(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                                 indent=2) + '\n', encoding='utf-8')
    return {'config': 'inputs/config.json', 'catalog': 'inputs/catalog.json',
            'shapes': 'inputs/shapes.ttl', 'origin': 'inputs/original-config.json',
            'origin_sha256': origin_sha}
