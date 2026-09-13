# AI Engineering Standard

<p align="center">
  <strong>AI Development, Training & Agent Engineering Standards</strong>
</p>

<p align="center">
  <strong>v2.0.0 — Public Release Candidate</strong>
</p>

<p align="center">
  <a href="https://github.com/eaglesjo/AIEngineeringStandard/releases"><img src="https://img.shields.io/github/v/release/eaglesjo/AIEngineeringStandard?label=public%20release" alt="Public release"></a>
  <a href="https://github.com/eaglesjo/codingStandard-dev/actions/workflows/validate-coding-standard.yml"><img src="https://github.com/eaglesjo/codingStandard-dev/actions/workflows/validate-coding-standard.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
</p>

**Language:** English · [한국어](i18n/ko/README.md) · [Français](i18n/fr/README.md) · [Español](i18n/es/README.md) · [简体中文](i18n/zh-CN/README.md) · [日本語](i18n/ja/README.md) · [Русский](i18n/ru/README.md) · [Türkçe](i18n/tr/README.md) · [Deutsch](i18n/de/README.md) · [Italiano](i18n/it/README.md) · [Português](i18n/pt/README.md) · [العربية](i18n/ar/README.md) · [हिन्दी](i18n/hi/README.md) · [Bahasa Indonesia](i18n/id/README.md) · [Tiếng Việt](i18n/vi/README.md) · [ไทย](i18n/th/README.md) · [Nederlands](i18n/nl/README.md) · [Polski](i18n/pl/README.md) · [Svenska](i18n/sv/README.md) · [Українська](i18n/uk/README.md)

> **Repository model:** `codingStandard-dev` is the public development and validation gate. Validated releases are promoted to [`eaglesjo/AIEngineeringStandard`](https://github.com/eaglesjo/AIEngineeringStandard). `codingStandard-private` is the Luna/internal continuity surface.

## What is AI Engineering Standard?

AI Engineering Standard is a reusable engineering standard for AI-assisted development, model training, experimentation, LLM/Vision workflows, general ML/DL workflows, and AI coding agents.

Version 2.0 establishes a machine-readable architecture and policy contract, explicit agent/Skill routing, environment-aware runtime behavior, cross-platform installation lifecycle controls, multilingual runtime quality gates, executable conformance checks, and dependency-compatibility alignment rules.

## 2.0.0 highlights

- Canonical layered repository architecture with machine-readable project, architecture, and policy profiles.
- Project-level `AGENTS.md` with common and domain-specific agent/Skill routing.
- LLM, Vision, ML, and Google Colab lifecycle guidance with measured environment/resource resolution.
- Cross-platform installer lifecycle with installation state, ownership hashes, update reconciliation, and protected uninstall behavior.
- Multilingual runtime resource completeness, semantic policy parity, and runtime/documentation consistency validation across 20 runtime locales.
- Architecture, policy, environment, installer, i18n, RAG, Colab, and CPU smoke validation gates.
- Executable agent-conformance schema and policy with explicit PASS/PARTIAL/ADAPTER/UNTESTED/UNSUPPORTED/FAIL outcomes.
- Codex runtime adapter and bounded evidence collection when the Codex CLI is available.
- Dependency compatibility policy anchored to the developer-selected library/version, with deterministic alignment and isolated real pip resolver validation.

## Supported AI development tools

The repository provides documented adapters, instruction files, Skills, or integration paths for OpenAI Codex, Claude Code, Gemini CLI, GitHub Copilot, Cursor, Windsurf, Cline, Continue, JetBrains Junie, Amazon Q Developer, and Aider. Tool capabilities can differ by client and version.

## Supported environments

| Environment | Status |
|---|---|
| Python | Supported |
| Jupyter Notebook | Supported |
| Google Colab | Supported |
| Visual Studio Code | Supported |
| Linux | Supported |
| macOS | Supported and CI-validated |
| Windows PowerShell / PowerShell 7 | Supported and CI-validated |

## Quick start

Clone the public distribution repository into the project you want to configure.

### Windows / PowerShell

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

### Linux / macOS

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Available domains are `common`, `ml`, `llm`, `vision`, `colab`, and `all`. Existing files can be handled with the installer conflict policies; use dry-run mode to preview changes.

## Installation lifecycle

Successful installs record ownership and hashes in `.codingstandard/installation.json`. The installer supports state inspection, update/reconciliation, safe uninstall, and explicit force mode for recovery. PowerShell equivalents are provided for supported lifecycle commands.

See [`INSTALL.md`](INSTALL.md) for the complete installation contract.

## Repository structure

```text
.
├── core/common/
├── domains/{ml,llm,vision}/
├── platform/colab/
├── examples/colab/
├── docs/{development,releases}/
├── i18n/
├── profiles/
├── scripts/{development,installers,validation}/
├── tests/validation/
├── .github/
└── VERSION
```

Legacy root-level domain trees and obsolete script paths are not part of the supported 2.0 layout.

## Architecture and policy profiles

`profiles/project.json` is the project-level contract. It resolves the canonical repository architecture and policy profiles, which define layer boundaries, dependency direction, runtime assumptions, validation, testing, reproducibility, platform, secrets, and network rules.

Agents must inspect these profiles before implementation changes and apply stricter child/task policies when present.

## Environment and ML policy

The shared environment profiler measures OS, Python/runtime, CPU, RAM, disk, accelerators, VRAM, CUDA/ROCm/MPS/DirectML capability, precision support, and Jupyter/Colab state. Runtime recommendations are derived from measured capabilities rather than a named machine profile.

The ML lifecycle covers data validation, experiment design, evaluation, training, inference, distributed training, HPO, reproducibility, resource tracking, and recovery. LLM and Vision inherit the common lifecycle and add domain-specific controls. Colab treats notebook runtimes as ephemeral and requires bootstrap, smoke testing, durable checkpointing, and resume validation for long-running work.

## Multilingual quality

Twenty runtime locales are validated for resource completeness, semantic policy parity, and runtime/documentation consistency. The canonical policy-intent contract includes environment validation, resource measurement, early stopping, checkpoint recovery, and tests for behavior changes.

## Validation

Before release promotion, run the repository's applicable validation gates. The primary validation entrypoint is:

```bash
python scripts/validation/validate.py
```

Additional checks cover i18n quality/consistency, installer lifecycle behavior, architecture/policy contracts, deterministic RAG regression, Colab notebooks, and LLM/Vision CPU smoke tests. GitHub Actions provides cross-platform execution evidence.

For the release process and candidate gates, see [`docs/releases/RELEASE.md`](docs/releases/RELEASE.md), [`docs/releases/RELEASE_STATUS.md`](docs/releases/RELEASE_STATUS.md), and [`docs/releases/RELEASE_CANDIDATE.md`](docs/releases/RELEASE_CANDIDATE.md).

## Release provenance

`codingStandard-dev` is the source used for implementation and validation. Only validated commits are promoted to the public distribution repository. The public `AIEngineeringStandard` repository is the release surface; this development repository is not itself the final public distribution identity.
