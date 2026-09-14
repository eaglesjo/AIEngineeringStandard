# AI Engineering Standard — 日本語

> **AI 開発・学習・エージェントエンジニアリング標準**
>
> **バージョン：** v2.0.0 — 公開リリース候補

**言語：** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · 日本語 · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard は、AI 支援開発、モデル学習、実験、LLM/Vision ワークフロー、一般的な ML/DL ワークフロー、AI コーディングエージェントのための再利用可能なエンジニアリング標準です。

## 2.0.0 の主な内容

- 機械可読なアーキテクチャ／ポリシー契約と、明示的な Agent/Skill ルーティング。
- 実際に検出・計測した環境とリソースに基づく実行方針。
- クロスプラットフォームのインストール、更新、状態管理、安全なアンインストール。
- 20 の runtime locale に対するリソース完全性、意味的パリティ、ドキュメント整合性の検証。
- AI コード品質検証、AI/LLM 評価、証拠のプロヴェナンス、再現性契約。
- ML、LLM、Vision、Google Colab を対象とした実行・検証標準。

## クイックスタート

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

利用可能なドメインは `common`、`ml`、`llm`、`vision`、`colab`、`all` です。

## 検証

```bash
python ./AIEngineeringStandard/scripts/validation/validate.py
python ./AIEngineeringStandard/scripts/installers/test_installers.py
```

インストール方法は [`INSTALL.md`](../../INSTALL.md)、公開リリース手順は [`RELEASE.md`](../../docs/releases/RELEASE.md) を参照してください。
