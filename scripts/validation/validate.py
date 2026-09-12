from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_HARDWARE_PATTERNS = [re.compile(r"RTX\s*3050", re.I), re.compile(r"3050\s*Ti", re.I), re.compile(r"4\s*GB\s*VRAM", re.I), re.compile(r"16\s*GB\s*(RAM|System RAM)", re.I)]
ROUTING_FILES = ["CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md", ".github/instructions/ml.instructions.md", ".github/instructions/llm.instructions.md", ".github/instructions/vision.instructions.md", ".github/instructions/colab.instructions.md", ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md", ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md", ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md"]
LEGACY_EXECUTION_REFS = ("COMMON/AGENT.md", "COMMON/SKILL.md", "COMMON/ENVIRONMENT.md", "LLM/environment.py", "LLM/memory_smoke_test.py", "VISION/memory_smoke_test.py", "scripts/validate.py", "scripts/check_i18n.py", "scripts/test_installers.py")
REQUIRED_FILES = [
    "VERSION", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "INSTALL.md", "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "core/common/environment.py", "core/common/experiment.py", "core/common/dependencies.py", "core/common/dependency-compatibility-policy.md", "core/agent/README.md", "core/skill/README.md", "core/skill/PORTABLE_SKILL_CONTRACT.md", "core/plugin/README.md", "core/mcp/README.md", "core/validation/README.md", "core/validation/conformance-result.schema.json", "core/validation/conformance-evidence.schema.json", "core/validation/SECURITY_PROVENANCE_CONTRACT.md", "core/validation/security-result.schema.json", "profiles/agent/README.md", "compatibility/agents.json",
    "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/ml/ENVIRONMENT.md", "domains/ml/README.md", "domains/ml/skills/README.md", "domains/ml/skills/data/SKILL.md", "domains/ml/skills/evaluation/SKILL.md", "domains/ml/skills/experiment/SKILL.md", "domains/ml/skills/training/SKILL.md", "domains/ml/skills/distributed-training/SKILL.md", "domains/ml/skills/hyperparameter-optimization/SKILL.md", "domains/ml/skills/inference/SKILL.md", "domains/ml/skills/mlops/SKILL.md", "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md", "domains/llm/environment.py", "domains/llm/memory_smoke_test.py", "domains/llm/experiment.py", "domains/llm/skills/finetuning/SKILL.md", "domains/llm/skills/peft/SKILL.md", "domains/llm/skills/quantization/SKILL.md", "domains/llm/skills/rag/SKILL.md", "domains/vision/AGENT.md", "domains/vision/SKILL.md", "domains/vision/ENVIRONMENT.md", "domains/vision/memory_smoke_test.py", "domains/vision/README.md", "platform/colab/AGENT.md", "platform/colab/SKILL.md", "platform/colab/validate_runtime.py", "examples/colab/clean_runtime_validation.ipynb", "examples/colab/llm_qlora_validation.ipynb", "docs/development/ML_RUNTIME_VALIDATION.md", "tests/integration/ml_classification_smoke.py", "tests/integration/llm_qlora_strategy_smoke.py", "tests/integration/test_dependency_resolver_pip.py",
    "tests/validation/fixtures/conformance-result.pass.json", "tests/validation/fixtures/conformance/codex-static.expected.json", "tests/validation/fixtures/conformance/codex-runtime.scenario.json", "tests/validation/fixtures/conformance/codex-runtime-failure-recovery.scenario.json", "tests/validation/fixtures/security-result.pass.json", "tests/validation/fixtures/portable-skill/SKILL.md", "tests/validation/fixtures/dependency-alignment-selected-library.json", "tests/validation/test_dependency_alignment.py", "tests/validation/test_dependency_compatibility_policy.py", "scripts/validation/resolve_dependency_alignment.py", "scripts/validation/validate_2_0_schemas.py", "scripts/validation/validate_portable_skill.py", "scripts/validation/run_conformance.py", "scripts/validation/validate_conformance_fixture.py", "scripts/validation/run_runtime_conformance.py",
    ".github/instructions/ml.instructions.md", ".github/instructions/colab.instructions.md", "scripts/installers/install-domains.ps1", "scripts/installers/install-domains.sh", "scripts/validation/check_i18n.py", "scripts/validation/check_i18n_quality.py", "scripts/validation/check_i18n_consistency.py", "scripts/validation/check_structure.py", "scripts/validation/validate-domains.py", "scripts/validation/validate_agent_routing.py", "scripts/validation/validate_profiles.py", "scripts/installers/test_installers.py", "scripts/development/test_environment.py", "scripts/development/test_dependencies.py", "scripts/installers/test_installers_windows.ps1", ".github/workflows/windows-install-test.yml", "tests/validation/test_i18n_consistency.py", "tests/colab/README.md", "tests/colab/codingstandard_colab_test.ipynb", "LICENSE",
]

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr); raise SystemExit(1)
def run_checker(path: Path, label: str, *args: str) -> None:
    proc = subprocess.run([sys.executable, str(path), *args], cwd=str(ROOT), capture_output=True, text=True, check=False)
    if proc.stdout: print(proc.stdout, end="")
    if proc.returncode != 0:
        if proc.stderr: print(proc.stderr, file=sys.stderr, end="")
        fail(f"{label} failed")
def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing: fail("Missing required files: " + ", ".join(missing))
def check_python() -> None:
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts: continue
        try: ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc: fail(f"Python syntax error in {path}: {exc}")
