"""Command-line arguments for the local evaluation review workflow."""
from pathlib import Path
import json


def configure(commands):
    review = commands.add_parser(
        "review", help="review evaluation graphs; never adopts formal vocabulary data",
        description="Actor and authorization record operator statements, not authenticated identities.",
    )
    actions = review.add_subparsers(dest="review_command", required=True)
    scan = actions.add_parser("scan", help="scan all catalog sources into a new review store")
    scan.add_argument("--catalog", type=Path, required=True)
    scan.add_argument("--output", type=Path, required=True)
    scan.add_argument("--previous", type=Path)

    listing = actions.add_parser("list", help="list review records and current revision")
    listing.add_argument("store", type=Path)
    listing.add_argument("--status", choices=("pending", "accepted", "deferred", "rejected", "withdrawn", "needs_review"))
    listing.add_argument("--limit", type=int, default=20)
    show = actions.add_parser("show", help="inspect one record and its evidence")
    show.add_argument("store", type=Path)
    show.add_argument("record_id")

    propose = actions.add_parser("propose", help="record a mapping proposal without accepting it")
    propose.add_argument("store", type=Path)
    propose.add_argument("--subject", required=True)
    propose.add_argument("--object", required=True)
    propose.add_argument("--relation", choices=("exactMatch", "closeMatch", "broadMatch", "narrowMatch", "relatedMatch"), required=True)
    decide = actions.add_parser("decide", help="record an operator decision with explicit authorization")
    decide.add_argument("store", type=Path)
    decide.add_argument("record_id")
    decide.add_argument("--decision", choices=("accepted", "deferred", "rejected", "withdrawn"), required=True)
    decide.add_argument("--authorization", required=True, help="operator's authorization statement; not identity authentication")
    batch = actions.add_parser("decide-batch", help="record all decisions in one event, or reject the whole batch")
    batch.add_argument("store", type=Path)
    batch.add_argument("--decisions-file", type=Path, required=True, help="JSON array of objects with id and decision")
    batch.add_argument("--authorization", required=True, help="operator's authorization statement; not identity authentication")
    for action in (propose, decide, batch):
        action.add_argument("--reason", required=True)
        action.add_argument("--actor", required=True)
        action.add_argument("--expected-revision", required=True)

    preview = actions.add_parser("preview", help="preview a batch without recording decisions")
    preview.add_argument("store", type=Path)
    preview.add_argument("--decisions-file", type=Path, required=True)

    build = actions.add_parser("build", help="build accepted evaluation mappings into a new directory")
    build.add_argument("store", type=Path)
    build.add_argument("--output", type=Path, required=True)


def execute(args):
    from kb_vocab import review

    if args.review_command == "preview":
        return review.preview(args.store, json.loads(args.decisions_file.read_text(encoding="utf-8")))
    if args.review_command == "scan":
        return review.scan(args.catalog, args.output, previous=args.previous)
    if args.review_command == "list":
        return review.inspect(args.store, status=args.status, limit=args.limit)
    if args.review_command == "show":
        return review.inspect(args.store, record_id=args.record_id)
    if args.review_command == "propose":
        return review.propose(args.store, subject=args.subject, object=args.object,
                              predicate=args.relation, reason=args.reason, actor=args.actor,
                              expected_revision=args.expected_revision)
    if args.review_command == "decide":
        return review.decide(args.store, record_id=args.record_id, decision=args.decision,
                             actor=args.actor, authorization=args.authorization, reason=args.reason,
                             expected_revision=args.expected_revision)
    if args.review_command == "decide-batch":
        decisions = json.loads(args.decisions_file.read_text(encoding="utf-8"))
        return review.decide_batch(args.store, decisions=decisions, actor=args.actor,
                                   authorization=args.authorization, reason=args.reason,
                                   expected_revision=args.expected_revision)
    return review.build(args.store, args.output)
