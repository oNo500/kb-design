"""Conservative identity continuity: exact keys only, never infer renames."""
import hashlib
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from rdflib import Graph, URIRef


def mint(source, key):
    return URIRef('urn:uuid:' + str(uuid5(NAMESPACE_URL, 'kb-vocab:' + source + ':' + key)))


def align(source, keys, old):
    keys=set(keys)
    missing=set(old)-keys
    if missing:
        raise ValueError('identity source keys disappeared; rename/removal requires explicit alignment: ' + ', '.join(sorted(missing)[:8]))
    if len(set(old.values())) != len(old) or any(not isinstance(v,URIRef) for v in old.values()):
        raise ValueError('identity source contains duplicate or invalid URIs')
    result={key: old[key] if key in old else mint(source,key) for key in keys}
    if len(set(result.values())) != len(result):
        raise ValueError('identity allocation collided with an existing URI')
    return result


def load_verified(path):
    path=Path(path).resolve();raw=path.read_bytes()
    manifest=json.loads((path.parent/'manifest.json').read_bytes())
    expected=manifest.get('files',{}).get(path.name)
    if isinstance(expected,dict):expected=expected.get('sha256')
    if expected!=hashlib.sha256(raw).hexdigest():
        raise ValueError('identity source differs from its manifest')
    return Graph().parse(data=raw,format='turtle',publicID=path.as_uri()),raw
