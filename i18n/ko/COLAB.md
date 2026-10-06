# Google Colab 검증

이 문서는 AI Engineering Standard의 Google Colab 실행 및 검증 방법을 설명합니다.

## 저장소

검증 대상 저장소는 `eaglesjo/AIEngineeringStandard`입니다. Notebook은 특정 개발 머신에 의존하지 않고 clean runtime에서 실행되어야 합니다.

## 검사 항목

1. 저장소를 Colab runtime에 clone합니다.
2. Python, PyTorch, CPU, RAM, accelerator, VRAM, CUDA/MPS capability와 runtime 정보를 감지합니다.
3. 공통 LLM environment profiler를 실행합니다.
4. checkpoint 저장/재로드를 포함한 작은 LLM training smoke test를 실행합니다.
5. image tensor를 사용하는 작은 Vision training smoke test를 실행합니다.
6. repository validation을 실행합니다.
7. resource 정보와 pass/fail 상태를 JSON으로 기록합니다.
8. clean runtime에서 Notebook을 top-to-bottom 실행할 수 있는지 확인합니다.

Colab runtime은 ephemeral합니다. 중요 checkpoint와 artifact는 durable storage에 저장하고 reset 이후 Resume을 검증합니다.

## CI와 로컬 실행

Colab Notebook 검증과 GitHub Actions CI는 역할이 다릅니다. Actions는 bounded automated verification이며 Colab runtime 자체를 대신하지 않습니다.

## 관련 검증

- 종합 repository validation: `python3 scripts/validation/validate.py`
- installer lifecycle: `python3 scripts/installers/test_installers.py`
- v2.1 contract validation: `python3 scripts/validation/validate_2_1_contracts.py`

테스트는 의도적으로 작게 구성되어 있습니다. Colab smoke test 통과는 최소 실행 경로를 검증하지만 임의의 production model이 현재 Colab runtime 자원에 적합하다는 것을 보장하지는 않습니다.
