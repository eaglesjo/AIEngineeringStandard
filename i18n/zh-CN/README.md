# AI Engineering Standard — 简体中文

> **AI 开发、训练与智能体工程标准**
>
> **版本：** v2.0.0 — 公共发布候选版

**语言：** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · 简体中文 · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard 是一套可复用的工程标准，面向 AI 辅助开发、模型训练、实验、LLM/Vision 工作流、通用 ML/DL 工作流以及 AI 编程智能体。

## 2.0.0 重点

- 机器可读的架构与策略契约，以及明确的 Agent/Skill 路由。
- 基于实际环境检测和资源测量的运行策略。
- 跨平台安装、更新、状态管理与安全卸载生命周期。
- 对 20 个 runtime locale 进行资源完整性、语义一致性和文档一致性验证。
- AI 代码质量验证、AI/LLM 评估、证据溯源与可复现性契约。
- 覆盖 ML、LLM、Vision 和 Google Colab 的执行与验证标准。

## 快速开始

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

可用域：`common`、`ml`、`llm`、`vision`、`colab` 和 `all`。

## 验证

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

安装详情请参阅 [`INSTALL.md`](../../INSTALL.md)，发布流程请参阅 [`RELEASE.md`](../../docs/releases/RELEASE.md)。
