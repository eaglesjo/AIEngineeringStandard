# AI Engineering Standard — 한국어

<p align="center"><strong>AI 개발·학습·에이전트 엔지니어링 표준</strong></p>
<p align="center"><strong>v2.2.1 — Safer Installer Lifecycle</strong></p>

> 이 페이지는 AI Engineering Standard의 유일한 한국어 문서 진입점입니다. 영어가 canonical source이며, 한국어는 유일하게 지원되는 localized/runtime locale입니다.

## 저장소 역할

이 저장소는 AI Engineering Standard의 **개발·검증·릴리스 단일 source of truth**입니다. 별도의 private/development/staging/promotion 저장소를 사용하지 않습니다.

현재 릴리스 예정 버전은 **v2.2.1**이며, 버전이 고정된 PyPI 패키지와 CLI를 소비자 프로젝트의 기본 설치 경로로 제공합니다.

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
         ↙      ↘
Local Validation  GitHub Actions CI
       Gate           ↓
         ↘           ↙
             main
               ↓
          Version Tag
               ↓
        GitHub Release
```

GitHub Actions는 **검증과 bounded execution을 위한 실행 수단**이며 두 번째 source of truth가 아닙니다. 초록색 workflow만으로 Acceptance를 결정하지 않고, source SHA와 실제 출력/evidence를 확인합니다.

## ChatGPT Web 에이전트 연결 설정

ChatGPT 대화에서 이 저장소를 조회·수정하도록 하려면, 사용 가능한 환경에서는 **ChatGPT의 GitHub 연결**과 **GitHub의 ChatGPT Codex Connector App 설치**를 각각 설정합니다. 두 설정은 별개이며, 한쪽을 연결했다고 다른 쪽까지 완료된 것은 아닙니다.

1. ChatGPT에서 [Plugins / GitHub 연결 설정](https://chatgpt.com/plugins)을 열고 계정에서 제공되는 GitHub 연동을 설치하거나 연결합니다. 제품 UI의 메뉴명과 위치는 달라질 수 있습니다.
2. GitHub에서 [ChatGPT Codex Connector GitHub App](https://github.com/apps/chatgpt-codex-connector)을 설치하고 이 저장소에 대한 접근을 허용합니다. 필요한 저장소만 선택하는 최소 권한 구성을 권장합니다. 이미 특정 저장소만 허용한 설치라면 해당 목록에 이 저장소를 추가합니다.
3. 조직 정책상 승인이 필요하면 조직 관리자에게 앱 또는 연동 승인을 요청합니다.
4. 일반 ChatGPT 대화에서 저장소 URL을 제공하고, 변경을 요청하기 전에 에이전트가 실제로 조회할 수 있는 저장소와 사용 가능한 읽기·쓰기·샌드박스·Actions 기능을 먼저 확인하도록 요청합니다.

두 연결은 서로 보완하는 경로이며, 셸 실행·Actions 디스패치·릴리스·패키지 발행 권한을 자동으로 보장하지 않습니다. 에이전트는 연결 상태와 실제 권한을 검증해야 하며, 설정이 완료됐다고 추정해서는 안 됩니다. 하나의 연결을 사용할 수 없다면 구체적인 제한을 알리고, 확인된 기능만 사용합니다.


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

소비자 프로젝트에서는 저장소를 직접 clone할 필요 없이 PyPI 패키지를 설치합니다.

### 권장: pipx

```bash
pipx install ai-engineering-standard==2.2.1
ai-engineering-standard install --language ko --domain all
```

미리보기(파일을 쓰지 않음):

```bash
ai-engineering-standard install --language ko --domain all --dry-run
```

### 대안: pip

```bash
python -m pip install ai-engineering-standard==2.2.1
ai-engineering-standard install --language ko --domain all
```

사용 가능한 도메인은 `common`, `ml`, `llm`, `vision`, `colab`, `all`입니다. canonical source 언어는 English이며, localized locale은 한국어 하나만 지원합니다. 지원 locale 목록은 `i18n/languages.json`에서 관리합니다.

## v2.2.0 PyPI 패키지 스모크 테스트

macOS의 격리된 Python 3.14 가상환경에서 공개된 PyPI 패키지 `2.2.0`을 설치하고 CLI 설치·상태 확인·검증 흐름을 실행했습니다.

검증 명령:

```bash
python3 -m venv /tmp/aes-v220-test
source /tmp/aes-v220-test/bin/activate
python -m pip install ai-engineering-standard==2.2.0
ai-engineering-standard --version

mkdir -p /tmp/aes-v220-consumer
ai-engineering-standard install \
  --target /tmp/aes-v220-consumer \
  --language ko \
  --domain common \
  --policy overwrite
ai-engineering-standard status --target /tmp/aes-v220-consumer --json
ai-engineering-standard validate --target /tmp/aes-v220-consumer
```

결과:

- PyPI 패키지 설치 및 CLI 버전 확인 성공: `ai-engineering-standard 2.2.0`
- 한국어 `common` 도메인 파일 18개 설치
- 상태 확인 및 검증 결과: `installed: true`, `version: 2.2.0`, `language: ko`, `domain: common`
- 누락 파일 0개(`missing: 0`), 수정 감지 파일 0개(`modified: 0`)

이 결과는 Python 3.14, 한국어, `common` 도메인에 대한 공개 패키지 스모크 테스트입니다. 모든 도메인·언어 조합을 검증했다는 의미는 아닙니다.

## v2.2.1 변경 사항

- 오래된 파일 정리 실패를 포함해 업데이트를 트랜잭션으로 처리하고 롤백을 보장합니다.
- 사용자가 수정한 오래된 파일을 보존하고, 파일 삭제 전 안전하지 않은 제거를 거부합니다.
- `validate`를 지원되는 CLI 명령으로 노출합니다.
- 실제 업데이트까지 실행하는 패키지 CLI 생명주기 CI를 확장합니다.

## 검증

저장소의 개발 검증 명령:

```bash
python3 scripts/validation/validate.py
python3 scripts/installers/test_installers.py
python3 scripts/validation/validate_2_1_contracts.py
```

GitHub Actions CI도 repository validation contract를 자동 검증합니다.

## Google Colab

공개 저장소에는 clean runtime, LLM QLoRA, RAG 경로를 검증할 수 있는 Colab Notebook이 포함되어 있습니다. Colab은 ephemeral runtime으로 취급하고 durable checkpoint/artifact와 Resume 검증을 적용합니다.

## 한국어 품질

런타임 지원 locale은 English(en)와 한국어(ko) 2개이며, 한국어 runtime locale은 resource completeness, semantic policy parity, runtime/documentation consistency 검증을 받습니다. 누락된 domain-specific 한국어 번역은 영어 canonical source로 fallback합니다.

자세한 설치 절차는 [INSTALL.md](../../INSTALL.md)를 참고하세요.

## 릴리스 링크

- [GitHub Release v2.2.1](https://github.com/eaglesjo/AIEngineeringStandard/releases/tag/v2.2.1)
- [PyPI 패키지 v2.2.1](https://pypi.org/project/ai-engineering-standard/2.2.1/)
- [GitHub Actions 릴리스 workflow](https://github.com/eaglesjo/AIEngineeringStandard/blob/main/.github/workflows/publish-package.yml)
