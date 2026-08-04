# toto

Last reviewed: 2026-08-04 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.
- `toto`는 루트 Bun 워크스페이스(`bun run test:toto`, `bun run verify:toto`)와 루트 uv 워크스페이스(`tool.uv.workspace.members`) 양쪽에 동시에 속한 유일한 서브모듈이라서, 두 런타임의 계약이 갈라지면 다른 프로젝트보다 먼저 여기서 드러난다(2026-08-04 `docs/CODEMAPS/WORKSPACE.md`/`dependencies.md` 확인).

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

### 2026-04-25 - 재현 가능한 클론 게이트 (gitlink 커밋 완료, CI 검증 남음)

Status: proposed

Why now: gitlink는 이제 루트 인덱스에 커밋돼 있다(`git ls-files --stage`에 `160000 5897ef44... toto` 확인, 2026-08-04). 남은 위험은 그 상태가 실제로 재현 가능한지, 즉 신규 클론에서 `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 순서가 CI에서 항상 그린으로 끝나는지 아직 검증되지 않았다는 점이다.

First slice: 신규 클론을 흉내 내는 CI 잡에서 위 순서를 그대로 실행해 실패 지점(서브모듈 인증, 시드, 컴파일)을 표로 남기고, 그린이 되면 pinning 완료로 간주한다.

### 2026-08-04 - Bun·uv 이중 워크스페이스 제약 정합성 게이트

Status: proposed

Why now: `toto`는 루트 Bun 워크스페이스와 루트 uv 워크스페이스에 동시에 등록된 유일한 서브모듈이라서, 루트 `pyproject.toml`의 `tool.uv.constraint-dependencies`(pandas, numpy, pytest 등)와 `toto` 자체 Python 의존성이 갈라져도 `bun run verify:toto`만으로는 드러나지 않는다.

First slice: `bun run verify:toto` 실행 경로에 `uv run python scripts/verify-python-dependency-constraints.py --package kbo-dashboard`(또는 동등한 필터)를 추가해, Bun 쪽 컴파일/테스트 통과와 uv 제약 정합성을 한 게이트에서 함께 확인한다.
