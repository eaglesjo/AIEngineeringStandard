# AI Engineering Standard — 한국어

<p align="center"><strong>AI 개발·학습·에이전트 엔지니어링 표준</strong></p>

> 이 페이지는 AI Engineering Standard의 유일한 한국어 문서 진입점입니다. 영어가 canonical source이며, 한국어가 유일한 localized/runtime locale이며 유일하게 지원되는 한국어 런타임 로케일입니다.

## 저장소 역할

이 저장소는 AI Engineering Standard의 **개발·검증·릴리스 단일 source of truth**입니다. 별도의 private/development/staging/promotion 저장소를 사용하지 않습니다.

현재 표준 버전은 **v2.1.0 — Contract-First Multi-Agent Engineering**입니다.

## 2.1 멀티에이전트 계약

핵심 모델은 다음 순서를 따릅니다.

```text
Agent
  ↓
Agent Role
  ↓
Agent Contract
  ↓
Work Unit
  ↓
Handoff
  ↓
Evidence
  ↓
Evaluation
  ↓
Acceptance
```

Work Unit은 canonical trace boundary이며, runtime adapter는 이 계약의 의미를 재정의하지 않습니다.

## CI / GitHub Actions

저장소는 로컬 검증과 GitHub Actions CI를 함께 사용합니다.

```text
Feature / Fix / Docs
        ↓
Pull Request
        ↓
Local Validation Gate
        ↓
GitHub Actions CI
        ↓
main
        ↓
Version Tag
        ↓
GitHub Release
```

GitHub Actions는 **검증과 bounded execution을 위한 실행 수단**이며 두 번째 source of truth가 아닙니다. 초록색 workflow만으로 Acceptance를 결정하지 않고, source SHA와 실제 출력/evidence를 확인합니다.

## Repository Execution

실행 계약은 `core/runtime/execution/`에 정의되어 있습니다.

핵심 순서:

```text
정확한 commit SHA
→ capability inventory
→ sandbox 우선
→ 필요한 경우 bounded Actions
→ source/output 검증
→ failure classification
→ remote-state lifecycle
→ durable result
→ Evidence
```

Actions mission은 repository, immutable SHA, purpose, inputs, operations, expected outputs, permissions, terminal state, verification을 명시해야 합니다.

## 빠른 시작

Linux / macOS:

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target .
```

사용 가능한 도메인은 `common`, `ml`, `llm`, `vision`, `colab`, `all`입니다. canonical source 언어는 English이며, localized locale은 한국어 하나만 지원합니다.

## 검증

```bash
python3 scripts/validation/validate.py
python3 scripts/installers/test_installers.py
python3 scripts/validation/validate_2_1_contracts.py
```

GitHub Actions의 CI도 동일한 repository validation contract를 자동 검증합니다.

## Google Colab

공개 저장소에는 clean runtime, LLM QLoRA, RAG 경로를 검증할 수 있는 Colab Notebook이 포함되어 있습니다. Colab은 ephemeral runtime으로 취급하고 durable checkpoint/artifact와 Resume 검증을 적용합니다.

## 한국어 품질

한국어 runtime locale은 resource completeness, semantic policy parity, runtime/documentation consistency 검증을 받습니다. 누락된 domain-specific 한국어 번역은 영어 canonical source로 fallback합니다.

자세한 설치 절차는 [INSTALL.md](../../INSTALL.md)를 참고하세요.
