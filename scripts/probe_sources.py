#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.source_model import add_calendar_months

ALLOWED_METHODS = frozenset(("HEAD", "GET"))
FORMAL_FIELDS = frozenset(
    ("url", "urls", "version", "status", "review", "roles", "basis", "source", "match")
)
EVIDENCE_PRIORITY = {"status": 0, "doi": 1, "landing": 1, "archive": 2, "mirror": 3}
EVIDENCE_ROLES = frozenset(EVIDENCE_PRIORITY)
WATCH_SIGNALS = {
    "availability": "temporarily_unavailable",
    "redirect": "address_change",
    "version": "new_version",
    "revision": "content_change",
    "replacement": "replacement",
    "withdrawal": "withdrawal",
}


def parse_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(value[:10])


def load_observation_sequence(path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def observation_id(entity, signal, endpoint, observed_at):
    identity = f"{entity}\t{signal}\t{endpoint}\t{observed_at}".encode("utf-8")
    return "probe-" + hashlib.sha256(identity).hexdigest()[:24]


def previous_observation_id(rows, entity, signal):
    matches = [
        row
        for row in rows
        if row.get("entity") == entity and row.get("signal") == signal
    ]
    return matches[-1]["id"] if matches else None


def response_requires_body(response):
    return response.get("available", False) and not (
        response.get("publisher_version")
        or response.get("locator_fragment")
        or response.get("withdrawal")
        or response.get("replacement")
    )


def classify_response(endpoint, response):
    if not response.get("available", False):
        return ["temporarily_unavailable"]

    signals = []
    if response.get("redirect") and response["redirect"] != endpoint["locator"]:
        signals.append("address_change")
    if response.get("content_changed"):
        signals.append("content_change")
    if (
        "publisher_version" in response
        and response["publisher_version"] != endpoint.get("previous_version")
    ):
        signals.append("new_version")
    if response.get("replacement"):
        signals.append("replacement")
    if response.get("withdrawal"):
        signals.append("withdrawal")
    return signals


def sanitize_response(response):
    allowed = (
        "available",
        "status_code",
        "redirect",
        "etag",
        "last_modified",
        "publisher_version",
        "replacement",
        "withdrawal",
        "error",
    )
    return {key: response[key] for key in allowed if key in response}


def content_fingerprint(endpoint, response):
    if response.get("publisher_version"):
        return {
            "method": "publisher_version",
            "value": response["publisher_version"],
            "confidence": "high",
        }
    if response.get("locator_fragment"):
        normalized = " ".join(response["locator_fragment"].split())
        return {
            "method": "locator_fragment_sha256",
            "value": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
            "confidence": "medium",
        }
    normalized = " ".join(response.get("body", "").split())
    return {
        "method": "whole_page_sha256",
        "value": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
        "confidence": "low",
    }


def probe_due_endpoints(endpoints, previous, transport, today):
    rows = []
    ordered = sorted(
        endpoints,
        key=lambda row: (
            row["entity"],
            row["locator"],
            row.get("purpose", "signal"),
            row.get("signal", ""),
        ),
    )
    for endpoint in ordered:
        response = transport("HEAD", endpoint["locator"])
        if response_requires_body(response):
            response = transport("GET", endpoint["locator"])

        if endpoint.get("purpose", "signal") == "evidence":
            observed_at = today.isoformat()
            rows.append(
                {
                    "id": observation_id(
                        endpoint["entity"], "evidence", endpoint["locator"], observed_at
                    ),
                    "observed_at": observed_at,
                    "entity": endpoint["entity"],
                    "endpoint": endpoint["locator"],
                    "role": endpoint["role"],
                    "signal": "evidence",
                    "available": response.get("available", False),
                    "previous": previous_observation_id(
                        previous + rows, endpoint["entity"], "evidence"
                    ),
                    "response": sanitize_response(response),
                }
            )
            continue

        expected_signal = WATCH_SIGNALS.get(endpoint["signal"], endpoint["signal"])
        for signal in classify_response(endpoint, response):
            if signal != expected_signal:
                continue
            observed_at = today.isoformat()
            row = {
                "id": observation_id(
                    endpoint["entity"], signal, endpoint["locator"], observed_at
                ),
                "observed_at": observed_at,
                "entity": endpoint["entity"],
                "endpoint": endpoint["locator"],
                "role": endpoint["role"],
                "signal": signal,
                "available": response.get("available", False),
                "previous": previous_observation_id(
                    previous + rows, endpoint["entity"], signal
                ),
                "response": sanitize_response(response),
            }
            if signal == "content_change":
                row.update(content_fingerprint(endpoint, response))
            rows.append(row)
    return rows


def hash_formal_tree(root):
    digest = hashlib.sha256()
    for directory in ("design", "scripts", "vocab"):
        formal_dir = root / directory
        if not formal_dir.exists():
            continue
        for path in sorted(formal_dir.rglob("*")):
            if path.is_file():
                digest.update(str(path.relative_to(root)).encode("utf-8"))
                digest.update(path.read_bytes())
    return digest.hexdigest()


def last_observed_date(previous, entity, signal):
    dates = [
        parse_date(row["observed_at"])
        for row in previous
        if row.get("entity") == entity and row.get("signal") == signal
    ]
    return max(dates) if dates else date(1970, 1, 1)


def unique_endpoints(rows):
    unique = {}
    for row in rows:
        key = (
            row["entity"],
            row["purpose"],
            row["role"],
            row["signal"],
            row["locator"],
        )
        unique[key] = row
    return list(unique.values())


def load_probe_endpoints(root, previous):
    document = yaml.safe_load((root / "vocab/entities.yaml").read_text(encoding="utf-8"))
    rows = []
    for entity in document["entities"]:
        url_roles = {row["url"]: row["role"] for row in entity.get("urls", [])}
        for address in entity.get("urls", []):
            if address["role"] not in EVIDENCE_ROLES:
                continue
            rows.append(
                {
                    "entity": entity["id"],
                    "locator": address["url"],
                    "role": address["role"],
                    "purpose": "evidence",
                    "signal": "evidence",
                    "last_observed": last_observed_date(
                        previous, entity["id"], "evidence"
                    ),
                    "cadence_months": 1,
                    "previous_version": entity.get("version"),
                }
            )
        for watch in entity.get("watch", []):
            for watch_signal in watch["signals"]:
                if watch_signal not in WATCH_SIGNALS:
                    raise ValueError(f"unsupported watch signal: {watch_signal}")
                cadence_key = (
                    watch_signal
                    if watch_signal in ("availability", "redirect")
                    else "content"
                )
                signal = WATCH_SIGNALS[watch_signal]
                rows.append(
                    {
                        "entity": entity["id"],
                        "locator": watch["locator"],
                        "role": url_roles.get(watch["locator"], "watch"),
                        "purpose": "signal",
                        "signal": signal,
                        "last_observed": last_observed_date(
                            previous, entity["id"], signal
                        ),
                        "cadence_months": watch["cadence_months"][cadence_key],
                        "previous_version": entity.get("version"),
                    }
                )
    return sorted(
        unique_endpoints(rows),
        key=lambda row: (
            row["entity"],
            row["purpose"],
            row["role"],
            row["signal"],
            row["locator"],
        ),
    )


def group_by_entity(observations):
    grouped = {}
    for row in observations:
        grouped.setdefault(row["entity"], []).append(row)
    return grouped


def schedule_due(last_observed, cadence_months, today):
    return today >= add_calendar_months(last_observed, cadence_months)


def select_evidence(observations):
    candidates = [
        row
        for row in observations
        if row.get("available") and row.get("role") in EVIDENCE_PRIORITY
    ]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda row: (
            EVIDENCE_PRIORITY[row["role"]],
            row["observed_at"],
            row["role"],
            row["id"],
        ),
    )


