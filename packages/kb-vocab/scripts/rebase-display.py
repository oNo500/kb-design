"""Carry existing display labels to a reduced base without creating translations."""
import argparse
import hashlib
import json
from pathlib import Path
from rdflib import Graph,URIRef,Literal,SKOS
from rdflib.compare import isomorphic
from kb_vocab.publication import _verify


def sha(raw):return hashlib.sha256(raw).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous',required=True,type=Path)
    parser.add_argument('--base',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();previous=args.previous.resolve();base=args.base.resolve();out=args.output
    if out.exists():raise ValueError('Output must be new')
    _verify(base)
    manifest_raw=(previous/'manifest.json').read_bytes();manifest=json.loads(manifest_raw)
    if manifest.get('kind')!='bilingual-display':raise ValueError('Expected bilingual display')
    for name,digest in manifest['files'].items():
        if Path(name).name!=name or sha((previous/name).read_bytes())!=digest:raise ValueError('Previous display hash mismatch')
    metadata=json.loads((previous/'label-provenance.json').read_bytes())
    oldpath=Path(metadata['base'])/'vocabulary.ttl';oldraw=oldpath.read_bytes()
    if sha(oldraw)!=metadata['base_sha256']:raise ValueError('Previous translation base changed')
    old=Graph().parse(data=oldraw,format='turtle');raw=(base/'vocabulary.ttl').read_bytes();new=Graph().parse(data=raw,format='turtle')
    delta=Graph();kept=[];removed=[];subjects=set(new.subjects())
    olddelta=Graph().parse(previous/'translations.zh.ttl')
    for row in metadata['labels']:
        uri=URIRef(row['uri'])
        if uri not in subjects:removed.append(row);continue
        # Existing translations cannot silently follow changed English names.
        if {v for v in old.objects(uri,SKOS.prefLabel) if v.language=='en'}!={v for v in new.objects(uri,SKOS.prefLabel) if v.language=='en'}:
            raise ValueError('English label changed; cannot reuse translation: '+str(uri))
        triple=(uri,URIRef(row['property']),Literal(row['label'],lang=row['language']))
        if triple not in olddelta:raise ValueError('Label evidence does not match previous translation')
        delta.add(triple);kept.append(row)
    merged=new+delta
    out.mkdir(parents=True)
    delta.serialize(out/'translations.zh.ttl',format='turtle');merged.serialize(out/'vocabulary.multilingual.ttl',format='turtle')
    assert isomorphic(merged,Graph().parse(out/'vocabulary.multilingual.ttl'))
    metadata.update(base=str(base),base_sha256=sha(raw),vocabulary_sha256=sha((out/'vocabulary.multilingual.ttl').read_bytes()),labels=kept,
                    rebase={'previous_display':str(previous),'previous_manifest_sha256':sha(manifest_raw),'original_translation_base_sha256':sha(oldraw),'removed_labels':len(removed),'rule':'Keep existing labels only for surviving URIs with unchanged English preferred labels; no new translations.'})
    (out/'label-provenance.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    (out/'report.json').write_text(json.dumps({'retained_labels':len(kept),'removed_labels':len(removed),'new_translations':0},indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'kind':'bilingual-display','base_sha256':sha(raw),'files':{p.name:sha(p.read_bytes()) for p in out.iterdir()}},indent=2)+'\n')
    print((out/'report.json').read_text())

if __name__=='__main__':main()
