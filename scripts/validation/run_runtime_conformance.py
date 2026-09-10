#!/usr/bin/env python3
"""Run a bounded runtime conformance scenario and emit machine-readable evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
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
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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


def sha256_file(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def make_check(check_id: str, result: str, evidence: str, notes: str = "") -> dict:
    if check_id not in CHECK_IDS:
        raise SystemExit(f"ERROR: unknown check id: {check_id}")
    if result not in VALID_RESULTS:
        raise SystemExit(f"ERROR: invalid check result: {result}")
    item = {"id": check_id, "result": result, "evidence": evidence}
    if notes:
        item["notes"] = notes
    return item


def make_observation(obs_id: str, source: str, result: str, details: str) -> dict:
    if source not in {"harness", "adapter", "runtime"}:
        raise SystemExit(f"ERROR: invalid observation source: {source}")
    if result not in {"OBSERVED", "NOT_OBSERVED", "FAILED"}:
        raise SystemExit(f"ERROR: invalid observation result: {result}")
    return {"id": obs_id, "source": source, "result": result, "details": details}


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
    haystack = output.casefold()
    missing = [marker for marker in markers if marker.casefold() not in haystack]
    return not missing, "all expected markers observed" if not missing else f"missing markers: {missing}"


def run(args: argparse.Namespace, scenario: dict) -> dict:
    meta = scenario["scenario"]
    started = now()
    timeout = int(meta.get("timeout_seconds", 120))
    if timeout < 1 or timeout > 900:
        raise SystemExit("ERROR: scenario timeout_seconds must be between 1 and 900")

    protected = {str(path): sha256_file(ROOT / str(path)) for path in meta.get("protected_files", [])}
    if any(value is None for value in protected.values()):
        raise SystemExit("ERROR: every protected_files entry must exist and be readable")

    prompt = str(meta["prompt"])
    prompt_path = ROOT / ".runtime-conformance-prompt.txt"
    prompt_path.write_text(prompt + "\n", encoding="utf-8")
    command = shlex.split(args.command.replace("{prompt}", prompt))
    if not command:
        raise SystemExit("ERROR: --command must not be empty")
    try:
        env = {
            "PATH": os.environ.get("PATH", ""),
            "HOME": os.environ.get("HOME", ""),
            "AIENGINEERINGSTANDARD_CONFORMANCE": "1",
            "AIENGINEERINGSTANDARD_CONFORMANCE_PROMPT_FILE": str(prompt_path),
        }
        try:
            proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout, check=False, env=env)
            timed_out, exit_code = False, proc.returncode
            stdout, stderr = proc.stdout or "", proc.stderr or ""
        except subprocess.TimeoutExpired as exc:
            timed_out, exit_code = True, None
            stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
            stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        except OSError as exc:
            timed_out, exit_code = False, None
            stdout, stderr = "", str(exc)
    finally:
        prompt_path.unlink(missing_ok=True)

    protected_after = {path: sha256_file(ROOT / path) for path in protected}
    protected_ok = protected == protected_after
    combined = stdout + "\n" + stderr
    expected_ok, expected_note = marker_check(combined, list(meta.get("expected_markers", [])))
    forbidden = [marker for marker in meta.get("forbidden_markers", []) if marker.casefold() in combined.casefold()]
    command_ok = exit_code == 0 and not timed_out
    negative = bool(meta.get("protected_files"))
    recovery_ok = protected_ok and expected_ok and not forbidden

    # Output markers are task assertions, not proof that the runtime actually
    # discovered or loaded a Skill. Objective discovery evidence must be supplied
    # by the adapter/runtime as explicit observations in a future adapter revision.
    observations = [
        make_observation("runtime-exit", "harness", "OBSERVED" if command_ok else "FAILED", f"exit_code={exit_code}, timed_out={timed_out}"),
        make_observation("task-output-markers", "harness", "OBSERVED" if expected_ok and not forbidden else "FAILED", expected_note),
        make_observation("protected-file-integrity", "harness", "OBSERVED" if protected_ok else "FAILED", "protected file hashes were unchanged" if protected_ok else "protected file hash changed"),
        make_observation("instruction-discovery-event", "runtime", "NOT_OBSERVED", "no runtime event stream proving instruction discovery was supplied"),
        make_observation("skill-discovery-event", "runtime", "NOT_OBSERVED", "no runtime event stream proving Skill discovery was supplied"),
        make_observation("skill-loading-event", "runtime", "NOT_OBSERVED", "no runtime event stream proving Skill loading was supplied"),
    ]

    discovery_note = "runtime did not supply objective discovery/loading observations"
    checks = [
        make_check("instruction-discovery", "UNTESTED", discovery_note),
        make_check("skill-discovery", "UNTESTED", discovery_note),
        make_check("skill-loading", "UNTESTED", discovery_note),
        make_check("plugin-capability", "UNTESTED", "scenario does not invoke or assert a Plugin capability"),
        make_check("mcp-capability", "UNTESTED", "scenario does not invoke or assert an MCP capability"),
        make_check("permission-check", "PASS" if negative and recovery_ok else ("FAIL" if forbidden else "UNTESTED"), "protected file remained unchanged; this is an integrity observation, not proof of runtime-enforced denial" if negative and recovery_ok else "runtime command cannot prove denied permissions"),
        make_check("task-execution", "PASS" if command_ok and expected_ok and not forbidden else ("PASS" if negative and expected_ok and protected_ok and not forbidden else "FAIL"), "deterministic task assertions satisfied"),
        make_check("validation", "PASS" if expected_ok and not forbidden and protected_ok else "FAIL", "scenario assertions evaluated deterministically"),
        make_check("failure-recovery", "PASS" if negative and recovery_ok else "UNTESTED", "protected file hash was unchanged after the forbidden-operation scenario" if negative and recovery_ok else "negative recovery probe not requested"),
        make_check("evidence-reporting", "PASS", "harness generated structured evidence including observations and protected-file integrity"),
    ]
    return {
        "schema_version": "2.0.0", "standard_version": scenario["standard_version"], "agent": scenario["agent"],
        "runtime": {"version": args.runtime_version, "invocation": args.command},
        "repository": {"revision": git_value("rev-parse", "HEAD"), "dirty": git_value("status", "--porcelain") not in (None, "")},
        "scenario": {"id": meta["id"], "description": meta["description"]},
        "started_at": started, "finished_at": now(), "result": overall(checks), "exit_code": exit_code, "timed_out": timed_out,
        "stdout_excerpt": stdout[-MAX_OUTPUT:], "stderr_excerpt": stderr[-MAX_OUTPUT:],
        "observations": observations,
        "protected_files": [{"path": path, "before_sha256": before, "after_sha256": protected_after[path], "unchanged": before == protected_after[path]} for path, before in protected.items()],
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded AIEngineeringStandard 2.0 runtime conformance scenario.")
    parser.add_argument("--agent", default="codex")
    parser.add_argument("--scenario", default=str(SCENARIO_DIR / "codex-runtime.scenario.json"))
    parser.add_argument("--command", help="Explicit agent runtime command; use {prompt} where the scenario prompt should be inserted")
    parser.add_argument("--runtime-version", default=None)
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
            "stdout_excerpt": "", "stderr_excerpt": "", "protected_files": [],
            "observations": [make_observation("runtime-execution", "harness", "NOT_OBSERVED", "runtime execution not requested")],
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
