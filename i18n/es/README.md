# AI Engineering Standard — Español

<p align="center"><strong>Estándares de ingeniería para desarrollo, entrenamiento y agentes de IA</strong></p>

> Esta página es el punto de entrada en español de la documentación de codingStandard. El español forma parte de las 20 locales de ejecución y está sujeto a los mismos controles de completitud de recursos, paridad semántica y coherencia entre el entorno de ejecución y la documentación.

`codingStandard` es un estándar de ingeniería reutilizable para el desarrollo asistido por IA, el entrenamiento de modelos, la experimentación, los flujos de trabajo LLM/Vision, los proyectos generales de ML/DL y los agentes de programación con IA.

## Inicio rápido

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

En Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Los dominios disponibles son `common`, `ml`, `llm`, `vision`, `colab` y `all`. Puedes usar el modo dry-run para previsualizar los cambios y las políticas de conflicto para gestionar los archivos existentes.

## Google Colab

El repositorio público ofrece notebooks de Google Colab para validar el estándar completo, un entorno limpio y los flujos de trabajo de LLM QLoRA y RAG.

## Calidad multilingüe

La documentación y los recursos de ejecución se gestionan por separado, pero las 20 locales de ejecución están sujetas a los mismos criterios de calidad: completitud de recursos, paridad semántica de las políticas y coherencia entre el entorno de ejecución y la documentación.

Para conocer los procedimientos detallados de instalación y validación, consulta el [README en inglés](../../README.md) y [INSTALL.md](../../INSTALL.md).
