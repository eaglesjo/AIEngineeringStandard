# AI Engineering Standard — Nederlands

> **Engineeringstandaarden voor AI-ontwikkeling, training en agents**
>
> **Versie:** v2.0.0 — Publieke releasecandidate

**Talen:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · Nederlands · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard is een herbruikbare engineeringstandaard voor AI-ondersteunde ontwikkeling, modeltraining, experimenten, LLM/Vision-workflows, algemene ML/DL-workflows en AI-codeeragents.

## Hoogtepunten van 2.0.0

- Machineleesbare architectuur- en beleidscontracten met expliciete Agent/Skill-routing.
- Runtimegedrag op basis van de daadwerkelijk gedetecteerde omgeving en beschikbare resources.
- Platformonafhankelijke levenscyclus voor installatie, updates en veilige verwijdering.
- Validatie van resourcevolledigheid, semantische pariteit en documentatieconsistentie voor 20 runtime-locales.
- AI-codekwaliteitscontrole, AI/LLM-evaluatie, provenance van bewijs en reproduceerbaarheidscontracten.
- Uitvoerings- en validatiestandaarden voor ML, LLM, Vision en Google Colab.

## Snel starten

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Beschikbare domeinen: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Validatie

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Zie [`INSTALL.md`](../../INSTALL.md) voor installatie en [`RELEASE.md`](../../docs/releases/RELEASE.md) voor het releaseproces.
