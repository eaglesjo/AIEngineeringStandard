# 설치 가이드

`AIEngineeringStandard`의 공식 설치기입니다.

## 1. Clone

```bash
git clone https://github.com/eaglesjo/AIEngineeringStandard.git
```

적용하려는 프로젝트의 루트에서 설치기를 실행합니다.

## 2. 언어와 도메인 선택

설치기는 English canonical source와 **한국어만 지원되는 localized locale**을 사용합니다.

```text
언어
  en = English (canonical)
  ko = Korean (localized)

도메인
  common = 공통 규칙만
  ml     = Common + 일반 ML/DL lifecycle
  llm    = Common + LLM
  vision = Common + Vision
  colab  = Common + Colab runtime 정책
  all    = Common + ML + LLM + Vision + Colab
```

명시적 한국어 설치:

```bash
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh . ko ml overwrite false
```

Windows / PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\AIEngineeringStandard\scripts\installers\install-domains.ps1 -Target . -Language ko -Domain ml -Policy overwrite
```

지원하지 않는 locale은 installer에서 거부됩니다.

## 3. 설치 전 미리보기

```bash
bash ./AIEngineeringStandard/scripts/installers/install-domains.sh . ko all ask true
```

Dry-run은 대상 프로젝트를 변경하지 않습니다.

## 4. 설치 후 검증

```bash
python3 scripts/validation/validate.py
python3 scripts/installers/test_installers.py
python3 scripts/validation/validate_2_1_contracts.py
```

GitHub Actions CI에서도 동일한 repository validation gate를 자동 실행합니다.

## 5. 실행 / CI

반복적인 편집·디버깅은 sandbox/local 환경을 우선합니다. CI가 필요하면 GitHub Actions의 bounded execution을 사용합니다.

Actions 실행은 immutable source SHA, 최소 권한, output verification, failure classification, remote-state cleanup 규칙을 따릅니다.

## 6. Colab

Colab은 ephemeral runtime으로 취급합니다. dependency bootstrap, 실제 자원 측정, smoke test, durable checkpoint/artifact, Resume 검증을 적용합니다.
