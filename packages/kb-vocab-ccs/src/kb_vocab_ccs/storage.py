"""Pinned inputs and new-directory outputs; no modification of source files."""
from contextlib import contextmanager
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def write_json(path, value):
    path.write_bytes(json_bytes(value))


def load_config(path=None):
    raw = path.read_bytes() if path else files('kb_vocab_ccs').joinpath('config/ccs.json').read_bytes()
    config = json.loads(raw)
    if config.get('schema_version') != 1:
        raise ValueError('不支持的配置版本')
    source = config['source']
    if not re.fullmatch(r'https://github.com/[\w.-]+/[\w.-]+', source['repository']):
        raise ValueError('来源必须为明确的 GitHub 仓库 URL')
    for field, length in [('commit', 40), ('sha256', 64)]:
        if not re.fullmatch('[0-9a-f]{' + str(length) + '}', source[field]):
            raise ValueError(f'来源 {field} 必须为完整小写十六进制值')
    if not source['path'] or source['path'].startswith('/') or '..' in source['path'].split('/'):
        raise ValueError('来源文件路径无效')
    base = config['identity_base_iri']
    if not isinstance(base, str) or any(c.isspace() for c in base) or not urlsplit(base).scheme or '#' in base:
        raise ValueError('身份基准必须为不含片段的绝对 IRI')
    scheme = config['scheme']
    for key in ('name', 'scope_note'):
        value = scheme[key]
        if not isinstance(value['value'], str) or not value['value'].strip():
            raise ValueError(f'{key} 正文不能为空')
        if not isinstance(value['language'], str) or not re.fullmatch(r'[A-Za-z]+(?:-[A-Za-z0-9]+)*', value['language']):
            raise ValueError(f'{key} 必须提供语言标签')
    if not isinstance(scheme['basis'], str) or not scheme['basis'].strip():
        raise ValueError('本地补充必须说明采纳依据')
    return config


def download_url(config):
    source = config['source']
    repo = source['repository'].removeprefix('https://github.com/')
    return f"https://raw.githubusercontent.com/{repo}/{source['commit']}/{quote(source['path'])}"


def verify_source(raw, config):
    if sha256(raw).hexdigest() != config['source']['sha256']:
        raise ValueError('原件 SHA-256 不符合来源锁定配置；停止生成')


@contextmanager
def new_directory(output):
    """Build off to the side; errors never leave a completed-looking output."""
    if output.exists():
        raise ValueError(f'输出目录已存在，请指定新目录：{output}')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.ccs-', dir=output.parent) as temp:
        staging = Path(temp)/'result'
        staging.mkdir()
        yield staging
        if output.exists():
            raise ValueError(f'输出目录已存在：{output}')
        staging.rename(output)


def fetch(config, cache, offline=False):
    target = cache/config['source']['sha256']
    if target.exists():
        verify_source((target/'source.xml').read_bytes(), config)
        return target/'source.xml'
    if offline:
        raise ValueError('离线缓存中没有此版本；先 fetch 或为 build 指定 --source')
    url = download_url(config)
    request = Request(url, headers={'User-Agent':'kb-vocab-ccs/0.1.0'})
    with urlopen(request, timeout=60) as response:
        raw = response.read(20_000_001)
    if len(raw) > 20_000_000:
        raise ValueError('来源超过当前适配器的 20 MB 输入上限')
    verify_source(raw, config)
    with new_directory(target) as stage:
        (stage/'source.xml').write_bytes(raw)
        write_json(stage/'source.json', {'source':config['source'], 'download_url':url, 'bytes':len(raw)})
    return target/'source.xml'
