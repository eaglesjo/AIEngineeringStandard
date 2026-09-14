# AI Engineering Standard — Français

> **Standards d’ingénierie pour le développement, l’entraînement et les agents IA**
>
> **Version :** v2.0.0 — Release Candidate public

**Langues :** [English](../../README.md) · [한국어](../ko/README.md) · Français · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard est un standard d’ingénierie réutilisable pour le développement assisté par IA, l’entraînement de modèles, l’expérimentation, les workflows LLM/Vision, le ML/DL généraliste et les agents de programmation.

## Points clés de la 2.0.0

- Contrats d’architecture et de politique lisibles par machine, avec routage explicite des agents et Skills.
- Détection de l’environnement et adaptation aux ressources réellement disponibles.
- Cycle de vie d’installation, de mise à jour et de désinstallation sécurisé sur les principales plateformes.
- Contrôles de complétude, de parité sémantique et de cohérence pour 20 locales runtime.
- Vérification de la qualité du code IA, évaluation IA/LLM, traçabilité des preuves et reproductibilité.
- Standards d’exécution et de validation pour ML, LLM, Vision et Google Colab.

## Démarrage rapide

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Sous Windows / PowerShell :

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Domaines disponibles : `common`, `ml`, `llm`, `vision`, `colab` et `all`.

## Validation

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Voir [`INSTALL.md`](../../INSTALL.md) pour l’installation et [`RELEASE.md`](../../docs/releases/RELEASE.md) pour le processus de publication.
