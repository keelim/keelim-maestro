# toto

Last reviewed: 2026-05-23 KST

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

### 2026-04-25 - 클린 클론 재현성 CI 게이트

Status: in progress

Why now: 루트 WORKSPACE.md 스냅샷에 `toto`가 `5897ef44`로 pinned commit 등록된 것으로 기록됐다. gitlink 커밋 단계는 완료된 것으로 보이지만, `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 순서가 CI에서 자동으로 그린을 내는지 확인이 필요하다.

First slice: CI에서 clean clone 시나리오를 재현해 `bun run verify:toto`가 그린인지 자동 확인하는 게이트를 추가한다. 이것이 재현성 핵심 가치를 지속 보장하는 마지막 단계다.

### 2026-05-23 - Python 환경 부트스트랩 경로 단일화

Status: proposed

Why now: `bun run bootstrap`은 로컬 `.venv` + pip으로 환경을 구성하지만, 루트 `pyproject.toml`/`uv.lock`은 `toto`를 uv 워크스페이스 멤버로 선언하고 있다. 두 경로가 공존하면 어느 Python 환경이 `bun run verify:toto`의 기준인지 불명확하고, 루트와 로컬 패키지 버전 pinning이 조용히 어긋날 수 있다.

First slice: 두 경로의 현재 패키지 버전을 비교하고, CI에서 어느 경로를 쓸지 명시적으로 선택하거나 uv 경로 하나로 통합하는 방향을 결정한다.

### 2026-05-23 - KBO 시즌 데이터 최신성 경보

Status: proposed

Why now: 대시보드가 읽기전용이어서 시드된 `PredictionCardDTO` 데이터가 오래된 시즌을 계속 보여줘도 자동으로 알 수 없다. 현재 시즌 범위와 시드 기록의 연도/라운드를 비교하지 않으면 "화면은 열리지만 틀린 데이터"를 조용히 노출하는 상황이 생긴다.

First slice: 시드 매니페스트에 기록된 시즌 범위를 홈 화면에 짧게 표시하고, 현재 연도보다 오래된 시즌임이 명확하면 경보 배너를 띄우는 freshness 표시기를 추가한다.
