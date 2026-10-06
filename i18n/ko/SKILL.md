# 한국어 AI 개발 Skill

Python 기반 AI/ML, LLM, Jupyter, VS Code Jupyter, Google Colab 및 local/cloud 실행에 적용합니다.

## 작업 시작

```text
저장소 상태
→ immutable source SHA
→ Python / active kernel
→ OS / architecture
→ IDE / Jupyter / Colab runtime
→ GPU / accelerator / VRAM
→ CPU / system RAM / disk
→ dependency
→ experiment requirements
```

## 실행 순서

```text
정확한 source 확인
→ capability 측정
→ sandbox 우선
→ Smoke Test
→ Lock
→ Execute
→ Evaluate
→ Evidence / durable result
```

GitHub Actions가 필요하면 bounded mission으로 실행합니다. Actions는 interactive remote shell이 아니며 canonical source of truth도 아닙니다.

실패한 workflow는 무작정 재실행하지 않습니다. job/step/log/artifact를 확인하고 `SOURCE_TEST`, `MISSION_DEFECT`, `PERMISSION_AUTH`, `QUOTA_PLATFORM`, `STALE_SOURCE`, `TRANSIENT_INFRASTRUCTURE` 중 하나로 분류한 뒤 retry 여부를 결정합니다.

## Memory Smoke Test

장시간 학습 전에 작은 workload로 다음을 검증합니다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save/reload
```

## 완료 조건

```text
[ ] exact source SHA
[ ] capability inventory
[ ] environment profile
[ ] runtime configuration
[ ] memory smoke test
[ ] environment lock
[ ] Early Stopping
[ ] best checkpoint / Resume
[ ] reproducibility/resource metadata
[ ] validation
[ ] evidence / durable result
```
