"""Read-only command for field inventory."""
import argparse
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
import sys
from time import perf_counter

from rdflib import Graph

from .inventory import inventory
from .report import markdown
from .structure import load_structure


def main(argv=None):
    parser = argparse.ArgumentParser(prog="kb-vocab-shacl")
    commands = parser.add_subparsers(dest="command", required=True)
    cmd = commands.add_parser("inventory", help="统计字段有无，不执行 SHACL 校验")
    cmd.add_argument("input", type=Path, help="本地 Turtle 文件")
    cmd.add_argument("--type", dest="resource_type", help="例如 Concept、Label、Collection")
    cmd.add_argument("--output", type=Path, help="新建报告目录；省略则输出 Markdown")
    args = parser.parse_args(argv)
    try:
        if args.output and args.output.exists():
            raise ValueError(f"Output already exists: {args.output}")
        start = perf_counter()
        raw = args.input.read_bytes()
        data = Graph().parse(data=raw, format="turtle", publicID=args.input.resolve().as_uri())
        structure, roots = load_structure()
        result = inventory(data, structure=structure, roots=roots, resource_type=args.resource_type)
        directory = files("kb_vocab_shacl").joinpath("shapes")
        result["run"] = {
            "input": str(args.input.resolve()), "input_sha256": sha256(raw).hexdigest(),
            "elapsed_seconds": perf_counter() - start,
            "shape_files": {name: sha256(directory.joinpath(name).read_bytes()).hexdigest()
                            for name in ("structure.ttl", "skos.ttl", "skos-xl.ttl", "skos-thes.ttl", "metadata.ttl", "profile.ttl")},
            "shacl_validation_executed": False,
        }
        text = markdown(result)
        if args.output:
            args.output.mkdir(parents=True, exist_ok=False)
            (args.output / "inventory.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            (args.output / "统计-词表字段.md").write_text(text, encoding="utf-8")
            print(f"报告：{args.output.resolve()}\n读取与统计：{result['run']['elapsed_seconds']:.3f} 秒")
        else:
            print(text)
        return 0
    except Exception as error:
        print(f"统计失败：{error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
