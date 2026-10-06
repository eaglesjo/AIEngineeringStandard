from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def test_execution_mission_schema():
    path = ROOT / "core/runtime/execution/mission.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"]["const"] == "1.0.0"
    assert "source_sha" in schema["required"]
    assert "capability_inventory" in schema["required"]
    assert "lifecycle" in schema["required"]
    assert schema["properties"]["capability_inventory"]["properties"]["decision"]["enum"] == ["REUSE_SANDBOX", "USE_ACTIONS", "BLOCKED"]
    assert schema["properties"]["lifecycle"]["properties"]["phase"]["enum"] == ["CREATED", "EXECUTING", "TERMINAL"]
    assert schema["properties"]["verification"]["properties"]["source_sha"]["const"] is True


def test_execution_mission_validator():
    proc = subprocess.run([sys.executable, "scripts/validation/validate_execution_contract.py"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert proc.returncode == 0, proc.stderr
    assert "execution mission validation passed" in proc.stdout
