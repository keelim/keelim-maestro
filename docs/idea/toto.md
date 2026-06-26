# toto

Last reviewed: 2026-06-26 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.
- SUBMODULES.md 기준으로 gitlink가 `5897ef44`에 고정돼 있고, Bun 워크스페이스(`toto-kbo-streamlit-dashboard`)와 uv 워크스페이스(`kbo-dashboard`) 양쪽에 동시 등록되어 있다.

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

### 2026-04-25 - 재현 가능한 클론 CI 게이트

Status: proposed

Why now: SUBMODULES.md 기준으로 toto gitlink(`5897ef44`)는 루트 인덱스에 이미 커밋되어 있다. 남은 과제는 신규 클론 환경에서 `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 순서가 CI에서 그린으로 돌아오는지 확인하는 것이다.

First slice: CI에서 bare clone → submodule init → bootstrap → verify:toto 체인을 한 번 실행하고, 실패하면 경로·시드·의존성 불일치를 잡아 재현성 보장을 완료로 간주한다.

### 2026-06-26 - Bun+uv 이중 실행 경로 통합 smoke gate

Status: proposed

Why now: toto는 Bun 워크스페이스(`toto-kbo-streamlit-dashboard`)와 uv 워크스페이스(`kbo-dashboard`) 양쪽에 동시 등록되어 있어서, 한 경로만 테스트하면 나머지 경로가 조용히 깨질 수 있다. WORKSPACE.md가 두 런타임 경로를 모두 명시한다.

First slice: `bun run dev:toto`(Bun 경로)와 `uv run --package kbo-dashboard --group dev pytest toto/tests`(uv 경로)를 같은 CI 단계에서 순서대로 실행하고, 두 경로 모두 그린이 되어야 smoke gate 통과로 간주한다.
