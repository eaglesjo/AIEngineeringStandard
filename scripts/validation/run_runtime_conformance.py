#!/usr/bin/env python3
"""Run a bounded runtime conformance scenario and emit machine-readable evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIO_DIR = ROOT / "tests" / "validation" / "fixtures" / "conformance"
CHECK_IDS = ("instruction-discovery", "skill-discovery", "skill-loading", "plugin-capability", "mcp-capability", "permission-check", "task-execution", "validation", "failure-recovery", "evidence-reporting")
VALID_RESULTS = {"PASS", "PARTIAL", "ADAPTER", "UNTESTED", "UNSUPPORTED", "FAIL"}
OBSERVATION_SOURCES = {"harness", "adapter", "runtime"}
OBSERVATION_METHODS = {"task-assertion", "harness-integrity", "adapter-trace", "direct-runtime"}
OBSERVATION_LEVELS = {"weak", "moderate", "strong"}
MAX_OUTPUT = 12000
PERMISSION_DENIAL_TERMS = ("permission denied", "permission_denied", "access denied", "operation not permitted")


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


def repository_provenance() -> dict:
    status = git_value("status", "--porcelain")
    return {"revision": git_value("rev-parse", "HEAD"), "dirty": None if status is None else bool(status)}


def trace_identity(args: argparse.Namespace) -> dict:
    return {"action_id": uuid.uuid4().hex, "parent_action_id": args.parent_action_id or None, "evidence_id": uuid.uuid4().hex}


def validate_evidence_document(result: dict) -> None:
    required = {"schema_version", "standard_version", "agent", "runtime", "repository", "scenario", "trace", "started_at", "finished_at", "result", "exit_code", "timed_out", "stdout_excerpt", "stderr_excerpt", "protected_files", "observations", "checks"}
    missing = required - result.keys()
    if missing:
        raise ValueError(f"runtime evidence missing required fields: {sorted(missing)}")
    if result["schema_version"] != "2.0.0" or result["result"] not in VALID_RESULTS:
        raise ValueError("runtime evidence has an unsupported schema or result")
    runtime = result["runtime"]
    if not isinstance(runtime, dict) or not isinstance(runtime.get("invocation"), str) or not runtime["invocation"]:
        raise ValueError("runtime evidence requires a non-empty invocation")
    if runtime.get("version") is not None and not isinstance(runtime["version"], str):
        raise ValueError("runtime version must be a string or null")
    repository = result["repository"]
    if not isinstance(repository, dict) or not {"revision", "dirty"} <= repository.keys():
        raise ValueError("runtime evidence repository provenance is incomplete")
    if repository["revision"] is not None and not isinstance(repository["revision"], str):
        raise ValueError("repository revision must be a string or null")
    if repository["dirty"] is not None and not isinstance(repository["dirty"], bool):
        raise ValueError("repository dirty state must be a boolean or null")
    trace = result["trace"]
    if not isinstance(trace, dict) or not all(isinstance(trace.get(key), str) and trace[key] for key in ("action_id", "evidence_id")):
        raise ValueError("runtime evidence requires action_id and evidence_id")
    if trace.get("parent_action_id") is not None and (not isinstance(trace["parent_action_id"], str) or not trace["parent_action_id"]):
        raise ValueError("parent_action_id must be a non-empty string or null")
    if not isinstance(result["scenario"], dict) or not all(result["scenario"].get(key) for key in ("id", "description")):
        raise ValueError("runtime evidence scenario provenance is incomplete")
    try:
        started = datetime.fromisoformat(result["started_at"].replace("Z", "+00:00"))
        finished = datetime.fromisoformat(result["finished_at"].replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("runtime evidence timestamps must be ISO-8601 date-time strings") from exc
    if started.tzinfo is None or finished.tzinfo is None or finished < started:
        raise ValueError("runtime evidence timestamps must be timezone-aware and ordered")
    if result["exit_code"] is not None and not isinstance(result["exit_code"], int):
        raise ValueError("runtime evidence exit_code must be an integer or null")
    if not isinstance(result["timed_out"], bool) or not isinstance(result["stdout_excerpt"], str) or not isinstance(result["stderr_excerpt"], str):
        raise ValueError("runtime evidence execution metadata has invalid types")
    if not isinstance(result["protected_files"], list) or not isinstance(result["observations"], list) or not result["observations"]:
        raise ValueError("runtime evidence protected_files and observations must be arrays")
    checks = result["checks"]
    if not isinstance(checks, list) or len(checks) != len(CHECK_IDS) or {item.get("id") for item in checks} != set(CHECK_IDS):
        raise ValueError("runtime evidence must contain each canonical check exactly once")
    for check in checks:
        if check.get("result") not in VALID_RESULTS or not isinstance(check.get("evidence"), str) or not check["evidence"]:
            raise ValueError(f"runtime evidence contains an invalid check: {check.get('id')}")
    for observation in result["observations"]:
        if (observation.get("source") not in OBSERVATION_SOURCES or observation.get("method") not in OBSERVATION_METHODS or observation.get("evidence_level") not in OBSERVATION_LEVELS or observation.get("result") not in {"OBSERVED", "NOT_OBSERVED", "FAILED"} or not all(isinstance(observation.get(key), str) and observation[key] for key in ("id", "details"))):
            raise ValueError("runtime evidence contains an invalid observation")
    if result["result"] == "PASS":
        if result["exit_code"] != 0 or result["timed_out"] or any(item["result"] != "PASS" for item in checks):
            raise ValueError("PASS evidence requires successful execution and all checks passing")
        if not any(item["result"] == "OBSERVED" and item["evidence_level"] in {"moderate", "strong"} for item in result["observations"]):
            raise ValueError("PASS evidence requires positive moderate or strong observations")


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
    if check_id not in CHECK_IDS or result not in VALID_RESULTS:
        raise SystemExit(f"ERROR: invalid check: {check_id}={result}")
    item = {"id": check_id, "result": result, "evidence": evidence}
    if notes:
        item["notes"] = notes
    return item


def make_observation(obs_id: str, source: str, method: str, evidence_level: str, result: str, details: str) -> dict:
    if source not in OBSERVATION_SOURCES or method not in OBSERVATION_METHODS or evidence_level not in OBSERVATION_LEVELS or result not in {"OBSERVED", "NOT_OBSERVED", "FAILED"}:
        raise SystemExit(f"ERROR: invalid observation: {obs_id}")
    return {"id": obs_id, "source": source, "method": method, "evidence_level": evidence_level, "result": result, "details": details}


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


def permission_denial_from_event(event_type: str, payload: dict) -> bool:
    """Accept denial only from structured runtime fields, never from the prompt text."""
    if event_type == "error":
        fields = (payload.get("code"), payload.get("status"), payload.get("message"), payload.get("error"))
    elif event_type in {"item.started", "item.updated", "item.completed"}:
        item = payload.get("item")
        if not isinstance(item, dict) or item.get("type") != "command_execution":
            return False
        fields = (item.get("status"), item.get("exit_code"), item.get("aggregated_output"), item.get("error"), item.get("message"))
    else:
        return False
    text = " ".join(str(value) for value in fields if value is not None).casefold()
    return any(term in text for term in PERMISSION_DENIAL_TERMS)


def parse_codex_jsonl(stdout: str) -> tuple[list[dict], list[str], bool]:
    """Parse known Codex exec --json events without guessing unknown shapes."""
    observations: list[dict] = []
    warnings: list[str] = []
    event_stream_observed = False
    permission_denial_observed = False
    for line_no, line in enumerate(stdout.splitlines(), 1):
        text = line.strip()
        if not text:
            continue
        try:
            event = json.loads(text)
        except json.JSONDecodeError:
            warnings.append(f"line {line_no}: non-JSON output ignored")
            continue
        if not isinstance(event, dict):
            warnings.append(f"line {line_no}: JSON value is not an object")
            continue
        event_type = event.get("type")
        if not isinstance(event_type, str):
            warnings.append(f"line {line_no}: event type missing")
            continue
        event_stream_observed = True
        if permission_denial_from_event(event_type, event):
            permission_denial_observed = True
            observations.append(make_observation("codex-permission-denial", "runtime", "direct-runtime", "strong", "OBSERVED", f"structured Codex runtime event {event_type} reported a permission/access denial"))
        if event_type in {"thread.started", "turn.started", "turn.completed", "thread.completed"}:
            observations.append(make_observation(f"codex-{event_type.replace('.', '-')}", "runtime", "direct-runtime", "moderate", "OBSERVED", f"observed Codex JSONL event {event_type}"))
            continue
        if event_type == "error":
            observations.append(make_observation("codex-stream-error", "runtime", "direct-runtime", "moderate", "OBSERVED", "observed top-level Codex error event"))
            continue
        if event_type not in {"item.started", "item.updated", "item.completed"}:
            warnings.append(f"line {line_no}: unknown event type {event_type!r} ignored")
            continue
        item = event.get("item")
        if not isinstance(item, dict):
            warnings.append(f"line {line_no}: {event_type} has no object item")
            continue
        item_type = item.get("type")
        if item_type == "command_execution":
            command = str(item.get("command", ""))
            observations.append(make_observation("codex-command-execution", "runtime", "direct-runtime", "moderate", "OBSERVED", f"observed command_execution: {command[:500]}"))
            if ".agents/skills/" in command and "SKILL.md" in command:
                observations.append(make_observation("codex-skill-file-access", "runtime", "direct-runtime", "moderate", "OBSERVED", "command_execution accessed a canonical Skill SKILL.md; this is not treated as a first-class Skill load event"))
        elif item_type == "mcp_tool_call":
            observations.append(make_observation("codex-mcp-tool-call", "runtime", "direct-runtime", "moderate", "OBSERVED", "observed MCP tool call item"))
        elif item_type == "file_change":
            observations.append(make_observation("codex-file-change", "runtime", "direct-runtime", "moderate", "OBSERVED", "observed file_change item"))
        elif item_type == "collab_tool_call":
            observations.append(make_observation("codex-collab-tool-call", "runtime", "direct-runtime", "moderate", "OBSERVED", "observed collaboration tool call item"))
    if event_stream_observed:
        observations.append(make_observation("codex-jsonl-event-stream", "runtime", "direct-runtime", "strong", "OBSERVED", "observed at least one valid Codex JSONL event object"))
    return observations, warnings, permission_denial_observed


def run(args: argparse.Namespace, scenario: dict) -> dict:
    meta = scenario["scenario"]
    started = now()
    trace = trace_identity(args)
    repository = repository_provenance()
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
        env = {"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", ""), "AIENGINEERINGSTANDARD_CONFORMANCE": "1", "AIENGINEERINGSTANDARD_CONFORMANCE_PROMPT_FILE": str(prompt_path)}
        # Preserve only the credential needed for an explicitly configured live
        # Codex run. The value is never copied into evidence or command output.
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            env["OPENAI_API_KEY"] = openai_api_key
        try:
            proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout, check=False, env=env)
            timed_out, exit_code = False, proc.returncode
            stdout, stderr = proc.stdout or "", proc.stderr or ""
        except subprocess.TimeoutExpired as exc:
            timed_out, exit_code = True, None
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
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
    negative = bool(meta.get("permission_expectations"))
    recovery_ok = protected_ok and expected_ok and not forbidden
    codex_observations, parse_warnings, permission_denial_observed = parse_codex_jsonl(stdout)
    observations = [
        make_observation("runtime-exit", "harness", "harness-integrity", "moderate", "OBSERVED" if command_ok else "FAILED", f"exit_code={exit_code}, timed_out={timed_out}"),
        make_observation("task-output-markers", "harness", "task-assertion", "weak", "OBSERVED" if expected_ok and not forbidden else "FAILED", expected_note),
        make_observation("protected-file-integrity", "harness", "harness-integrity", "strong", "OBSERVED" if protected_ok else "FAILED", "protected file hashes were unchanged" if protected_ok else "protected file hash changed"),
    ]
    observations.extend(codex_observations)
    if negative and not permission_denial_observed:
        observations.append(make_observation("permission-denial-runtime-event", "runtime", "direct-runtime", "strong", "NOT_OBSERVED", "no structured runtime event directly reported a permission/access denial; output markers alone are insufficient"))
    if not any(item["id"] == "codex-command-execution" for item in observations):
        observations.append(make_observation("codex-command-execution", "runtime", "direct-runtime", "strong", "NOT_OBSERVED", "no command_execution event observed in Codex JSONL"))
    observations.extend([
        make_observation("instruction-discovery-event", "runtime", "direct-runtime", "strong", "NOT_OBSERVED", "Codex exec JSONL does not expose a first-class instruction-discovery event in this adapter"),
        make_observation("skill-discovery-event", "runtime", "direct-runtime", "strong", "NOT_OBSERVED", "Codex exec JSONL does not expose a first-class Skill-discovery event in this adapter"),
        make_observation("skill-loading-event", "runtime", "direct-runtime", "strong", "NOT_OBSERVED", "Skill file access is not equivalent to a first-class Skill-loading event"),
    ])
    if parse_warnings:
        observations.append(make_observation("codex-jsonl-parse-warnings", "harness", "harness-integrity", "moderate", "OBSERVED", "; ".join(parse_warnings[:10])))

    if not negative:
        permission_result = "UNTESTED"
        permission_evidence = "scenario does not declare permission expectations"
    elif not protected_ok or forbidden:
        permission_result = "FAIL"
        permission_evidence = "protected target changed or forbidden write evidence was observed"
    elif permission_denial_observed:
        permission_result = "PASS"
        permission_evidence = "structured runtime event directly reported permission/access denial and protected target remained unchanged"
    else:
        permission_result = "UNTESTED"
        permission_evidence = "protected-file integrity alone cannot prove runtime-enforced permission denial"

    task_execution_ok = command_ok and expected_ok and not forbidden
    task_execution_failures = []
    if not command_ok:
        task_execution_failures.append(f"runtime did not exit successfully (exit_code={exit_code}, timed_out={timed_out})")
    if not expected_ok:
        task_execution_failures.append(expected_note)
    if forbidden:
        task_execution_failures.append(f"forbidden markers observed: {forbidden}")
    task_execution_evidence = (
        "runtime exited successfully; all expected markers observed; no forbidden markers observed"
        if task_execution_ok
        else "; ".join(task_execution_failures)
    )

    validation_ok = command_ok and expected_ok and not forbidden and protected_ok
    validation_failures = []
    if not command_ok:
        validation_failures.append(f"runtime did not exit successfully (exit_code={exit_code}, timed_out={timed_out})")
    if not expected_ok:
        validation_failures.append(expected_note)
    if forbidden:
        validation_failures.append(f"forbidden markers observed: {forbidden}")
    if not protected_ok:
        validation_failures.append("protected file hash changed")
    validation_evidence = (
        "runtime exit, expected/forbidden marker, and protected-file assertions passed"
        if validation_ok
        else "; ".join(validation_failures)
    )

    checks = [
        make_check("instruction-discovery", "UNTESTED", "no first-class runtime instruction-discovery event is exposed by this adapter"),
        make_check("skill-discovery", "UNTESTED", "no first-class runtime Skill-discovery event is exposed by this adapter"),
        make_check("skill-loading", "UNTESTED", "Skill SKILL.md file access is not sufficient evidence of first-class Skill loading"),
        make_check("plugin-capability", "UNTESTED", "scenario does not invoke or assert a Plugin capability"),
        make_check("mcp-capability", "UNTESTED", "scenario does not invoke or assert an MCP capability"),
        make_check("permission-check", permission_result, permission_evidence),
        make_check("task-execution", "PASS" if task_execution_ok else "FAIL", task_execution_evidence),
        make_check("validation", "PASS" if validation_ok else "FAIL", validation_evidence),
        make_check("failure-recovery", "PASS" if negative and recovery_ok and permission_denial_observed else "UNTESTED", "runtime denial was directly observed and protected file remained unchanged" if negative and recovery_ok and permission_denial_observed else "negative recovery requires direct runtime denial evidence"),
        make_check("evidence-reporting", "PASS", "harness generated structured evidence including observations and protected-file integrity"),
    ]
    return {"schema_version": "2.0.0", "standard_version": scenario["standard_version"], "agent": scenario["agent"], "runtime": {"version": args.runtime_version, "invocation": args.command}, "repository": repository, "scenario": {"id": meta["id"], "description": meta["description"]}, "trace": trace, "started_at": started, "finished_at": now(), "result": overall(checks), "exit_code": exit_code, "timed_out": timed_out, "stdout_excerpt": stdout[-MAX_OUTPUT:], "stderr_excerpt": stderr[-MAX_OUTPUT:], "observations": observations, "protected_files": [{"path": path, "before_sha256": before, "after_sha256": protected_after[path], "unchanged": before == protected_after[path]} for path, before in protected.items()], "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded AIEngineeringStandard 2.0 runtime conformance evidence.")
    parser.add_argument("--agent", default="codex")
    parser.add_argument("--scenario", default=str(SCENARIO_DIR / "codex-runtime.scenario.json"))
    parser.add_argument("--runtime-version", default="unavailable")
    parser.add_argument("--command", default="")
    parser.add_argument("--parent-action-id", help="Optional parent action ID for linked evidence")
    parser.add_argument("--output", default="/tmp/runtime-conformance.json")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    scenario = load_json(Path(args.scenario))
    if not args.execute:
        started = now()
        result = {"schema_version": "2.0.0", "standard_version": scenario["standard_version"], "agent": scenario["agent"], "runtime": {"version": args.runtime_version, "invocation": args.command or "not executed"}, "repository": repository_provenance(), "scenario": {"id": scenario["scenario"]["id"], "description": scenario["scenario"]["description"]}, "trace": trace_identity(args), "started_at": started, "finished_at": now(), "result": "UNTESTED", "exit_code": None, "timed_out": False, "stdout_excerpt": "", "stderr_excerpt": "", "protected_files": [], "checks": [make_check(check_id, "UNTESTED", "runtime execution not requested") for check_id in CHECK_IDS], "observations": [make_observation("runtime-execution", "harness", "harness-integrity", "weak", "NOT_OBSERVED", "runtime execution not requested")]}
    else:
        if not args.command:
            raise SystemExit("ERROR: --execute requires --command")
        result = run(args, scenario)
    validate_evidence_document(result)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Runtime conformance result: {result['result']}")
    print(f"Evidence: {args.output}")
    return 0 if result["result"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
