# AI Engineering Standard — Português

<p align="center"><strong>Padrões de engenharia para desenvolvimento, treinamento e agentes de IA</strong></p>

> Esta página é a porta de entrada em português para a documentação do codingStandard. O português faz parte das 20 localidades de execução e segue os mesmos controles de completude de recursos, paridade semântica e consistência entre runtime e documentação.

`codingStandard` é um padrão de engenharia reutilizável para desenvolvimento assistido por IA, treinamento de modelos, experimentação, fluxos de trabalho com LLM/Vision, projetos gerais de ML/DL e agentes de programação com IA.

## Início rápido

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

Os domínios disponíveis são `common`, `ml`, `llm`, `vision`, `colab` e `all`. O modo dry-run permite visualizar as alterações antes da instalação, enquanto as políticas de conflito definem como os arquivos existentes serão tratados.

## Google Colab

O repositório público oferece notebooks do Google Colab para validar o padrão completo, um ambiente de execução limpo e os fluxos de trabalho LLM QLoRA e RAG.

## Qualidade multilíngue

A documentação e os recursos de runtime são gerenciados separadamente, mas as 20 localidades de execução seguem os mesmos critérios de qualidade: completude dos recursos, paridade semântica das políticas e consistência entre runtime e documentação.

Para obter os procedimentos detalhados de instalação e validação, consulte o [README em inglês](../../README.md) e o [INSTALL.md](../../INSTALL.md).
