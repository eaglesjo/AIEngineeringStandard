# AI Engineering Standard — Deutsch

<p align="center"><strong>Ingenieurstandards für KI-Entwicklung, Training und Agenten</strong></p>

> Diese Seite ist der deutsche Einstieg in die Dokumentation von codingStandard. Deutsch gehört zu den 20 Laufzeit-Lokalisierungen und unterliegt denselben Prüfungen auf Ressourcen-Vollständigkeit, semantische Übereinstimmung sowie Konsistenz zwischen Laufzeit und Dokumentation.

`codingStandard` ist ein wiederverwendbarer Engineering-Standard für KI-gestützte Entwicklung, Modelltraining, Experimente, LLM-/Vision-Workflows, allgemeine ML-/DL-Projekte und KI-Programmieragenten.

## Schnellstart

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Verfügbar sind die Bereiche `common`, `ml`, `llm`, `vision`, `colab` und `all`. Mit dem Dry-Run-Modus können Änderungen vorab geprüft werden; Konfliktrichtlinien legen fest, wie vorhandene Dateien behandelt werden.

## Google Colab

Das öffentliche Repository stellt Google-Colab-Notebooks zur Verfügung, mit denen der vollständige Standard, eine saubere Laufzeitumgebung sowie die Workflows für LLM QLoRA und RAG validiert werden können.

## Mehrsprachige Qualität

Dokumentation und Laufzeitressourcen werden getrennt verwaltet, aber für alle 20 Laufzeit-Lokalisierungen gelten dieselben Qualitätskriterien: Ressourcen-Vollständigkeit, semantische Übereinstimmung der Richtlinien und Konsistenz zwischen Laufzeit und Dokumentation.

Ausführliche Installations- und Validierungsanweisungen finden Sie im [englischen README](../../README.md) und in [INSTALL.md](../../INSTALL.md).
