# AI Engineering Standard — Nederlands

<p align="center"><strong>Technische standaarden voor AI-ontwikkeling, modeltraining en AI-agents</strong></p>

> Deze pagina is het Nederlandstalige startpunt voor de documentatie van codingStandard. Nederlands is een van de 20 runtime-locales en wordt aan dezelfde controles onderworpen voor volledigheid van resources, semantische gelijkwaardigheid en consistentie tussen runtime en documentatie.

`codingStandard` is een herbruikbare technische standaard voor AI-ondersteunde ontwikkeling, modeltraining, experimenten, LLM/Vision-workflows, algemene ML/DL-projecten en AI-codeeragents.

## Snel starten

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Beschikbare domeinen zijn `common`, `ml`, `llm`, `vision`, `colab` en `all`. Met de dry-runmodus kun je wijzigingen vooraf bekijken; conflictbeleid bepaalt hoe bestaande bestanden worden afgehandeld.

## Google Colab

De openbare repository bevat Google Colab-notebooks waarmee de volledige standaard, een schone runtime en de LLM QLoRA- en RAG-workflows kunnen worden gevalideerd.

## Meertalige kwaliteit

Documentatie en runtime-resources worden afzonderlijk beheerd, maar voor alle 20 runtime-locales gelden dezelfde kwaliteitscriteria: volledigheid van resources, semantische gelijkwaardigheid van beleid en consistentie tussen runtime en documentatie.

Raadpleeg voor de volledige installatie- en validatieprocedure de [Engelse README](../../README.md) en [INSTALL.md](../../INSTALL.md).
