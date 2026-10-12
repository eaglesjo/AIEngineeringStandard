"""Regression tests for release preflight remote-tag safety."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "release" / "check_release.py"
SPEC = importlib.util.spec_from_file_location("check_release", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
check_release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_release)


def _completed(args: tuple[str, ...], code: int = 0, stdout: str = "", stderr: str = ""):
    return subprocess.CompletedProcess(args, code, stdout, stderr)


def _run_preflight(tmp_path: Path, remote_tag_code: int, remote_tag_stderr: str = ""):
    (tmp_path / "VERSION").write_text("9.9.9\n", encoding="utf-8")
    calls: list[tuple[str, ...]] = []

    def fake_run(*args: str):
        calls.append(args)
        if args[:3] == ("git", "fetch", "--prune"):
            return _completed(args)
        if args == ("git", "branch", "--show-current"):
            return _completed(args, stdout="main\n")
        if args == ("git", "status", "--porcelain"):
            return _completed(args)
        if args == ("git", "rev-parse", "--verify", "origin/main"):
            return _completed(args, stdout="a" * 40 + "\n")
        if args == ("git", "rev-parse", "HEAD"):
            return _completed(args, stdout="a" * 40 + "\n")
        if args == ("git", "rev-parse", "--verify", "refs/tags/v9.9.9"):
            return _completed(args, code=1, stderr="tag not found")
        if args == ("git", "ls-remote", "--exit-code", "--tags", "origin", "refs/tags/v9.9.9"):
            return _completed(args, code=remote_tag_code, stderr=remote_tag_stderr)
        if "scripts/validation/validate.py" in args:
            return _completed(args)
        if "scripts/installers/test_installers.py" in args:
            return _completed(args)
        raise AssertionError(f"Unexpected command: {args}")

    with patch.object(check_release, "ROOT", tmp_path), patch.object(check_release, "run", side_effect=fake_run):
        result = None
        error = None
        try:
            result = check_release.main()
        except SystemExit as exc:
            error = exc
    return result, error, calls


def test_existing_remote_tag_blocks_preflight(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    result, error, calls = _run_preflight(tmp_path, remote_tag_code=0)

    assert result is None
    assert error is not None and error.code == 1
    assert "release tag already exists on origin: v9.9.9" in capsys.readouterr().err
    assert not any("scripts/validation/validate.py" in call for call in calls)


def test_remote_tag_lookup_error_fails_closed(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    result, error, calls = _run_preflight(
        tmp_path, remote_tag_code=128, remote_tag_stderr="fatal: could not read from remote\n"
    )

    captured = capsys.readouterr()
    assert result is None
    assert error is not None and error.code == 1
    assert "could not read from remote" in captured.err
    assert "unable to verify whether release tag exists on origin: v9.9.9" in captured.err
    assert not any("scripts/validation/validate.py" in call for call in calls)


def test_missing_remote_tag_allows_remaining_preflight(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    result, error, calls = _run_preflight(tmp_path, remote_tag_code=2)

    assert error is None
    assert result == 0
    assert "release preflight passed: v9.9.9" in capsys.readouterr().out
    assert any("scripts/validation/validate.py" in call for call in calls)
    assert any("scripts/installers/test_installers.py" in call for call in calls)
