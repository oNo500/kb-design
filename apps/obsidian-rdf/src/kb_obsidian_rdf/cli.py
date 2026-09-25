"""Explicit commands for RDF-backed vaults; no implicit formal destination."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

import yaml

from . import __version__
from .common import ContractError, json_bytes, read_json
from .layout import INDEXES, PROJECTS, RESOURCES


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kb-obsidian-rdf",
                                     description="为 Obsidian 文章查找词条、选择引用和检索内容")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="固定词表版本与使用范围，生成输入清单")
    prepare.add_argument("--source-root", required=True, type=Path, help="包含原词表输出的项目根目录")
    prepare.add_argument("--authority", required=True, type=Path, help="本次使用授权与范围记录")
    prepare.add_argument("--mode", choices=("preview", "formal"), default="preview", help="实例用途；默认开发预览")
    prepare.add_argument("--entities", type=Path, help="正式创建使用的统一实体交付目录；current 会固定为具体版本")
    prepare.add_argument("--output", required=True, type=Path, help="新输入清单路径")
    prepare.add_argument("--previous-vault", type=Path, help="刷新时固定旧交付及历史依赖")
    initialize = commands.add_parser("init", help="按输入清单在空目标建立知识库")
    initialize.add_argument("--input", required=True, type=Path)
    refresh = commands.add_parser("refresh", help="比较参考版本；显式 --apply 才写入")
    refresh.add_argument("--input", required=True, type=Path)
    refresh.add_argument("--apply", action="store_true")
    refresh.add_argument("--offline", action="store_true", help="确认已关闭该库并暂停同步和外部编辑")
    maintain = commands.add_parser("maintain", help="比较配置和视图；显式 --apply --offline 才维护，不刷新词表")
    maintain.add_argument("--apply", action="store_true")
    maintain.add_argument("--offline", action="store_true", help="确认已关闭该库并暂停同步和外部编辑")
    check = commands.add_parser("check", help="检查当前参考文件及文章字段和引用")
    check.add_argument("--path", action="append", dest="paths", help="限定文章路径，相对 vault，可重复")
    fields = ("subject", "entities", "type", "genre", "form", "references")
    search = commands.add_parser("search", help="按文章字段查找可用名称与别名，返回简短候选")
    search.add_argument("--field", required=True, choices=fields)
    search.add_argument("--query", default="", help="名称或别名；省略则列出该字段的选项")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--include-unavailable", action="store_true", help="同时查看不能新选用的记录")
    get = commands.add_parser("get", help="按明确引用或唯一名称读取条目摘要")
    articles = commands.add_parser("articles", help="按文章已有的字段引用检索文章")
    for command in (get, articles):
        command.add_argument("--field", required=True, choices=fields)
        target = command.add_mutually_exclusive_group(required=True)
        target.add_argument("--ref", dest="reference", help="IRI、带范围的 ID 或明确条目链接")
        target.add_argument("--term", help="该字段内唯一的准确名称或别名")
    get.add_argument("--details", action="store_true", help="附完整的结构化条目详情")
    get.add_argument("--link", action="store_true", help="只输出可粘贴到文章属性的内部链接")
    articles.add_argument("--descendants", action="store_true", help="subject 检索包含明确的下位概念")
    create = commands.add_parser("new", help="创建一篇字段与引用有效的 draft")
    create.add_argument("--title", required=True)
    create.add_argument("--folder", default=RESOURCES, help=f"人工索引目录 {INDEXES} 或 PARA 四区，例如 {PROJECTS}/website-redesign")
    create.add_argument("--type", required=True, dest="type_id")
    create.add_argument("--genre", required=True, dest="genre_id")
    create.add_argument("--subject", action="append", default=[], dest="subjects")
    create.add_argument("--subject-name", action="append", default=[], dest="subject_names", help="按主题范围内唯一名称选择，可重复")
    create.add_argument("--entity", action="append", default=[], dest="entities")
    create.add_argument("--entity-name", action="append", default=[], dest="entity_names", help="按实体范围内唯一名称选择，可重复")
    create.add_argument("--reference", action="append", default=[], dest="references")
    create.add_argument("--form")
    create.add_argument("--level")
    create.add_argument("--language")
    recover = commands.add_parser("recover", help="核对中断现场并恢复完整参考输出")
    recover.add_argument("--offline", action="store_true", help="确认已关闭该库并暂停同步和外部编辑")
    for command in (initialize, refresh, maintain, check, create, recover, search, get, articles):
        command.add_argument("--vault", required=True, type=Path, help="显式目标目录，无正式库默认路径")
    for command in (prepare, initialize, refresh, maintain, check, create, recover, search, get, articles):
        command.add_argument("--json", action="store_true", help="向终端输出完整 JSON 结果")
        command.add_argument("--state-root", type=Path, help="库外工程状态根目录，默认使用项目 output/obsidian-rdf/state")
    return parser


def _report(vault: Path, result: dict, state_root: Path | None = None) -> Path:
    from .storage import safe_path, state_directory, vault_lock
    mode = result.get("mode", "preview")
    usage = ("本库已按固定范围授权使用；字段与引用检查不代替内容语义审阅。" if mode == "formal"
             else "本库用于开发预览，字段与引用通过不代表正式准用或内容语义已审阅。")
    lines = ["# 知识库检查", "", f"文章数量：{result.get('checked_count', 0)}。",
             f"错误：{len(result.get('errors', []))}；其他提示：{len(result.get('issues', []))}。", "",
             usage, ""]
    unregistered = result.get("unregistered", [])
    lines.extend([f"未登记文件：{result.get('unregistered_count', len(unregistered))}；未纳入文章字段校验，不计作通过。", ""])
    if unregistered:
        lines.extend(["## 未登记文件", ""])
        for item in unregistered:
            lines.extend(["````text", f"{item['path']}：{item['reason']}".replace("````", "｀｀｀｀"), "````", ""])
    lines.extend(["## 词表检查", "", "沿用已交付版本的 SHACL 结果，本次文章检查不重新运行词表规则。", ""])
    lines.extend(_vocabulary_summary(result.get("vocabulary_validation", {})))
    lines.append("")
    for title, key in (("检查错误", "errors"), ("检查提示", "issues"), ("准用依据", "formal_unconfirmed")):
        values = result.get(key, [])
        if values:
            lines.extend([f"## {title}", ""])
            for item in values:
                # Code fences prevent source text from injecting links or rendered markup.
                lines.extend(["````text", str(item).replace("````", "｀｀｀｀"), "````", ""])
    lines.extend(["## 未检查项", ""])
    lines.extend(f"- {item}" for item in result.get("not_checked", []))
    with vault_lock(vault, state_root=state_root):
        state = state_directory(vault, state_root=state_root)
        directory = safe_path(state, "reports")
        directory.mkdir(parents=True, exist_ok=True)
        safe_path(state, "reports/check.json").write_bytes(json_bytes(result))
        report_path = safe_path(state, "reports/check.md")
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def _vocabulary_summary(value: dict) -> list[str]:
    profiles = value.get("shacl", {}).get("profiles", [])
    lines = []
    for profile in profiles:
        counts = {key.rsplit("#", 1)[-1]: count for key, count in profile.get("counts", {}).items()}
        lines.append(f"词表 {profile['profile']}：Violation {counts.get('Violation', 0)}，"
                     f"Warning {counts.get('Warning', 0)}，Info {counts.get('Info', 0)}；"
                     f"目标 {profile.get('target_count', 0)} 个。")
    if not profiles:
        lines.append("词表 SHACL 未执行或无结果记录。")
    if not value.get("entity_facts", {}).get("executed"):
        lines.append("实体事实和内容语义未由上述结构规则确认。")
    if value.get("formal_use", {}).get("confirmed"):
        lines.append("本次应用使用范围已有明确授权，原词表状态及未核事项保留。")
    return lines


def _execute(args: argparse.Namespace) -> dict:
    if args.command == "maintain":
        from .product import maintain
        return maintain(args.vault, apply=args.apply, offline=args.offline, state_root=args.state_root)
    if args.command == "search":
        from .query import search_entries
        return search_entries(args.vault, field=args.field, query=args.query,
                              limit=args.limit, include_unavailable=args.include_unavailable, state_root=args.state_root)
    if args.command == "get":
        from .query import get_entry
        return get_entry(args.vault, field=args.field, reference=args.reference,
                         term=args.term, details=args.details, state_root=args.state_root)
    if args.command == "articles":
        from .query import find_articles
        return find_articles(args.vault, field=args.field, reference=args.reference,
                             term=args.term, descendants=args.descendants, state_root=args.state_root)
    if args.command == "prepare":
        from .prepare import prepare
        return prepare(args.source_root, args.output, authority=args.authority,
                       previous_vault=args.previous_vault, state_root=args.state_root,
                       mode=args.mode, entities=args.entities)
    if args.command in {"init", "refresh"}:
        from .build import build_delivery
        from .storage import initialize, refresh
        print("读取固定输入，检查并生成参考页…", file=sys.stderr, flush=True)
        if args.command == "refresh":
            previous = read_json(args.input).get("previous_delivery")
            if not isinstance(previous, dict) or Path(previous.get("path", "")).resolve() != args.vault.resolve():
                raise ContractError("刷新清单的 previous_delivery 必须明确指向当前 vault，请重新 prepare --previous-vault")
        delivery = build_delivery(args.input)
        if args.command == "init":
            if read_json(args.input).get("previous_delivery") is not None:
                raise ContractError("初建清单不能携带上次交付；请使用独立的初建清单")
            result = initialize(args.vault, delivery, state_root=args.state_root)
        else:
            result = refresh(args.vault, delivery, apply=args.apply, offline=args.offline, state_root=args.state_root)
        manifest = json.loads(delivery.state_files["manifest.json"])
        result["mode"] = manifest["mode"]
        result["preview_mode"] = manifest["mode"] == "preview"
        records = json.loads(delivery.state_files["records.json"])["records"]
        result["resources"] = dict(Counter(row["kind"] for row in records if row["use"] == "current"))
        result["vocabulary_validation"] = manifest["validation"]
        return result
    if args.command == "new":
        from .content import new_content
        from .query import get_entry
        subjects = list(args.subjects)
        entities = list(args.entities)
        for field, names, targets in (("subject", args.subject_names, subjects),
                                       ("entities", args.entity_names, entities)):
            for name in names:
                identity = get_entry(args.vault, field=field, term=name, state_root=args.state_root)["items"][0]["identity"]
                targets.append(identity["iri"] if "iri" in identity
                               else identity["catalog"] + ":" + identity["id"])
        return new_content(args.vault, title=args.title, type_id=args.type_id,
                           genre_id=args.genre_id, subjects=subjects, entities=entities,
                           references=args.references, form=args.form, level=args.level,
                           language=args.language, folder=args.folder, state_root=args.state_root)
    if args.command == "check":
        from .content import check_content
        result = check_content(args.vault, paths=args.paths, state_root=args.state_root)
        result["report_path"] = str(_report(args.vault, result, args.state_root))
        return result
    from .storage import recover
    return recover(args.vault, offline=args.offline, state_root=args.state_root)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = _execute(args)
        if args.json:
            sys.stdout.buffer.write(json_bytes(result))
        elif args.command == "get" and args.link:
            print(result["items"][0]["link"])
        elif args.command in {"search", "get"}:
            from .render import KIND_NAMES
            print(f"{args.field}：{result.get('total', len(result['items']))} 条候选，显示 {len(result['items'])} 条。")
            for item in result["items"]:
                print(f"\n{item['label']} · {KIND_NAMES.get(item['kind'], item['kind'])}")
                summary = item.get("summary")
                print(summary.get("text", "") if isinstance(summary, dict) else summary or "来源未提供定义或范围说明。")
                print(item["link"])
                if not item.get("available", True):
                    print("仅供查看，不可用于新的选择。")
                if args.command == "get" and args.details:
                    print(json_bytes(item.get("details", {})).decode().rstrip())
        elif args.command == "articles":
            print(f"找到 {result.get('total', len(result['items']))} 篇文章。")
            for item in result["items"]:
                print(f"{item.get('title', item['path'])} · {item['path']}")
            if result.get("issues"):
                print(f"文章检查提示：{len(result['issues'])} 条。")
                for item in result["issues"][:5]:
                    print(f"  {item.get('path', '')} {item.get('field', '')}：{item.get('message', '')}")
            if result.get("unregistered_count"):
                print(f"另有 {result['unregistered_count']} 个未登记文件未纳入文章检索，未计作校验通过。")
        elif args.command == "check":
            print(f"检查 {result.get('checked_count', 0)} 篇文章；错误 {len(result.get('errors', []))}；"
                  f"提示 {len(result.get('issues', []))}；正式准用未确认 {len(result.get('formal_unconfirmed', []))}。")
            print(f"未登记文件 {result.get('unregistered_count', 0)}：未纳入文章字段校验，不计作通过。")
            for item in result.get("unregistered", [])[:5]:
                print(f"  {item['path']}：{item['reason']}")
            for item in result.get("errors", [])[:15]:
                print(f"  {item.get('path', '')} {item.get('field', '')}：{item.get('message', '')}")
            print("\n".join(_vocabulary_summary(result.get("vocabulary_validation", {}))))
            print(f"完整报告：{result['report_path']}")
        elif args.command == "prepare":
            print(f"输入清单：{result['input']}")
            for key, count in result["resources"].items():
                print(f"  {key}：{count}")
        elif args.command == "new":
            print(f"文章：{args.vault.resolve() / result['path']}")
        elif args.command == "maintain":
            print(f"产物维护：{result['status']}；拟写入 {len(result['write_set'])} 个文件；已写入 {len(result['written'])} 个文件。")
            for item in result['changes']:
                if item['action'] not in {"unchanged", "equivalent"}:
                    print(f"  {item['action']}：{item['path']}")
            print(f"完整写集、差异和结果：{result['report_path']}")
        elif args.command in {"init", "refresh"}:
            statuses = {"initialized": "已建立", "preview": "差异预览，未切换",
                        "installed": "已更新", "unchanged": "没有变化"}
            print(f"{statuses.get(result.get('status'), result.get('status'))}：{args.vault.resolve()}")
            print("参考记录：" + "；".join(f"{kind} {count}" for kind, count in sorted(result["resources"].items())))
            if "changes" in result:
                print("参考变化：" + "；".join(f"{kind} {len(paths)}" for kind, paths in result["changes"].items()))
                print(f"用户文件候选更新：{len(result.get('user_file_changes', []))}，不会覆盖原文件。")
            print("\n".join(_vocabulary_summary(result["vocabulary_validation"])))
            print("正式使用实例；来源状态与未核事项保留。" if result["mode"] == "formal"
                  else "开发预览；正式准用未确认。")
        else:
            print(json_bytes(result).decode().rstrip())
        return 1 if result.get("ok") is False or result.get("errors") else 0
    except (ContractError, OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        candidates = getattr(exc, "candidates", [])
        if args.json:
            failure = {"ok": False, "error": {"code": getattr(exc, "code", "operation_failed"),
                       "message": str(exc), "candidates": candidates}}
            sys.stderr.write(json_bytes(failure).decode())
        else:
            print(f"操作失败：{exc}", file=sys.stderr)
            for item in candidates:
                print(f"  {item['label']} · {item['kind']} · {item['path']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
