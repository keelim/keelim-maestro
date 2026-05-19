# toto

Last reviewed: 2026-05-19 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.

## Open ideas

### 2026-04-18 - 시즌 스냅샷 매니페스트

Status: proposed

Why now: 대시보드가 읽기전용 스켈레톤인 만큼, 같은 시즌을 다시 시드했을 때 같은 행 수와 같은 결과가 나오는지 확인할 수 있어야 한다.

First slice: 시드 대상 시즌의 원본 파일, 행 수, 체크섬, 예상 요약값을 기록한 매니페스트를 만들고 `bun run seed` 결과와 비교한다.

### 2026-04-18 - 데이터 공급자 어댑터 분리

Status: proposed

Why now: 지금은 로컬 스켈레톤이지만, 나중에 CSV/fixture/API 중 무엇을 쓰든 UI는 같은 계약만 보면 되게 만들어야 유지보수가 쉽다.

First slice: 경기 결과와 순위 조회를 담당하는 얇은 provider 인터페이스를 정의하고, `streamlit_app/Home.py`가 그 인터페이스만 호출하도록 바꾼다.

### 2026-04-18 - 읽기전용 스모크 게이트

Status: proposed

Why now: 이 저장소의 핵심 가치는 수정이 아니라 재현이므로, 실수로 쓰기 경로나 외부 변조가 들어와도 바로 잡아내는 게 먼저다.

First slice: 앱 부팅, 홈 임포트, `verify` 흐름을 묶은 스모크 테스트를 추가하고, 비정상 쓰기 경로나 경로 드리프트가 있으면 실패하게 만든다.

### 2026-04-25 - gitlink 커밋 및 재현 가능한 클론 게이트

Status: proposed

Why now: `toto`가 `.gitmodules`에 선언돼 있지만 gitlink가 루트 인덱스에 커밋되지 않아서, 신규 클론 시 디렉터리가 없고 `bun run dev:toto`·`bun run verify:toto`를 실행할 수 없다. 재현성을 핵심 가치로 내세운 프로젝트에서 이 비대칭은 가장 먼저 해소해야 할 운영 위험이다.

First slice: 안정 커밋을 골라 gitlink를 루트 인덱스에 커밋하고, `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 순서가 CI에서 그린으로 돌아오면 pinning 완료로 간주한다.

### 2026-05-19 - 예측 모델 등록·백테스트 계약 동기화 게이트

Status: proposed

Why now: `toto`는 `PredictionCardDTO`·`BacktestSummaryDTO`로 예측 결과와 백테스트 요약을 분리하고 있으며, `view_models.py`가 `selected_model_name`과 `selection_rationale`을 노출하고 `test_no_recommendation_surface.py`가 금지 표현을 감시한다. 예측 모델이 추가되거나 DTO 계약이 바뀔 때 씨드 데이터·모델 요약·선택 근거 세 계층이 동시에 맞는지 확인하는 게이트가 없으면 드리프트가 조용히 쌓인다.

First slice: `BacktestSummaryDTO` 필드와 `repository.get_model_summaries()` 결과, `view_models.selection_rationale` 출력을 교차 비교하는 계약 검사를 `bun run verify`에 포함하고, 모델 추가 시 세 계층이 동시에 업데이트됐는지 확인한다.
