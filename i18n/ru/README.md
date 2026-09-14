# AI Engineering Standard — Русский

> **Стандарты инженерии для разработки, обучения и AI-агентов**
>
> **Версия:** v2.0.0 — публичный релиз-кандидат

**Языки:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · Русский · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard — переиспользуемый инженерный стандарт для разработки с помощью ИИ, обучения моделей, экспериментов, LLM/Vision, общих ML/DL-процессов и AI-агентов для программирования.

## Главное в 2.0.0

- Машиночитаемые контракты архитектуры и политик и явная маршрутизация Agent/Skill.
- Работа с учётом фактически обнаруженного окружения и доступных ресурсов.
- Кроссплатформенный жизненный цикл установки, обновления и безопасного удаления.
- Проверка полноты ресурсов, семантического соответствия и согласованности документации для 20 локалей runtime.
- Проверка качества AI-кода, оценка AI/LLM, происхождение доказательств и контракты воспроизводимости.
- Стандарты выполнения и проверки для ML, LLM, Vision и Google Colab.

## Быстрый старт

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Доступные домены: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Проверка

```bash
python ./AIEngineeringStandard/scripts/validation/validate.py
python ./AIEngineeringStandard/scripts/installers/test_installers.py
```

Подробности установки: [`INSTALL.md`](../../INSTALL.md). Процесс публикации: [`RELEASE.md`](../../docs/releases/RELEASE.md).
