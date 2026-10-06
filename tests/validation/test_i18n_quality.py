#!/usr/bin/env python3
"""Tests for the v1.16 i18n quality validator."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "validation" / "check_i18n_quality.py"

spec = importlib.util.spec_from_file_location("check_i18n_quality", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

EXPECTED_LOCALES = ["en", "ko"]
EXPECTED_INTENTS = {
    "environment.validate",
    "resources.memory.measure",
    "tasks.early_stopping",
    "recovery.checkpoint",
    "behavior_change.tests",
}


def test_grade_order() -> None:
    assert module.grade(True, True, True) == "A"
    assert module.grade(True, True, False) == "B"
    assert module.grade(True, False, False) == "C"
    assert module.grade(False, True, False) == "D"
    assert module.grade(False, False, False) == "F"


def test_quality_contract_is_korean_locale_contract() -> None:
    quality = json.loads((ROOT / "i18n" / "quality.json").read_text(encoding="utf-8"))
    assert quality["contract_version"] == "1.16"
    assert quality["canonical_locale"] == "en"
    assert quality["required_runtime_locales"] == EXPECTED_LOCALES
    assert quality["quality_levels"]["runtime_minimum"] == "A"


def test_policy_intents_have_complete_korean_vocabulary() -> None:
    vocabulary = json.loads((ROOT / "i18n" / "concepts" / "policy-vocabulary.json").read_text(encoding="utf-8"))
    concepts = vocabulary["concepts"]
    assert EXPECTED_INTENTS <= concepts.keys()
    for intent_id in EXPECTED_INTENTS:
        intent = concepts[intent_id]
        assert intent["required"] is True
        assert intent["canonical"]
        assert set(intent["locales"]) == set(EXPECTED_LOCALES)
        assert all(intent["locales"][locale] for locale in EXPECTED_LOCALES)


def test_semantic_parity_uses_policy_intent_vocabulary() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        canonical = root / "core/common/AGENT.md"
        localized = root / "i18n/ko/core/common/AGENT.md"
        canonical.parent.mkdir(parents=True)
        localized.parent.mkdir(parents=True)
        canonical.write_text("Validate the environment and runtime.\n", encoding="utf-8")
        localized.write_text("실행환경과 런타임을 검증합니다.\n", encoding="utf-8")
        old_root = module.ROOT
        try:
            module.ROOT = root
            failures = module.semantic_parity(
                "ko",
                {"path": "i18n/ko"},
                {
                    "concepts": {
                        "environment.validate": {
                            "required": True,
                            "canonical": ["environment", "runtime"],
                            "locales": {"ko": ["환경", "런타임"]},
                        }
                    }
                },
            )
        finally:
            module.ROOT = old_root
        assert failures == []


if __name__ == "__main__":
    test_grade_order()
    test_quality_contract_is_korean_locale_contract()
    test_policy_intents_have_complete_korean_vocabulary()
    test_semantic_parity_uses_policy_intent_vocabulary()
    print("i18n quality tests passed")
