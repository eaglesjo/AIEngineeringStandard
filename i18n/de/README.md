# AI Engineering Standard — Deutsch

> **Engineering-Standards für KI-Entwicklung, Training und Agenten**
>
> **Version:** v2.0.0 — Öffentlicher Release Candidate

**Sprachen:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · Deutsch · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard ist ein wiederverwendbarer Engineering-Standard für KI-gestützte Entwicklung, Modelltraining, Experimente, LLM/Vision-Workflows, allgemeine ML/DL-Workflows und KI-Coding-Agenten.

## Die wichtigsten Neuerungen in 2.0.0

- Maschinenlesbare Architektur- und Richtlinienverträge mit explizitem Agent-/Skill-Routing.
- Laufzeitverhalten auf Basis der tatsächlich erkannten Umgebung und verfügbaren Ressourcen.
- Plattformübergreifender Lebenszyklus für Installation, Aktualisierung und sichere Deinstallation.
- Prüfung von Ressourcen-Vollständigkeit, semantischer Parität und Dokumentationskonsistenz für 20 Runtime-Lokalen.
- Prüfung der KI-Codequalität, KI/LLM-Evaluierung, Evidenz-Provenienz und Reproduzierbarkeitsverträge.
- Ausführungs- und Validierungsstandards für ML, LLM, Vision und Google Colab.

## Schnellstart

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Verfügbare Bereiche: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Validierung

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Installationsdetails stehen in [`INSTALL.md`](../../INSTALL.md), der Veröffentlichungsprozess in [`RELEASE.md`](../../docs/releases/RELEASE.md).
