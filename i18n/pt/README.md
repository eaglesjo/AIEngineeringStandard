# AI Engineering Standard — Português

> **Padrões de engenharia para desenvolvimento, treinamento e agentes de IA**
>
> **Versão:** v2.0.0 — Candidato público a lançamento

**Idiomas:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · Português · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard é um padrão de engenharia reutilizável para desenvolvimento assistido por IA, treinamento de modelos, experimentação, fluxos LLM/Vision, ML/DL em geral e agentes de programação com IA.

## Destaques da 2.0.0

- Contratos de arquitetura e políticas legíveis por máquina, com roteamento explícito de Agents e Skills.
- Comportamento baseado no ambiente detectado e nos recursos realmente disponíveis.
- Ciclo de vida multiplataforma para instalação, atualização e desinstalação segura.
- Validação de integridade dos recursos, paridade semântica e consistência da documentação para 20 locales de runtime.
- Verificação da qualidade de código gerado por IA, avaliação de IA/LLM, proveniência das evidências e contratos de reprodutibilidade.
- Padrões de execução e validação para ML, LLM, Vision e Google Colab.

## Início rápido

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Domínios disponíveis: `common`, `ml`, `llm`, `vision`, `colab`, `all`.

## Validação

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

Consulte [`INSTALL.md`](../../INSTALL.md) para instalação e [`RELEASE.md`](../../docs/releases/RELEASE.md) para o processo de publicação.
