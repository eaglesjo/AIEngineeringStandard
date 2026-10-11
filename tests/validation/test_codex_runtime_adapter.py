#!/usr/bin/env python3
"""Self-test the Codex adapter and runtime harness with a deterministic fake runtime.

This does not claim Codex conformance. It verifies adapter/harness plumbing,
JSONL event observation, argument construction, evidence generation, and
protected-file recovery logic without requiring a live Codex installation.
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
import json
import sys

if sys.argv[1:] == ["--version"]:
    print("codex-fake 0.0.0")
    raise SystemExit(0)

args = sys.argv[1:]
if len(args) < 6 or args[:5] != ["exec", "--json", "--ephemeral", "--sandbox", "read-only"]:
    print("unexpected invocation: " + repr(args), file=sys.stderr)
    raise SystemExit(2)

prompt = args[5]
print(json.dumps({"type": "thread.started", "thread_id": "fake-thread"}))
print(json.dumps({"type": "turn.started", "turn_id": "fake-turn"}))

if "FORBIDDEN_RUNTIME_WRITE" in prompt or "overwrite" in prompt.casefold():
    print(json.dumps({"type": "item.started", "item": {"type": "command_execution", "command": "attempt overwrite tests/validation/fixtures/portable-skill/SKILL.md", "status": "in_progress"}}))
    print(json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": "attempt overwrite tests/validation/fixtures/portable-skill/SKILL.md", "status": "failed", "exit_code": 1, "aggregated_output": "permission denied: protected file is outside granted permissions"}}))
    print(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "Refused: permission denied for the protected file; no write was performed."}}))
else:
    print(json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": "cat .agents/skills/portable-skill/SKILL.md", "aggregated_output": "portable-skill 2.0", "exit_code": 0, "status": "completed"}}))
    print(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "portable-skill 2.0"}}))

print(json.dumps({"type": "turn.completed", "turn_id": "fake-turn"}))
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
        if basic_evidence["result"] != "PARTIAL":
            raise SystemExit(f"basic self-test expected PARTIAL, got {basic_evidence['result']!r}")
        basic_checks = {item["id"]: item["result"] for item in basic_evidence["checks"]}
        if basic_checks["instruction-discovery"] != "UNTESTED":
            raise SystemExit("basic self-test incorrectly claimed instruction discovery")
        if basic_checks["skill-discovery"] != "UNTESTED" or basic_checks["skill-loading"] != "UNTESTED":
            raise SystemExit("basic self-test incorrectly claimed Skill discovery/loading")
        basic_observations = {item["id"]: item["result"] for item in basic_evidence["observations"]}
        if basic_observations["codex-jsonl-event-stream"] != "OBSERVED":
            raise SystemExit("basic self-test did not observe Codex JSONL events")
        if basic_observations["codex-command-execution"] != "OBSERVED":
            raise SystemExit("basic self-test did not observe command execution")
        if basic_observations["codex-skill-file-access"] != "OBSERVED":
            raise SystemExit("basic self-test did not observe Skill file access")
        if basic_observations["skill-loading-event"] != "NOT_OBSERVED":
            raise SystemExit("basic self-test incorrectly promoted Skill file access to Skill loading")
        if basic_evidence["runtime"]["version"] != "codex-fake 0.0.0":
            raise SystemExit("adapter did not record fake runtime version")
        invocation = basic_evidence["runtime"]["invocation"]
        if "exec --json --ephemeral --sandbox read-only" not in invocation:
            raise SystemExit("adapter did not construct the JSONL read-only invocation")

        # A missing expected marker must produce a truthful FAIL explanation,
        # while still using only the deterministic fake runtime (zero model cost).
        failing_scenario = json.loads(BASIC.read_text(encoding="utf-8"))
        failing_scenario["scenario"]["expected_markers"].append("marker-that-the-fake-runtime-never-emits")
        failing_scenario_path = tmp_path / "failing-scenario.json"
        failing_scenario_path.write_text(json.dumps(failing_scenario), encoding="utf-8")
        failing_out = tmp_path / "failing.json"
        failing = run(
            sys.executable, str(ADAPTER), "--execute", "--scenario", str(failing_scenario_path), "--output", str(failing_out), env=env
        )
        if failing.returncode != 1:
            raise SystemExit(f"failure-path self-test expected exit 1, got {failing.returncode}:\\n{failing.stdout}\\n{failing.stderr}")
        failing_evidence = json.loads(failing_out.read_text(encoding="utf-8"))
        if failing_evidence["result"] != "FAIL":
            raise SystemExit(f"failure-path self-test expected FAIL, got {failing_evidence['result']!r}")
        failing_checks = {item["id"]: item for item in failing_evidence["checks"]}
        if failing_checks["task-execution"]["result"] != "FAIL" or "missing markers" not in failing_checks["task-execution"]["evidence"]:
            raise SystemExit("failure-path task-execution evidence did not explain the missing marker")
        if failing_checks["validation"]["result"] != "FAIL" or "missing markers" not in failing_checks["validation"]["evidence"]:
            raise SystemExit("failure-path validation evidence did not explain the missing marker")

        # Model the real-world CLI-option failure without invoking a live runtime.
        # A launch/argument error must fail the scenario while leaving permission
        # and recovery conformance UNTESTED (no runtime denial was observed).
        failing_cli = tmp_path / "codex-cli-error"
        failing_cli.write_text(
            "#!/usr/bin/env python3\\n"
            "import sys\\n"
            "if sys.argv[1:] == ['--version']:\\n"
            "    print('codex-fake-cli-error 0.0.0')\\n"
            "    raise SystemExit(0)\\n"
            "print(\"error: unexpected argument '--ask-for-approval' found\", file=sys.stderr)\\n"
            "raise SystemExit(2)\\n",
            encoding="utf-8",
        )
        failing_cli.chmod(failing_cli.stat().st_mode | stat.S_IXUSR)
        cli_error_env = env.copy()
        cli_error_env["CODEX_BIN"] = str(failing_cli)
        cli_error_out = tmp_path / "cli-error.json"
        cli_error = run(
            sys.executable, str(ADAPTER), "--execute", "--scenario", str(RECOVERY), "--output", str(cli_error_out), env=cli_error_env
        )
        if cli_error.returncode != 1:
            raise SystemExit(f"CLI-error self-test expected exit 1, got {cli_error.returncode}:\\n{cli_error.stdout}\\n{cli_error.stderr}")
        cli_error_evidence = json.loads(cli_error_out.read_text(encoding="utf-8"))
        if cli_error_evidence["result"] != "FAIL" or cli_error_evidence["exit_code"] != 2:
            raise SystemExit("CLI-error self-test did not record the failed runtime invocation")
        if "unexpected argument" not in cli_error_evidence["stderr_excerpt"]:
            raise SystemExit("CLI-error self-test lost the actionable runtime stderr")
        cli_error_checks = {item["id"]: item for item in cli_error_evidence["checks"]}
        if cli_error_checks["task-execution"]["result"] != "FAIL" or "exit_code=2" not in cli_error_checks["task-execution"]["evidence"]:
            raise SystemExit("CLI-error self-test did not explain the non-zero exit")
        if cli_error_checks["permission-check"]["result"] != "UNTESTED" or cli_error_checks["failure-recovery"]["result"] != "UNTESTED":
            raise SystemExit("CLI-error self-test incorrectly claimed permission denial or recovery")
        if cli_error_evidence["protected_files"][0]["unchanged"] is not True:
            raise SystemExit("CLI-error self-test did not preserve protected-file integrity")

        recovery_out = tmp_path / "recovery.json"
        recovery = run(
            sys.executable, str(ADAPTER), "--execute", "--scenario", str(RECOVERY), "--output", str(recovery_out), env=env
        )
        if recovery.returncode != 0:
            raise SystemExit(f"recovery adapter self-test failed:\n{recovery.stdout}\n{recovery.stderr}")
        recovery_evidence = json.loads(recovery_out.read_text(encoding="utf-8"))
        if recovery_evidence["result"] != "PARTIAL":
            raise SystemExit(f"recovery self-test expected PARTIAL, got {recovery_evidence['result']!r}")
        recovery_checks = {item["id"]: item["result"] for item in recovery_evidence["checks"]}
        if recovery_checks["instruction-discovery"] != "UNTESTED" or recovery_checks["skill-discovery"] != "UNTESTED" or recovery_checks["skill-loading"] != "UNTESTED":
            raise SystemExit("recovery self-test incorrectly claimed discovery/loading")
        if recovery_checks["permission-check"] != "PASS" or recovery_checks["failure-recovery"] != "PASS":
            raise SystemExit("recovery self-test did not produce PASS permission/recovery evidence")
        if recovery_checks["validation"] != "PASS" or recovery_checks["evidence-reporting"] != "PASS":
            raise SystemExit("recovery self-test did not produce PASS validation/evidence-reporting evidence")
        recovery_observations = {item["id"]: item["result"] for item in recovery_evidence["observations"]}
        if recovery_observations["codex-command-execution"] != "OBSERVED":
            raise SystemExit("recovery self-test did not observe the forbidden command attempt")
        if recovery_observations["codex-permission-denial"] != "OBSERVED":
            raise SystemExit("recovery self-test did not observe structured permission denial")

    print("Codex adapter self-test passed (fake runtime; no live Codex conformance claimed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
