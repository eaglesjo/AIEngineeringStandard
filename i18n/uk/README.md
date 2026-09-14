# AI Engineering Standard — Українська

<p align="center"><strong>Інженерні стандарти для розробки, навчання моделей та AI-агентів</strong></p>

> Ця сторінка є україномовною точкою входу до документації codingStandard. Українська — одна з 20 локалей середовища виконання та проходить такі самі перевірки повноти ресурсів, семантичної відповідності й узгодженості між середовищем виконання та документацією.

`codingStandard` — це багаторазово використовуваний інженерний стандарт для розробки за допомогою AI, навчання моделей, експериментів, робочих процесів LLM/Vision, загальних ML/DL-проєктів та AI-агентів для програмування.

## Швидкий старт

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Доступні домени: `common`, `ml`, `llm`, `vision`, `colab` і `all`. Режим dry-run дає змогу попередньо переглянути зміни, а політики конфліктів визначають спосіб обробки наявних файлів.

## Google Colab

Публічний репозиторій містить ноутбуки Google Colab для перевірки всього стандарту, чистого середовища виконання, а також робочих процесів LLM QLoRA і RAG.

## Багатомовна якість

Документація та ресурси середовища виконання керуються окремо, але для всіх 20 локалей застосовуються однакові критерії якості: повнота ресурсів, семантична відповідність політик та узгодженість між середовищем виконання і документацією.

Докладні інструкції зі встановлення та перевірки наведено в [README англійською](../../README.md) і [INSTALL.md](../../INSTALL.md).
