"""Import a verified bilingual display artifact independently of the English view."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from rdflib import Graph

APP=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('build',type=Path);args=parser.parse_args()
build=args.build.resolve();manifest=json.loads((build/'manifest.json').read_bytes())
if manifest.get('kind')!='bilingual-display':raise ValueError('Expected bilingual display artifact')
for name,digest in manifest['files'].items():
    if Path(name).name!=name:raise ValueError('Invalid artifact path')
    if hashlib.sha256((build/name).read_bytes()).hexdigest()!=digest:raise ValueError('Artifact hash mismatch: '+name)
raw=(build/'vocabulary.multilingual.ttl').read_bytes();labels=(build/'label-provenance.json').read_bytes();metadata=json.loads(labels)
if metadata.get('vocabulary_sha256')!=hashlib.sha256(raw).hexdigest():raise ValueError('Label metadata does not match vocabulary')
spec=importlib.util.spec_from_file_location('sync_translated_base',APP/'sync-current.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
sync.ENDPOINT='http://127.0.0.1:9030/skosmos/data?graph=urn%3Akb-design%3Apreview%3Atranslated'
receipt={'build':str(build),'source_sha256':sync.sha(raw),'english_base_sha256':metadata['base_sha256'],'endpoint':sync.ENDPOINT}
print(json.dumps(sync.publish(APP/'output/translated',Graph().parse(data=raw,format='turtle'),sync.navigation(raw),receipt,labels),indent=2))
