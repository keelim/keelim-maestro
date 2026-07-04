# toto

Last reviewed: 2026-07-04 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.
- `toto` gitlink는 이제 루트 인덱스에 커밋되어 있고(`git ls-files --stage | grep 160000`로 확인), 루트 `package.json`에 `dev:toto`/`test:toto`/`verify:toto` 스크립트가 살아 있다.

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

## Resolved

### 2026-04-25 - gitlink 커밋 및 재현 가능한 클론 게이트

Status: done (2026-07-04 확인)

Evidence: `git ls-files --stage | grep 160000`에 `toto`가 커밋된 gitlink(`5897ef44…`, `main`)로 등록돼 있고, `docs/CODEMAPS/SUBMODULES.md`도 이를 활성 워크스페이스 멤버로 기록한다. 루트 `package.json`에 `dev:toto`/`test:toto`/`verify:toto` 스크립트가 존재해, `git submodule update --init toto` 이후 곧바로 실행 가능하다. `.reports/codemap-diff.txt`는 이 상태가 최소 2026-06-29부터 안정적으로 유지되고 있음을 보여준다.

Follow-up: 신규 클론 시 실제로 `git submodule update --init toto && bun run bootstrap && bun run verify:toto`가 CI에서 그린으로 돌아오는지는 여전히 수동 확인 대상이다. 회귀가 보이면 이 항목을 다시 열 것.
