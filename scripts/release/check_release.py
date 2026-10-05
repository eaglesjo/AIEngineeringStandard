#!/usr/bin/env python3
"""Validate the exact local state required before publishing a release."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        fail("VERSION is empty")

    branch = run("git", "branch", "--show-current")
    if branch.returncode != 0 or branch.stdout.strip() != "main":
        fail("release must be prepared from local main")

    status = run("git", "status", "--porcelain")
    if status.returncode != 0:
        fail("unable to inspect git status")
    if status.stdout.strip():
        fail("working tree must be clean")

    remote = run("git", "rev-parse", "--verify", "origin/main")
    head = run("git", "rev-parse", "HEAD")
    if remote.returncode != 0 or head.returncode != 0:
        fail("origin/main is unavailable")
    if remote.stdout.strip() != head.stdout.strip():
        fail("local main must match origin/main exactly")

    tag = f"v{version}"
    existing = run("git", "rev-parse", "--verify", f"refs/tags/{tag}")
    if existing.returncode == 0:
        fail(f"release tag already exists: {tag}")

    validation = run(sys.executable, "scripts/validation/validate.py")
    if validation.returncode != 0:
        print(validation.stdout, end="")
        print(validation.stderr, file=sys.stderr, end="")
        fail("repository validation failed")

    installers = run(sys.executable, "scripts/installers/test_installers.py")
    if installers.returncode != 0:
        print(installers.stdout, end="")
        print(installers.stderr, file=sys.stderr, end="")
        fail("installer lifecycle tests failed")

    print(f"release preflight passed: {tag} @ {head.stdout.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
