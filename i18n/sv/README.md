# AI Engineering Standard — Svenska

<p align="center"><strong>Tekniska standarder för AI-utveckling, modellträning och AI-agenter</strong></p>

> Den här sidan är den svenska ingången till dokumentationen för codingStandard. Svenska är en av 20 runtime-lokaliseringar och omfattas av samma kontroller för resursfullständighet, semantisk överensstämmelse och konsekvens mellan runtime och dokumentation.

`codingStandard` är en återanvändbar teknisk standard för AI-assisterad utveckling, modellträning, experiment, LLM/Vision-arbetsflöden, allmänna ML/DL-projekt och AI-agenter för programmering.

## Snabbstart

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Tillgängliga områden är `common`, `ml`, `llm`, `vision`, `colab` och `all`. Med dry-run-läget kan du förhandsgranska ändringarna, och konfliktreglerna anger hur befintliga filer ska hanteras.

## Google Colab

Det offentliga arkivet innehåller Google Colab-notebooks för att validera hela standarden, en ren runtime-miljö samt arbetsflöden för LLM QLoRA och RAG.

## Flerspråkig kvalitet

Dokumentation och runtime-resurser hanteras separat, men alla 20 runtime-lokaliseringar följer samma kvalitetskriterier: fullständiga resurser, semantisk överensstämmelse mellan policyer och konsekvens mellan runtime och dokumentation.

För detaljerade installations- och valideringssteg, se [README på engelska](../../README.md) och [INSTALL.md](../../INSTALL.md).
