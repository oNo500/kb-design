"""Generate a complete source-preserving knowledge model from pinned configuration.

Source statements are retained. Domain membership is a separate, configured
assertion; it neither merges concepts nor changes their hierarchy.
"""
from collections import Counter, defaultdict
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import shutil
import tempfile

from rdflib import BNode, DCTERMS, Graph, Literal, Namespace, RDF, SKOS, URIRef
from rdflib.compare import isomorphic
from .review_catalog import read_catalog, index_concepts
from .validation import validate_graph
from .normalization import normalize_sources
from .shacl_validation import validate_profile
from .accounting import verify_normalization
from .replay import configuration_origin, write_replay_inputs

PROV = Namespace("http://www.w3.org/ns/prov#")


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _json(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n'


def _closure(graph,anchor):
    seen=set();pending=[anchor]
    while pending:
        node=pending.pop()
        if node in seen:continue
        seen.add(node)
        if (node,RDF.type,SKOS.Collection) in graph:
            pending.extend(graph.objects(node,SKOS.member))
        if (node,RDF.type,SKOS.Concept) in graph:
            pending.extend(graph.subjects(SKOS.broader,node))
            pending.extend(graph.objects(node,SKOS.narrower))
    return seen


def _domain_graph(base,members,groups,overlay):
    """Keep member assertions and readable boundary references, without adopting boundary members."""
    graph=Graph();graph.bind('skos',SKOS);graph.bind('dcterms',DCTERMS)
    for node in members|groups:
        for triple in base.triples((node,None,None)):graph.add(triple)
    for triple in overlay:graph.add(triple)
    pending=[o for _,_,o in graph if isinstance(o,BNode)];seen=set()
    while pending:
        node=pending.pop()
        if node in seen:continue
        seen.add(node)
        for triple in base.triples((node,None,None)):
            graph.add(triple)
            if isinstance(triple[2],BNode):pending.append(triple[2])
    # Nonmember endpoints stay references. Copy identity and description, not
    # another layer of their hierarchy or any invented domain membership.
    objects={o for _,_,o in graph if isinstance(o,URIRef)}
    fields=(RDF.type,SKOS.prefLabel,SKOS.altLabel,SKOS.hiddenLabel,SKOS.definition,SKOS.scopeNote,DCTERMS.description,SKOS.inScheme)
    for node in objects-members-groups:
        for predicate in fields:
            for value in base.objects(node,predicate):graph.add((node,predicate,value))
    # Explicitly typed source schemes referenced by members remain queryable.
    for node in set(graph.objects(None,SKOS.inScheme)):
        for predicate in (RDF.type,SKOS.prefLabel,DCTERMS.title,DCTERMS.description,SKOS.scopeNote):
            for value in base.objects(node,predicate):graph.add((node,predicate,value))
    return graph


def _names(value, languages, label):
    if not isinstance(value,dict) or not value:
        raise ValueError(f'{label} requires language-tagged text')
    for language,text in value.items():
        if (not isinstance(language,str) or not re.fullmatch('[A-Za-z]+(?:-[A-Za-z0-9]+)*',language)
                or language.lower().split('-')[0] not in languages or not isinstance(text,str) or not text.strip()):
            raise ValueError(f'{label} must use nonempty English or Chinese text')
    if len({lang.lower() for lang in value})!=len(value):raise ValueError('Duplicate language tags')


def _iri(value):
    if not isinstance(value,str) or not re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',value) or any(c.isspace() for c in value):
        raise ValueError('Expected an absolute IRI')
    return URIRef(value)


def _read_config(path):
    raw=path.read_bytes();config=json.loads(raw)
    if not isinstance(config,dict) or config.get('schema_version')!=2:
        raise ValueError('Expected organization schema_version 2 for the single-vocabulary profile')
    allowed={'schema_version','catalog','sources','domains','vocabulary','languages','shapes'}
    if set(config)-{'replay_origin'}!=allowed:raise ValueError('Missing or unknown organization configuration fields')
    languages=config['languages']
    if not isinstance(languages,list) or len(languages)!=2 or set(languages)!={'en','zh'}:
        raise ValueError('The v3 output language policy is en and zh')
    if not isinstance(config['catalog'],str) or not isinstance(config['shapes'],str) or not isinstance(config['sources'],dict):
        raise ValueError('Configuration requires catalog, shapes and pinned sources')
    vocab=config['vocabulary']
    if not isinstance(vocab,dict) or set(vocab)!={'uri','label','scope','top_concepts'}:raise ValueError('Invalid vocabulary configuration')
    _iri(vocab['uri']);_names(vocab['label'],languages,'Vocabulary name');_names(vocab['scope'],languages,'Vocabulary scope')
    if not isinstance(vocab['top_concepts'],list):raise ValueError('top_concepts must be an explicit list')
    domains=config['domains']
    if not isinstance(domains,list) or not domains:raise ValueError('Configuration needs domain groups')
    ids=set();uris={vocab['uri']}
    for domain in domains:
        if not isinstance(domain,dict) or set(domain)-{'id','uri','legacy_scheme','label','whole_sources','branches'}:
            raise ValueError('Invalid or obsolete domain fields')
        ident=domain.get('id','')
        if not isinstance(ident,str) or not re.fullmatch('[a-z][a-z0-9-]*',ident) or ident in ids:
            raise ValueError('Domain IDs must be unique lowercase slugs')
        ids.add(ident);uri=str(_iri(domain.get('uri')))
        if uri in uris:raise ValueError('Vocabulary and group identities must be distinct')
        if domain.get('legacy_scheme')==uri:raise ValueError('Do not retype an old Scheme IRI as a Collection')
        uris.add(uri);_names(domain.get('label'),languages,'Group name')
        if not isinstance(domain.get('whole_sources',[]),list) or not isinstance(domain.get('branches',[]),list):
            raise ValueError('Domain source and branch rules must be lists')
    return raw,config


def _write_json(path,value):
    path.write_text(_json(value),encoding='utf-8')


def build_system(config_file,output,previous_file=None):
    config_file=Path(config_file).absolute();output=Path(output).absolute()
    if output.exists():raise ValueError(f'Output already exists: {output}')
    if previous_file is None and (config_file.parent/'previous.ttl').exists():previous_file=config_file.parent/'previous.ttl'
    previous_raw=Path(previous_file).read_bytes() if previous_file else None
    config_raw,config=_read_config(config_file);config_hash=_sha(config_raw)
    origin_raw=configuration_origin(config_file,config_raw,config);origin_hash=_sha(origin_raw)
    catalog=(config_file.parent/config['catalog']).absolute();catalog_raw=catalog.read_bytes()
    shapes_path=(config_file.parent/config['shapes']).absolute();shapes_raw=shapes_path.read_bytes()
    sources=read_catalog(catalog)
    if set(sources)!=set(config['sources']):raise ValueError('Catalog must contain exactly the pinned source set')
    source_raw={};raw_graph=Graph()
    for name,source in sources.items():
        if source['sha256']!=config['sources'][name]:raise ValueError(f'Source hash differs from pinned configuration: {name}')
        path=Path(source['path']);raw=path.read_bytes()
        if _sha(raw)!=source['sha256']:raise ValueError(f'Source changed during loading: {name}')
        if (path.parent/'manifest.json').exists() and output.resolve().is_relative_to(path.resolve().parent):
            raise ValueError('Build output must be outside source directories')
        source_raw[name]=raw
        for triple in source['graph']:raw_graph.add(triple)
    index=index_concepts(sources);source_baseline=validate_graph(raw_graph)
    base,changes,normalization=normalize_sources(sources,config['languages'])
    if not normalization['source_accounting_complete'] or not normalization['source_concepts_preserved']:
        raise ValueError('Normalization failed complete source accounting')
    accounting=verify_normalization(sources,base,changes,config['languages'])
    scheme=_iri(config['vocabulary']['uri']);generated={scheme}
    if any(raw_graph.triples((scheme,None,None))):raise ValueError('Vocabulary identity collides with a source')
    scheme_graph=Graph();scheme_graph.bind('skos',SKOS)
    scheme_graph.add((scheme,RDF.type,SKOS.ConceptScheme))
    for language,text in config['vocabulary']['label'].items():scheme_graph.add((scheme,SKOS.prefLabel,Literal(text,lang=language)))
    for language,text in config['vocabulary']['scope'].items():scheme_graph.add((scheme,SKOS.scopeNote,Literal(text,lang=language)))
    tops={_iri(value) for value in config['vocabulary']['top_concepts']}
    if not tops<={URIRef(uri) for uri in index}:raise ValueError('A configured top concept is not in the pinned sources')
    for node in tops:
        scheme_graph.add((scheme,SKOS.hasTopConcept,node));scheme_graph.add((node,SKOS.topConceptOf,scheme))
    organization=scheme_graph+Graph()
    for node in set(base.subjects(RDF.type,SKOS.Concept))|set(base.subjects(RDF.type,SKOS.Collection)):
        organization.add((node,SKOS.inScheme,scheme))
    memberships=defaultdict(set);derivations=defaultdict(list);domain_data=[];migration=[]
    for domain in config['domains']:
        ident=domain['id'];group=_iri(domain['uri']);generated.add(group)
        if any(raw_graph.triples((group,None,None))):raise ValueError('Group identity collides with a source')
        members=set();collections=set();references=[]
        for name in domain.get('whole_sources',[]):
            if name not in sources:raise ValueError(f'Unknown whole source: {name}')
            g=sources[name]['graph'];selected=set(g.subjects(RDF.type,SKOS.Concept))
            members|=selected;collections|=set(g.subjects(RDF.type,SKOS.Collection))
            rule={'source':name,'mode':'whole_source'}
            for node in selected:derivations[(str(node),ident)].append(rule)
        for branch in domain.get('branches',[]):
            if not isinstance(branch,dict) or set(branch)!={'source','uri','mode'} or branch['source'] not in sources:
                raise ValueError('Invalid branch configuration')
            if branch['mode'] not in {'inherit','reference_only'}:raise ValueError('Unknown inheritance mode')
            name=branch['source'];g=sources[name]['graph'];anchor=_iri(branch['uri'])
            if not ((anchor,RDF.type,SKOS.Concept) in g or (anchor,RDF.type,SKOS.Collection) in g):
                raise ValueError(f'Branch anchor is not a source Concept or Collection: {anchor}')
            if branch['mode']=='reference_only':references.append(branch);continue
            reached=_closure(g,anchor);selected={n for n in reached if (n,RDF.type,SKOS.Concept) in g}
            members|=selected;collections|={n for n in reached if (n,RDF.type,SKOS.Collection) in g}
            rule={'source':name,'mode':'branch','anchor':str(anchor)}
            for node in selected:derivations[(str(node),ident)].append(rule)
        overlay=scheme_graph+Graph();overlay.add((group,RDF.type,SKOS.Collection));overlay.add((group,SKOS.inScheme,scheme))
        for language,text in domain['label'].items():overlay.add((group,SKOS.prefLabel,Literal(text,lang=language)))
        overlay.add((group,SKOS.scopeNote,Literal('本分组的成员由所引用的来源继承规则确定；仅作参考的分支不产生成员，分组不表示该领域已完整覆盖。',lang='zh')))
        overlay.add((group,SKOS.scopeNote,Literal('Membership follows the referenced source inheritance rules. Reference-only branches do not add members; complete domain coverage is not asserted.',lang='en')))
        overlay.add((group,PROV.wasDerivedFrom,URIRef('urn:sha256:'+origin_hash+'#domain/'+ident)))
        for node in members:
            memberships[str(node)].add(ident);overlay.add((group,SKOS.member,node))
        for triple in overlay:organization.add(triple)
        if domain.get('legacy_scheme'):
            migration.append({'old_scheme':domain['legacy_scheme'],'new_collection':str(group),'reason':'domain_scheme_restructured_as_group','concept_identities_changed':False})
        domain_data.append({'id':ident,'uri':str(group),'label':domain['label'],'members':members,'collections':collections,'overlay':overlay,'references':references})
    full=base+organization
    expected={URIRef(uri) for uri in index}
    if set(full.subjects(RDF.type,SKOS.Concept))!=expected:raise ValueError('Source concept identity set changed')
    if set(full.subjects(RDF.type,SKOS.ConceptScheme))!={scheme}:raise ValueError('Expected exactly one self vocabulary')
    for node in expected:
        if set(full.objects(node,SKOS.inScheme))!={scheme}:raise ValueError('Concept lacks the unique self vocabulary')
    if any(isinstance(value,Literal) and value.language and value.language.lower().split('-')[0] not in {'en','zh'} for _,_,value in full):
        raise ValueError('Unsupported language leaked into output')
    validation=validate_graph(full)
    if validation['errors']:raise ValueError('Normalized graph has errors: '+_json(validation['errors'][:5]))
    profile=validate_profile(full,shapes_path,generated_nodes=generated)
    if not profile['conforms'] or profile['violations']:
        raise ValueError('SHACL profile rejected normalized data: '+_json(profile['violations'][:8]))
    from .version_diff import compare_graphs
    previous_graph=Graph().parse(data=previous_raw,format='turtle',publicID=Path(previous_file).resolve().as_uri()) if previous_raw is not None else Graph()
    difference=compare_graphs(previous_graph,full)
    difference['baseline']={'sha256':_sha(previous_raw),'path':str(Path(previous_file).resolve())} if previous_raw is not None else None
    if previous_raw is not None and difference['concepts']['removed']:
        raise ValueError('Cross-version identity loss blocks automatic publication: '+str(len(difference['concepts']['removed']))+' prior concepts missing; inspect with kb-vocab diff')
    coverage=[{'uri':uri,'source':item['source'],'vocabulary':str(scheme),'domains':sorted(memberships[uri]),
               'status':'grouped' if memberships[uri] else 'ungrouped',
               'rules':{d:derivations[(uri,d)] for d in sorted(memberships[uri])}}
              for uri,item in sorted(index.items())]
    ungrouped={URIRef(row['uri']) for row in coverage if not row['domains']}
    labels=defaultdict(set)
    for node in expected:
        for value in full.objects(node,SKOS.prefLabel):labels[((value.language or '').lower(),str(value).casefold())].add(str(node))
    ambiguities=[{'language':language,'normalized_label':label,'concepts':sorted(nodes)} for (language,label),nodes in sorted(labels.items()) if len(nodes)>1]
    summaries=[{'id':d['id'],'collection':d['uri'],'label':d['label'],'members':len(d['members']),
                'source_collections':len(d['collections']),'reference_only':d['references']} for d in domain_data]
    report={'specification_version':3,'source_concepts':len(index),'source_triples':len(raw_graph),'output_triples':len(full),
            'self_vocabularies':1,'vocabulary':str(scheme),'domain_groups':len(domain_data),
            'assigned_concepts':len(index)-len(ungrouped),'unassigned_concepts':len(ungrouped),
            'domains':summaries,'source_statements_preserved':all(t in full for t in raw_graph),
            'source_copies_preserved':True,'source_concepts_preserved':True,'source_accounting_complete':accounting['verified'],
            'languages':config['languages'],'filtered_languages':normalization['filtered_languages'],
            'introduced_validation_errors':[],'source_validation_errors':len(source_baseline['errors']),
            'validation_valid':True,'shacl_conforms':True,'shacl_warnings':len(profile['warnings']),
            'ambiguous_label_groups':len(ambiguities),
            'scope':'Single self vocabulary with domain Collections. Full source concepts retained; changed/filtered source statements accounted separately. No invented history, semantic merge or full-domain completeness claim.'}
    output.parent.mkdir(parents=True,exist_ok=True);stage=Path(tempfile.mkdtemp(prefix='.system-',dir=output.parent))
    try:
        (stage/'sources').mkdir();(stage/'domains').mkdir();(stage/'inputs').mkdir()
        for name,raw in source_raw.items():(stage/'sources'/(_sha(name.encode())[:12]+'.ttl')).write_bytes(raw)
        full.serialize(stage/'vocabulary.ttl',format='turtle');organization.serialize(stage/'organization.ttl',format='turtle')
        domain_validation={}
        for domain in domain_data:
            view=_domain_graph(full,domain['members'],domain['collections'],domain['overlay'])
            checked=validate_graph(view)
            if checked['errors']:raise ValueError('Domain view has structural errors: '+_json(checked['errors'][:5]))
            domain_validation[domain['id']]=checked
            view.serialize(stage/'domains'/(domain['id']+'.ttl'),format='turtle')
        leftover=_domain_graph(full,ungrouped,set(),scheme_graph)
        checked=validate_graph(leftover)
        if checked['errors']:raise ValueError('Ungrouped view has errors: '+_json(checked['errors'][:5]))
        leftover.serialize(stage/'unassigned.ttl',format='turtle')
        replay=write_replay_inputs(stage,config_raw,catalog_raw,shapes_raw,sources,origin_raw)
        _write_json(stage/'accounting.json',accounting)
        _write_json(stage/'version-diff.json',difference)
        if previous_raw is not None:(stage/'inputs/previous.ttl').write_bytes(previous_raw)
        from .environment import archive_environment, tool_version
        recovery=archive_environment(stage)
        _write_json(stage/'coverage.json',coverage);_write_json(stage/'report.json',report)
        _write_json(stage/'normalization.json',normalization);_write_json(stage/'migration.json',migration)
        with (stage/'transformation-ledger.jsonl').open('w',encoding='utf-8') as stream:
            for change in changes:stream.write(json.dumps(change,ensure_ascii=False,sort_keys=True)+'\n')
        profile['report_graph'].serialize(stage/'shacl-report.ttl',format='turtle')
        profile_json={key:value for key,value in profile.items() if key!='report_graph'}
        _write_json(stage/'validation.json',{'source_baseline':source_baseline,'output':validation,'introduced_errors':[],
                                           'shacl':profile_json,'domains':domain_validation,'unassigned':checked})
        _write_json(stage/'warnings.json',{'shacl':profile['warnings'],'graph':validation['warnings'],'same_label_groups':ambiguities})
        source_manifest={name:{'path':s['path'],'base':s['base'],'sha256':s['sha256'],'copy':'sources/'+_sha(name.encode())[:12]+'.ttl'} for name,s in sources.items()}
        _write_json(stage/'provenance.json',{'sources':source_manifest,'organization_rules':'inputs/original-config.json','replay':replay,'statement_accounting':'accounting.json',
                    'concept_accounting':'coverage.json','source_transformations':'transformation-ledger.jsonl',
                    'statement_evidence':'Unchanged source statements are identified by source graph + subject/predicate/object. Changed and derived statements have explicit ledger entries.'})
        restored=Graph().parse(stage/'vocabulary.ttl',format='turtle')
        if not isomorphic(full,restored):raise ValueError('Turtle round trip changed the graph')
        rows=['| 领域分组 | 成员数 | 数据 |','|---|---:|---|']
        for domain in summaries:
            title=domain['label'].get('zh',domain['label'].get('en',domain['id']))
            rows.append(f'| {title} | {domain["members"]:,} | [Turtle](domains/{domain["id"]}.ttl) |')
        (stage/'index.md').write_text('# 词表构建\n\n'
            f'一份自有词表，{len(domain_data)} 个领域分组，{len(index):,} 个来源概念。全部概念属于自有词表；{len(ungrouped):,} 个概念尚未分组。\n\n'
            '- [完整词表](vocabulary.ttl)\n- [组织声明](organization.ttl)\n- [未分组数据](unassigned.ttl)\n'
            '- [逐概念对账](coverage.json)\n- [来源对应](provenance.json)\n- [字段转换记录](transformation-ledger.jsonl)\n'
            '- [语言与转换统计](normalization.json)\n- [结构迁移](migration.json)\n- [自动校验](validation.json)\n- [警告](warnings.json)\n\n'
            +'\n'.join(rows)+'\n\n领域数量按 Collection 的 member 统计，分图中的外部引用上下文不自动成为本组成员；多个分组可以共享概念。\n\n'
            f'SHACL 无阻断错误，保留 {len(profile["warnings"])} 项来源缺项或兼容提示；同名标签提示 {len(ambiguities)} 组，不作自动合并或全量人工审查。\n\n'
            '生成文字只保留中英文及其语言变体；未标语言的原值保留。六份来源字节副本完整保留，主图过滤和结构调整逐项记账，不再宣称主图包含全部原始三元组。\n'
            '没有依据的历史、停用、替代及映射值不生成。数据生成不证明领域知识覆盖完整，也不自动切换旧 YAML 消费者。\n',encoding='utf-8')
        for name,raw in source_raw.items():
            if (stage/'sources'/(_sha(name.encode())[:12]+'.ttl')).read_bytes()!=raw:raise ValueError('Source copy changed')
        tool_files={path.name:_sha(path.read_bytes()) for path in Path(__file__).parent.glob('*.py')}
        manifest={'schema_version':4,'recovery':recovery,'replay':replay,'specification_version':3,'tool':{'name':'kb-vocab','version':tool_version(),'code_sha256':tool_files},
                  'inputs':{'config':{'path':str(config_file),'sha256':config_hash},'catalog':{'path':str(catalog),'sha256':_sha(catalog_raw)},
                            'shapes':{'path':str(shapes_path),'sha256':_sha(shapes_raw)},'sources':source_manifest},
                  'reproducibility':'Stable configured URIs and RDF graph equivalence; byte-identical serialization is not asserted',
                  'files':{str(path.relative_to(stage)):_sha(path.read_bytes()) for path in sorted(stage.rglob('*')) if path.is_file()}}
        _write_json(stage/'manifest.json',manifest)
        if (config_file.read_bytes()!=config_raw or catalog.read_bytes()!=catalog_raw or shapes_path.read_bytes()!=shapes_raw
                or configuration_origin(config_file,config_raw,config)!=origin_raw):
            raise ValueError('Build inputs changed during generation')
        if previous_file and Path(previous_file).read_bytes()!=previous_raw:raise ValueError('Previous version changed during generation')
        for name,source in sources.items():
            if _sha(Path(source['path']).read_bytes())!=source['sha256']:raise ValueError(f'Source changed before publication: {name}')
        if output.exists():raise ValueError('Output appeared during generation')
        stage.rename(output)
    finally:
        if stage.exists():shutil.rmtree(stage)
    return report
