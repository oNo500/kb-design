"""Preserve the selected source graph, then add explicitly adopted representation."""
from hashlib import sha256
import re
from urllib.parse import urljoin

from defusedxml import ElementTree as ET
from rdflib import BNode, Graph, Literal, Namespace, RDF, SKOS, URIRef
from rdflib.compare import isomorphic

from .storage import json_bytes, new_directory, verify_source, write_json

XL = Namespace('http://www.w3.org/2008/05/skos-xl#')
NAMESPACES = {'rdf':str(RDF), 'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
              'skos':str(SKOS), 'dc':'http://purl.org/dc/elements/1.1/'}
R = '{' + str(RDF) + '}'
LANG = '{http://www.w3.org/XML/1998/namespace}lang'


def parse_source(raw, base):
    # Only expand the four reviewed namespace constants; never load a DTD.
    text = raw.decode('utf-8')
    if '<!DOCTYPE' in text:
        matches = list(re.finditer(r'<!DOCTYPE\s+rdf:RDF\s*\[(.*?)\]>', text, re.S))
        if len(matches) != 1:
            raise ValueError('来源 DTD 不属于已支持的固定命名空间声明')
        body = matches[0].group(1)
        pattern = r'<!ENTITY\s+(\w+)\s+"([^"]+)"\s*>'
        pairs = re.findall(pattern, body)
        if len(pairs) != 4 or dict(pairs) != NAMESPACES or re.sub(pattern, '', body).strip():
            raise ValueError('拒绝非预期 DTD 或外部实体')
        text = text[:matches[0].start()] + text[matches[0].end():]
        for key, value in NAMESPACES.items():
            text = text.replace('&'+key+';', value)
    xml = ET.fromstring(text)
    if xml.tag != R+'RDF' or xml.attrib:
        raise ValueError('仅支持已核对的 RDF 根结构；新增 xml:base 等结构须先审查')
    iri_changes = {}
    identifiers = []
    for node in xml.iter():
        for attr in (R+'about', R+'resource'):
            if attr not in node.attrib:
                continue
            original = node.attrib[attr]
            if any(c.isspace() and c != ' ' for c in original):
                raise ValueError('IRI 包含未支持的空白字符')
            adapted = original.replace(' ', '%20')
            if original != adapted:
                iri_changes[original] = adapted
            node.set(attr, adapted)
    # Serializing XML here preserves text and language inheritance. RDFLib owns RDF parsing.
    adapted_xml = ET.tostring(xml, encoding='utf-8', xml_declaration=True)
    graph = Graph().parse(data=adapted_xml, format='xml', publicID=base)
    expected = Graph()
    subjects = set()
    for node in xml:
        if set(node.attrib) - {R+'about', LANG} or R+'about' not in node.attrib:
            raise ValueError('来源对象结构已变化，需要审查后适配')
        if node.tag not in ('{'+str(SKOS)+'}Concept', '{'+str(SKOS)+'}ConceptScheme'):
            raise ValueError('来源出现未审查的资源类型')
        subject = URIRef(urljoin(base, node.attrib[R+'about']))
        if subject in subjects:
            raise ValueError('来源存在重复资源记录或 URI 适配碰撞')
        subjects.add(subject)
        identifiers.append({'source_identifier':next((a for a,b in iri_changes.items() if b==node.attrib[R+'about']),node.attrib[R+'about']),
                            'resolved_iri':str(subject)})
        expected.add((subject, RDF.type, URIRef(node.tag[1:].replace('}', '', 1))))
        for field in node:
            if len(field) or set(field.attrib) - {R+'resource', LANG}:
                raise ValueError('来源出现嵌套或非预期字段，停止而不丢弃')
            predicate = URIRef(field.tag[1:].replace('}', '', 1))
            if R+'resource' in field.attrib:
                if (field.text or '').strip():
                    raise ValueError('资源引用混有正文')
                value = URIRef(urljoin(base, field.attrib[R+'resource']))
            else:
                value = Literal(field.text or '', lang=field.attrib.get(LANG,node.attrib.get(LANG)))
            expected.add((subject, predicate, value))
    if set(graph) != set(expected):
        raise ValueError('独立 XML 内容核对与 RDF 解析不一致')
    return graph, adapted_xml, iri_changes, sorted(identifiers,key=lambda x:x['resolved_iri'])


