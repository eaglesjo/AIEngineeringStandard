from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_2_2_distribution_contract() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validation" / "validate_2_2_distribution.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
