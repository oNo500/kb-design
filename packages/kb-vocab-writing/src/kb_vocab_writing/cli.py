"""Thin commands over acquisition, formatting and shared validation."""
import argparse
from pathlib import Path
import sys

from .workflow import collect,build
from .validation import inspect_bundle,summary_text


def main(argv=None):
    parser=argparse.ArgumentParser(prog='kb-vocab-writing')
    commands=parser.add_subparsers(dest='command',required=True)
    c=commands.add_parser('collect',help='复用 kb-sources 收集原件和原文结构，不自动提取概念')
    source=c.add_mutually_exclusive_group(required=True)
    source.add_argument('--manifest',type=Path);source.add_argument('--snapshot',type=Path)
    c.add_argument('--output',type=Path,required=True)
    b=commands.add_parser('build',help='把带出处的概念输入格式化为 Turtle')
    b.add_argument('input',type=Path);b.add_argument('--sources',type=Path,required=True)
    b.add_argument('--output',type=Path,required=True);b.add_argument('--preview',action='store_true',help='输出未确认样稿，不代表正式采纳')
    for name,help_text in [('inventory','统计字段有无，不运行 SHACL'),('check','统计并运行 structure、target，列出未检查范围')]:
        v=commands.add_parser(name,help=help_text);v.add_argument('bundle',type=Path);v.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='collect':
            result=collect(args.output,manifest=args.manifest,snapshot=args.snapshot)
            print(f"来源文件：{len(result['files'])}；锁定清单：{(args.output/'sources.json').resolve()}")
        elif args.command=='build':
            result=build(args.input,args.sources,args.output,preview=args.preview)
            print(f"概念：{len(result['concepts'])}；名称：{len(result['labels'])}；模式：{result['mode']}\n词表：{(args.output/'vocabulary.ttl').resolve()}\n本次尚未运行 SHACL；输入确认不等于发布。")
        else:
            report=inspect_bundle(args.bundle,args.output,run_checks=args.command=='check')
            print(summary_text(report));print(f'报告：{args.output.resolve()}')
            if report['conforms'] is False:return 1
        return 0
    except Exception as error:
        print(f'{args.command} 失败：{error}',file=sys.stderr)
        return 2
