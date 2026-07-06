# toto

Last reviewed: 2026-07-06 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.
- `toto` gitlink가 루트 인덱스에 커밋되어(`5897ef44`, `docs/CODEMAPS/SUBMODULES.md` 및 `git ls-files --stage`로 확인) 신규 클론 시 디렉터리가 비는 문제는 해소됐다. 다음 병목은 부트스트랩 체인 자체의 회귀 검증이다.

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

### 2026-04-25 - 재현 가능한 클론 회귀 게이트 (gitlink 고정 완료 후속)

Status: proposed (gitlink 고정 부분은 resolved)

Resolved: `toto` gitlink가 루트 인덱스에 커밋됐다 (`5897ef44`, 2026-05-12 `pin updated child project commits` 커밋 이후 `git ls-files --stage`·`docs/CODEMAPS/SUBMODULES.md`로 확인). 신규 클론 시 디렉터리가 없던 원래 문제는 해소됨.

Why now: gitlink 고정만으로는 `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 체인이 CI에서 실제로 그린으로 도는지까지 보장하지 않는다. 재현성이 핵심 가치인 프로젝트에서 다음 위험은 "고정은 됐지만 부트스트랩 체인이 조용히 깨지는 것"이다.

First slice: CI에 `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 전체 체인을 매 PR마다 실행하는 회귀 게이트를 추가하고, 실패 시 어느 단계에서 끊겼는지 바로 보이게 한다.
