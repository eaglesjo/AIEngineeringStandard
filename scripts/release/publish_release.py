#!/usr/bin/env python3
"""Create and publish an annotated Git tag and GitHub Release."""
from __future__ import annotations

import shutil
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
    if shutil.which("gh") is None:
        fail("GitHub CLI (gh) is required to publish a GitHub Release")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    tag = f"v{version}"

    preflight = run(sys.executable, "scripts/release/check_release.py")
    if preflight.returncode != 0:
        print(preflight.stdout, end="")
        print(preflight.stderr, file=sys.stderr, end="")
        return preflight.returncode

    commit = run("git", "rev-parse", "HEAD")
    if commit.returncode != 0:
        fail("unable to resolve HEAD")

    create_tag = run("git", "tag", "-a", tag, "-m", f"Release {tag}")
    if create_tag.returncode != 0:
        print(create_tag.stderr, file=sys.stderr, end="")
        fail(f"unable to create annotated tag {tag}")

    push_tag = run("git", "push", "origin", tag)
    if push_tag.returncode != 0:
        run("git", "tag", "-d", tag)
        print(push_tag.stderr, file=sys.stderr, end="")
        fail(f"unable to push tag {tag}")

    release = run("gh", "release", "create", tag, "--generate-notes", "--title", tag)
    if release.returncode != 0:
        print(release.stdout, end="")
        print(release.stderr, file=sys.stderr, end="")
        fail(f"tag {tag} was pushed, but GitHub Release creation failed")

    print(f"published {tag} from {commit.stdout.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
