# AI Engineering Standard — Русский

<p align="center"><strong>Инженерные стандарты для разработки, обучения моделей и AI-агентов</strong></p>

> Эта страница является русской точкой входа в документацию codingStandard. Русский входит в число 20 локалей среды выполнения и проходит те же проверки полноты ресурсов, семантической согласованности и согласованности между runtime и документацией.

`codingStandard` — это переиспользуемый инженерный стандарт для разработки с помощью ИИ, обучения моделей, экспериментов, рабочих процессов LLM/Vision, общих проектов ML/DL и AI-агентов для программирования.

## Быстрый старт

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Доступны домены `common`, `ml`, `llm`, `vision`, `colab` и `all`. Режим dry-run позволяет предварительно просмотреть изменения, а политики конфликтов — определить, как обрабатывать существующие файлы.

## Google Colab

Публичный репозиторий предоставляет ноутбуки Google Colab для проверки всего стандарта, clean runtime, а также рабочих процессов LLM QLoRA и RAG.

## Качество локализации

Документация и ресурсы runtime управляются отдельно, но для всех 20 локалей применяются единые критерии качества: полнота ресурсов, семантическая эквивалентность политик и согласованность между runtime и документацией.

Подробные инструкции по установке и валидации см. в [README на английском](../../README.md) и [INSTALL.md](../../INSTALL.md).
