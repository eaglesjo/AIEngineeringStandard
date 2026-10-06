# 한국어 실행환경 규칙

실제 실행환경을 측정하고 workload에 맞는 안전한 runtime configuration을 결정합니다.

## 기본 흐름

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

실제 repository와 immutable source SHA를 먼저 확인하고 CPU, RAM, disk, GPU/accelerator, VRAM, framework capability, Python/runtime, IDE/kernel 상태를 측정합니다.

## 실행환경과 CI

로컬/sandbox 실행을 iterative development의 기본으로 사용합니다. GitHub Actions는 sandbox가 제공하지 못하는 bounded validation, supply, transport, recovery, cleanup 또는 remote execution에 사용합니다.

Actions 실행 전에는 required capabilities와 available sandbox capabilities를 비교합니다. Actions를 사용한 경우 source SHA와 관련 output을 검증하고 execution evidence에 remote execution임을 명시합니다.

## Runtime 분류

- `os`: Python이 보고하는 실제 호스트/runtime 운영체제
- `execution_environment`: `local`, `jupyter`, `vscode`, `colab` 등의 실제 실행 환경
- `execution_type`: `local` 또는 `cloud`

특정 장비를 runtime 조건으로 고정하지 않습니다. OS/runtime, framework 및 background process를 위한 memory headroom을 남기고 100% 사용을 목표로 하지 않습니다.

Colab처럼 ephemeral한 runtime에서는 durable checkpoint와 artifact persistence, Resume 검증을 적용합니다.

## 실패와 복구

실패 workflow는 로그와 결과를 확인한 뒤 원인을 분류합니다. 동일한 mission을 근거 없이 반복 실행하지 않습니다.

원격 임시 state는 task ownership과 terminal status를 확인한 후 정리합니다. UNKNOWN ownership은 destructive cleanup을 차단합니다.
