# AI Engineering Standard — Italiano

<p align="center"><strong>Standard di ingegneria per lo sviluppo, l’addestramento e gli agenti di IA</strong></p>

> Questa pagina è il punto di ingresso in italiano alla documentazione di codingStandard. L’italiano fa parte delle 20 localizzazioni di runtime e segue gli stessi controlli di completezza delle risorse, parità semantica e coerenza tra runtime e documentazione.

`codingStandard` è uno standard di ingegneria riutilizzabile per lo sviluppo assistito dall’IA, l’addestramento dei modelli, la sperimentazione, i workflow LLM/Vision, i progetti ML/DL generali e gli agenti IA per la programmazione.

## Avvio rapido

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

I domini disponibili sono `common`, `ml`, `llm`, `vision`, `colab` e `all`. La modalità dry-run consente di visualizzare in anteprima le modifiche, mentre le politiche di conflitto determinano come gestire i file esistenti.

## Google Colab

Il repository pubblico fornisce notebook Google Colab per validare l’intero standard, un ambiente runtime pulito e i workflow LLM QLoRA e RAG.

## Qualità multilingue

La documentazione e le risorse di runtime sono gestite separatamente, ma tutte le 20 localizzazioni di runtime seguono gli stessi criteri di qualità: completezza delle risorse, parità semantica delle policy e coerenza tra runtime e documentazione.

Per le procedure dettagliate di installazione e validazione, consulta il [README in inglese](../../README.md) e [INSTALL.md](../../INSTALL.md).
