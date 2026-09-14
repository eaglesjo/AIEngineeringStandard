# AI Engineering Standard — 简体中文

<p align="center"><strong>AI 开发、训练与智能体工程标准</strong></p>

> 本页面是 codingStandard 的简体中文文档入口。简体中文属于 20 个运行时 locale，并接受统一的资源完整性、语义一致性以及运行时与文档一致性验证。

`codingStandard` 是一套可复用的 AI 工程标准，适用于 AI 辅助开发、模型训练、实验、LLM/Vision 工作流、通用 ML/DL 项目以及 AI 编程智能体。

## 快速开始

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell：

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

可用领域包括 `common`、`ml`、`llm`、`vision`、`colab` 和 `all`。可以先使用 dry-run 预览变更，并通过冲突策略处理目标项目中已有的文件。

## Google Colab

公共仓库提供 Google Colab 验证笔记本，可用于验证完整标准、clean runtime、LLM QLoRA 和 RAG 工作流。

## 多语言质量

文档与运行时资源分开管理，但 20 个运行时 locale 均采用统一的质量标准，包括资源完整性、策略语义一致性，以及运行时与文档之间的一致性。

详细的安装和验证流程请参阅[英文 README](../../README.md)和 [INSTALL.md](../../INSTALL.md)。
