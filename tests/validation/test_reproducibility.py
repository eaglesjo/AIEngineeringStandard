#!/usr/bin/env python3
"""Focused tests for reproducibility identity and acceptance."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validation/validate_reproducibility.py"
FIXTURES = ROOT / "tests/validation/fixtures/reproducibility"


def run_validator(document: dict) -> subprocess.CompletedProcess[str]:
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


def test_valid_fixture_is_reproducible() -> None:
    result = run_validator(load_fixture("valid.json"))
    assert result.returncode == 0, result.stderr


def test_dirty_revision_cannot_be_reproducible() -> None:
    result = run_validator(load_fixture("invalid_dirty.json"))
    assert result.returncode != 0
    assert "dirty revision" in result.stderr


if __name__ == "__main__":
    test_valid_fixture_is_reproducible()
    test_dirty_revision_cannot_be_reproducible()
    print("Reproducibility focused tests passed")
