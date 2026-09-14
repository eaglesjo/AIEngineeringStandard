# AI Engineering Standard — 한국어

> **AI 개발·학습·에이전트 엔지니어링 표준**
>
> **버전:** v2.0.0 — Public Release Candidate

**언어:** [English](../../README.md) · 한국어 · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Bahasa Indonesia](../id/README.md) · [Tiếng Việt](../vi/README.md) · [ไทย](../th/README.md) · [Nederlands](../nl/README.md) · [Polski](../pl/README.md) · [Svenska](../sv/README.md) · [Українська](../uk/README.md)

AI Engineering Standard는 AI 지원 개발, 모델 학습, 실험, LLM/Vision, 일반 ML/DL 워크플로와 AI 코딩 에이전트를 위한 재사용 가능한 엔지니어링 표준입니다.

## 2.0.0 핵심

- 머신 리더블 아키텍처·정책 계약과 명확한 Agent/Skill 라우팅
- 환경 감지와 리소스 측정에 기반한 실행 정책
- Windows, macOS, Linux를 위한 설치·업데이트·안전한 제거 수명주기
- 20개 runtime locale의 리소스 완전성·semantic parity·문서 일관성 검증
- AI 코드 품질 검증, AI/LLM 평가, provenance, 재현성 계약
- ML, LLM, Vision, Google Colab을 포함한 실행·검증 표준

## 빠른 시작

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

도메인은 `common`, `ml`, `llm`, `vision`, `colab`, `all`을 지원합니다.

## 검증

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

설치 상세는 [`INSTALL.md`](../../INSTALL.md), 공개 릴리스 정책은 [`RELEASE.md`](../../docs/releases/RELEASE.md)를 참고하세요.
