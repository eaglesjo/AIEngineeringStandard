#!/usr/bin/env python3
"""Validate consistency between runtime locale resources and documentation catalog."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "i18n" / "languages.json"
QUALITY = ROOT / "i18n" / "quality.json"
REQUIRED_COMMON = ("core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md")

# Localized terms accepted as explicit references to runtime/execution support.
# The validator checks the semantic claim in the locale's own language rather
# than requiring the English word "runtime" to appear in every README.
RUNTIME_TERMS: dict[str, tuple[str, ...]] = {
    "ar": ("التشغيل", "بيئة التشغيل"),
    "de": ("Laufzeit", "Laufzeitumgebung"),
    "en": ("runtime",),
    "es": ("ejecución", "entorno de ejecución"),
    "fr": ("exécution", "environnement d’exécution", "environnement d'exécution"),
    "hi": ("रनटाइम", "रनटाइम वातावरण"),
    "id": ("runtime", "waktu proses", "lingkungan runtime"),
    "it": ("runtime", "ambiente di esecuzione"),
    "ja": ("ランタイム", "実行環境"),
    "ko": ("런타임", "실행 환경"),
    "nl": ("runtime", "runtimeomgeving"),
    "pl": ("uruchomieni", "środowiskiem uruchomieniowym", "środowisko uruchomieniowe"),
    "pt": ("runtime", "ambiente de execução"),
    "ru": ("среда выполнения", "выполнения"),
    "sv": ("runtime", "körningsmiljö"),
    "th": ("รันไทม์", "สภาพแวดล้อมรันไทม์"),
    "tr": ("çalışma zamanı", "çalışma zamanında"),
    "uk": ("середовище виконання", "виконання"),
    "vi": ("runtime", "môi trường chạy", "môi trường thực thi"),
    "zh-CN": ("运行时", "运行环境"),
}


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path.relative_to(ROOT)}")
    return value


def entries(catalog: dict, key: str) -> dict[str, dict]:
    value = catalog.get(key)
    if not isinstance(value, list):
        raise ValueError(f"i18n/languages.json {key} must be a list")
    result: dict[str, dict] = {}
    for entry in value:
        if not isinstance(entry, dict) or not isinstance(entry.get("locale"), str):
            raise ValueError(f"i18n/languages.json {key} contains an invalid entry")
        locale = entry["locale"]
        if locale in result:
            raise ValueError(f"duplicate locale in {key}: {locale}")
        result[locale] = entry
    return result


def validate_documentation_claim(locale: str, entry: dict, required_count: int) -> list[str]:
    errors: list[str] = []
    doc_path = entry.get("path")
    display_name = entry.get("name")
    if not isinstance(doc_path, str):
        return [f"{locale}: documentation path is missing"]
    if not isinstance(display_name, str) or not display_name.strip():
        errors.append(f"{locale}: documentation display name is missing")
    path = ROOT / doc_path
    if not path.is_file():
        errors.append(f"{locale}: documentation file does not exist: {doc_path}")
        return errors

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{locale}: documentation file cannot be read: {doc_path}: {exc}")
        return errors

    if isinstance(display_name, str) and display_name.strip() and display_name not in text:
        errors.append(f"{locale}: documentation does not identify locale as {display_name}")

    runtime_terms = RUNTIME_TERMS.get(locale, ("runtime",))
    if not any(term.casefold() in text.casefold() for term in runtime_terms):
        errors.append(f"{locale}: documentation does not describe runtime support")

    # Every runtime locale README must expose the current contract size so stale
    # "docs-only" or partial-runtime claims cannot silently survive a release.
    if str(required_count) not in text:
        errors.append(f"{locale}: documentation does not state the current runtime locale count ({required_count})")

    return errors


def validate() -> int:
    try:
        catalog = load_json(CATALOG)
        quality = load_json(QUALITY)
        runtime = entries(catalog, "runtime_resources")
        docs = entries(catalog, "documentation")
    except ValueError as exc:
        print(f"i18n consistency failed: {exc}", file=sys.stderr)
        return 1

    required = quality.get("required_runtime_locales")
    if not isinstance(required, list) or not required:
        print("i18n consistency failed: required_runtime_locales must be a non-empty list", file=sys.stderr)
        return 1

    errors: list[str] = []
    runtime_locales = set(runtime)
    required_locales = set(required)
    if runtime_locales != required_locales:
        errors.append(
            "runtime locale set mismatch: "
            f"catalog-only={sorted(runtime_locales - required_locales)}, "
            f"quality-only={sorted(required_locales - runtime_locales)}"
        )

    for locale in required:
        entry = runtime.get(locale)
        if entry is None:
            continue
        path_value = entry.get("path")
        if not isinstance(path_value, str):
            errors.append(f"{locale}: runtime path is missing")
            continue
        runtime_root = ROOT / path_value
        if not runtime_root.is_dir():
            errors.append(f"{locale}: runtime path does not exist: {path_value}")
            continue
        for rel in REQUIRED_COMMON:
            if not (runtime_root / rel).is_file():
                errors.append(f"{locale}: missing runtime resource: {path_value}/{rel}")

        doc = docs.get(locale)
        if doc is None:
            errors.append(f"{locale}: missing documentation catalog entry")
            continue
        errors.extend(validate_documentation_claim(locale, doc, len(required)))

    doc_locales = set(docs)
    if not required_locales.issubset(doc_locales):
        errors.append(f"documentation missing runtime locales: {sorted(required_locales - doc_locales)}")

    if errors:
        print("i18n consistency failed:")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print(f"i18n consistency OK: {len(required)} runtime locales mapped to documentation")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
