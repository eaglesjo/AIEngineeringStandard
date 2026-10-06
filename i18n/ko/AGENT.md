# 한국어 AI Agent 공통 규칙

이 파일은 한국어 배포 환경의 보조 Agent entrypoint입니다. 정책의 원본은 `AGENTS.md`와 `core/common/`입니다.

## 적용 순서

```text
AGENTS.md
→ core/common/
→ domains/ml/ + 관련 LLM/Vision domain
→ Colab이면 platform/colab/
→ task-specific Skills
```

## 저장소와 검증

이 저장소가 개발·검증·릴리스의 canonical source입니다. 변경 전 저장소, 실행환경, 의존성, 데이터 계약, 테스트, 보안 제약을 확인합니다.

작은 의미 있는 테스트 후 전체 검증을 수행합니다. v2.1 contract 변경은 Agent → Role → Contract → Work Unit → Handoff → Evidence → Evaluation → Acceptance 모델을 보존해야 합니다.

## CI / 실행

- GitHub Actions는 repository validation architecture의 일부입니다.
- `.github/workflows/ci.yml`이 canonical automated CI entrypoint입니다.
- 실행 계약은 `core/runtime/execution/OPERATING_POLICY.md`와 `mission.schema.json`을 따릅니다.
- sandbox/local 실행을 우선하고, Actions는 bounded validation 또는 필요한 remote execution에 사용합니다.
- green workflow만으로 Acceptance를 판단하지 않습니다.
- source SHA와 실제 output/evidence를 확인합니다.
- workflow, artifact, mission payload에 secret을 넣지 않습니다.
- 임시 remote state는 ownership과 terminal status를 확인한 뒤 정리합니다.

일반 ML/DL에서는 Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps lifecycle을 적용합니다.

실제 Python/runtime과 CPU/RAM/disk/accelerator/VRAM을 측정하고 smoke test 후 configuration을 lock합니다. 장시간 학습에는 validation, best checkpoint, Resume, 필요한 경우 Early Stopping을 적용합니다.

Notebook은 fresh kernel/runtime에서 top-to-bottom 실행 가능해야 합니다. Colab은 ephemeral runtime으로 취급하고 durable checkpoint/artifact 및 Resume 검증을 사용합니다.
