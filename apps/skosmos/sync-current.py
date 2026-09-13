"""Synchronize one verified vocabulary build and its navigation, with a receipt."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from rdflib import Graph, SKOS
from rdflib.compare import isomorphic
from kb_vocab.publication import _verify

APP=Path(__file__).resolve().parent
ENDPOINT='http://127.0.0.1:9030/skosmos/data?graph=urn%3Akb-design%3Apreview%3Acurrent'


def sha(raw):return hashlib.sha256(raw).hexdigest()

def write(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name('.'+path.name+'.pending')
    temporary.write_bytes(raw);temporary.replace(path)

def encode(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()

def fetch_or_put(method,raw=None):
    request=Request(ENDPOINT,data=raw,method=method,headers={'Content-Type':'text/turtle','Accept':'text/turtle'})
    try:
        with urlopen(request,timeout=180) as response:return response.read()
    except HTTPError as exc:
        if method=='GET' and exc.code==404:return b''
        raise

def verify_remote(expected):
    actual=Graph().parse(data=fetch_or_put('GET'),format='turtle')
    if not isomorphic(expected,actual):raise ValueError('Database graph differs from expected preview')
    return len(actual)

def preview(raw):
    graph=Graph().parse(data=raw,format='turtle')
    for p,inverse in [(SKOS.broader,SKOS.narrower),(SKOS.narrower,SKOS.broader),
                      (SKOS.topConceptOf,SKOS.hasTopConcept),(SKOS.hasTopConcept,SKOS.topConceptOf)]:
        for s,o in list(graph.subject_objects(p)):graph.add((o,inverse,s))
    return graph

def navigation(raw):
    spec=importlib.util.spec_from_file_location('kb_navigation',APP/'build-navigation.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.build_navigation(Graph().parse(data=raw,format='turtle'))
    result['source_sha256']=sha(raw)
    return result

def publish(output,graph,nav,receipt):
    output=Path(output);navpath=output/'navigation/navigation.json';receiptpath=output/'sync-receipt.json'
    previous=fetch_or_put('GET')
    saved={p:p.read_bytes() if p.exists() else None for p in (navpath,receiptpath)}
    write(output/'sync-status.json',encode({'state':'running','source_sha256':receipt['source_sha256']}))
    try:
        fetch_or_put('PUT',graph.serialize(format='turtle').encode())
        triples=verify_remote(graph)
        navraw=encode(nav);write(navpath,navraw)
        if navpath.read_bytes()!=navraw:raise ValueError('Navigation changed during synchronization')
        complete={**receipt,'state':'complete','preview_triples':triples,'navigation_sha256':sha(navraw),
                  'verified_at':datetime.now(timezone.utc).isoformat(),'graph_isomorphic':True}
        write(receiptpath,encode(complete))
        write(output/'sync-status.json',encode({'state':'complete','source_sha256':receipt['source_sha256']}))
        return complete
    except Exception as failure:
        try:
            fetch_or_put('PUT',previous)
            for path,raw in saved.items():
                if raw is None:path.unlink(missing_ok=True)
                else:write(path,raw)
            verify_remote(Graph().parse(data=previous,format='turtle'))
            state='rolled_back'
        except Exception as recovery_failure:
            state='recovery_failed'
            write(output/'sync-status.json',encode({'state':state,'error':str(failure),'recovery_error':str(recovery_failure)}))
            raise RuntimeError('Synchronization failed and rollback could not be verified') from recovery_failure
        write(output/'sync-status.json',encode({'state':state,'error':str(failure)}))
        raise

def run(build,check=False):
    build=Path(build).resolve();_verify(build)
    raw=(build/'vocabulary.ttl').read_bytes()
    receipt={'build':str(build),'build_id':build.name,'build_manifest_sha256':sha((build/'manifest.json').read_bytes()),
             'source_sha256':sha(raw),'sync_code_sha256':sha(Path(__file__).read_bytes()),
             'navigation_code_sha256':sha((APP/'build-navigation.py').read_bytes()),
             'configuration_sha256':sha((APP/'config/skosmos.ttl').read_bytes()),'endpoint':ENDPOINT}
    graph=preview(raw)
    output=APP/'output';output.mkdir(exist_ok=True)
    lock=output/'.sync-lock'
    try:lock.mkdir()
    except FileExistsError:raise ValueError('Another sync is active; inspect a stale lock before retrying')
    try:
        if check:
            saved=json.loads((output/'sync-receipt.json').read_bytes())
            status=json.loads((output/'sync-status.json').read_bytes())
            if saved.get('state')!='complete' or status.get('state')!='complete':raise ValueError('Synchronization is not complete')
            if any(saved.get(k)!=v for k,v in receipt.items()):raise ValueError('Synchronization receipt does not match requested build or application code')
            navraw=(output/'navigation/navigation.json').read_bytes()
            if sha(navraw)!=saved['navigation_sha256']:raise ValueError('Navigation hash mismatch')
            if json.loads(navraw).get('source_sha256')!=sha(raw):raise ValueError('Navigation source mismatch')
            verify_remote(graph)
            return dict(saved,live_verified=True)
        return publish(output,graph,navigation(raw),receipt)
    finally:lock.rmdir()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',type=Path,default=APP/'../../output/vocabulary/current')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:print(json.dumps(run(args.build,args.check),ensure_ascii=False,indent=2))
    except Exception as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr);raise SystemExit(1)
