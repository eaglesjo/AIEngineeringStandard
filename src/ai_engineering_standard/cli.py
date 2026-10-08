"""Command-line interface for the AIEngineeringStandard distribution."""

from __future__ import annotations

import argparse
import importlib.resources as resources
from pathlib import Path
from typing import Sequence

from . import __version__
from .installer import run_installer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-engineering-standard",
        description="Install and manage AIEngineeringStandard in a project.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    install = sub.add_parser("install", help="Install standard resources into a project.")
    install.add_argument("--target", default=".", help="Target project directory.")
    install.add_argument("--language", default=None, help="Locale, e.g. en or ko.")
    install.add_argument(
        "--domain",
        choices=("common", "ml", "llm", "vision", "colab", "all"),
        default=None,
        help="Installation domain.",
    )
    install.add_argument(
        "--policy",
        choices=("ask", "merge", "overwrite", "skip"),
        default="ask",
        help="Conflict policy for existing files.",
    )
    install.add_argument("--dry-run", action="store_true", help="Preview without writing files.")

    status = sub.add_parser("status", help="Inspect the installed standard state.")
    status.add_argument("--target", default=".", help="Target project directory.")
    status.add_argument("--json", action="store_true", help="Emit JSON.")

    update = sub.add_parser("update", help="Reconcile an existing installation with this package.")
    update.add_argument("--target", default=".", help="Target project directory.")
    update.add_argument("--policy", choices=("ask", "merge", "overwrite", "skip"), default="merge")
    update.add_argument("--dry-run", action="store_true")

    uninstall = sub.add_parser("uninstall", help="Remove files owned by the installation.")
    uninstall.add_argument("--target", default=".", help="Target project directory.")
    uninstall.add_argument("--force", action="store_true", help="Remove modified managed files too.")
    uninstall.add_argument("--dry-run", action="store_true")

    validate = sub.add_parser("validate", help="Validate the target installation state.")
    validate.add_argument("--target", default=".", help="Target project directory.")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    with resources.as_file(resources.files("ai_engineering_standard.resources")) as resource_root:
        return run_installer(args, Path(resource_root))


if __name__ == "__main__":
    raise SystemExit(main())
