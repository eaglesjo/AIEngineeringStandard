# AI Engineering Standard — 日本語

<p align="center"><strong>AI 開発・学習・エージェントエンジニアリング標準</strong></p>

> このページは codingStandard の日本語ドキュメント入口です。日本語は 20 のランタイムロケールの一つであり、リソースの完全性、意味的な整合性、ランタイムとドキュメントの一貫性について同じ検証を受けます。

`codingStandard` は、AI 支援開発、モデル学習、実験、LLM/Vision ワークフロー、一般的な ML/DL プロジェクト、AI コーディングエージェント向けの再利用可能なエンジニアリング標準です。

## クイックスタート

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell：

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

利用できるドメインは `common`、`ml`、`llm`、`vision`、`colab`、`all` です。dry-run モードで変更内容を事前確認でき、競合ポリシーによって既存ファイルの扱いを選択できます。

## Google Colab

公開リポジトリには、標準全体、clean runtime、LLM QLoRA、RAG の各ワークフローを検証できる Google Colab ノートブックが用意されています。

## 多言語品質

ドキュメントとランタイムリソースは別々に管理されますが、20 のランタイムロケールすべてに同じ品質基準を適用します。リソースの完全性、ポリシーの意味的整合性、ランタイムとドキュメントの一貫性を検証します。

詳細なインストールおよび検証手順については、[English README](../../README.md) と [INSTALL.md](../../INSTALL.md) を参照してください。
