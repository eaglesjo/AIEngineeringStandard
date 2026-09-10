#!/usr/bin/env python3
"""Codex runtime adapter for the AIEngineeringStandard 2.0 harness.

The adapter intentionally does not guess authentication, sandbox, or permission
settings. The caller supplies the Codex executable and its execution arguments.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / "scripts" / "validation" / "run_runtime_conformance.py"
DEFAULT_SCENARIO = ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime.scenario.json"


def executable() -> str:
    value = os.environ.get("CODEX_BIN", "codex")
    resolved = shutil.which(value)
    if not resolved:
        raise SystemExit(f"ERROR: Codex executable not found: {value}. Set CODEX_BIN to the runtime executable.")
    return resolved


def version(binary: str) -> str:
    proc = subprocess.run([binary, "--version"], cwd=ROOT, capture_output=True, text=True, check=False)
    output = (proc.stdout or proc.stderr).strip()
    if proc.returncode != 0 or not output:
        raise SystemExit("ERROR: unable to determine Codex runtime version with --version")
    return output.splitlines()[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Invoke the AIEngineeringStandard 2.0 Codex runtime adapter.")
    parser.add_argument("--scenario", default=str(DEFAULT_SCENARIO))
    parser.add_argument("--output", default="/tmp/codex-runtime-conformance.json")
    parser.add_argument("--execute", action="store_true", help="Invoke the configured Codex runtime")
    args = parser.parse_args()

    binary = executable()
    runtime_version = version(binary)
    # CODEX_RUNTIME_ARGS is intentionally caller-controlled. The harness still
    # bounds execution and records the exact invocation in its evidence output.
    runtime_args = os.environ.get("CODEX_RUNTIME_ARGS", "").strip()
    command = " ".join([binary, runtime_args, "{prompt}"]).strip()

    print(f"Codex executable: {binary}")
    print(f"Codex runtime version: {runtime_version}")
    print(f"Harness scenario: {args.scenario}")
    print(f"Runtime arguments source: CODEX_RUNTIME_ARGS={'set' if runtime_args else 'empty'}")

    cmd = [
        sys.executable, str(HARNESS),
        "--agent", "codex",
        "--scenario", args.scenario,
        "--runtime-version", runtime_version,
        "--command", command,
        "--output", args.output,
    ]
    if args.execute:
        cmd.append("--execute")
    return subprocess.run(cmd, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
