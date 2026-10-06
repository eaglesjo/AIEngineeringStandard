from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.validation.check_i18n import validate


COMMON = ("core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md")
LOCALE_TERMS = {
    "ko": "환경 메모리 Early Stopping Checkpoint",
    "zh-CN": "环境 内存 Early Stopping Checkpoint",
    "ja": "環境 メモリ Early Stopping Checkpoint",
    "ru": "среда память Early Stopping Checkpoint",
}


def write(path: Path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def build_tree(root: Path, runtime_locales: tuple[str, ...] = ("en", "ko"), docs_only: tuple[str, ...] = ()) -> None:
    write(root / "README.md", "English")
    documentation = [{"locale": "en", "name": "English", "path": "README.md"}]
    for locale in runtime_locales:
        if locale == "en":
            continue
        write(root / f"i18n/{locale}/README.md", locale)
        documentation.append({"locale": locale, "name": locale, "path": f"i18n/{locale}/README.md"})
    for locale in docs_only:
        write(root / f"i18n/{locale}/README.md", locale)
        documentation.append({"locale": locale, "name": locale, "path": f"i18n/{locale}/README.md"})

    for rel in COMMON:
        write(root / rel, "environment memory Early Stopping Checkpoint")

    runtime_resources = []
    for locale in runtime_locales:
        path = "." if locale == "en" else f"i18n/{locale}"
        runtime_resources.append(
            {
                "locale": locale,
                "name": locale,
                "path": path,
                "fallback": None if locale == "en" else "en",
            }
        )
        if locale != "en":
            terms = LOCALE_TERMS.get(locale, "environment memory Early Stopping Checkpoint")
            for rel in COMMON:
                write(root / path / rel, terms)

    write(
        root / "i18n/languages.json",
        json.dumps(
            {
                "default": "en",
                "documentation": documentation,
                "runtime_resources": runtime_resources,
            }
        ),
    )


class I18nParityTests(unittest.TestCase):
    def test_non_korean_documentation_locale_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_tree(root, runtime_locales=("en", "ko"), docs_only=("fr", "es", "tr"))
            errors = validate(root, root / "i18n/languages.json")
            self.assertTrue(any("documentation locale set must be exactly en,ko" in error for error in errors))

    def test_missing_runtime_common_resource_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_tree(root)
            (root / "i18n/ko/core/common/ENVIRONMENT.md").unlink()
            errors = validate(root, root / "i18n/languages.json")
            self.assertTrue(any("missing required common resource" in error for error in errors))

    def test_unsupported_runtime_locale_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_tree(root, runtime_locales=("en", "xx"))
            errors = validate(root, root / "i18n/languages.json")
            self.assertTrue(any("unsupported locale remains in catalog" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
