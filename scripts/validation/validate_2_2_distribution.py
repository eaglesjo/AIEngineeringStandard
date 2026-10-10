#!/usr/bin/env python3
"""Validate the AIEngineeringStandard 2.2 installable distribution contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(path: str) -> Path:
    value = ROOT / path
    if not value.is_file():
        fail(f"Missing required distribution file: {path}")
    return value


def main() -> None:
    pyproject = require("pyproject.toml").read_text(encoding="utf-8")
    version = require("VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"Expected a semantic distribution version, got {version!r}")
    if '[project.scripts]' not in pyproject or 'ai-engineering-standard = "ai_engineering_standard.cli:main"' not in pyproject:
        fail("Missing canonical CLI entry point.")
    if 'requires-python = ">=3.10"' not in pyproject:
        fail("Python 3.10+ compatibility contract is missing.")
    required_mappings = (
        '"core" = "ai_engineering_standard/resources/core"',
        '"domains" = "ai_engineering_standard/resources/domains"',
        '"i18n" = "ai_engineering_standard/resources/i18n"',
        '"scripts/installers/installation.py" = "ai_engineering_standard/resources/installation_engine.py"',
    )
    for mapping in required_mappings:
        if mapping not in pyproject:
            fail(f"Missing package resource mapping: {mapping}")
    cli = require("src/ai_engineering_standard/cli.py").read_text(encoding="utf-8")
    if "importlib.resources" not in cli or "resources.as_file" not in cli:
        fail("CLI must load packaged resources through importlib.resources.")
    engine = require("scripts/installers/installation.py").read_text(encoding="utf-8")
    if "SCHEMA_VERSION = 2" not in engine:
        fail("Installation manifest schema was not upgraded to v2.")
    if '"product": "AIEngineeringStandard"' not in engine:
        fail("Installation manifest product identity is not AIEngineeringStandard.")
    readme = require("README.md").read_text(encoding="utf-8")
    install = require("INSTALL.md").read_text(encoding="utf-8")
    release = require(".github/workflows/publish-package.yml").read_text(encoding="utf-8")
    clone = "git clone https://github.com/eaglesjo/AIEngineeringStandard.git"
    if "pypa/gh-action-pypi-publish@release/v1" not in release:
        fail("Release workflow is missing the PyPI Trusted Publishing action.")
    if "id-token: write" not in release:
        fail("Release workflow is missing OIDC id-token permission.")
    if "tags:" not in release or "v*.*.*" not in release:
        fail("Release workflow must be tag-driven.")
    if clone in readme or clone in install:
        fail("Consumer documentation still requires repository cloning.")
    if not re.search(r"pipx install ai-engineering-standard", readme):
        fail("README is missing the package installation path.")
    print(f"AIEngineeringStandard {version} distribution validation passed")


if __name__ == "__main__":
    main()
