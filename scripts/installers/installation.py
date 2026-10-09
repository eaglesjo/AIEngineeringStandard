#!/usr/bin/env python3
"""Cross-platform installer lifecycle engine for codingStandard."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
from typing import Any

SUPPORTED_DOMAINS = ("common", "ml", "llm", "vision", "colab", "all")
SUPPORTED_POLICIES = ("ask", "merge", "overwrite", "skip")
MANIFEST_DIR = ".codingstandard"
MANIFEST_FILE = "installation.json"
SCHEMA_VERSION = 2
CATALOG_FILE = "i18n/languages.json"

COMMON = [
    "AGENTS.md", ".agents/skills/ai-engineering-standard/SKILL.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md",
    ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md", ".aider.conf.yml",
    "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "core/common/environment.py", "core/common/experiment.py", "core/common/dependencies.py",
]
DOMAIN_FIXED = {
    "ml": [".github/instructions/ml.instructions.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/ml/ENVIRONMENT.md", "domains/ml/README.md"],
    "llm": [".github/instructions/llm.instructions.md", "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md", "domains/llm/environment.py", "domains/llm/experiment.py", "domains/llm/memory_smoke_test.py", "domains/llm/README.md", "domains/llm/config/training.yaml", "domains/llm/config/ablation.yaml"],
    "vision": [".github/instructions/vision.instructions.md", "domains/vision/AGENT.md", "domains/vision/SKILL.md", "domains/vision/ENVIRONMENT.md", "domains/vision/memory_smoke_test.py", "domains/vision/README.md", "domains/vision/config/training.yaml", "domains/vision/config/ablation.yaml"],
    "colab": ["platform/colab/AGENT.md", "platform/colab/SKILL.md"],
}


def read_version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def supported_languages(root: Path) -> tuple[str, ...]:
    catalog = root / CATALOG_FILE
    try:
        data = json.loads(catalog.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid language catalog: {catalog}: {exc}") from exc
    locales = {str(item["locale"]) for item in data.get("runtime_resources", []) if isinstance(item, dict) and item.get("locale")}
    if "en" not in locales:
        locales.add("en")
    return tuple(sorted(locales))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_target_path(target: Path, rel: str) -> Path:
    normalized = rel.replace("\\", "/")
    parts = normalized.split("/")
    if not normalized or normalized.startswith("/") or PureWindowsPath(normalized).drive or any(part in {"", ".", ".."} for part in parts):
        raise SystemExit(f"Unsafe managed path in installation manifest or template: {rel!r}")
    root = target.resolve()
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise SystemExit(f"Refusing to follow symlink in managed path: {rel}")
    return path


def manifest_path(target: Path) -> Path:
    return safe_target_path(target, f"{MANIFEST_DIR}/{MANIFEST_FILE}")


def load_manifest(target: Path) -> dict[str, Any]:
    path = manifest_path(target)
    if not path.is_file():
        raise SystemExit(f"No AIEngineeringStandard installation manifest found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid installation manifest: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Invalid installation manifest: top-level value must be an object.")
    schema_version = data.get("schema_version")
    if type(schema_version) is not int or schema_version not in (1, SCHEMA_VERSION):
        raise SystemExit(f"Unsupported installation manifest schema: {schema_version!r}")

    tracked = data.get("files")
    if not isinstance(tracked, list):
        raise SystemExit("Invalid installation manifest: 'files' must be a list.")
    seen: set[str] = set()
    for index, item in enumerate(tracked):
        if not isinstance(item, dict):
            raise SystemExit(f"Invalid installation manifest: files[{index}] must be an object.")
        rel = item.get("path")
        if not isinstance(rel, str):
            raise SystemExit(f"Invalid installation manifest: files[{index}].path must be a string.")
        safe_target_path(target, rel)
        if rel in seen:
            raise SystemExit(f"Invalid installation manifest: duplicate managed path {rel!r}.")
        seen.add(rel)
        digest = item.get("installed_sha256")
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-fA-F]{64}", digest) is None:
            raise SystemExit(f"Invalid installation manifest: files[{index}].installed_sha256 must be a SHA-256 hex digest.")
        source_digest = item.get("source_sha256")
        if source_digest is not None and (
            not isinstance(source_digest, str) or re.fullmatch(r"[0-9a-fA-F]{64}", source_digest) is None
        ):
            raise SystemExit(f"Invalid installation manifest: files[{index}].source_sha256 must be a SHA-256 hex digest.")

    for field in ("language", "domain"):
        if field in data and not isinstance(data[field], str):
            raise SystemExit(f"Invalid installation manifest: '{field}' must be a string.")
    if "domain" in data and data["domain"] not in SUPPORTED_DOMAINS:
        raise SystemExit(f"Invalid installation manifest: unsupported domain {data['domain']!r}.")
    return data


def source_root_for(root: Path, language: str) -> Path:
    locale_root = root / "i18n" / language
    return locale_root if language != "en" and locale_root.is_dir() else root


def collect_files(root: Path, domain: str) -> list[str]:
    paths = list(COMMON)
    domains = ("ml", "llm", "vision", "colab") if domain == "all" else (domain,) if domain != "common" else ()
    for item in domains:
        paths.extend(DOMAIN_FIXED[item])
        skill_root = root / "domains" / item / "skills"
        if skill_root.is_dir():
            paths.extend(str(p.relative_to(root)) for p in sorted(skill_root.rglob("SKILL.md")))
    return list(dict.fromkeys(paths))


def resolve_source(root: Path, language: str, rel: str) -> Path:
    localized = source_root_for(root, language) / rel
    return localized if localized.is_file() else root / rel


def prompt_language() -> str:
    print("Available languages: " + ", ".join(supported_languages(Path(__file__).resolve().parents[2])))
    choice = input("Language [en]: ").strip()
    return choice or "en"


def prompt_domain() -> str:
    print("Domain: 1) Common  2) ML  3) LLM  4) Vision  5) Colab  6) All")
    choice = input("Domain [6]: ").strip()
    return {"1": "common", "2": "ml", "3": "llm", "4": "vision", "5": "colab"}.get(choice, "all")


def prompt_policy(rel: str) -> str:
    while True:
        choice = input(f"Existing {rel} [m]erge [o]verwrite [s]kip: ").strip().lower()
        if choice in {"m", "o", "s"}:
            return {"m": "merge", "o": "overwrite", "s": "skip"}[choice]


def merge_text(old: str, new: str, rel: str) -> str:
    if rel.endswith((".py", ".yaml", ".yml", ".sh", ".bash")):
        start, end = "# BEGIN CODINGSTANDARD MANAGED BLOCK", "# END CODINGSTANDARD MANAGED BLOCK"
    else:
        start, end = "<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->", "<!-- END CODINGSTANDARD MANAGED BLOCK -->"
    if start in old:
        before, remainder = old.split(start, 1)
        _, after = remainder.split(end, 1) if end in remainder else (remainder, "")
        return f"{before}{start}\n{new.rstrip()}\n{end}{after}"
    return f"{old.rstrip()}\n\n{start}\n{new.rstrip()}\n{end}\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".installation-", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def restore_snapshot(snapshots: dict[Path, bytes | None]) -> None:
    failures: list[str] = []
    for path, content in reversed(list(snapshots.items())):
        try:
            if content is None:
                path.unlink(missing_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        except OSError as exc:
            failures.append(f"{path}: {exc}")
    if failures:
        raise OSError("Rollback incomplete: " + "; ".join(failures))


def install(root: Path, target: Path, language: str, domain: str, policy: str, dry_run: bool) -> int:
    languages = supported_languages(root)
    if language not in languages:
        raise SystemExit(f"language: {'|'.join(languages)}")
    if domain not in SUPPORTED_DOMAINS:
        raise SystemExit(f"domain: {'|'.join(SUPPORTED_DOMAINS)}")
    if policy not in SUPPORTED_POLICIES:
        raise SystemExit(f"policy: {'|'.join(SUPPORTED_POLICIES)}")

    files = collect_files(root, domain)
    state: dict[str, Any] = {}
    existing_manifest = manifest_path(target)
    if existing_manifest.is_file():
        previous = load_manifest(target)
        state = {item["path"]: item for item in previous.get("files", [])}

    # Validate every source and destination before changing the project.
    plan: list[tuple[str, Path, Path]] = []
    for rel in files:
        src = resolve_source(root, language, rel)
        dst = safe_target_path(target, rel)
        if not src.is_file():
            raise SystemExit(f"Missing template: {rel}")
        plan.append((rel, src, dst))

    if language != "en":
        print(f"Language resource mode: {language} (translated locale with English fallback for missing domain resources)")

    if dry_run:
        for rel, _src, dst in plan:
            print(f"[DRY-RUN] {'EXIST' if dst.exists() else 'CREATE'} {rel}")
        print(f"Install preview: language={language} domain={domain} files={len(files)}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    snapshots: dict[Path, bytes | None] = {}
    try:
        for rel, src, dst in plan:
            action = "create"
            if dst.exists():
                action = policy if policy != "ask" else prompt_policy(rel)
            if action == "skip":
                continue
            if dst not in snapshots:
                snapshots[dst] = dst.read_bytes() if dst.is_file() else None
            dst.parent.mkdir(parents=True, exist_ok=True)
            if action == "merge":
                write_text(dst, merge_text(dst.read_text(encoding="utf-8"), src.read_text(encoding="utf-8"), rel))
            else:
                shutil.copyfile(src, dst)
            state[rel] = {"path": rel, "installed_sha256": sha256_file(dst), "source_sha256": sha256_file(src)}

        manifest = {
            "schema_version": SCHEMA_VERSION,
            "product": "AIEngineeringStandard",
            "distribution": "package",
            "coding_standard_version": read_version(root),
            "language": language,
            "domain": domain,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "source_root": str(root),
            "files": [state[p] for p in sorted(state)],
        }
        manifest_file = manifest_path(target)
        if manifest_file not in snapshots:
            snapshots[manifest_file] = manifest_file.read_bytes() if manifest_file.is_file() else None
        write_text_atomic(manifest_file, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    except BaseException as original:
        try:
            restore_snapshot(snapshots)
        except OSError as rollback_error:
            raise SystemExit(f"Installation failed ({original}); {rollback_error}") from original
        raise

    print(f"Installed: language={language} domain={domain} version={manifest['coding_standard_version']} files={len(state)}")
    return 0

def state(target: Path, as_json: bool) -> int:
    data = load_manifest(target)
    tracked = data.get("files", [])
    modified, missing = [], []
    for item in tracked:
        path = safe_target_path(target, item["path"])
        if not path.is_file():
            missing.append(item["path"])
        elif sha256_file(path) != item.get("installed_sha256"):
            modified.append(item["path"])
    result = {"installed": True, "version": data.get("coding_standard_version"), "language": data.get("language"), "domain": data.get("domain"), "files": len(tracked), "modified": len(modified), "missing": len(missing)}
    if as_json:
        print(json.dumps({**result, "modified_paths": modified, "missing_paths": missing}, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {str(value).lower() if isinstance(value, bool) else value}")
        for label, paths in (("modified_paths", modified), ("missing_paths", missing)):
            if paths:
                print(f"{label}:")
                for path in paths:
                    print(f"  {path}")
    return 2 if modified or missing else 0


def update(root: Path, target: Path, policy: str, dry_run: bool) -> int:
    data = load_manifest(target)
    language = str(data["language"])
    domain = str(data["domain"])
    old_files = {item["path"]: item for item in data.get("files", [])}
    desired_paths = set(collect_files(root, domain))
    rc = install(root, target, language, domain, policy, dry_run)
    if rc or dry_run:
        return rc
    current = load_manifest(target)
    current_paths = {item["path"] for item in current.get("files", [])}
    for rel, item in old_files.items():
        if rel in desired_paths or rel not in current_paths:
            continue
        path = safe_target_path(target, rel)
        if not path.exists():
            continue
        if sha256_file(path) == item.get("installed_sha256"):
            path.unlink()
            print(f"Removed obsolete managed file: {rel}")
        else:
            print(f"Preserved modified obsolete file: {rel}")
    current["files"] = [item for item in current.get("files", []) if item["path"] in desired_paths and safe_target_path(target, item["path"]).is_file()]
    write_text(manifest_path(target), json.dumps(current, ensure_ascii=False, indent=2) + "\n")
    return 0


def uninstall(target: Path, force: bool, dry_run: bool) -> int:
    data = load_manifest(target)
    modified = []
    for item in data.get("files", []):
        path = safe_target_path(target, item["path"])
        if not path.exists():
            continue
        if sha256_file(path) != item.get("installed_sha256"):
            modified.append(item["path"])
            continue
        if dry_run:
            print(f"[DRY-RUN] REMOVE {item['path']}")
        else:
            path.unlink()
            print(f"Removed: {item['path']}")
    if modified and not force:
        print("Refusing to remove modified files without --force:")
        for rel in modified:
            print(f"  {rel}")
        return 2
    for rel in modified:
        path = safe_target_path(target, rel)
        if dry_run:
            print(f"[DRY-RUN] FORCE REMOVE {rel}")
        elif path.exists():
            path.unlink()
            print(f"Force removed: {rel}")
    if dry_run:
        print(f"Uninstall preview: files={len(data.get('files', []))}")
        return 0
    manifest_path(target).unlink(missing_ok=True)
    try:
        (target / MANIFEST_DIR).rmdir()
    except OSError:
        pass
    return 0


def validate(target: Path) -> int:
    try:
        data = load_manifest(target)
    except SystemExit as exc:
        print(str(exc))
        return 2
    if data.get("product") not in ("codingStandard", "AIEngineeringStandard"):
        print("Invalid product identity in installation manifest.")
        return 2
    return state(target, False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    install_parser = sub.add_parser("install")
    install_parser.add_argument("target", nargs="?", default=".")
    install_parser.add_argument("language", nargs="?")
    install_parser.add_argument("domain", nargs="?")
    install_parser.add_argument("policy", nargs="?", default="ask")
    install_parser.add_argument("dry_run", nargs="?", default="false")
    state_parser = sub.add_parser("state")
    state_parser.add_argument("target", nargs="?", default=".")
    state_parser.add_argument("--json", action="store_true")
    update_parser = sub.add_parser("update")
    update_parser.add_argument("target", nargs="?", default=".")
    update_parser.add_argument("--policy", choices=SUPPORTED_POLICIES, default="merge")
    update_parser.add_argument("--dry-run", action="store_true")
    uninstall_parser = sub.add_parser("uninstall")
    uninstall_parser.add_argument("target", nargs="?", default=".")
    uninstall_parser.add_argument("--force", action="store_true")
    uninstall_parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "install":
        language = args.language or prompt_language()
        domain = args.domain or prompt_domain()
        if args.dry_run not in {"true", "false"}:
            raise SystemExit("dry_run: true|false")
        root = Path(__file__).resolve().parents[2]
        return install(root, Path(args.target).resolve(), language, domain, args.policy, args.dry_run == "true")
    target = Path(args.target).resolve()
    if args.command == "state":
        return state(target, args.json)
    if args.command == "update":
        root = Path(__file__).resolve().parents[2]
        return update(root, target, args.policy, args.dry_run)
    return uninstall(target, args.force, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
