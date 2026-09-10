#!/usr/bin/env python3
"""Codex runtime adapter for the AIEngineeringStandard 2.0 harness.

The adapter uses Codex's documented non-interactive ``codex exec`` surface.
Runtime-specific policy remains configurable and is never inferred by the
standard itself.
"""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / "scripts" / "validation" / "run_runtime_conformance.py"
DEFAULT_SCENARIO = ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime.scenario.json"


def executable() -> str | None:
    value = os.environ.get("CODEX_BIN", "codex")
    return shutil.which(value)


def version(binary: str) -> str | None:
    try:
        proc = subprocess.run([binary, "--version"], cwd=ROOT, capture_output=True, text=True, check=False, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (proc.stdout or proc.stderr).strip()
    if proc.returncode != 0 or not output:
        return None
    return output.splitlines()[0]


def run_harness(args: argparse.Namespace, command: str | None, runtime_version: str | None) -> int:
    cmd = [
        sys.executable, str(HARNESS),
        "--agent", "codex",
        "--scenario", args.scenario,
        "--runtime-version", runtime_version or "unavailable",
        "--output", args.output,
    ]
    if command:
        cmd.extend(["--command", command])
    if args.execute and command:
        cmd.append("--execute")
    return subprocess.run(cmd, cwd=ROOT, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Invoke the AIEngineeringStandard 2.0 Codex runtime adapter.")
    parser.add_argument("--scenario", default=str(DEFAULT_SCENARIO))
    parser.add_argument("--output", default="/tmp/codex-runtime-conformance.json")
    parser.add_argument("--execute", action="store_true", help="Invoke the configured Codex runtime")
    args = parser.parse_args()

    binary = executable()
    if not binary:
        print("Codex executable: unavailable")
        print("Result: UNTESTED (Codex runtime is not installed or CODEX_BIN is not resolvable)")
        return run_harness(args, None, None)

    runtime_version = version(binary)
    if not runtime_version:
        print(f"Codex executable: {binary}")
        print("Result: UNTESTED (Codex --version could not be determined)")
        return run_harness(args, None, None)

    # OpenAI documents ``codex exec`` for scripts/CI. It runs read-only by
    # default, which is the safest baseline for this conformance probe.
    # CODEX_RUNTIME_ARGS may add explicit, version-validated runtime settings.
    runtime_args = os.environ.get("CODEX_RUNTIME_ARGS", "").strip()
    parts = [binary, "exec", "--ephemeral"]
    if runtime_args:
        parts.extend(shlex.split(runtime_args))
    parts.append("{prompt}")
    command = shlex.join(parts)

    print(f"Codex executable: {binary}")
    print(f"Codex runtime version: {runtime_version}")
    print(f"Harness scenario: {args.scenario}")
    print(f"Runtime arguments source: CODEX_RUNTIME_ARGS={'set' if runtime_args else 'empty'}")
    print("Sandbox baseline: Codex exec default read-only")

    return run_harness(args, command, runtime_version)


if __name__ == "__main__":
    raise SystemExit(main())
