"""Tests for complete, traceable runtime-conformance evidence records."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "validation" / "run_runtime_conformance.py"
SCENARIO = ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime.scenario.json"


def load_evidence(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_provenance(evidence: dict, parent_action_id: str | None) -> None:
    required = {
        "schema_version", "standard_version", "agent", "runtime", "repository",
        "scenario", "trace", "started_at", "finished_at", "result", "exit_code",
        "timed_out", "stdout_excerpt", "stderr_excerpt", "protected_files",
        "observations", "checks",
    }
    assert required <= evidence.keys()
    assert evidence["trace"]["action_id"]
    assert evidence["trace"]["evidence_id"]
    assert evidence["trace"]["parent_action_id"] == parent_action_id
    assert evidence["repository"]["dirty"] in (True, False, None)
    assert evidence["repository"]["revision"] is None or evidence["repository"]["revision"]
    assert datetime.fromisoformat(evidence["started_at"].replace("Z", "+00:00"))
    assert datetime.fromisoformat(evidence["finished_at"].replace("Z", "+00:00"))
    assert len({check["id"] for check in evidence["checks"]}) == 10


def test_dry_run_emits_schema_complete_provenance(tmp_path: Path) -> None:
    output = tmp_path / "dry-run.json"
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--scenario", str(SCENARIO), "--output", str(output), "--parent-action-id", "parent-123"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    evidence = load_evidence(output)
    assert evidence["result"] == "UNTESTED"
    assert evidence["exit_code"] is None
    assert evidence["timed_out"] is False
    assert_provenance(evidence, "parent-123")
    observations = {item["id"]: item for item in evidence["observations"]}
    assert observations["protected-file-integrity"]["result"] == "NOT_OBSERVED"


def test_executed_run_emits_traceable_provenance(tmp_path: Path) -> None:
    fake_runtime = tmp_path / "fake-runtime.py"
    fake_runtime.write_text(
        "import json\n"
        "print('portable-skill 2.0')\n"
        "print(json.dumps({'type': 'turn.completed', 'turn_id': 'fixture-turn'}))\n",
        encoding="utf-8",
    )
    output = tmp_path / "executed.json"
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--scenario", str(SCENARIO), "--output", str(output),
         "--execute", "--command", f"{sys.executable} {fake_runtime}",
         "--runtime-version", "fixture-runtime/1.0", "--parent-action-id", "parent-456"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    evidence = load_evidence(output)
    assert evidence["result"] == "PARTIAL"
    assert evidence["runtime"]["version"] == "fixture-runtime/1.0"
    assert evidence["trace"]["parent_action_id"] == "parent-456"
    assert evidence["exit_code"] == 0
    assert_provenance(evidence, "parent-456")



def test_permission_recovery_requires_direct_runtime_denial(tmp_path: Path) -> None:
    recovery_scenario = ROOT / "tests" / "validation" / "fixtures" / "conformance" / "codex-runtime-failure-recovery.scenario.json"
    fake_runtime = tmp_path / "fake-denial-runtime.py"
    fake_runtime.write_text(
        "import json\\n"
        "print('Refused: permission denied')\\n"
        "print(json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'attempt overwrite protected target', 'status': 'failed', 'exit_code': 1, 'aggregated_output': 'permission denied: protected file is outside granted permissions'}}))\\n",
        encoding="utf-8",
    )
    output = tmp_path / "recovery.json"
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--scenario", str(recovery_scenario), "--output", str(output),
         "--execute", "--command", f"{sys.executable} {fake_runtime}", "--runtime-version", "fixture-runtime/1.0"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    evidence = load_evidence(output)
    checks = {item["id"]: item for item in evidence["checks"]}
    observations = {item["id"]: item for item in evidence["observations"]}
    assert checks["permission-check"]["result"] == "PASS"
    assert checks["failure-recovery"]["result"] == "PASS"
    assert observations["codex-permission-denial"]["evidence_level"] == "strong"
    assert observations["protected-file-integrity"]["result"] == "OBSERVED"
    assert evidence["protected_files"][0]["unchanged"] is True
    assert_provenance(evidence, None)
