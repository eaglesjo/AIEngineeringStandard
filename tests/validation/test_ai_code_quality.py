#!/usr/bin/env python3
"""Focused tests for the AI code quality acceptance contract."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validation/validate_ai_code_quality.py"
FIXTURES = ROOT / "tests/validation/fixtures/ai-code-quality"


def run_validator(document: dict) -> subprocess.CompletedProcess[str]:
    import tempfile

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(document, handle)
        path = handle.name
    try:
        runner = (
            "import json, runpy; "
            f"ns = runpy.run_path({str(VALIDATOR)!r}); "
            f"ns['validate_schema'](); "
            f"ns['validate_contract'](json.load(open({path!r}, encoding='utf-8')))"
        )
        return subprocess.run([sys.executable, "-c", runner], cwd=ROOT, text=True, capture_output=True)
    finally:
        Path(path).unlink(missing_ok=True)


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_valid_fixture_is_accepted() -> None:
    result = run_validator(load_fixture("valid.json"))
    assert result.returncode == 0, result.stderr


def test_failed_required_check_cannot_be_accepted() -> None:
    result = run_validator(load_fixture("invalid_not_all_pass.json"))
    assert result.returncode != 0
    assert "requires PASS for every required quality check" in result.stderr


if __name__ == "__main__":
    test_valid_fixture_is_accepted()
    test_failed_required_check_cannot_be_accepted()
    print("AI code quality focused tests passed")
