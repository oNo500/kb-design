"""Readable paths are presentation; identity and installed paths remain stable."""
from __future__ import annotations

from collections import defaultdict
import json
from pathlib import PurePosixPath
import re
import unicodedata

from .common import ContractError, reference_path, safe_relative
from .layout import KIND_DIRECTORIES, VOCABULARY


def identity_key(identity):
    return json.dumps(identity, sort_keys=True, ensure_ascii=False)


def path_key(path):
    # Compare as on common case-insensitive and Unicode-normalizing filesystems.
    return unicodedata.normalize('NFC', path).casefold()


def filename_stem(label, byte_limit=220):
    """Sanitize the filename only; the original label is never rewritten."""
    stem = re.sub(r'[<>:"/\\|?*#\^\[\]%\x00-\x1f\x7f]', '-', str(label).lower())
    stem = re.sub(r'[\s_-]+', '-', stem).strip(' .-')
    stem = stem.encode('utf8')[:byte_limit].decode('utf8', errors='ignore').rstrip(' .-') or 'entry'
    if re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])', stem.split('.')[0], re.IGNORECASE):
        stem = 'entry-' + stem
    return stem


def assign_paths(records, previous_records=()):
    """Allocate a complete batch, retaining all previous nonhistorical paths.

    A collision gives every fresh colliding name an identity hash suffix,
    independent of input order. Retired entry paths remain reserved for history.
    """
    installed, occupied = {}, {}
    for old in previous_records:
        if old['use'] == 'historical':
            continue
        identity = identity_key(old['identity'])
        path = safe_relative(old['path'])
        if not path.startswith(f'{VOCABULARY}/{KIND_DIRECTORIES.get(old["kind"], "invalid-kind")}/') or not path.endswith('.md'):
            raise ContractError('旧条目路径与对象种类不符')
        key = path_key(path)
        if identity in installed or key in occupied and occupied[key] != identity:
            raise ContractError('上次交付身份或文件路径重复')
        installed[identity] = old
        occupied[key] = identity

    fresh = []
    for record in records:
        identity = identity_key(record['identity'])
        old = installed.get(identity)
        if old:
            if old['kind'] != record['kind']:
                raise ContractError('同一身份刷新后改变对象种类')
            record['path'] = old['path']
        else:
            record['path'] = f'{VOCABULARY}/{KIND_DIRECTORIES[record["kind"]]}/{filename_stem(record["label"])}.md'
            fresh.append(record)

    suffix_lengths = {}
    while True:
        groups = defaultdict(list)
        for record in fresh:
            groups[path_key(record['path'])].append(record)
        conflicts = [record for key, group in groups.items() if len(group) > 1 or key in occupied for record in group]
        if not conflicts:
            break
        for record in conflicts:
            identity = identity_key(record['identity'])
            length = suffix_lengths.get(identity, 0)
            if length == 64:
                raise ContractError('身份摘要与已有条目产生不可消解的路径冲突')
            length = 8 if length == 0 else length * 2
            token = PurePosixPath(reference_path(record['kind'], record['identity'])).stem
            record['path'] = f'{VOCABULARY}/{KIND_DIRECTORIES[record["kind"]]}/{filename_stem(record["label"], 235 - length)}-{token[:length]}.md'
            suffix_lengths[identity] = length
