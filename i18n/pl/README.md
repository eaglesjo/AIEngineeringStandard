# AI Engineering Standard — Polski

> **Standardy inżynierii tworzenia, trenowania i agentów AI**
>
> **Wersja:** v2.0.0 — publiczny kandydat do wydania

**Języki:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · Polski · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard to wielokrotnego użytku standard inżynieryjny dla programowania wspomaganego przez AI, trenowania modeli, eksperymentów, przepływów LLM/Vision, ogólnego ML/DL oraz agentów AI do programowania.

## Najważniejsze elementy 2.0.0

- Maszynowo czytelne kontrakty architektury i polityk oraz jawne routowanie Agent/Skill.
- Zachowanie środowiska uruchomieniowego oparte na faktycznie wykrytej konfiguracji i dostępnych zasobach.
- Wieloplatformowy cykl życia instalacji, aktualizacji i bezpiecznego odinstalowania.
- Walidacja kompletności zasobów, parytetu semantycznego i spójności dokumentacji dla 20 locale runtime.
- Weryfikacja jakości kodu AI, ewaluacja AI/LLM, proweniencja dowodów i kontrakty odtwarzalności.
- Standardy uruchamiania i walidacji dla ML, LLM, Vision i Google Colab.

## Szybki start

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Dostępne domeny: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Walidacja

```bash
python ./AIEngineeringStandard/scripts/validation/validate.py
python ./AIEngineeringStandard/scripts/installers/test_installers.py
```

Instalacja: [`INSTALL.md`](../../INSTALL.md). Proces wydania: [`RELEASE.md`](../../docs/releases/RELEASE.md).
