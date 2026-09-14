# AI Engineering Standard — Polski

<p align="center"><strong>Standardy inżynierii oprogramowania dla rozwoju, trenowania modeli i agentów AI</strong></p>

> Ta strona jest polskim punktem wejścia do dokumentacji codingStandard. Język polski jest jednym z 20 języków uruchomieniowych i podlega tym samym kontrolom kompletności zasobów, zgodności semantycznej oraz spójności między środowiskiem uruchomieniowym a dokumentacją.

`codingStandard` to wielokrotnego użytku standard inżynierski dla programowania wspomaganego przez AI, trenowania modeli, eksperymentów, przepływów pracy LLM/Vision, ogólnych projektów ML/DL oraz agentów AI do programowania.

## Szybki start

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Dostępne domeny to `common`, `ml`, `llm`, `vision`, `colab` i `all`. Tryb dry-run pozwala najpierw wyświetlić planowane zmiany, a zasady konfliktów określają sposób obsługi istniejących plików.

## Google Colab

Publiczne repozytorium udostępnia notebooki Google Colab do walidacji całego standardu, czystego środowiska uruchomieniowego oraz przepływów pracy LLM QLoRA i RAG.

## Jakość wielojęzyczna

Dokumentacja i zasoby uruchomieniowe są zarządzane osobno, ale wszystkie 20 lokalizacji uruchomieniowych podlega tym samym kryteriom jakości: kompletności zasobów, zgodności semantycznej zasad oraz spójności między środowiskiem uruchomieniowym a dokumentacją.

Szczegółowe procedury instalacji i walidacji opisano w [README w języku angielskim](../../README.md) oraz [INSTALL.md](../../INSTALL.md).
