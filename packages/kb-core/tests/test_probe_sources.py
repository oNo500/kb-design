import hashlib
import json
import pathlib
import tempfile
import unittest
from datetime import date

from kb_core.probe_sources import (
    ALLOWED_METHODS,
    append_false_positive,
    classify_response,
    evaluate_unavailability,
    load_probe_endpoints,
    probe_due_endpoints,
    probe_repository,
    schedule_due,
    select_evidence,
)
from source_governance_helpers import materialized_current_layout

ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"
PROBE_FIXTURES = FIXTURES / "probe"


def load_response(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fixed_transport(response):
    def request(method, url):
        if method not in ALLOWED_METHODS:
            raise ValueError(method)
        return dict(response, requested_url=url, requested_method=method)

    return request


def endpoint_transport(responses):
    def request(method, url):
        if method not in ALLOWED_METHODS:
            raise ValueError(method)
        return dict(responses[url], requested_url=url, requested_method=method)

    return request


def tree_hash(root):
    digest = hashlib.sha256()
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def failure_series(*dates):
    return [
        {
            "id": f"failure-{index}",
            "observed_at": value,
            "signal": "temporarily_unavailable",
            "available": False,
        }
        for index, value in enumerate(dates, 1)
    ]


def evidence_observation(role):
    return {
        "id": f"evidence-{role}",
        "observed_at": "2026-08-31",
        "role": role,
        "available": True,
    }


def evidence_series(*roles):
    return [evidence_observation(role) for role in roles]


class ProbeSourcesTests(unittest.TestCase):
    def run_case(self, name):
        response = load_response(PROBE_FIXTURES / name)
        with materialized_current_layout(PROBE_FIXTURES / "root") as root:
            with tempfile.TemporaryDirectory() as tmp:
                before = tree_hash(root)
                result = probe_repository(
                    root,
                    pathlib.Path(tmp),
                    fixed_transport(response),
                    date(2026, 8, 31),
                    {},
                )
                self.assertEqual(before, tree_hash(root))
                return result

    def test_address_change_only_requests_review(self):
        self.assertEqual(
            "address_change", self.run_case("address-change.json")["signals"][0]
        )

    def test_content_change_only_requests_review(self):
        self.assertEqual(
            "content_change", self.run_case("content-change.json")["signals"][0]
        )

    def test_new_version_only_requests_review(self):
        self.assertEqual(
            "new_version", self.run_case("new-version.json")["signals"][0]
        )

    def test_replacement_only_requests_review(self):
        self.assertEqual(
            "replacement", self.run_case("replacement.json")["signals"][0]
        )

    def test_withdrawal_signal_does_not_set_formal_status(self):
        self.assertNotIn("status", self.run_case("withdrawal.json"))

    def test_temporary_unavailability_does_not_block_release(self):
        self.assertFalse(
            self.run_case("temporarily-unavailable.json")["release_blocked"]
        )

    def test_transport_allows_only_head_and_get(self):
        self.assertEqual({"HEAD", "GET"}, set(ALLOWED_METHODS))

    def test_probe_never_writes_formal_root(self):
        self.run_case("content-change.json")

    def test_monthly_and_quarterly_schedule_boundaries(self):
        self.assertTrue(schedule_due(date(2026, 7, 31), 1, date(2026, 8, 31)))
        self.assertFalse(schedule_due(date(2026, 6, 1), 3, date(2026, 8, 31)))
        self.assertTrue(schedule_due(date(2026, 5, 31), 3, date(2026, 8, 31)))

    def test_semiannual_and_annual_schedule_boundaries(self):
        self.assertTrue(schedule_due(date(2026, 2, 28), 6, date(2026, 8, 31)))
        self.assertTrue(schedule_due(date(2025, 8, 31), 12, date(2026, 8, 31)))

    def test_three_failures_under_fourteen_days_do_not_block(self):
        observations = failure_series("2026-08-18", "2026-08-24", "2026-08-30")
        self.assertFalse(
            evaluate_unavailability(observations, date(2026, 8, 31), False)
        )

    def test_three_distinct_failures_spanning_fourteen_days_block_when_unreproducible(
        self,
    ):
        observations = failure_series("2026-08-17", "2026-08-24", "2026-08-31")
        self.assertTrue(
            evaluate_unavailability(observations, date(2026, 8, 31), False)
        )

    def test_duplicate_day_is_not_an_independent_observation(self):
        observations = failure_series("2026-08-17", "2026-08-17", "2026-08-31")
        self.assertFalse(
            evaluate_unavailability(observations, date(2026, 8, 31), False)
        )

    def test_evidence_priority_is_status_doi_archive_mirror(self):
        selected = select_evidence(evidence_series("mirror", "archive", "doi", "status"))
        self.assertEqual("status", selected["role"])

    def test_available_official_evidence_prevents_unavailability_block(self):
        observations = failure_series("2026-08-17", "2026-08-24", "2026-08-31")
        observations.append(evidence_observation("doi"))
        self.assertFalse(
            evaluate_unavailability(observations, date(2026, 8, 31), False)
        )

    def test_url_roles_create_real_evidence_endpoints(self):
        with materialized_current_layout(PROBE_FIXTURES / "root") as root:
            endpoints = load_probe_endpoints(root, [])
        evidence_roles = {
            row["role"] for row in endpoints if row["purpose"] == "evidence"
        }
        self.assertEqual(
            {"status", "doi", "landing", "archive", "mirror"}, evidence_roles
        )

    def test_production_probe_selects_highest_priority_collected_evidence(self):
        with materialized_current_layout(PROBE_FIXTURES / "root") as root:
            endpoints = load_probe_endpoints(root, [])
            responses = {
                row["locator"]: {"available": True, "status_code": 200}
                for row in endpoints
            }
            with tempfile.TemporaryDirectory() as tmp:
                result = probe_repository(
                    root,
                    pathlib.Path(tmp),
                    endpoint_transport(responses),
                    date(2026, 8, 31),
                    {},
                )
        self.assertEqual("status", result["selected_evidence"]["z39-19"]["role"])

    def test_missing_publisher_version_does_not_signal_new_version(self):
        endpoint = {"locator": "https://example.test", "previous_version": "2005"}
        self.assertNotIn("new_version", classify_response(endpoint, {"available": True}))

    def test_equal_publisher_version_does_not_signal_new_version(self):
        endpoint = {"locator": "https://example.test", "previous_version": "2005"}
        response = {"available": True, "publisher_version": "2005"}
        self.assertNotIn("new_version", classify_response(endpoint, response))

    def test_explicit_different_publisher_version_signals_new_version(self):
        endpoint = {"locator": "https://example.test", "previous_version": "2005"}
        response = {"available": True, "publisher_version": "2010"}
        self.assertIn("new_version", classify_response(endpoint, response))

    def test_false_positive_is_appended_and_preserves_prior_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "observations.jsonl"
            path.write_text('{"id":"probe-1"}\n', encoding="utf-8")
            row = append_false_positive(
                path,
                "probe-1",
                "2026-08-31T12:00:00Z",
                "human",
                "dynamic navigation",
            )
            self.assertEqual("false_positive", row["classification"])
            self.assertEqual(2, len(path.read_text(encoding="utf-8").splitlines()))

    def test_observation_sequence_links_previous_id(self):
        previous = [
            {
                "id": "probe-old",
                "entity": "z39-19",
                "signal": "content_change",
                "observed_at": "2026-07-31",
            }
        ]
        endpoint = {
            "entity": "z39-19",
            "locator": "https://example.test/z39",
            "role": "status",
            "signal": "content_change",
            "previous_version": "2005",
        }
        response = {
            "available": True,
            "content_changed": True,
            "publisher_version": "2010",
        }
        rows = probe_due_endpoints(
            [endpoint], previous, fixed_transport(response), date(2026, 8, 31)
        )
        self.assertEqual("probe-old", rows[0]["previous"])


if __name__ == "__main__":
    unittest.main()
