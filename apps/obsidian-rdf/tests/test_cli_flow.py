"""Exercise the public commands and their shared identity/write-set contract."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from kb_obsidian_rdf.common import digest, json_bytes
from kb_obsidian_rdf import __version__
from kb_obsidian_rdf.storage import state_directory


class CommandFlowTests(unittest.TestCase):
    def test_create_query_and_refresh_preserve_article_identity_and_user_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            data = root/'data.ttl'
            data.write_text('@prefix s: <http://www.w3.org/2004/02/skos/core#> .\n'
                            '<urn:topic> a s:Concept; s:prefLabel "主题"@zh .\n'
                            '<urn:tool> a <https://schema.org/SoftwareApplication>; s:prefLabel "工具"@zh .\n')
            permission={'preview_reference':'explicit test authorization',
                        'scope_reference':'the two fixture records','formal_reference':None}
            source=dict(key='fixture',path=str(data),format='turtle',identity='fixture',version='1',
                        sha256=digest(data.read_bytes()),scope={'subject_iris':['urn:topic']},
                        trial_subjects=['urn:topic'],authority=permission)
            entity_source={**source,'key':'fixture-entities',
                           'scope':{'entity_class_iris':['https://schema.org/SoftwareApplication']},
                           'trial_subjects':['urn:tool']}
            auxiliary=[]
            for kind, identifier in [('types','tutorial'),('genres','background')]:
                p=root/f'{kind}.yaml'
                p.write_text(f'schema_version: 3\nversion: test\n{kind}:\n'
                             f'  - id: {identifier}\n    label: {{zh: 示例}}\n    status: active\n')
                auxiliary.append(dict(key=kind,kind=kind,path=str(p),format='yaml',schema_version=3,
                                      version='test',sha256=digest(p.read_bytes()),
                                      authority={**permission,'formal_reference':'adopted fixture type and genre'}))
            spec=dict(format_version=1,mode='preview',sources=[source,entity_source],auxiliary=auxiliary,
                      display={'languages':['zh','en']},rules={'shacl_profiles':['structure']},
                      producer={'name':'kb-obsidian-rdf','version':__version__},previous_delivery=None)
            spec['compatible_sources']=[['fixture','fixture-entities']]
            input_path=root/'input.json'; input_path.write_bytes(json_bytes(spec))
            vault=root/'preview'
            state_root=root/'engine-state'
            def run(*args, expected=0):
                command=[sys.executable,'-m','kb_obsidian_rdf',*map(str,args),'--state-root',str(state_root),'--json']
                result=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=45,
                                      env=os.environ.copy())
                self.assertEqual(result.returncode,expected,result.stdout+result.stderr)
                return json.loads(result.stdout) if expected==0 else result
            run('init','--input',input_path,'--vault',vault)
            state=state_directory(vault,state_root=state_root)
            self.assertFalse(any(p.suffix in {'.json','.ttl'} for p in vault.rglob('*')))
            self.assertFalse((vault/'preview-admin').exists())
            (vault/'00-inbox'/'free-note.md').write_text('自由捕获，无须填写文章元数据。\n')
            (vault/'03-resources'/'reading-material.md').write_text('# 外部资料\n\n保留原文和出处。\n')
            selected=run('search','--vault',vault,'--field','subject','--query','主题')
            self.assertEqual([item['identity'] for item in selected['items']],[{'iri':'urn:topic'}])
            self.assertEqual(run('get','--vault',vault,'--field','entities','--term','工具')['items'][0]['identity'],{'iri':'urn:tool'})
            created=run('new','--vault',vault,'--title','JavaScript 测试_文章','--folder','01-projects/test-project','--type','tutorial',
                        '--genre','background','--subject-name','主题','--entity-name','工具')
            article=vault/created['path']
            with article.open('a',encoding='utf-8') as out:
                out.write((vault/'07-templates/article.md').read_text())
            initial=article.read_bytes()
            self.assertEqual(created['path'],'01-projects/test-project/javascript-测试-文章.md')
            result=run('check','--vault',vault)
            self.assertEqual(result['checked_count'],1)
            self.assertTrue(result['formal_unconfirmed'])
            self.assertEqual(result['unregistered_count'],1)
            self.assertFalse(result['coverage']['complete'])
            self.assertIn('reading-material.md',Path(result['report_path']).read_text())
            self.assertFalse(Path(result['report_path']).is_relative_to(vault))
            linked=run('articles','--vault',vault,'--field','entities','--term','工具')
            self.assertEqual([item['path'] for item in linked['items']],[created['path']])
            run('new','--vault',vault,'--title','错误文章','--type','tutorial',
                '--genre','background','--subject','urn:tool',expected=1)
            self.assertEqual(list((vault/'01-projects').rglob('*.md')),[article])
            view=vault/'06-views/personal.base';view.write_text('views: []\n')
            data.write_text(data.read_text().replace('主题','新的显示名'))
            source['sha256']=digest(data.read_bytes());source['version']='2'
            entity_source['sha256']=digest(data.read_bytes());entity_source['version']='2'
            spec['previous_delivery']={'path':str(vault),
                                       'state_root':str(state_root),
                                       'sha256':digest((state/'current/manifest.json').read_bytes())}
            next_input=root/'next.json';next_input.write_bytes(json_bytes(spec))
            old_manifest=(state/'current/manifest.json').read_bytes()
            run('refresh','--input',next_input,'--vault',vault)
            self.assertEqual((state/'current/manifest.json').read_bytes(),old_manifest)
            run('refresh','--input',next_input,'--vault',vault,'--apply','--offline')
            self.assertEqual(article.read_bytes(),initial)
            self.assertEqual(view.read_text(),'views: []\n')
            self.assertTrue(run('check','--vault',vault)['ok'])
            archived=vault/'04-archives/test-project'/article.name
            archived.parent.mkdir(parents=True)
            article.rename(archived)
            self.assertEqual(archived.read_bytes(),initial)
            matches=run('articles','--vault',vault,'--field','entities','--term','工具')
            self.assertEqual(matches['items'][0]['path'],'04-archives/test-project/javascript-测试-文章.md')
            self.assertEqual(matches['items'][0]['identifier'],created['identifier'])
            self.assertFalse(any(p.suffix in {'.json','.ttl'} for p in vault.rglob('*')))
