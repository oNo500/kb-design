"""Atomic revisioned local edit storage; readers never observe partial JSON."""
from contextlib import contextmanager
import json
from pathlib import Path
import os
from uuid import uuid4
from .local_edits import empty,validate


def encode(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()

def atomic(path,raw):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    pending=path.with_name('.'+path.name+'.'+uuid4().hex)
    try:pending.write_bytes(raw);os.replace(pending,path)
    finally:pending.unlink(missing_ok=True)

def load(path):
    path=Path(path)
    return validate(json.loads(path.read_bytes())) if path.exists() else empty()

@contextmanager
def lock(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    try:path.mkdir()
    except FileExistsError:raise ValueError('Another maintenance writer is active; inspect a stale lock before retrying')
    try:yield
    finally:path.rmdir()

def change(path,transform,expected_revision=None):
    path=Path(path)
    with lock(path.with_name(path.name+'.lock')):
        old=load(path)
        if expected_revision is not None and old['revision']!=expected_revision:raise ValueError('Local edit revision changed; reload before editing')
        new=validate(transform(old))
        if new['revision']!=old['revision']+1:raise ValueError('A local edit must advance exactly one revision')
        event=new['history'][-1]
        event['before']=[p for p in old['patches'] if p not in new['patches']]
        event['after']=[p for p in new['patches'] if p not in old['patches']]
        atomic(path,encode(new));return new
