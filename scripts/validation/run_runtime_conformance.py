#!/usr/bin/env python3
"""Run a bounded runtime conformance scenario and emit machine-readable evidence.

This harness never executes Skills, Plugins, or MCP components directly. It invokes
an explicitly supplied agent runtime command, captures bounded output, and applies
only deterministic scenario assertions.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIO_DIR = ROOT / "tests" / "validation" / "fixtures" / "conformance"
CHECK_IDS = (
    "instruction-discovery", "skill-discovery", "skill-loading", "plugin-capability",
    "mcp-capability", "permission-check", "task-execution", "validation",
    "failure-recovery", "evidence-reporting",
)
VALID_RESULTS = {"PASS", "PARTIAL", "ADAPTER", "UNTESTED", "UNSUPPORTED", "FAIL"}
MAX_OUTPUT = 12000


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: cannot read JSON scenario {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"ERROR: scenario must be a JSON object: {path}")
    return value


def git_value(*args: str) -> str | None:
    try:
        proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
    except OSError:
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def make_check(check_id: str, result: str, evidence: str, notes: str = "") -> dict:
    if check_id not in CHECK_IDS:
        raise SystemExit(f"ERROR: unknown check id: {check_id}")
    if result not in VALID_RESULTS:
        raise SystemExit(f"ERROR: invalid check result: {result}")
    item = {"id": check_id, "result": result, "evidence": evidence}
    if notes:
        item["notes"] = notes
    return item


def overall(checks: list[dict]) -> str:
    results = {item["result"] for item in checks}
    if "FAIL" in results:
        return "FAIL"
    if results == {"UNTESTED"}:
        return "UNTESTED"
    if "UNTESTED" in results:
        return "PARTIAL"
    if "ADAPTER" in results and results <= {"PASS", "ADAPTER"}:
        return "ADAPTER"
    if "PARTIAL" in results:
        return "PARTIAL"
    if "UNSUPPORTED" in results:
        return "UNSUPPORTED"
    return "PASS"


def marker_check(output: str, markers: list[str]) -> tuple[bool, str]:
    missing = [marker for marker in markers if marker not in output]
    return not missing, "all expected markers observed" if not missing else f"missing markers: {missing}"


def run(args: argparse.Namespace, scenario: dict) -> dict:
    meta = scenario["scenario"]
    started = now()
    command = shlex.split(args.command)
    if not command:
        raise SystemExit("ERROR: --command must not be empty")
    timeout = int(meta.get("timeout_seconds", 120))
    if timeout < 1 or timeout > 900:
        raise SystemExit("ERROR: scenario timeout_seconds must be between 1 and 900")

    prompt = str(meta["prompt"])
    prompt_path = ROOT / ".runtime-conformance-prompt.txt"
    prompt_path.write_text(prompt + "\n", encoding="utf-8")
    try:
        command.extend([args.prompt_flag, prompt]) if args.prompt_flag else None
        try:
            proc = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                env={"PATH": __import__("os").environ.get("PATH", ""), "HOME": __import__("os").environ.get("HOME", "")},
            )
            timed_out = False
            exit_code = proc.returncode
            stdout = proc.stdout or ""
            stderr = proc.stderr or ""
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            exit_code = None
            stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
            stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        except OSError as exc:
            timed_out = False
            exit_code = None
            stdout = ""
            stderr = str(exc)
    finally:
        prompt_path.unlink(missing_ok=True)

    combined = stdout + "\n" + stderr
    expected_ok, expected_note = marker_check(combined, list(meta.get("expected_markers", [])))
    forbidden = [marker for marker in meta.get("forbidden_markers", []) if marker in combined]
    command_ok = exit_code == 0 and not timed_out

    checks = [
        make_check("instruction-discovery", "PASS" if command_ok and expected_ok else "FAIL", "runtime completed and expected instruction/task markers were observed" if command_ok and expected_ok else expected_note),
        make_check("skill-discovery", "PASS" if command_ok and expected_ok else "FAIL", expected_note),
        make_check("skill-loading", "PASS" if command_ok and expected_ok else "FAIL", expected_note),
        make_check("plugin-capability", "UNTESTED", "scenario does not invoke or assert a Plugin capability"),
        make_check("mcp-capability", "UNTESTED", "scenario does not invoke or assert an MCP capability"),
        make_check("permission-check", "FAIL" if forbidden else "UNTESTED", "forbidden secret-like marker observed in runtime output" if forbidden else "runtime command cannot prove denied permissions; explicit permission evidence required"),
        make_check("task-execution", "PASS" if command_ok and expected_ok and not forbidden else "FAIL", "exit code 0 with deterministic markers and no forbidden markers" if command_ok and expected_ok and not forbidden else "runtime execution did not satisfy deterministic assertions"),
        make_check("validation", "PASS" if expected_ok and not forbidden else "FAIL", "scenario assertions evaluated deterministically"),
        make_check("failure-recovery", "UNTESTED", "negative/failure-recovery probe is not executed implicitly; run a dedicated bounded scenario"),
        make_check("evidence-reporting", "PASS", "harness generated structured evidence including repository revision and runtime invocation"),
    ]
    return {
        "schema_version": "2.0.0",
        "standard_version": scenario["standard_version"],
        "agent": scenario["agent"],
        "runtime": {"version": args.runtime_version, "invocation": args.command},
        "repository": {"revision": git_value("rev-parse", "HEAD"), "dirty": git_value("status", "--porcelain") not in (None, "")},
        "scenario": {"id": meta["id"], "description": meta["description"]},
        "started_at": started,
        "finished_at": now(),
        "result": overall(checks),
        "exit_code": exit_code,
        "timed_out": timed_out,
        "stdout_excerpt": stdout[-MAX_OUTPUT:],
        "stderr_excerpt": stderr[-MAX_OUTPUT:],
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded AIEngineeringStandard 2.0 runtime conformance scenario.")
    parser.add_argument("--agent", default="codex")
    parser.add_argument("--scenario", default=str(SCENARIO_DIR / "codex-runtime.scenario.json"))
    parser.add_argument("--command", help="Explicit agent runtime command; required with --execute")
    parser.add_argument("--runtime-version", default=None)
    parser.add_argument("--prompt-flag", default="", help="Optional flag used by the agent CLI to receive the prompt, e.g. --prompt")
    parser.add_argument("--output", default="/tmp/runtime-conformance.json")
    parser.add_argument("--execute", action="store_true", help="Actually invoke the supplied runtime command")
    args = parser.parse_args()
    scenario = load_json(Path(args.scenario))
    if scenario.get("agent") != args.agent:
        raise SystemExit(f"ERROR: scenario agent {scenario.get('agent')!r} does not match --agent {args.agent!r}")

    if not args.execute:
        evidence = {
            "schema_version": "2.0.0", "standard_version": scenario["standard_version"], "agent": args.agent,
            "runtime": {"version": args.runtime_version, "invocation": "not executed"},
            "repository": {"revision": git_value("rev-parse", "HEAD"), "dirty": git_value("status", "--porcelain") not in (None, "")},
            "scenario": {"id": scenario["scenario"]["id"], "description": scenario["scenario"]["description"]},
            "started_at": now(), "finished_at": now(), "result": "UNTESTED", "exit_code": None, "timed_out": False,
            "stdout_excerpt": "", "stderr_excerpt": "",
            "checks": [make_check(check_id, "UNTESTED", "runtime execution not requested") for check_id in CHECK_IDS],
        }
    else:
        if not args.command:
            raise SystemExit("ERROR: --command is required with --execute")
        evidence = run(args, scenario)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if evidence["result"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
