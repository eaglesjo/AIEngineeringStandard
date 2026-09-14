#!/usr/bin/env python3
"""Validate vendor-neutral reproducibility evidence and artifact identity."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "core/validation/reproducibility.schema.json"


def fail(message: str) -> None:
    print(f"Reproducibility validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_schema() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("contract must use JSON Schema Draft 2020-12")
    if schema.get("properties", {}).get("schema_version", {}).get("const") != "2.0.0":
        fail("contract schema_version must be 2.0.0")


def validate_contract(document: dict) -> None:
    if not isinstance(document, dict) or document.get("schema_version") != "2.0.0":
        fail("schema_version must be 2.0.0")
    for field in ("task_id", "experiment", "artifacts", "acceptance"):
        if field not in document:
            fail(f"missing required field: {field}")
    experiment = document["experiment"]
    required = ("experiment_id", "variant", "seed", "config_hash", "git_revision", "dirty")
    if any(key not in experiment for key in required):
        fail("experiment identity is incomplete")
    if experiment["dirty"]:
        fail("reproducibility evidence cannot be accepted from a dirty revision")
    artifacts = document["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        fail("artifacts must be a non-empty array")
    ids = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            fail("each artifact must be an object")
        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, str) or not artifact_id.strip() or artifact_id in ids:
            fail("artifact ids must be unique, non-empty strings")
        ids.add(artifact_id)
        digest = artifact.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            fail(f"invalid sha256 artifact identity: {artifact_id}")
        if not isinstance(artifact.get("source"), str) or not artifact["source"].strip():
            fail(f"artifact source is required: {artifact_id}")
    acceptance = document["acceptance"]
    if acceptance.get("status") == "REPRODUCIBLE" and experiment["dirty"]:
        fail("REPRODUCIBLE requires a clean revision")
    if acceptance.get("status") not in {"REPRODUCIBLE", "NOT_REPRODUCIBLE", "INCOMPLETE"}:
        fail("invalid acceptance status")
    if not isinstance(acceptance.get("basis"), str) or not acceptance["basis"].strip():
        fail("acceptance basis is required")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    validate_schema()
    sample = {
        "schema_version": "2.0.0",
        "task_id": "validation-fixture",
        "experiment": {
            "experiment_id": "fixture-experiment",
            "variant": "baseline",
            "seed": 42,
            "config_hash": sha256_text("{}")[:16],
            "model_revision": "model-r1",
            "dataset_revision": "dataset-r1",
            "environment_profile": "python-3.11",
            "git_revision": "abcdef1234567",
            "dirty": False,
        },
        "artifacts": [{
            "id": "input-1",
            "kind": "input",
            "sha256": sha256_text("fixture-input"),
            "source": "fixture",
            "revision": "r1",
        }],
        "acceptance": {"status": "REPRODUCIBLE", "basis": "complete identity metadata and immutable artifact digest"},
    }
    validate_contract(sample)
    print("Reproducibility contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
