"""Source, build, inventory and check are separately repeatable commands."""
import argparse
import json
from pathlib import Path
import sys

from .adapter import build
from .routing import write_review, partition
from .storage import fetch, load_config
from .validation import check, field_inventory


def main(argv=None):
    parser = argparse.ArgumentParser(prog='kb-vocab-ccs')
    commands = parser.add_subparsers(dest='command',required=True)
    download = commands.add_parser('fetch',help='获取固定版本原件，核对哈希并缓存')
    download.add_argument('--config',type=Path)
    download.add_argument('--cache',type=Path,default=Path('output/vocabulary/ccs/cache'))
    download.add_argument('--offline',action='store_true')
    generate = commands.add_parser('build',help='从原件和配置生成自有表示，不执行 SHACL')
    generate.add_argument('--config',type=Path)
    generate.add_argument('--source',type=Path,help='本地 XML 原件；省略时只读取缓存，不联网')
    generate.add_argument('--cache',type=Path,default=Path('output/vocabulary/ccs/cache'))
    generate.add_argument('--output',type=Path,required=True,help='尚不存在的构建目录')
    review = commands.add_parser('review',help='提取专名清单或检查已有判断，等待人工确认')
    review.add_argument('input',type=Path)
    review.add_argument('--plan',type=Path)
    review.add_argument('--output',type=Path,required=True)
    route = commands.add_parser('partition',help='按已确认清单生成概念词表与实体词表')
    route.add_argument('input',type=Path)
    route.add_argument('--plan',type=Path,required=True)
    route.add_argument('--output',type=Path,required=True)
    inv = commands.add_parser('inventory',help='复用 SHACL 结构统计字段有无')
    inv.add_argument('input',type=Path,help='构建目录或 TTL 文件')
    inv.add_argument('--output',type=Path)
    verify = commands.add_parser('check',help='运行 SHACL 并保存报告')
    verify.add_argument('input',type=Path,help='构建目录或 TTL 文件')
    verify.add_argument('--profile',choices=['all','structure','target','standard'],default='all')
    verify.add_argument('--output',type=Path,required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'fetch':
            path = fetch(load_config(args.config),args.cache,args.offline)
            print(f'原件：{path.resolve()}')
        elif args.command == 'build':
            config = load_config(args.config)
            source = args.source or fetch(config,args.cache,offline=True)
            manifest = build(source,config,args.output)
            count = manifest['counts']
            print(f"词表：{(args.output/'vocabulary.ttl').resolve()}\n概念：{count['concepts']}；XL 名称：{count['xl_labels']}。尚未运行 SHACL，请执行 check。")
        elif args.command == 'review':
            counts=write_review(args.input,args.output,args.plan)
            print(f'清单：{args.output.resolve()}\n{dict(counts)}')
        elif args.command == 'partition':
            report=partition(args.input,json.loads(args.plan.read_bytes()),args.output)
            print(json.dumps(report,ensure_ascii=False,indent=2))
            print(f'结果：{args.output.resolve()}')
        elif args.command == 'inventory':
            print(field_inventory(args.input,args.output))
            if args.output:
                print(f'报告：{args.output.resolve()}')
        else:
            code, text = check(args.input,args.output,args.profile)
            print(text)
            print(f'报告：{args.output.resolve()}')
            return code
        return 0
    except Exception as error:
        print(f'{args.command} 失败：{error}',file=sys.stderr)
        return 2
