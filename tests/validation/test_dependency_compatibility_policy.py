#!/usr/bin/env python3
"""Contract tests for the normative dependency compatibility policy."""
from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "core" / "common" / "dependency-compatibility-policy.md"
class DependencyCompatibilityPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None: cls.text = POLICY.read_text(encoding="utf-8")
    def test_selected_library_is_a_compatibility_anchor(self) -> None:
        self.assertIn("compatibility anchor", self.text); self.assertIn("preserve the developer's selected library/version", self.text)
    def test_policy_requires_smallest_compatible_change(self) -> None:
        self.assertIn("smallest compatible change", self.text); self.assertNotIn("minimum compatible change", self.text)
    def test_policy_rejects_unrelated_dependency_drift(self) -> None:
        self.assertIn("broad or unexplained upgrades/downgrades", self.text); self.assertIn("unjustified broad dependency change", self.text)
    def test_policy_requires_runtime_validation_and_recording(self) -> None:
        self.assertIn("smoke testing", self.text); self.assertIn("regression testing", self.text); self.assertIn("result and evidence are recorded", self.text)
if __name__ == "__main__": unittest.main()
