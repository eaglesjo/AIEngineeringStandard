# AI Engineering Standard — Italiano

> **Standard di ingegneria per sviluppo, training e agenti di IA**
>
> **Versione:** v2.0.0 — Release candidate pubblico

**Lingue:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · Italiano · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard è uno standard di ingegneria riutilizzabile per sviluppo assistito dall’IA, addestramento di modelli, sperimentazione, workflow LLM/Vision, ML/DL generale e agenti di coding basati sull’IA.

## Novità della 2.0.0

- Contratti di architettura e policy leggibili dalle macchine, con routing esplicito di Agent e Skill.
- Comportamento runtime basato sull’ambiente rilevato e sulle risorse realmente disponibili.
- Ciclo di vita multipiattaforma per installazione, aggiornamento e disinstallazione sicura.
- Verifica di completezza delle risorse, parità semantica e coerenza documentale per 20 locale runtime.
- Verifica della qualità del codice IA, valutazione IA/LLM, provenienza delle evidenze e contratti di riproducibilità.
- Standard di esecuzione e validazione per ML, LLM, Vision e Google Colab.

## Avvio rapido

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Domini disponibili: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Validazione

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Per l’installazione: [`INSTALL.md`](../../INSTALL.md). Per il processo di rilascio: [`RELEASE.md`](../../docs/releases/RELEASE.md).
