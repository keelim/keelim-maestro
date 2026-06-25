# toto

Last reviewed: 2026-06-25 KST

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

### 2026-06-25 - 이중 워크스페이스 lockfile 통합 점검 게이트

Status: proposed

Why now: `toto`는 Bun 워크스페이스(`toto-kbo-streamlit-dashboard`)와 uv 워크스페이스(`kbo-dashboard`) 양쪽에 동시 등록된 유일한 멤버다. Bun lockfile과 uv lockfile이 독립적으로 갱신되면 JS 빌드 경로와 Python 실행 환경이 조용히 어긋날 수 있으며, 현재는 두 lockfile을 함께 검증하는 단일 게이트가 없다.

First slice: PR마다 `bun install --frozen-lockfile`(Bun 측)과 `uv lock --check`(Python 측)를 함께 실행해 두 lockfile이 현재 코드와 일관성을 유지하는지 CI에서 단일 게이트로 확인하고, 불일치 발생 시 명시적 실패로 표시한다.

### 2026-06-25 - Bun-uv 이중 테스트 경로 교차 검증 게이트

Status: proposed

Why now: 루트 SCRIPTS.md에서 `bun run test:toto`(Bun 필터 경로)와 `uv run --package kbo-dashboard --group dev pytest toto/tests`(uv 직접 경로) 두 가지 테스트 진입점이 공존한다. 두 경로가 독립적으로 실행되면 한쪽에서만 잡히는 회귀가 생겨도 통과로 보일 수 있다.

First slice: CI에서 두 진입점 모두를 순서대로 실행해 테스트 커버리지가 동등하게 유지되는지 확인하고, 어느 한쪽에서만 실패가 발생하면 경로별 실패 원인을 명시적으로 표시하는 통합 검증 스텝을 만든다.
