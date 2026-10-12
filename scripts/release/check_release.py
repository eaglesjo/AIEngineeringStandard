#!/usr/bin/env python3
"""Validate the exact local state required before publishing a release."""
from __future__ import annotations

import json
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

    fetch = run("git", "fetch", "--prune", "origin", "main")
    if fetch.returncode != 0:
        print(fetch.stderr, file=sys.stderr, end="")
        fail("unable to refresh origin/main")

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
    head_sha = head.stdout.strip()
    if remote.stdout.strip() != head_sha:
        fail("local main must match origin/main exactly")

    tag = f"v{version}"
    existing = run("git", "rev-parse", "--verify", f"refs/tags/{tag}")
    if existing.returncode == 0:
        fail(f"release tag already exists locally: {tag}")

    # Check the remote directly as well: a tag may exist on GitHub without
    # being present in the local clone or fetched tag refs.
    remote_tag = run("git", "ls-remote", "--exit-code", "--tags", "origin", f"refs/tags/{tag}")
    if remote_tag.returncode == 0:
        fail(f"release tag already exists on origin: {tag}")
    if remote_tag.returncode != 2:
        if remote_tag.stderr:
            print(remote_tag.stderr, file=sys.stderr, end="")
        fail(f"unable to verify whether release tag exists on origin: {tag}")

    # A clean local tree is not enough: require a successful CI run for this
    # exact main commit before creating and pushing a release tag.
    ci = run(
        "gh", "run", "list", "--workflow", "ci.yml", "--branch", "main",
        "--commit", head_sha, "--limit", "10",
        "--json", "status,conclusion,headSha",
    )
    if ci.returncode != 0:
        if ci.stderr:
            print(ci.stderr, file=sys.stderr, end="")
        fail(f"unable to verify GitHub Actions CI for commit {head_sha}")
    try:
        ci_runs = json.loads(ci.stdout)
    except json.JSONDecodeError:
        fail("GitHub Actions returned invalid CI run data")
    if not isinstance(ci_runs, list) or not ci_runs:
        fail(f"no GitHub Actions CI run found for commit {head_sha}")
    latest = ci_runs[0]
    if not isinstance(latest, dict) or latest.get("headSha") != head_sha:
        fail(f"GitHub Actions CI result does not match commit {head_sha}")
    if latest.get("status") != "completed" or latest.get("conclusion") != "success":
        fail(
            f"GitHub Actions CI must complete successfully for {head_sha} "
            f"(status={latest.get('status')}, conclusion={latest.get('conclusion')})"
        )

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

    print(f"release preflight passed: {tag} @ {head_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
