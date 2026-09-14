# AI Engineering Standard — Українська

> **Стандарти інженерії для розробки, навчання та AI-агентів**
>
> **Версія:** v2.0.0 — публічний кандидат на реліз

**Мови:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · Українська

AI Engineering Standard — це багаторазово використовуваний інженерний стандарт для розробки за допомогою ШІ, навчання моделей, експериментів, робочих процесів LLM/Vision, загального ML/DL та AI-агентів для програмування.

## Основні можливості 2.0.0

- Машинно читані контракти архітектури та політик із чіткою маршрутизацією Agent/Skill.
- Поведінка під час виконання на основі фактично виявленого середовища та доступних ресурсів.
- Кросплатформений життєвий цикл встановлення, оновлення та безпечного видалення.
- Перевірка повноти ресурсів, семантичної паритетності та узгодженості документації для 20 runtime locale.
- Перевірка якості AI-коду, оцінювання AI/LLM, походження доказів і контракти відтворюваності.
- Стандарти виконання та перевірки для ML, LLM, Vision і Google Colab.

## Швидкий старт

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Доступні домени: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Перевірка

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Інструкції зі встановлення: [`INSTALL.md`](../../INSTALL.md). Процес релізу: [`RELEASE.md`](../../docs/releases/RELEASE.md).
