# AI Engineering Standard — Français

<p align="center"><strong>Standards d’ingénierie pour le développement, l’entraînement et les agents d’IA</strong></p>

> Cette page est le point d’entrée français de la documentation de codingStandard. Le français fait partie des 20 locales d’exécution et bénéficie des mêmes contrôles de complétude des ressources, de parité sémantique et de cohérence entre l’exécution et la documentation.

`codingStandard` est un standard d’ingénierie réutilisable pour le développement assisté par l’IA, l’entraînement de modèles, l’expérimentation, les workflows LLM/Vision, les projets ML/DL généraux et les agents de programmation IA.

## Démarrage rapide

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Sous Windows / PowerShell :

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Les domaines disponibles sont `common`, `ml`, `llm`, `vision`, `colab` et `all`. Vous pouvez utiliser le mode dry-run pour prévisualiser les changements et les politiques de conflit pour gérer les fichiers existants.

## Google Colab

Le dépôt public fournit des notebooks Google Colab permettant de valider le standard complet, un environnement propre, ainsi que les parcours LLM QLoRA et RAG.

## Qualité multilingue

La documentation et les ressources d’exécution sont gérées séparément, mais les 20 locales d’exécution sont soumises aux mêmes critères de qualité : complétude des ressources, parité sémantique des politiques et cohérence entre l’exécution et la documentation.

Pour les procédures détaillées d’installation et de validation, consultez le [README en anglais](../../README.md) et [INSTALL.md](../../INSTALL.md).
