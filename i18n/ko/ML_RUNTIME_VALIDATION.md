# ML/DL 런타임 검증

이 문서는 AI Engineering Standard 설치 후 실제 실행 계약을 검증합니다.

## Agent 라우팅

저장소 루트에서 실행합니다.

```bash
python scripts/validation/validate_agent_routing.py
```

검증 대상은 일반 PyTorch 학습, LLM QLoRA, Vision detection, Colab LLM training입니다.

## Repository validation

전체 검증은 다음 순서로 실행합니다.

```bash
python3 scripts/validation/validate.py
python3 scripts/installers/test_installers.py
python3 scripts/validation/validate_2_1_contracts.py
```

GitHub Actions CI는 동일한 repository validation contract를 자동 실행합니다. Actions의 green 상태만으로 Acceptance를 판단하지 않고 source SHA와 실제 output/evidence를 확인합니다.

## Colab runtime

새 Colab runtime에서 Notebook을 처음부터 끝까지 실행합니다.

Notebook은 활성 Python kernel과 실행 환경, accelerator/RAM/disk를 보고하고 Agent routing, 작은 PyTorch smoke test, checkpoint 저장/복원을 검증해야 합니다.

Checkpoint를 Colab reset 이후에도 유지해야 한다면 연결된 영속 저장 위치를 사용합니다. Notebook VM 파일 시스템은 폐기 가능한 것으로 취급합니다.

## 해석

검증 성공은 설치된 정책을 탐색할 수 있고 선택한 runtime을 측정할 수 있으며 대표 workload를 안전하게 시작하고 recovery artifact를 복원할 수 있음을 의미합니다. 모든 Colab accelerator 종류나 모든 모델 크기가 테스트되었다는 뜻은 아닙니다.
