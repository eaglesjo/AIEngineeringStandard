# AI Engineering Standard — Svenska

> **Tekniska standarder för AI-utveckling, träning och agenter**
>
> **Version:** v2.0.0 — Offentlig releasekandidat

**Språk:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · Svenska · [Українська](../uk/README.md)

AI Engineering Standard är en återanvändbar teknisk standard för AI-assisterad utveckling, modellträning, experiment, LLM/Vision-arbetsflöden, generell ML/DL och AI-baserade kodningsagenter.

## Höjdpunkter i 2.0.0

- Maskinläsbara arkitektur- och policykontrakt med tydlig Agent/Skill-routing.
- Körbeteende baserat på den faktiska miljön och de resurser som upptäcks.
- Plattformoberoende livscykel för installation, uppdatering och säker avinstallation.
- Validering av resursfullständighet, semantisk paritet och dokumentationskonsistens för 20 runtime-lokaliseringar.
- Kvalitetskontroll av AI-kod, AI/LLM-utvärdering, evidensproveniens och reproducerbarhetskontrakt.
- Körnings- och valideringsstandarder för ML, LLM, Vision och Google Colab.

## Snabbstart

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Tillgängliga domäner: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Validering

```bash
python ./AIEngineeringStandard/scripts/validation/validate.py
python ./AIEngineeringStandard/scripts/installers/test_installers.py
```

Se [`INSTALL.md`](../../INSTALL.md) för installation och [`RELEASE.md`](../../docs/releases/RELEASE.md) för releaseprocessen.