def evaluate_unavailability(observations, today, human_reproducible):
    failures = sorted(
        {
            parse_date(row["observed_at"])
            for row in observations
            if row.get("signal") == "temporarily_unavailable"
            and parse_date(row["observed_at"]) <= today
        }
    )
    spans_fourteen = len(failures) >= 3 and (failures[-1] - failures[0]).days >= 14
    return (
        spans_fourteen
        and select_evidence(observations) is None
        and not human_reproducible
    )


def summarize_observations(observations, today, human_reproducible):
    by_entity = group_by_entity(observations)
    blocked = sorted(
        entity
        for entity, rows in by_entity.items()
        if evaluate_unavailability(
            rows, today, human_reproducible.get(entity, False)
        )
    )
    review_rows = [row for row in observations if row.get("signal") != "evidence"]
    return {
        "signals": sorted({row["signal"] for row in review_rows}),
        "needs_review": sorted({row["entity"] for row in review_rows}),
        "release_blocked": bool(blocked),
        "blocked_entities": blocked,
        "selected_evidence": {
            entity: selected
            for entity, rows in by_entity.items()
            if (selected := select_evidence(rows)) is not None
        },
    }


def write_observations(output_dir, observations, summary):
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "observations.jsonl").open("a", encoding="utf-8") as stream:
        for row in observations:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def append_false_positive(path, observation_id, classified_at, reviewer, reason):
    row = {
        "observation": observation_id,
        "classification": "false_positive",
        "classified_at": classified_at,
        "reviewer": reviewer,
        "reason": reason,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return row


def probe_repository(root, output_dir, transport, today, human_reproducible):
    before = hash_formal_tree(root)
    previous = load_observation_sequence(output_dir / "observations.jsonl")
    due = [
        endpoint
        for endpoint in load_probe_endpoints(root, previous)
        if schedule_due(endpoint["last_observed"], endpoint["cadence_months"], today)
    ]
    observations = probe_due_endpoints(due, previous, transport, today)
    result = summarize_observations(previous + observations, today, human_reproducible)
    write_observations(output_dir, observations, result)
    if before != hash_formal_tree(root):
        raise RuntimeError("probe modified formal repository")
    if FORMAL_FIELDS.intersection(result):
        raise RuntimeError("probe result contains formal fields")
    return {"observations": previous + observations, **result}


def fixture_transport(fixture_dir, fixture_response):
    response = json.loads(
        (fixture_dir / fixture_response).read_text(encoding="utf-8")
    )

    def request(method, url):
        if method not in ALLOWED_METHODS:
            raise ValueError(method)
        return dict(response, requested_url=url, requested_method=method)

    return request


def build_parser():
    parser = argparse.ArgumentParser(description="Run isolated source probes")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--fixture-dir", type=Path, required=True)
    parser.add_argument("--fixture-response", default="content-change.json")
    parser.add_argument("--human-reproducible-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--live", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.live:
        raise SystemExit("live transport is not available in fixture-only probe runs")
    human_reproducible = json.loads(
        args.human_reproducible_file.read_text(encoding="utf-8")
    )
    result = probe_repository(
        args.root,
        args.output,
        fixture_transport(args.fixture_dir, args.fixture_response),
        args.today,
        human_reproducible,
    )
    print(
        json.dumps(
            {
                "observations": len(result["observations"]),
                "signals": result["signals"],
                "release_blocked": result["release_blocked"],
                "output": str(args.output),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
