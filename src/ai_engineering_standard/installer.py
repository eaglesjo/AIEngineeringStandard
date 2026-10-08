"""Bridge the installed CLI to the repository-independent lifecycle engine."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType


def _load_engine(resource_root: Path) -> ModuleType:
    engine_path = resource_root / "_installer_engine.py"
    if not engine_path.is_file():
        raise RuntimeError("Packaged installation engine is missing.")
    spec = importlib.util.spec_from_file_location(
        "ai_engineering_standard._installer_engine",
        engine_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load packaged installation engine.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_installer(args: argparse.Namespace, resource_root: Path) -> int:
    engine = _load_engine(resource_root)
    if args.command == "install":
        language = args.language or engine.prompt_language(resource_root)
        domain = args.domain or engine.prompt_domain()
        return engine.install(
            resource_root,
            Path(args.target).resolve(),
            language,
            domain,
            args.policy,
            args.dry_run,
        )
    target = Path(args.target).resolve()
    if args.command == "status":
        return engine.state(target, args.json)
    if args.command == "update":
        return engine.update(resource_root, target, args.policy, args.dry_run)
    if args.command == "uninstall":
        return engine.uninstall(target, args.force, args.dry_run)
    if args.command == "validate":
        return engine.validate(target)
    raise RuntimeError(f"Unsupported command: {args.command}")