def turtle_bytes(graph):
    # N-Triples is a Turtle subset. Sort library-serialized statements for byte determinism.
    # This also avoids serializer-dependent prefix and blank-node ordering.
    if any(isinstance(term, BNode) for triple in graph for term in triple):
        raise ValueError('当前确定性输出不支持空白节点；不能静默重命名')
    lines = sorted(graph.serialize(format='nt').splitlines())
    header = '# 程序生成，请修改来源配置后重建。\n# 每行依次为资源、属性和值；名称语言保留原标记。\n'
    return (header + '\n'.join(lines) + '\n').encode('utf-8')


def adapt(source, config):
    graph = Graph()
    for triple in source:
        graph.add(triple)
    schemes = set(graph.subjects(RDF.type, SKOS.ConceptScheme))
    if len(schemes) != 1:
        raise ValueError('CCS 适配要求原件恰好一份 ConceptScheme')
    scheme = next(iter(schemes))
    additions = []
    for key, predicate in [('name',SKOS.prefLabel),('scope_note',SKOS.scopeNote)]:
        record = config['scheme'][key]
        value = Literal(record['value'], lang=record['language'])
        if (scheme,predicate,value) not in graph:
            graph.add((scheme,predicate,value))
            additions.append({'subject':str(scheme),'property':str(predicate),'value':str(value),
                              'language':value.language,'basis':config['scheme']['basis']})
    labels = []
    for predicate, role in [(SKOS.prefLabel,XL.prefLabel),(SKOS.altLabel,XL.altLabel),(SKOS.hiddenLabel,XL.hiddenLabel)]:
        for subject, value in sorted(graph.subject_objects(predicate),key=lambda pair:(str(pair[0]),pair[1].n3())):
            if not isinstance(value, Literal):
                raise ValueError('普通名称必须为文字；不能强行转为字符串')
            identity = [str(subject),str(predicate),str(value),value.language,str(value.datatype) if value.datatype else None]
            label = URIRef('urn:kb-vocab-ccs:label:'+sha256(json_bytes(identity)).hexdigest())
            graph.add((subject,role,label))
            graph.add((label,RDF.type,XL.Label))
            graph.add((label,XL.literalForm,value))
            labels.append({'subject':str(subject),'role':str(role),'label':str(label),
                           'value':str(value),'language':value.language,'datatype':str(value.datatype) if value.datatype else None})
    if not set(source) <= set(graph):
        raise ValueError('适配删除了来源陈述')
    return graph, additions, sorted(labels,key=lambda x:x['label'])


def build(source_path, config, output):
    raw = source_path.read_bytes()
    verify_source(raw, config)
    source, adapted_xml, iri_changes, identifiers = parse_source(raw,config['identity_base_iri'])
    graph, additions, labels = adapt(source,config)
    source_ttl, vocab_ttl = turtle_bytes(source), turtle_bytes(graph)
    if not isomorphic(graph,Graph().parse(data=vocab_ttl,format='turtle')):
        raise ValueError('输出 Turtle 回读与适配图不一致')
    adaptations = {'iri_changes':iri_changes,'identifiers':identifiers,'local_additions':additions,'labels':labels}
    counts = {'concepts':len(set(graph.subjects(RDF.type,SKOS.Concept))),
              'top_concepts':len(set(graph.objects(None,SKOS.hasTopConcept))),
              'xl_labels':len(set(graph.subjects(RDF.type,XL.Label))),
              'source_triples':len(source),'output_triples':len(graph)}
    with new_directory(output) as stage:
        (stage/'source.xml').write_bytes(raw)
        (stage/'adapted.xml').write_bytes(adapted_xml)
        (stage/'source.ttl').write_bytes(source_ttl)
        (stage/'vocabulary.ttl').write_bytes(vocab_ttl)
        write_json(stage/'config.json',config)
        write_json(stage/'adaptations.json',adaptations)
        hashes = {p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}
        manifest = {'format_version':1,'adapter_version':'0.1.0','counts':counts,'files':hashes,
                    'source_sha256':config['source']['sha256'],'config_sha256':sha256(json_bytes(config)).hexdigest(),
                    'source_statements_preserved':True,'turtle_roundtrip_isomorphic':True,
                    'shacl_validation_executed':False,'pipeline_activated':False}
        write_json(stage/'manifest.json',manifest)
    return manifest
