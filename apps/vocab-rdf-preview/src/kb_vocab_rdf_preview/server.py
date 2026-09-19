"""Serve one local Turtle file as a lazily expanded hierarchy."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
import json
from pathlib import Path
from urllib.parse import urlsplit

from rdflib import Graph, Literal, Namespace, RDF, SKOS

XL = Namespace('http://www.w3.org/2008/05/skos-xl#')
DC = Namespace('http://purl.org/dc/elements/1.1/')


def load_tree(path):
    graph = Graph().parse(data=path.read_bytes(),format='turtle',publicID=path.resolve().as_uri())
    concepts = set(graph.subjects(RDF.type,SKOS.Concept))

    def label(node):
        values = set(graph.objects(node,SKOS.prefLabel))
        for record in graph.objects(node,XL.prefLabel):
            values.update(graph.objects(record,XL.literalForm))
        if not values:
            values.update(graph.objects(node,DC.title))
        def order(value):
            language = (value.language or '').lower() if isinstance(value,Literal) else ''
            rank = 0 if language == 'zh' or language.startswith('zh-') else 1 if language == 'en' or language.startswith('en-') else 2
            return rank, str(value), language
        return str(min(values,key=order)) if values else str(node)

    children = {node:set() for node in concepts}
    parents = {node:set() for node in concepts}
    edges = set(graph.subject_objects(SKOS.narrower))
    edges.update((parent,child) for child,parent in graph.subject_objects(SKOS.broader))
    for parent,child in edges:
        if parent in concepts and child in concepts:
            children[parent].add(child)
            parents[child].add(parent)
    labels = {node:label(node) for node in concepts}
    key = lambda node:(labels[node].casefold(),str(node))
    tops = set(graph.objects(None,SKOS.hasTopConcept)) | set(graph.subjects(SKOS.topConceptOf,None))
    roots = sorted((tops & concepts) | {node for node in concepts if not parents[node]},key=key)
    # Keep disconnected cyclic components reachable without changing their source relations.
    seen = set()
    def mark(start):
        pending = [start]
        while pending:
            node = pending.pop()
            if node not in seen:
                seen.add(node)
                pending.extend(children[node])
    for root in roots:
        mark(root)
    extra = []
    for node in sorted(concepts,key=key):
        if node not in seen:
            roots.append(node)
            extra.append(str(node))
            mark(node)
    schemes = sorted(graph.subjects(RDF.type,SKOS.ConceptScheme),key=str)
    return {'title':label(schemes[0]) if schemes else path.stem,
            'count':len(concepts),'roots':[str(node) for node in roots],'extra_roots':extra,
            'nodes':{str(node):{'label':labels[node],'children':[str(c) for c in sorted(children[node],key=key)]}
                     for node in sorted(concepts,key=str)}}


def render(data):
    # Escape script delimiters; names are inserted into the DOM only with textContent.
    payload = json.dumps(data,ensure_ascii=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e')
    template = files('kb_vocab_rdf_preview').joinpath('template.html').read_text(encoding='utf-8')
    return template.replace('__TREE_DATA__',payload)


def make_server(path, port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            allowed = {f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
            origin = self.headers.get('Origin')
            if self.headers.get('Host','').lower() not in allowed or (origin and origin not in {f'http://{host}' for host in allowed}):
                self.send_error(403)
                return
            if urlsplit(self.path).path != '/':
                self.send_error(404)
                return
            try:
                body = render(load_tree(path)).encode('utf-8')
            except Exception:
                self.send_error(500,'Unable to read Turtle file; check source and refresh.')
                return
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self,*args):
            pass

    return ThreadingHTTPServer(('127.0.0.1',port),Handler)


def default_source():
    for root in Path(__file__).resolve().parents:
        if (root/'pyproject.toml').exists() and (root/'packages').is_dir():
            return root/'output/vocabulary/ccs/build-48644c2ed653/vocabulary.ttl'
    raise ValueError('找不到仓库，请指定 TTL 文件路径')


def main(argv=None):
    parser = argparse.ArgumentParser(description='只读浏览 Turtle 词表分类树')
    parser.add_argument('input',nargs='?',type=Path,help='TTL 路径，默认当前 CCS 构建')
    parser.add_argument('--port',type=int,default=8766)
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error('端口必须在 0–65535 之间')
    try:
        source = (args.input or default_source()).resolve()
        load_tree(source)
        server = make_server(source,args.port)
    except Exception as error:
        parser.exit(2,f'无法启动：{error}\n')
    print(f'分类树：http://127.0.0.1:{server.server_port}\n只读词表：{source}\n浏览器刷新后重新读取；Ctrl+C 停止。',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__=='__main__':
    main()
