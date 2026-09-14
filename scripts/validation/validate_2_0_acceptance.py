#!/usr/bin/env python3
"""Validate that the four 2.0 evidence areas refer to one clean candidate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    print(f"2.0 acceptance validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate(document: dict) -> None:
    if document.get("schema_version") != "2.0.0":
        fail("schema_version must be 2.0.0")
    candidate = document.get("candidate", {})
    revision = candidate.get("revision")
    if not isinstance(revision, str) or len(revision) < 7 or candidate.get("dirty") is not False:
        fail("candidate must identify a clean revision")
    areas = document.get("areas", {})
    required = ("code_quality", "evaluation", "provenance", "reproducibility")
    if any(name not in areas for name in required):
        fail("all four acceptance areas are required")

    quality = areas["code_quality"]
    if quality.get("candidate", {}).get("revision") != revision or quality.get("candidate", {}).get("dirty") is not False:
        fail("code quality evidence does not match candidate")
    if quality.get("acceptance", {}).get("status") != "ACCEPTED":
        fail("code quality evidence is not accepted")
    if any(check.get("result") != "PASS" for check in quality.get("checks", [])):
        fail("code quality contains a non-PASS check")

    evaluation = areas["evaluation"]
    if evaluation.get("acceptance", {}).get("status") != "ACCEPTED":
        fail("evaluation evidence is not accepted")
    if evaluation.get("evaluation", {}).get("deterministic") is not True:
        fail("evaluation must be deterministic for the 2.0 gate")
    threshold = evaluation.get("acceptance", {}).get("threshold")
    scores = [case.get("score") for case in evaluation.get("cases", [])]
    if not scores or any(not isinstance(score, (int, float)) for score in scores):
        fail("evaluation cases must contain numeric scores")
    if sum(scores) / len(scores) < threshold:
        fail("evaluation overall score is below threshold")

    provenance = areas["provenance"]
    if provenance.get("repository", {}).get("revision") != revision:
        fail("provenance revision does not match candidate")
    if provenance.get("result") != "PASS":
        fail("provenance result is not PASS")
    trace = provenance.get("trace", {})
    if not trace.get("action_id") or not trace.get("evidence_id"):
        fail("provenance trace identity is incomplete")
    if not any(obs.get("result") == "OBSERVED" and obs.get("evidence_level") in {"moderate", "strong"} for obs in provenance.get("observations", [])):
        fail("provenance lacks a trusted observation")

    reproducibility = areas["reproducibility"]
    experiment = reproducibility.get("experiment", {})
    if experiment.get("git_revision") != revision or experiment.get("dirty") is not False:
        fail("reproducibility revision does not match candidate")
    if reproducibility.get("acceptance", {}).get("status") != "REPRODUCIBLE":
        fail("reproducibility evidence is not accepted")
    if not reproducibility.get("artifacts"):
        fail("reproducibility requires artifact identities")
    for artifact in reproducibility["artifacts"]:
        digest = artifact.get("sha256", "")
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            fail(f"invalid artifact digest: {artifact.get('id')}")

    if document.get("acceptance", {}).get("status") != "ACCEPTED":
        fail("overall acceptance is not ACCEPTED")
    if not isinstance(document.get("acceptance", {}).get("basis"), str) or not document["acceptance"]["basis"].strip():
        fail("overall acceptance basis is required")


def sample() -> dict:
    revision = "abcdef1234567890"
    digest = hashlib.sha256(b"fixture").hexdigest()
    return {
        "schema_version": "2.0.0",
        "candidate": {"revision": revision, "dirty": False},
        "areas": {
            "code_quality": {
                "candidate": {"revision": revision, "dirty": False},
                "checks": [{"result": "PASS"}],
                "acceptance": {"status": "ACCEPTED"}
            },
            "evaluation": {
                "evaluation": {"deterministic": True},
                "cases": [{"score": 1.0}],
                "acceptance": {"status": "ACCEPTED", "threshold": 1.0}
            },
            "provenance": {
                "repository": {"revision": revision},
                "result": "PASS",
                "trace": {"action_id": "a1", "evidence_id": "e1"},
                "observations": [{"result": "OBSERVED", "evidence_level": "strong"}]
            },
            "reproducibility": {
                "experiment": {"git_revision": revision, "dirty": False},
                "artifacts": [{"id": "x", "sha256": digest}],
                "acceptance": {"status": "REPRODUCIBLE"}
            }
        },
        "acceptance": {"status": "ACCEPTED", "basis": "all four areas match the same clean revision"}
    }


def main() -> int:
    validate(sample())
    print("2.0 cross-area acceptance validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
