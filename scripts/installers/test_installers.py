#!/usr/bin/env python3
"""Integration-test the cross-platform codingStandard installer lifecycle."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PS1 = ROOT / "scripts" / "installers" / "install-domains.ps1"
SH = ROOT / "scripts" / "installers" / "install-domains.sh"
ENGINE = ROOT / "scripts" / "installers" / "installation.py"
COMMON = [
    "AGENTS.md", ".agents/skills/ai-engineering-standard/SKILL.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md",
    ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md", ".aider.conf.yml",
    "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "core/common/environment.py", "core/common/experiment.py", "core/common/dependencies.py",
]
ML = [".github/instructions/ml.instructions.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/ml/ENVIRONMENT.md", "domains/ml/README.md"]
COLAB = ["platform/colab/AGENT.md", "platform/colab/SKILL.md"]
LOCALES = {"ko"}
UNSUPPORTED_LOCALES = {"fr", "es", "zh-CN", "ja", "ru", "tr", "de", "it", "pt", "ar", "hi", "id", "vi", "th", "nl", "pl", "sv", "uk"}


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=check, text=True, capture_output=True)


def check(target: Path, paths: list[str]) -> None:
    missing = [p for p in paths if not (target / p).is_file()]
    if missing:
        raise AssertionError(f"missing installed files: {missing}")


def lifecycle(target: Path) -> None:
    manifest = target / ".codingstandard" / "installation.json"
    if not manifest.is_file():
        raise AssertionError("installation manifest missing")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["schema_version"] == 2
    assert data["coding_standard_version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert data["language"] == "en"
    assert data["domain"] == "all"
    assert data["files"]

    state = run(["python3", str(ENGINE), "state", str(target)])
    assert "installed: true" in state.stdout
    assert "modified: 0" in state.stdout
    assert "missing: 0" in state.stdout

    removed = target / ML[0]
    removed.unlink()
    update = run(["bash", str(ROOT / "scripts/installers/update-domains.sh"), str(target), "--policy", "overwrite"])
    assert "Installed:" in update.stdout
    assert removed.is_file(), "update did not restore missing managed file"

    tracked = target / "AGENTS.md"
    tracked.write_text(tracked.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
    bad = run(["bash", str(ROOT / "scripts/installers/uninstall-domains.sh"), str(target)], check=False)
    assert bad.returncode == 2
    assert tracked.exists(), "modified file was removed without --force"
    assert manifest.exists(), "manifest disappeared after protected uninstall"

    forced = run(["bash", str(ROOT / "scripts/installers/uninstall-domains.sh"), str(target), "--force"])
    assert forced.returncode == 0
    assert not manifest.exists()
    assert not tracked.exists()


def test_bash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "new-project"
        dry = run(["bash", str(SH), str(target), "en", "all", "overwrite", "true"])
        assert not target.exists() or not any(target.iterdir()), "bash dry-run modified target"
        assert "DRY-RUN" in dry.stdout
        run(["bash", str(SH), str(target), "en", "all", "overwrite", "false"])
        check(target, COMMON + ML + COLAB)
        lifecycle(target)
        for locale in sorted(LOCALES):
            locale_target = Path(tmp) / f"{locale}-project"
            result = run(["bash", str(SH), str(locale_target), locale, "common", "overwrite", "false"])
            check(locale_target, COMMON)
            assert f"language={locale}" in result.stdout
        for locale in sorted(UNSUPPORTED_LOCALES):
            result = run(["bash", str(SH), str(Path(tmp) / f"unsupported-{locale}"), locale, "common", "overwrite", "false"], check=False)
            assert result.returncode != 0, f"unsupported locale was accepted: {locale}"


def test_manifest_path_traversal() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        target = base / "project"
        manifest_dir = target / ".codingstandard"
        manifest_dir.mkdir(parents=True)
        outside = base / "outside.txt"
        outside.write_text("keep this file safe\\n", encoding="utf-8")
        (manifest_dir / "installation.json").write_text(
            json.dumps({
                "schema_version": 2,
                "files": [{"path": "../outside.txt", "installed_sha256": "0" * 64}],
            }),
            encoding="utf-8",
        )
        result = run(["python3", str(ENGINE), "uninstall", str(target)], check=False)
        assert result.returncode != 0, "uninstaller accepted a path-traversal manifest entry"
        assert outside.read_text(encoding="utf-8") == "keep this file safe\\n"



def test_manifest_integrity_validation() -> None:
    malformed_manifests = [
        [],
        None,
        {"schema_version": 2, "files": {}},
        {"schema_version": 2, "files": ["AGENTS.md"]},
        {"schema_version": 2, "files": [{"path": "AGENTS.md"}]},
        {"schema_version": 2, "files": [{"path": "AGENTS.md", "installed_sha256": "not-a-digest"}]},
        {"schema_version": 2, "files": [
            {"path": "AGENTS.md", "installed_sha256": "0" * 64},
            {"path": "AGENTS.md", "installed_sha256": "1" * 64},
        ]},
        {"schema_version": 2, "files": [{"path": "AGENTS.md", "installed_sha256": "0" * 64, "source_sha256": "invalid"}]},
    ]
    for index, payload in enumerate(malformed_manifests):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            manifest_dir = target / ".codingstandard"
            manifest_dir.mkdir(parents=True)
            tracked = target / "AGENTS.md"
            tracked.write_text("keep this file safe\\n", encoding="utf-8")
            (manifest_dir / "installation.json").write_text(json.dumps(payload), encoding="utf-8")
            for command in ("state", "uninstall"):
                result = run(["python3", str(ENGINE), command, str(target)], check=False)
                assert result.returncode != 0, f"accepted malformed manifest #{index} with {command}"
            assert tracked.read_text(encoding="utf-8") == "keep this file safe\\n"
            assert (manifest_dir / "installation.json").is_file(), "malformed manifest was removed"



def test_install_rollback_on_write_failure() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        run(["bash", str(SH), str(target), "en", "common", "overwrite", "false"])
        manifest = target / ".codingstandard" / "installation.json"
        original_manifest = manifest.read_bytes()
        tracked = target / "AGENTS.md"
        original_tracked = tracked.read_bytes()
        injected_failure = r"""
