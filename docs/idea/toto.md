# toto

Last reviewed: 2026-05-17 KST

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

### 2026-04-25 - 재현 가능한 클론·CI 부트스트랩 게이트

Status: proposed

Why now: `toto`의 gitlink가 루트 인덱스에 `5897ef44` 커밋으로 고정되었지만(2026-05-17 확인), 신규 클론 환경에서 `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 전체 체인이 CI에서 그린인지 아직 자동 검증이 없다. 재현성을 핵심 가치로 내세운 프로젝트에서 체인 검증이 빠지면 운영 위험이 남는다.

First slice: `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 순서를 CI 잡으로 만들어 신규 클론 재현성을 자동으로 보장하고, 실패 시 어느 단계에서 깨졌는지 즉시 알 수 있는 에러 요약을 붙인다.

### 2026-05-17 - uv 워크스페이스 Python 의존성 정렬 검증

Status: proposed

Why now: 루트 `pyproject.toml`이 `toto`와 `rich`를 같은 uv 워크스페이스로 묶고 있어서, 두 멤버의 패키지 요구사항이 조용히 어긋나면 `toto` 부팅이나 pytest가 실패해도 uv 워크스페이스 충돌이 원인임을 추적하기 어렵다.

First slice: `uv.lock`에 고정된 실제 버전과 `toto`·`rich` 각 `pyproject.toml` 선언을 비교해 불일치·충돌 후보를 나열하고, `bun run verify:toto`보다 앞선 프리플라이트 단계로 붙인다.
