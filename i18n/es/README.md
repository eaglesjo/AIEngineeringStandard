# AI Engineering Standard — Español

> **Estándares de ingeniería para desarrollo, entrenamiento y agentes de IA**
>
> **Versión:** v2.0.0 — Candidato público a lanzamiento

**Idiomas:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · Español · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard es un estándar de ingeniería reutilizable para el desarrollo asistido por IA, el entrenamiento de modelos, la experimentación, los flujos LLM/Vision, ML/DL general y los agentes de programación.

## Novedades de la 2.0.0

- Contratos de arquitectura y políticas legibles por máquina, con enrutamiento explícito de agentes y Skills.
- Detección del entorno y comportamiento basado en los recursos realmente disponibles.
- Ciclo de vida seguro de instalación, actualización y desinstalación multiplataforma.
- Validación de integridad de recursos, paridad semántica y coherencia documental para 20 locales de runtime.
- Verificación de calidad del código generado con IA, evaluación de IA/LLM, procedencia de evidencias y reproducibilidad.
- Estándares de ejecución y validación para ML, LLM, Vision y Google Colab.

## Inicio rápido

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Dominios disponibles: `common`, `ml`, `llm`, `vision`, `colab` y `all`.

## Validación

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Consulta [`INSTALL.md`](../../INSTALL.md) para la instalación y [`RELEASE.md`](../../docs/releases/RELEASE.md) para el proceso de publicación.
