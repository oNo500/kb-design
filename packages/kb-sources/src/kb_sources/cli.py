"""Command-line interface for public source downloads and offline verification."""

import argparse
import json
from pathlib import Path

from kb_sources.download import SourceError, fetch, verify


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    download = commands.add_parser("fetch", help="download files into a new immutable snapshot")
    download.add_argument("--manifest", type=Path, required=True)
    download.add_argument("--output", type=Path, required=True)
    download.add_argument("--timeout", type=float, default=30)
    download.add_argument("--max-bytes", type=int, default=64 * 1024 * 1024, help="maximum bytes per file")
    download.add_argument("--retries", type=int, default=1)
    check = commands.add_parser("verify", help="verify a snapshot without network access")
    check.add_argument("snapshot", type=Path)
    extract = commands.add_parser("extract-html", help="extract source headings and paragraphs without inferring concepts")
    extract.add_argument("snapshot", type=Path)
    extract.add_argument("--file-id", required=True)
    extract.add_argument("--output", type=Path, required=True)
    convert = commands.add_parser("extract", help="extract a verified HTML or text PDF")
    convert.add_argument("snapshot", type=Path)
    convert.add_argument("--file-id", required=True)
    convert.add_argument("--output", type=Path, required=True)
    batch = commands.add_parser("extract-all", help="convert all files in selected snapshots")
    selection = batch.add_mutually_exclusive_group(required=True)
    selection.add_argument("--sources", type=Path)
    selection.add_argument("--snapshot", type=Path, action="append")
    batch.add_argument("--output", type=Path, required=True)
    ieee = commands.add_parser("extract-ieee", help="extract July 2025 IEEE terms and explicit source relations")
    ieee.add_argument("--acquisition", type=Path, required=True)
    ieee.add_argument("--output", type=Path, required=True)
    ieee.add_argument("--reference-csv", type=Path, help="third-party cleaned 2023 Thesaurus CSV")
    ieee.add_argument("--reference-taxonomy", type=Path, help="third-party 2025 dot-indented Taxonomy text")
    cognitive = commands.add_parser("fetch-cognitive-atlas", help="capture concept/task lists and all details; resume verified batches")
    cognitive.add_argument("--manifest", type=Path, required=True)
    cognitive.add_argument("--output", type=Path, required=True)
    cognitive.add_argument("--workers", type=int, default=4)
    export = commands.add_parser("export-cognitive-atlas", help="verify and export complete source transcription")
    export.add_argument("bundle", type=Path)
    export.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "export-cognitive-atlas":
            from kb_sources.cognitive_atlas import export_source
            print(json.dumps(export_source(args.bundle, args.output)))
        elif args.command == "fetch-cognitive-atlas":
            from kb_sources.cognitive_atlas import acquire
            report = acquire(args.manifest, args.output, args.workers)
            print(json.dumps({"output": str(args.output), "status": report["status"], **report["counts"]}))
        elif args.command == "extract-ieee":
            from kb_sources.ieee_thesaurus import extract_ieee
            references = None
            if bool(args.reference_csv) != bool(args.reference_taxonomy):
                raise SourceError('provide both reference CSV and taxonomy text, or neither')
            if args.reference_csv:
                from kb_sources.ieee_reference import load_reference
                references = load_reference(args.reference_csv, args.reference_taxonomy)
            summary = extract_ieee(args.acquisition, args.output, references=references)
            print(json.dumps({"output":str(args.output), **summary},ensure_ascii=False))
            return 2 if summary['unassigned_lines'] else 0
        elif args.command == "fetch":
            snapshot = fetch(args.manifest, args.output, timeout=args.timeout,
                             max_bytes=args.max_bytes, retries=args.retries)
            print(json.dumps({"snapshot": str(snapshot)}, ensure_ascii=False))
        elif args.command == "extract-all":
            from kb_sources.structure import extract_all, discover_snapshots
            report = extract_all(args.snapshot or discover_snapshots(args.sources), args.output)
            print(json.dumps({"output": str(args.output), "parsed": report["parsed"], "native": report["native"], "failed": report["failed"]}))
            return 1 if report['failed'] else 0
        elif args.command in ("extract-html", "extract"):
            from kb_sources.structure import extract_file
            document = extract_file(args.snapshot, args.file_id, args.output,
                                    expected_format='html' if args.command == 'extract-html' else None)
            print(json.dumps({"output": str(args.output), "headings": len(document['headings']),
                              "blocks": len(document['blocks']), "warnings": document['warnings']}, ensure_ascii=False))
        else:
            receipt = verify(args.snapshot)
            print(json.dumps({"snapshot": str(args.snapshot), "verified_files": len(receipt["files"])}, ensure_ascii=False))
    except (SourceError, OSError, ValueError) as exc:
        parser.exit(1, f"kb-sources: {exc}\n")
    return 0
