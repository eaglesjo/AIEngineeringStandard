# AI Engineering Standard

<p align="center">
  <strong>AI Development, Training & Agent Engineering Standards</strong>
</p>

<p align="center">
  <strong>v2.0.1 — Independent Development & Release</strong>
</p>

<p align="center">
  <a href="https://github.com/eaglesjo/AIEngineeringStandard/releases"><img src="https://img.shields.io/github/v/release/eaglesjo/AIEngineeringStandard?label=release" alt="Release"></a>
  <a href="https://github.com/eaglesjo/AIEngineeringStandard/actions/workflows/ci.yml"><img src="https://github.com/eaglesjo/AIEngineeringStandard/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
</p>

**Language:** English · [한국어](i18n/ko/README.md) · [Français](i18n/fr/README.md) · [Español](i18n/es/README.md) · [简体中文](i18n/zh-CN/README.md) · [日本語](i18n/ja/README.md) · [Русский](i18n/ru/README.md) · [Türkçe](i18n/tr/README.md) · [Deutsch](i18n/de/README.md) · [Italiano](i18n/it/README.md) · [Português](i18n/pt/README.md) · [العربية](i18n/ar/README.md) · [हिन्दी](i18n/hi/README.md) · [Bahasa Indonesia](i18n/id/README.md) · [Tiếng Việt](i18n/vi/README.md) · [ไทย](i18n/th/README.md) · [Nederlands](i18n/nl/README.md) · [Polski](i18n/pl/README.md) · [Svenska](i18n/sv/README.md) · [Українська](i18n/uk/README.md)

## What is AI Engineering Standard?

AI Engineering Standard is a reusable engineering standard for AI-assisted development, model training, experimentation, LLM/Vision workflows, general ML/DL workflows, and AI coding agents.

Version 2 establishes a machine-readable architecture and policy contract, explicit agent/Skill routing, environment-aware runtime behavior, cross-platform installation lifecycle controls, multilingual runtime quality gates, executable conformance checks, and dependency-compatibility alignment rules.

## Independent repository model

This repository is the **single source of truth for development, validation, and release**.

```text
feature/fix/docs
      ↓
Pull Request
      ↓
GitHub Actions CI
      ↓
main
      ↓
version tag
      ↓
release validation
      ↓
GitHub Release
```

There is no separate private repository, development repository, staging repository, or promotion/export step.

## 2.0.1 transition

Version 2.0.0 remains preserved as historical release provenance. Starting with 2.0.1, development and release are performed directly in this repository under the independent release contract.

## Quick start

Clone the repository into the project you want to configure.

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

Available domains are `common`, `ml`, `llm`, `vision`, `colab`, and `all`. Supported locales are defined by `i18n/languages.json`; the installer derives its accepted locale set from that catalog.

## Installation lifecycle

Successful installs record ownership and hashes in `.codingstandard/installation.json`. The installer supports state inspection, update/reconciliation, safe uninstall, and explicit force mode for recovery.

See [`INSTALL.md`](INSTALL.md) for the complete installation contract.

## Repository structure

```text
.
├── AGENTS.md
├── core/{agent,common,mcp,plugin,skill,validation}/
├── domains/{ml,llm,vision}/
├── platform/colab/
├── examples/colab/
├── docs/{development,releases}/
├── i18n/
├── profiles/
├── compatibility/
├── scripts/{development,installers,validation}/
├── tests/
├── .github/workflows/
└── VERSION
```

Legacy root-level domain trees and obsolete script paths are not part of the supported 2.x layout.

## Validation

Run the complete repository gate before merge or release:

```bash
python3 scripts/validation/validate.py
python3 scripts/installers/test_installers.py
```

GitHub Actions executes the same validation on Linux and macOS, with dedicated Windows installer validation.

## Release provenance

Release tags and GitHub Releases are created from this repository only. The release workflow validates that the tag exactly matches `VERSION`, runs the complete validation gates on the tagged commit, and then publishes the GitHub Release.

Historical tags and commits, including `v2.0.0`, are preserved.
