"""Application adapters run after vocabulary publication; failures are resumable."""
import json
import importlib.util
import hashlib
from pathlib import Path
import subprocess
import sys
from uuid import uuid4
from .edit_store import atomic,encode
from .display import rebase_display
from rdflib import Graph


def check_skosmos(app,build,display=True):
    """Verify already synchronized data before deciding to write it again."""
    try:
        spec=importlib.util.spec_from_file_location('kb_sync_check',app/'sync-current.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.run(build,check=True)
        receipt_path=app/'output/translated/sync-receipt.json'
        if display and receipt_path.exists():
            receipt=json.loads(receipt_path.read_bytes())
            if receipt.get('state')!='complete' or json.loads((app/'output/translated/sync-status.json').read_bytes()).get('state')!='complete':return False
            if receipt['english_base_sha256']!=hashlib.sha256((build/'vocabulary.ttl').read_bytes()).hexdigest():return False
            directory=Path(receipt['build']);raw=(directory/'vocabulary.multilingual.ttl').read_bytes()
            if hashlib.sha256(raw).hexdigest()!=receipt['source_sha256']:return False
            for relative,key in [('navigation/navigation.json','navigation_sha256'),('labels/label-provenance.json','label_provenance_sha256')]:
                if hashlib.sha256((app/'output/translated'/relative).read_bytes()).hexdigest()!=receipt[key]:return False
            module.ENDPOINT=module.ENDPOINT.replace('preview%3Acurrent','preview%3Atranslated')
            module.verify_remote(Graph().parse(data=raw,format='turtle'))
        return True
    except Exception:
        return False


def synchronize(build,applications,operation):
    results=[]
    for number,entry in enumerate(applications):
        if isinstance(entry,str):entry={'kind':'skosmos','directory':entry}
        if entry.get('kind')!='skosmos':raise ValueError('Unsupported application adapter')
        app=Path(entry['directory']).resolve();work=operation/'applications'/str(number);work.mkdir(parents=True,exist_ok=True)
        if check_skosmos(app,build,entry.get('display',True)):
            results.append({'application':str(app),'state':'unchanged','live_verified':True});continue
        receipt=app/'output/translated/sync-receipt.json';display=None
        if entry.get('display',True) and receipt.exists():
            previous=json.loads(receipt.read_bytes())['build']
            display=work/('display-'+uuid4().hex[:8]);rebase_display(previous,build,display)
        commands=[('current',[str(app/'sync-current.py'),'--build',str(build)])]
        if display:commands.append(('translated',[str(app/'sync-translated.py'),str(display)]))
        for phase,args in commands:
            result=subprocess.run([sys.executable,*args],cwd=app,capture_output=True,text=True)
            record={'application':str(app),'phase':phase,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
            atomic(work/(phase+'.json'),encode(record))
            if result.returncode:raise ValueError(f'{phase} application synchronization failed; see {work/(phase+".json")}')
            results.append({'application':str(app),'phase':phase,'state':'complete'})
    return results
