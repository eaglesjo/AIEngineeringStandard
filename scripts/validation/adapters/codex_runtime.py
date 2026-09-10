#!/usr/bin/env python3
"""Codex runtime adapter for the AIEngineeringStandard 2.0 harness.

The adapter uses Codex's documented non-interactive ``codex exec`` surface.
The conformance probe explicitly selects read-only sandboxing; the standard
never relies on an implicit or user-overridden permission profile.
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

    # The conformance baseline is deliberately fixed to read-only. This avoids
    # accepting an environment variable that could silently widen permissions.
    # The upstream Codex CLI exposes --sandbox/-s with a read-only mode.
    parts = [binary, "exec", "--ephemeral", "--sandbox", "read-only", "{prompt}"]
    command = shlex.join(parts)

    print(f"Codex executable: {binary}")
    print(f"Codex runtime version: {runtime_version}")
    print(f"Harness scenario: {args.scenario}")
    print("Sandbox baseline: read-only (explicitly requested by adapter)")
    print("Network baseline: not widened by adapter; runtime configuration remains observable")

    return run_harness(args, command, runtime_version)


if __name__ == "__main__":
    raise SystemExit(main())
