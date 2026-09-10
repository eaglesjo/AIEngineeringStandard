#!/usr/bin/env python3
"""Deterministic contract checks for the vendor-neutral runtime adapter boundary."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "core" / "validation" / "adapter-contract.md"
ADAPTER = ROOT / "scripts" / "validation" / "adapters" / "codex_runtime.py"
PROVENANCE = ROOT / "core" / "validation" / "evidence-provenance-policy.md"


def main() -> int:
    contract = CONTRACT.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    provenance = PROVENANCE.read_text(encoding="utf-8")

    required_contract_terms = (
        "discovery",
        "version",
        "invocation",
        "event parsing",
        "capability mapping",
        "evidence handoff",
        "UNTESTED",
        "NOT_OBSERVED",
        "PASS",
    )
    for term in required_contract_terms:
        assert term in contract, term

    required_adapter_markers = (
        "def executable(",
        "def version(",
        "codex exec --json",
        "--sandbox",
        "read-only",
        "--ephemeral",
        "run_runtime_conformance.py",
    )
    for marker in required_adapter_markers:
        assert marker in adapter, marker

    required_provenance_terms = (
        "standard_version",
        "runtime version/identity",
        "repository revision",
        "scenario ID",
        "timestamps",
        "check-level results",
        "observation source",
        "VERIFIED",
    )
    for term in required_provenance_terms:
        assert term in provenance, term

    print("Runtime adapter contract tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
