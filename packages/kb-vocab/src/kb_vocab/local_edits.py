"""Persistent, three-way local RDF edits. Source graphs are never modified."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
from uuid import uuid4
from rdflib import Graph,URIRef,Literal,BNode,RDF,SKOS
from rdflib.util import from_n3
from rdflib.namespace import PROV
from .normalization import INVERSES

NS=Graph().namespace_manager
RELATIONS=set(INVERSES)|{SKOS.member,SKOS.exactMatch,SKOS.closeMatch,SKOS.broadMatch,SKOS.narrowMatch,SKOS.relatedMatch}
PROTECTED={RDF.type,SKOS.inScheme,SKOS.topConceptOf,SKOS.hasTopConcept}


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def empty():return {'schema_version':1,'revision':0,'patches':[],'history':[]}

def iri(value):
    if not isinstance(value,str):raise ValueError('Expected an IRI or registered RDF prefix')
    if value.startswith('<') and value.endswith('>'):value=value[1:-1]
    prefix=value.split(':',1)[0]
    if prefix in dict(NS.namespaces()):value=str(NS.expand_curie(value))
    if ':' not in value or any(c.isspace() or c in '<>"{}|^`\\' for c in value):raise ValueError('Invalid IRI')
    return URIRef(value)

def term(value):
    if not isinstance(value,str):raise ValueError('RDF values must use N3 text, e.g. <urn:a> or "Name"@en')
    result=from_n3(value,nsm=NS)
    if not isinstance(result,(URIRef,Literal)):raise ValueError('Local edits require named IRIs or RDF literals; blank nodes are not stable edit targets')
    if isinstance(result,Literal) and result.language and result.language.lower().split('-')[0] not in {'en','zh'}:
        raise ValueError('Only English and Chinese literal edits are supported')
    return result

def _values(graph,s,p,language):
    values={o for o in graph.objects(s,p) if language is None or isinstance(o,Literal) and (o.language or '').lower()==language}
    if any(isinstance(o,BNode) for o in values):raise ValueError('Edit the named description resource; blank-node fields are read-only')
    return sorted(o.n3() for o in values)

def _node(graph,s):
    return sorted((str(p),o.n3()) for p,o in graph.predicate_objects(s) if p!=PROV.wasDerivedFrom)

def _event(doc,action,reason,ids):
    if not isinstance(reason,str) or not reason.strip():raise ValueError('A reason is required')
    doc['revision']+=1
    doc['history'].append({'revision':doc['revision'],'action':action,'reason':reason,'patches':ids,'at':datetime.now(timezone.utc).isoformat()})

def validate(doc):
    if not isinstance(doc,dict) or doc.get('schema_version')!=1 or not isinstance(doc.get('revision'),int) or not isinstance(doc.get('patches'),list) or not isinstance(doc.get('history'),list):
        raise ValueError('Invalid local edit document')
    ids=set()
    for patch in doc['patches']:
        if patch.get('id') in ids or not isinstance(patch.get('id'),str):raise ValueError('Duplicate or missing edit ID')
        ids.add(patch['id']);iri(patch['subject'])
        if patch['op'] not in {'set','add','remove','create','delete'}:raise ValueError('Unknown local operation')
        if patch['op'] in {'set','add','remove'}:
            if iri(patch['predicate']) in PROTECTED:raise ValueError('Identity/type/scheme fields are managed by create/delete and generation')
            for v in patch['values']+patch['baseline']:
                value=term(v)
                if iri(patch['predicate']) in {SKOS.prefLabel,SKOS.altLabel,SKOS.hiddenLabel} and not isinstance(value,Literal):raise ValueError('SKOS names require literal values')
        if patch['op']=='create':
            if iri(patch['type']) not in {SKOS.Concept,SKOS.Collection}:raise ValueError('Local creation supports Concepts and Collections')
            for p,values in patch['fields'].items():
                if iri(p) in PROTECTED:raise ValueError('Managed field in local creation')
                for v in values:
                    value=term(v)
                    if iri(p) in {SKOS.prefLabel,SKOS.altLabel,SKOS.hiddenLabel} and not isinstance(value,Literal):raise ValueError('SKOS names require literal values')
    return doc

def prepare(document,operations,upstream,visible,reason):
    doc=deepcopy(validate(document));ids=[];view,existing=apply(upstream,doc)
    if existing['conflicts']:raise ValueError('Resolve existing local conflicts before adding edits')
    if not isinstance(operations,list) or not operations:raise ValueError('Expected a nonempty operations list')
    for operation in operations:
        if not isinstance(operation,dict) or not {'op','subject'}<=set(operation):raise ValueError('Each operation needs op and subject')
        row=deepcopy(operation);s=iri(row['subject']);row['subject']=str(s);op=row['op']
        if op in {'set','add','remove'} and not isinstance(row.get('values'),list):raise ValueError('Property edits require a values list')
        if op=='create' and (not isinstance(row.get('fields'),dict) or any(not isinstance(v,list) for v in row['fields'].values())):raise ValueError('Creation fields must map properties to value lists')
        if op not in {'set','add','remove','create','delete'}:raise ValueError('Unknown local operation')
        if op!='create' and not any(view.triples((s,None,None))):raise ValueError('Local target is absent: '+str(s))
        if (s,RDF.type,SKOS.ConceptScheme) in view:raise ValueError('Edit the vocabulary configuration for Scheme changes')
        if op=='create':
            if any(view.triples((s,None,None))):raise ValueError('Local identity already exists')
            row['type']=str(iri(row['type']));row['fields']={str(iri(p)):sorted({term(v).n3() for v in vs}) for p,vs in row['fields'].items()}
            row['baseline']=[]
        elif op=='delete':
            row['baseline']=_node(upstream,s)
            doc['patches']=[p for p in doc['patches'] if p['subject']!=str(s) or p['op']=='remove']
        else:
            p=iri(row['predicate']);row['predicate']=str(p)
            language=row.get('language');language=language.lower() if language else None;row['language']=language
            row['values']=sorted({term(v).n3() for v in row['values']})
            if language and any(not isinstance(term(v),Literal) or (term(v).language or '').lower()!=language for v in row['values']):raise ValueError('Values must match the selected language')
            row['baseline']=_values(upstream,s,p,language)
            existing=[p for p in doc['patches'] if p['subject']==str(s) and p.get('predicate')==str(iri(row['predicate'])) and p.get('language')==language]
            if existing and (op=='set' or any(patch['op']=='set' for patch in existing)):
                current={term(v) for v in _values(view,s,p,language)};values={term(v) for v in row['values']}
                row['values']=sorted(v.n3() for v in (values if op=='set' else current|values if op=='add' else current-values))
                row['op']='set'
                doc['patches']=[patch for patch in doc['patches'] if patch not in existing]
            elif existing:
                # Retain per-value intent. The latest add/remove replaces only
                # overlapping earlier intentions, not ownership of the whole slot.
                touched={term(v) for v in row['values']}
                for patch in existing:
                    patch['values']=[v for v in patch['values'] if term(v) not in touched]
                doc['patches']=[patch for patch in doc['patches'] if patch not in existing or patch['values']]
        value_fields=row.get('fields',{}) if op=='create' else {row.get('predicate',''):row.get('values',[])}
        row['local_targets']=sorted({str(term(v)) for values in value_fields.values() for v in values if isinstance(term(v),URIRef) and any(view.triples((term(v),RDF.type,None)))})
        row['id']=str(uuid4());ids.append(row['id']);doc['patches'].append(row)
        validate(doc)
        view,report=apply(upstream,doc)
        if report['conflicts']:raise ValueError('Local edit conflicts: '+json.dumps(report['conflicts'],ensure_ascii=False))
    _event(doc,'apply',reason,ids)
    return doc


def apply(upstream,document):
    doc=validate(document);graph=upstream+Graph();conflicts=[];deleted=set();created=set();expectations=[]
    def conflict(row,code,incoming=None,**extra):
        conflicts.append({'id':row['id'],'patch_sha256':digest(row),'subject':row['subject'],'code':code,'incoming':incoming,**extra})
    def values_of(g,s,p,language):return {term(v) for v in _values(g,s,p,language)}
    rows=sorted(doc['patches'],key=lambda p:0 if p['op']=='create' else 1)
    for row in rows:
        s=iri(row['subject']);op=row['op']
        if op=='delete':continue
        if op=='create':
            if any(upstream.triples((s,None,None))):conflict(row,'identity_collision');continue
            graph.add((s,RDF.type,iri(row['type'])));created.add(s)
            for encoded_p,values in row['fields'].items():
                p=iri(encoded_p)
                for value in values:
                    o=term(value);graph.add((s,p,o))
                    if p in INVERSES:graph.add((o,INVERSES[p],s))
        else:
            if op!='remove' and not any(graph.triples((s,None,None))):conflict(row,'target_missing');continue
            p=iri(row['predicate']);language=row.get('language')
            baseline={term(v) for v in row['baseline']};incoming=values_of(upstream,s,p,language);values={term(v) for v in row['values']}
            current=values_of(graph,s,p,language)
            if op=='set':
                changed=incoming!=baseline and incoming!=values;desired=values
            else:
                desired=current|values if op=='add' else current-values
                changed=any((v in incoming)!=(v in baseline) and (v in incoming)!=(op=='add') for v in values)
            if changed:conflict(row,'field_changed',sorted(v.n3() for v in incoming),predicate=str(p));continue
            expectations.append((row,values))
            for value in current-desired:
                graph.remove((s,p,value))
                if p in INVERSES:graph.remove((value,INVERSES[p],s))
            for value in desired-current:
                graph.add((s,p,value))
                if p in INVERSES:graph.add((value,INVERSES[p],s))
    # Capture effective local references before deletion. Explicit field edits
    # can cancel creation-time relations; deleting their target cannot silently
    # cancel a still-effective local reference.
    references=[]
    for row in rows:
        fields=row['fields'] if row['op']=='create' else {row['predicate']:row['values']} if row['op'] in {'set','add'} else {}
        s=iri(row['subject'])
        for predicate,values in fields.items():
            p=iri(predicate)
            for value in values:
                o=term(value)
                if isinstance(o,URIRef) and (p in RELATIONS or str(o) in row.get('local_targets',[])) and (s,p,o) in graph:
                    references.append((row,s,o))
    for row in rows:
        if row['op']!='delete':continue
        s=iri(row['subject']);incoming=_node(upstream,s)
        if incoming and [list(t) for t in incoming]!=[list(t) for t in row['baseline']]:conflict(row,'node_changed',incoming);continue
        deleted.add(s);created.discard(s)
        graph.remove((s,None,None));graph.remove((None,None,s))
    for row,s,o in references:
        if s not in deleted and not any(graph.triples((o,RDF.type,None))):conflict(row,'relation_target_missing',target=str(o))
    for row,values in expectations:
        s=iri(row['subject'])
        if s in deleted:continue
        actual=values_of(graph,s,iri(row['predicate']),row.get('language'))
        agrees=(actual==values if row['op']=='set' else values<=actual if row['op']=='add' else not actual&values)
        if not agrees:conflict(row,'overlapping_local_edits')
    added=[tuple(x.n3() for x in t) for t in graph if t not in upstream]
    removed=[tuple(x.n3() for x in t) for t in upstream if t not in graph]
    return graph,{'added':sorted(added),'removed':sorted(removed),'revision':doc['revision'],'conflicts':conflicts,
                  'deleted_nodes':sorted(map(str,deleted)),'created_nodes':sorted(map(str,created)),
                  'patches':len(rows),'verified':not conflicts}


def undo(document,patch_id,reason):
    doc=deepcopy(validate(document));old=len(doc['patches'])
    doc['patches']=[p for p in doc['patches'] if p['id']!=patch_id]
    if len(doc['patches'])==old:raise ValueError('Unknown edit ID')
    _event(doc,'undo',reason,[patch_id]);return doc

def resolve(document,conflict,choice,reason):
    doc=deepcopy(validate(document));row=next((p for p in doc['patches'] if p['id']==conflict['id']),None)
    if row is None or digest(row)!=conflict['patch_sha256']:raise ValueError('Conflict is stale; rerun synchronization')
    if choice=='source':return undo(doc,row['id'],reason)
    if choice!='local' or conflict['code'] not in {'field_changed','node_changed'}:raise ValueError('Missing identities or targets require explicit editing or discarding the patch')
    row['baseline']=conflict['incoming'];_event(doc,'resolve-local',reason,[row['id']]);return doc


class EditConflict(ValueError):
    def __init__(self,report,upstream):
        super().__init__("Local edits conflict with incoming data; inspect conflicts and resolve before publishing")
        self.report=report
        self.upstream=upstream
