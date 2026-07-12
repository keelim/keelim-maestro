# toto

Last reviewed: 2026-07-12 KST

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

### 2026-04-25 - gitlink 회귀 방지 게이트 (2026-07-12 갱신: pinning 완료 확인)

Status: proposed

Why now: 루트 인덱스(`git ls-files --stage`)와 `docs/CODEMAPS/SUBMODULES.md`를 확인한 결과 `toto`의 gitlink(`5897ef441cb1...`)는 이미 루트 인덱스에 커밋되어 있어, 최초에 우려했던 "신규 클론 시 디렉터리 없음" 문제는 현재는 재현되지 않는다. 다만 pinned 커밋을 사람이 직접 갱신하는 한, 향후 어떤 변경으로 gitlink가 다시 누락되거나 stale해질 위험은 남아 있다.

First slice: `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 체인을 CI에서 주기 검증하는 게이트를 추가해, gitlink 누락이나 pinned 커밋과 실제 `origin/main` 간 과도한 지연을 조기에 잡아낸다.

### 2026-07-12 - 저장소 로컬 AGENTS.md 문서화 공백

Status: proposed

Why now: `toto` 저장소 자체의 코드맵 스냅샷(`docs/CODEMAPS/projects/toto.md`)이 "No root AGENTS.md was found; check for deeper instruction files before editing"라고 명시할 만큼, `toto`에는 루트가 아닌 저장소 로컬 계약 문서가 없다. `bun run bootstrap`/`seed`/`verify` 같은 실행 경로와 `src/kbo_dashboard/*` 계약은 이미 명확하지만, 이를 `toto` 저장소 안에서 다시 찾을 수 있는 문서가 없어 다음에 이 저장소를 단독으로 여는 사람(또는 에이전트)이 매번 루트 코드맵에만 의존하게 된다.

First slice: `toto` 저장소 안에 `AGENTS.md`(또는 `docs/CODEMAPS/`)를 추가해 read-only 스켈레톤이라는 정책, `bootstrap`/`seed`/`verify` 실행 순서, 그리고 provider 경계 규칙(데이터 공급자 어댑터 분리 항목과 연결)을 저장소 로컬 기준으로 남긴다. 이 작업은 `toto` 저장소 안에서 진행하며, 루트에서는 결과를 codemap에 반영하는 것까지만 다룬다.
