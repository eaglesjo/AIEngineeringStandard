#!/usr/bin/env python3
"""Tests for the runtime/documentation consistency validator."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "validation" / "check_i18n_consistency.py"
spec = importlib.util.spec_from_file_location("check_i18n_consistency", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_catalog_entries_reject_duplicates() -> None:
    catalog = {
        "runtime_resources": [
            {"locale": "en", "path": "."},
            {"locale": "en", "path": "i18n/en"},
        ],
        "documentation": [{"locale": "en", "path": "README.md"}],
    }
    try:
        module.entries(catalog, "runtime_resources")
    except ValueError as exc:
        assert "duplicate locale" in str(exc)
    else:
        raise AssertionError("duplicate locale was accepted")


def test_current_documentation_claims_match_runtime_contract() -> None:
    catalog = module.load_json(module.CATALOG)
    docs = module.entries(catalog, "documentation")
    quality = module.load_json(module.QUALITY)
    required = quality["required_runtime_locales"]

    for locale in required:
        errors = module.validate_documentation_claim(locale, docs[locale], len(required))
        assert errors == [], f"{locale}: {errors}"


def test_current_catalog_matches_runtime_contract() -> None:
    assert module.validate() == 0


if __name__ == "__main__":
    test_catalog_entries_reject_duplicates()
    test_current_documentation_claims_match_runtime_contract()
    test_current_catalog_matches_runtime_contract()
    print("i18n consistency tests passed")
