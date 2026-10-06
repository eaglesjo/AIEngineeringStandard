# AI Engineering Standard — 한국어

<p align="center"><strong>AI 개발·학습·에이전트 엔지니어링 표준</strong></p>

> 이 페이지는 AI Engineering Standard의 유일한 한국어 문서 진입점입니다. 영어는 표준의 canonical source이고, 한국어는 유일하게 지원되는 번역 런타임 로케일입니다.

`AI Engineering Standard`는 AI 보조 개발, 모델 학습, 실험, LLM/Vision 워크플로, 일반적인 ML/DL 작업, AI 코딩 에이전트를 위한 재사용 가능한 엔지니어링 표준입니다.

## 빠른 시작

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

사용 가능한 도메인은 `common`, `ml`, `llm`, `vision`, `colab`, `all`입니다. 설치 전에 dry-run으로 변경 내용을 확인할 수 있으며, 기존 파일은 설치기의 충돌 정책에 따라 처리됩니다.

## Google Colab

공개 저장소에는 전체 표준, clean runtime, LLM QLoRA, RAG 경로를 검증할 수 있는 Google Colab 노트북이 포함되어 있습니다.

## 한국어 품질

문서와 런타임 리소스는 영어 canonical source와 분리되어 관리되며, 한국어 런타임 로케일에는 리소스 완전성, 의미적 정책 일치성, 런타임과 문서 간 일관성 검증을 적용합니다.

자세한 설치 및 검증 절차는 [English README](../../README.md)와 [INSTALL.md](../../INSTALL.md)를 참고하세요.
