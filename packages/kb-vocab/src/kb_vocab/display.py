"""Carry valid existing display translations forward; never invent new labels."""
import hashlib
import json
from pathlib import Path
from rdflib import Graph,URIRef,Literal,SKOS
from rdflib.compare import isomorphic
from .publication import _verify
from .edit_store import encode


def sha(raw):return hashlib.sha256(raw).hexdigest()

def rebase_display(previous,base,output):
    previous,base,output=Path(previous).resolve(),Path(base).resolve(),Path(output).resolve()
    if output.exists():raise ValueError('Display output must be new')
    _verify(base)
    manifest_raw=(previous/'manifest.json').read_bytes();manifest=json.loads(manifest_raw)
    if manifest.get('kind')!='bilingual-display':raise ValueError('Expected bilingual display')
    for name,digest in manifest['files'].items():
        if Path(name).name!=name or sha((previous/name).read_bytes())!=digest:raise ValueError('Previous display hash mismatch')
    metadata=json.loads((previous/'label-provenance.json').read_bytes())
    oldraw=(Path(metadata['base'])/'vocabulary.ttl').read_bytes()
    if sha(oldraw)!=metadata['base_sha256']:raise ValueError('Previous translation base changed')
    old=Graph().parse(data=oldraw,format='turtle');raw=(base/'vocabulary.ttl').read_bytes();new=Graph().parse(data=raw,format='turtle')
    delta=Graph();kept=[];omitted=[];subjects=set(new.subjects())
    olddelta=Graph().parse(previous/'translations.zh.ttl')
    for row in metadata['labels']:
        uri=URIRef(row['uri']);reason=None
        if uri not in subjects:reason='node_removed'
        elif {v for v in old.objects(uri,SKOS.prefLabel) if v.language=='en'}!={v for v in new.objects(uri,SKOS.prefLabel) if v.language=='en'}:reason='english_changed'
        elif any((v.language or '').lower().split('-')[0]=='zh' for v in new.objects(uri,SKOS.prefLabel)):reason='base_has_chinese'
        triple=(uri,URIRef(row['property']),Literal(row['label'],lang=row['language']))
        if triple not in olddelta:raise ValueError('Translation evidence does not match previous RDF')
        if reason:omitted.append({'uri':str(uri),'reason':reason});continue
        delta.add(triple);kept.append(row)
    needs_translation=[r for r in omitted if r['reason']=='english_changed']
    needs_translation.extend({'uri':str(node),'reason':'new_node'} for node in subjects-set(old.subjects()) if any(v.language=='en' for v in new.objects(node,SKOS.prefLabel)) and not any((v.language or '').lower().split('-')[0]=='zh' for v in new.objects(node,SKOS.prefLabel)))
    merged=new+delta;output.mkdir(parents=True)
    delta.serialize(output/'translations.zh.ttl',format='turtle');merged.serialize(output/'vocabulary.multilingual.ttl',format='turtle')
    if not isomorphic(merged,Graph().parse(output/'vocabulary.multilingual.ttl')):raise ValueError('Display round-trip changed RDF')
    base_evidence=json.loads((base/'label-provenance.json').read_bytes())
    metadata['local_records']=base_evidence.get('local_records',[])
    metadata.update(base=str(base),base_sha256=sha(raw),vocabulary_sha256=sha((output/'vocabulary.multilingual.ttl').read_bytes()),labels=kept,
        complete=bool(metadata.get('complete')) and not needs_translation,
        rebase={'previous_display':str(previous),'previous_manifest_sha256':sha(manifest_raw),'original_translation_base_sha256':sha(oldraw),'omitted':omitted})
    (output/'label-provenance.json').write_bytes(encode(metadata))
    report={'retained_labels':len(kept),'omitted_labels':len(omitted),'new_translations':0,'needs_translation':needs_translation}
    (output/'report.json').write_bytes(encode(report))
    (output/'manifest.json').write_bytes(encode({'kind':'bilingual-display','base_sha256':sha(raw),'files':{p.name:sha(p.read_bytes()) for p in output.iterdir()}}))
    return report
