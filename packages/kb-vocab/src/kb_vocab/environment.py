"""Archive the actual tool code and pinned runtime dependency closure."""
import json
import platform
import shutil
from pathlib import Path
from importlib.metadata import version, requires, metadata as distribution_metadata
import tomllib
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


def project_metadata():
    project=Path(__file__).resolve().parents[2]/'pyproject.toml'
    if project.is_file():
        raw=project.read_bytes()
        return project,raw,tomllib.loads(raw.decode())['project']
    dist=distribution_metadata('kb-vocab')
    values={'name':'kb-vocab','version':dist['Version'],'requires-python':dist['Requires-Python'],
            'dependencies':requires('kb-vocab') or []}
    raw=('[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.build_meta"\n\n[project]\n'
         +''.join(f'{key} = {json.dumps(value)}\n' for key,value in values.items())
         +'\n[project.scripts]\nkb-vocab = "kb_vocab.cli:main"\n\n[tool.setuptools.packages.find]\nwhere = ["src"]\n'
         +'\n[tool.setuptools.package-data]\nkb_vocab = ["policies/*.json"]\n').encode()
    return None,raw,values


def tool_version():
    return project_metadata()[2]['version']


def archive_environment(stage):
    package=Path(__file__).resolve().parent
    project,project_raw,metadata=project_metadata()
    pending=list(metadata['dependencies']);resolved={}
    while pending:
        req=Requirement(pending.pop())
        if req.marker and not req.marker.evaluate({'extra':''}):continue
        name=canonicalize_name(req.name)
        installed=version(name)
        if req.specifier and installed not in req.specifier:
            raise ValueError(f'Installed dependency violates requirement: {req}')
        if name in resolved:continue
        resolved[name]=installed
        pending.extend(requires(name) or [])
    root=stage/'recovery';tool=root/'tool';target=tool/'src/kb_vocab'
    target.mkdir(parents=True)
    for path in package.rglob('*'):
        if path.is_file() and (path.suffix=='.py' or path.parent.name=='policies' and path.suffix=='.json'):
            out=target/path.relative_to(package);out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,out)
    (tool/'pyproject.toml').write_bytes(project_raw)
    for ancestor in (project.parents if project else []):
        lock=ancestor/'uv.lock'
        if lock.exists():shutil.copyfile(lock,root/'uv.lock');break
    (root/'requirements.txt').write_text(''.join(f'{name}=={v}\n' for name,v in sorted(resolved.items())))
    info={'python':platform.python_version(),'implementation':platform.python_implementation(),
          'platform':platform.platform(),'dependencies':resolved,
          'tool_version':metadata['version'],
          'scope':'Exact tool source and runtime version pins; dependency downloads and compatible Python are required. No offline OS image.'}
    (root/'environment.json').write_text(json.dumps(info,indent=2)+'\n')
    (root/'restore.py').write_text('''"""Create a separate runtime from this archive; requires uv and package access."""
import json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('Usage: python restore.py NEW_ENV_DIRECTORY')
env=Path(sys.argv[1]).resolve()
if env.exists():raise SystemExit('Environment directory must be new')
if env.is_relative_to(root.parent):raise SystemExit('Environment must be outside the immutable build archive')
info=json.loads((root/'environment.json').read_text())
subprocess.run(['uv','venv','--python',info['python'],str(env)],check=True)
python=env/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
subprocess.run(['uv','pip','install','--python',str(python),'-r',str(root/'requirements.txt')],check=True)
print(str(python)+' '+str(root/'run.py')+' --help')
''')
    (root/'run.py').write_text('''"""Run archived code, independent of an editable workspace installation."""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent/'tool/src'))
from kb_vocab.cli import main
raise SystemExit(main())
''')
    return {'directory':'recovery','environment':'recovery/environment.json',
            'requirements':'recovery/requirements.txt','tool':'recovery/tool',
            'restore':'recovery/restore.py','run':'recovery/run.py'}
