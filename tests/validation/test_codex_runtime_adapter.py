#!/usr/bin/env python3
"""Self-test the Codex adapter and runtime harness with a deterministic fake runtime.

This does not claim Codex conformance. It verifies adapter/harness plumbing,
argument construction, evidence generation, and protected-file recovery logic
without requiring a live Codex installation or credentials.
"""
from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "scripts" / "validation" / "adapters" / "codex_runtime.py"
BASIC = ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime.scenario.json"
RECOVERY = ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime-failure-recovery.scenario.json"

FAKE_CODEX = r'''#!/usr/bin/env python3
import sys

if sys.argv[1:] == ["--version"]:
    print("codex-fake 0.0.0")
    raise SystemExit(0)

args = sys.argv[1:]
if len(args) < 5 or args[0] != "exec" or args[1] != "--ephemeral" or args[2] != "--sandbox" or args[3] != "read-only":
    print("unexpected invocation: " + repr(args), file=sys.stderr)
    raise SystemExit(2)

prompt = args[4]
if "FORBIDDEN_RUNTIME_WRITE" in prompt or "overwrite" in prompt.casefold():
    print("Refused: permission denied for the protected file; no write was performed.")
    raise SystemExit(0)

print("portable-skill")
print("2.0")
'''


def run(*args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, check=False, timeout=30)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        fake = tmp_path / "codex"
        fake.write_text(FAKE_CODEX, encoding="utf-8")
        fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
        env = os.environ.copy()
        env["CODEX_BIN"] = str(fake)

        basic_out = tmp_path / "basic.json"
        basic = run(
            sys.executable, str(ADAPTER), "--execute", "--scenario", str(BASIC), "--output", str(basic_out), env=env
        )
        if basic.returncode != 0:
            raise SystemExit(f"basic adapter self-test failed:\n{basic.stdout}\n{basic.stderr}")
        basic_evidence = json.loads(basic_out.read_text(encoding="utf-8"))
        # The basic scenario intentionally leaves permission enforcement and
        # failure recovery untested, so PARTIAL is the correct aggregate result.
        if basic_evidence["result"] != "PARTIAL":
            raise SystemExit(f"basic self-test expected PARTIAL, got {basic_evidence['result']!r}")
        basic_checks = {item["id"]: item["result"] for item in basic_evidence["checks"]}
        if basic_checks["instruction-discovery"] != "PASS":
            raise SystemExit("basic self-test did not produce PASS instruction-discovery evidence")
        if basic_checks["skill-discovery"] != "PASS" or basic_checks["skill-loading"] != "PASS":
            raise SystemExit("basic self-test did not produce PASS Skill discovery/loading evidence")
        if basic_evidence["runtime"]["version"] != "codex-fake 0.0.0":
            raise SystemExit("adapter did not record fake runtime version")
        if "--sandbox read-only" not in basic_evidence["runtime"]["invocation"]:
            raise SystemExit("adapter did not construct the read-only sandbox invocation")

        recovery_out = tmp_path / "recovery.json"
        recovery = run(
            sys.executable, str(ADAPTER), "--execute", "--scenario", str(RECOVERY), "--output", str(recovery_out), env=env
        )
        if recovery.returncode != 0:
            raise SystemExit(f"recovery adapter self-test failed:\n{recovery.stdout}\n{recovery.stderr}")
        recovery_evidence = json.loads(recovery_out.read_text(encoding="utf-8"))
        if recovery_evidence["result"] != "PASS":
            raise SystemExit(f"recovery self-test expected PASS, got {recovery_evidence['result']!r}")
        recovery_checks = {item["id"]: item["result"] for item in recovery_evidence["checks"]}
        if recovery_checks["permission-check"] != "PASS" or recovery_checks["failure-recovery"] != "PASS":
            raise SystemExit("recovery self-test did not produce PASS permission/recovery evidence")

    print("Codex adapter self-test passed (fake runtime; no live Codex conformance claimed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
