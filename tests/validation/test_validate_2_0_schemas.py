#!/usr/bin/env python3
"""Regression tests for AIEngineeringStandard 2.0 result semantics."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "scripts" / "validation" / "validate_2_0_schemas.py"
FIXTURES = ROOT / "tests" / "validation" / "fixtures"

spec = importlib.util.spec_from_file_location("validate_2_0_schemas", VALIDATOR_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load validator: {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ConformanceResultSemanticTests(unittest.TestCase):
    def assert_invalid_fixture(self, filename: str) -> None:
        data = json.loads((FIXTURES / filename).read_text(encoding="utf-8"))
        with self.assertRaises(SystemExit):
            validator.validate_result(data, filename)

    def test_pass_requires_all_mandatory_checks(self) -> None:
        self.assert_invalid_fixture("conformance-result.invalid.pass-missing-check.json")

    def test_pass_rejects_untested_check(self) -> None:
        self.assert_invalid_fixture("conformance-result.invalid.pass-untested-check.json")

    def test_partial_rejects_failed_check(self) -> None:
        self.assert_invalid_fixture("conformance-result.invalid.partial-fail-check.json")

    def test_untested_rejects_executed_check(self) -> None:
        self.assert_invalid_fixture("conformance-result.invalid.untested-pass-check.json")


if __name__ == "__main__":
    unittest.main()
