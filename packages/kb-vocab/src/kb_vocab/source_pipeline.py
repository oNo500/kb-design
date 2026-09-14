"""Reuse existing acquisition/extraction/import adapters from source declarations."""
import hashlib
import importlib
import json
from pathlib import Path
import shutil
from uuid import uuid4
from .edit_store import atomic,encode

SUPPORTED={'ieee','msc','eric','philpapers','cognitive-atlas','unesco'}


def declaration_digest(entry):
    # Projection scope is not a change to the acquisition/import recipe.
    return hashlib.sha256(encode({k:v for k,v in entry.items() if k!='selection'})).hexdigest()


def materialize(entry,base,work,previous=None,refresh=False,cached=None):
    declaration=declaration_digest(entry)
    pipeline=entry.get('pipeline')
    if not refresh:
        if pipeline and cached and cached.get('declaration')==declaration and Path(cached['file']).is_file():
            return Path(cached['file']),declaration
        path=(base/entry.get('file',entry.get('directory',''))).resolve()
        if 'directory' in entry:path/='vocabulary.ttl'
        if path.is_file():return path,declaration
        if not pipeline:raise ValueError('Source file is missing: '+str(path))
    if not isinstance(pipeline,dict) or pipeline.get('importer') not in SUPPORTED:
        raise ValueError('Source refresh requires a supported pipeline importer: '+entry['name'])
    work.mkdir(parents=True,exist_ok=True);kind=pipeline['importer']
    source=(base/pipeline['input']).resolve() if 'input' in pipeline else None
    acquisition=pipeline.get('acquisition')
    if acquisition:
        try:
            from kb_sources.download import fetch,verify
        except ModuleNotFoundError as exc:raise ValueError('Acquisition requires the existing kb-sources package; offline edits do not') from exc
        manifest=(base/acquisition['manifest']).resolve()
        if kind=='cognitive-atlas':
            from kb_sources.cognitive_atlas import acquire,export_source
            bundle=work/'api';acquire(manifest,bundle);export_source(bundle,work/'transcription')
            source=work/'transcription/source.json'
        else:
            snapshot=fetch(manifest,work/'downloads');receipt=verify(snapshot)
            rows=[r for r in receipt['files'] if r['id']==acquisition['file_id']]
            if len(rows)!=1:raise ValueError('Acquisition must select one file ID')
            source=snapshot/rows[0]['filename']
            if kind=='ieee':
                from kb_sources.ieee_thesaurus import extract_ieee
                # Preserve the verified acquisition; extraction receives a derived
                # local wrapper instead of modifying the immutable download.
                inputs=work/'pdf-input';inputs.mkdir();shutil.copyfile(source,inputs/source.name)
                atomic(inputs/'acquisition.json',encode({'file':source.name,'sha256':rows[0]['sha256'],
                    'observed_version':receipt['source']['requested_version'],'source_url':rows[0]['final_url']}))
                extract_ieee(inputs/'acquisition.json',work/'transcription')
                source=work/'transcription/thesaurus.json'
    if pipeline.get('extract'):
        extraction=pipeline['extract']
        if extraction.get('kind')!='ieee-pdf' or kind!='ieee':raise ValueError('Unsupported extraction adapter')
        from kb_sources.ieee_thesaurus import extract_ieee
        extract_ieee((base/extraction['input']).resolve(),work/'extracted')
        source=work/'extracted/thesaurus.json'
    if source is None or not source.is_file():raise ValueError('Pipeline needs an existing input or acquisition')
    output=work/'projection';kwargs={}
    if previous and kind in {'ieee','eric','cognitive-atlas'}:
        identity=work/'identities';identity.mkdir()
        raw=Path(previous).read_bytes();atomic(identity/'vocabulary.ttl',raw)
        atomic(identity/'manifest.json',encode({'files':{'vocabulary.ttl':hashlib.sha256(raw).hexdigest()}}))
        kwargs['identity_file']=identity/'vocabulary.ttl'
    module=importlib.import_module('kb_vocab.'+kind.replace('-','_'))
    function='import_cognitive' if kind=='cognitive-atlas' else 'import_'+kind
    getattr(module,function)(source,output,**kwargs)
    return output/'vocabulary.ttl',declaration