def run_environment_tests() -> None:
    for path, label in (("test_environment.py", "Environment detection tests"), ("test_dependencies.py", "Dependency contract tests"), ("test_dependency_compatibility_policy.py", "Dependency compatibility policy tests"), ("test_dependency_alignment.py", "Dependency alignment tests")):
        run_checker(ROOT / ("tests" / "validation" / path) if path.startswith("test_dependency_") else (ROOT / "scripts" / "development" / path), label)
    run_checker(ROOT / "tests" / "integration" / "test_dependency_resolver_pip.py", "Real pip dependency resolver tests")
    run_checker(ROOT / "scripts" / "validation" / "validate-domains.py", "Domain resource validation")
    run_checker(ROOT / "scripts" / "validation" / "validate_agent_routing.py", "Agent routing validation")
def run_2_0_validation() -> None:
    run_checker(ROOT / "scripts" / "validation" / "validate_2_0_schemas.py", "AIEngineeringStandard 2.0 schema validation")
    run_checker(ROOT / "scripts" / "validation" / "validate_portable_skill.py", "Portable Agent Skill validation")
    run_checker(ROOT / "scripts" / "validation" / "run_conformance.py", "AIEngineeringStandard 2.0 static conformance", "--agent", "codex", "--check-only", "--output", "/tmp/codex-conformance.json")
    run_checker(ROOT / "scripts" / "validation" / "validate_conformance_fixture.py", "AIEngineeringStandard 2.0 conformance fixture", "--agent", "codex", "--result", "/tmp/codex-conformance.json")
    run_checker(ROOT / "scripts" / "validation" / "run_runtime_conformance.py", "AIEngineeringStandard 2.0 runtime harness dry run", "--agent", "codex", "--output", "/tmp/codex-runtime-conformance.json")
    run_checker(ROOT / "scripts" / "validation" / "run_runtime_conformance.py", "AIEngineeringStandard 2.0 recovery harness dry run", "--agent", "codex", "--scenario", "tests/validation/fixtures/conformance/codex-runtime-failure-recovery.scenario.json", "--output", "/tmp/codex-runtime-recovery.json")
def check_notebook() -> None:
    for path in (ROOT / "tests" / "colab" / "codingstandard_colab_test.ipynb", ROOT / "examples" / "colab" / "clean_runtime_validation.ipynb", ROOT / "examples" / "colab" / "llm_qlora_validation.ipynb"):
        try: notebook = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc: fail(f"Invalid Colab notebook JSON: {exc}")
        if notebook.get("nbformat") != 4: fail(f"Colab notebook must use nbformat 4: {path}")
        if not notebook.get("cells"): fail(f"Colab notebook has no cells: {path}")
def check_routing_paths() -> None:
    for rel in ROUTING_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for legacy in LEGACY_EXECUTION_REFS:
            if legacy in text: fail(f"Obsolete execution reference '{legacy}' remains in {rel}")
def check_hardware_neutrality() -> None:
    for root in (ROOT / "core", ROOT / "domains", ROOT / "platform"):
        for path in root.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_HARDWARE_PATTERNS:
                if pattern.search(text): fail(f"Machine-specific hardware assumption in {path}: {pattern.pattern}")
def check_no_legacy_installer() -> None:
    for path in (ROOT / "scripts").glob("install-coding-standard.*"): fail(f"Legacy installer must not exist before release: {path.name}")
def check_windows_workflow() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-install-test.yml").read_text(encoding="utf-8")
    if "runs-on: windows-latest" not in workflow: fail("Windows workflow must use the windows-latest runner")
    test_script = (ROOT / "scripts" / "installers" / "test_installers_windows.ps1").read_text(encoding="utf-8")
    haystack = workflow + "\n" + test_script
    for required in ("powershell", "pwsh", "-DryRun", "-ConflictAction Merge", "domains/ml", "platform/colab"):
        if required.lower() not in haystack.lower(): fail(f"Windows validation missing: {required}")
def check_version_consistency() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version): fail(f"VERSION must use semantic versioning: {version!r}")
    common_env = (ROOT / "core" / "common" / "environment.py").read_text(encoding="utf-8")
    match = re.search(r'STANDARD_VERSION\s*=\s*["\']([^"\']+)["\']', common_env)
    if not match: fail("core/common/environment.py is missing STANDARD_VERSION")
    if match.group(1) != version: fail(f"Version mismatch: VERSION={version}, core/common/environment.py={match.group(1)}")
def run_structure_check() -> None: run_checker(ROOT / "scripts" / "validation" / "check_structure.py", "Repository structure validation")
def run_profile_check() -> None: run_checker(ROOT / "scripts" / "validation" / "validate_profiles.py", "Architecture profile validation")
def run_i18n_check() -> None:
    run_checker(ROOT / "scripts" / "validation" / "check_i18n.py", "Multilingual localization check")
    run_checker(ROOT / "scripts" / "validation" / "check_i18n_quality.py", "i18n quality validation")
    run_checker(ROOT / "scripts" / "validation" / "check_i18n_consistency.py", "i18n runtime/documentation consistency")
def main() -> None:
    check_required_files(); run_structure_check(); run_profile_check(); check_python(); run_2_0_validation(); run_environment_tests(); check_notebook(); check_routing_paths(); check_hardware_neutrality(); check_no_legacy_installer(); check_windows_workflow(); check_version_consistency(); run_i18n_check(); print("codingStandard validation passed")
if __name__ == "__main__": main()
