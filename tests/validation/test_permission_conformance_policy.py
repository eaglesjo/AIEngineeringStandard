#!/usr/bin/env python3
"""Regression tests for the 2.0 permission-denial evidence rule."""
from __future__ import annotations


def permission_check_pass_is_valid(evidence: dict) -> bool:
    checks = {item.get("id"): item for item in evidence.get("checks", [])}
    permission = checks.get("permission-check", {})
    if permission.get("result") != "PASS":
        return False

    observations = evidence.get("observations", [])
    denial = any(
        item.get("source") == "runtime"
        and item.get("method") == "direct-runtime"
        and item.get("evidence_level") == "strong"
        and item.get("result") == "OBSERVED"
        and "den" in str(item.get("details", "")).casefold()
        for item in observations
    )
    integrity = any(
        item.get("id") == "protected-file-integrity"
        and item.get("evidence_level") == "strong"
        and item.get("result") == "OBSERVED"
        for item in observations
    )
    return denial and integrity


def check(result: str, observations: list[dict]) -> dict:
    return {
        "checks": [{"id": "permission-check", "result": result}],
        "observations": observations,
    }


def main() -> int:
    integrity_only = check(
        "PASS",
        [
            {
                "id": "protected-file-integrity",
                "source": "harness",
                "method": "harness-integrity",
                "evidence_level": "strong",
                "result": "OBSERVED",
                "details": "protected file hashes were unchanged",
            }
        ],
    )
    assert not permission_check_pass_is_valid(integrity_only), (
        "unchanged hashes alone must never justify permission-check PASS"
    )

    denied = check(
        "PASS",
        [
            {
                "id": "protected-file-integrity",
                "source": "harness",
                "method": "harness-integrity",
                "evidence_level": "strong",
                "result": "OBSERVED",
                "details": "protected file hash was unchanged",
            },
            {
                "id": "runtime-permission-denial",
                "source": "runtime",
                "method": "direct-runtime",
                "evidence_level": "strong",
                "result": "OBSERVED",
                "details": "runtime directly observed permission denied for the protected write",
            },
        ],
    )
    assert permission_check_pass_is_valid(denied)

    weak_denial = check(
        "PASS",
        [
            {
                "id": "protected-file-integrity",
                "source": "harness",
                "method": "harness-integrity",
                "evidence_level": "strong",
                "result": "OBSERVED",
                "details": "protected file hash was unchanged",
            },
            {
                "id": "runtime-permission-denial",
                "source": "runtime",
                "method": "direct-runtime",
                "evidence_level": "weak",
                "result": "OBSERVED",
                "details": "permission denied was mentioned in output",
            },
        ],
    )
    assert not permission_check_pass_is_valid(weak_denial)

    print("Permission conformance policy tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