import importlib.util
import sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("installation", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original_copy = module.shutil.copyfile
calls = 0
def fail_on_second_copy(source, destination):
    global calls
    calls += 1
    if calls == 2:
        Path(destination).write_text("partial failed write", encoding="utf-8")
        raise OSError("injected copy failure")
    return original_copy(source, destination)
module.shutil.copyfile = fail_on_second_copy
try:
    module.install(Path(sys.argv[2]), Path(sys.argv[3]), "en", "common", "overwrite", False)
except OSError as exc:
    assert "injected copy failure" in str(exc)
else:
    raise AssertionError("injected installer failure did not occur")
finally:
    module.shutil.copyfile = original_copy
"""
        result = run(["python3", "-c", injected_failure, str(ENGINE), str(ROOT), str(target)], check=False)
        assert result.returncode == 0, result.stderr
        assert manifest.read_bytes() == original_manifest, "manifest changed despite failed installation"
        assert tracked.read_bytes() == original_tracked, "tracked file was not restored after failure"
        assert not list((target / ".codingstandard").glob(".installation-*.tmp")), "atomic manifest temp file leaked"


def test_symlink_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        target = base / "project"
        outside = base / "outside"
        target.mkdir()
        outside.mkdir()
        (outside / "copilot-instructions.md").write_text("keep this file safe\\n", encoding="utf-8")
        try:
            (target / ".github").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            return

        result = run(
            ["python3", str(ENGINE), "install", str(target), "en", "common", "overwrite", "false"],
            check=False,
        )
        assert result.returncode != 0, "installer accepted a symlinked managed directory"
        assert (outside / "copilot-instructions.md").read_text(encoding="utf-8") == "keep this file safe\\n"
        assert not (outside / "copilot-instructions.md").is_symlink()


def test_powershell() -> None:
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        return
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "new-project"
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "all", "-Policy", "overwrite", "-DryRun"])
        assert not target.exists() or not any(target.iterdir()), "PowerShell dry-run modified target"
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "ml", "-Policy", "overwrite"])
        check(target, COMMON + ML)
        state = run([executable, "-NoProfile", "-File", str(ROOT / "scripts/installers/state-domains.ps1"), "-Target", str(target)])
        assert "installed: true" in state.stdout
        for locale in LOCALES:
            locale_target = Path(tmp) / f"ps-{locale}-project"
            run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(locale_target), "-Language", locale, "-Domain", "common", "-Policy", "overwrite"])
            check(locale_target, COMMON)


def main() -> int:
    test_bash()
    test_manifest_path_traversal()
    test_manifest_integrity_validation()
    test_install_rollback_on_write_failure()
    test_symlink_escape()
    test_powershell()
    print("installer lifecycle tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
