# toto (archived)

Last reviewed: 2026-08-23 KST

## Archive status

- `/toto`는 2026-06-04부로 루트 조정 레이어에서 아카이브됐다 (`AGENTS.md`의 `/toto` archive policy, `README.md`의 "Archived child checkouts" 표 기준).
- 더 이상 등록된 서브모듈, Bun/uv 워크스페이스 멤버, CodeGraph 대상, 코드맵 리프레시 대상, 활성 idea 백로그 대상이 아니다.
- 로컬 `toto/` 체크아웃이 남아 있어도 운영자 로컬 히스토리 컨텍스트로만 취급하며, 루트에서 리셋·정규화·재작성하지 않는다.
- 아래 항목은 아카이브 이전(2026-04-18~2026-04-25)에 제안됐던 아이디어의 기록이며, 사용자가 명시적으로 재활성화를 요청하지 않는 한 실행 대상이 아니다.

## Signals (아카이브 이전 기준, 참고용)

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저였다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 실행 경로를 정해주고 있었다.
- wheel 배포보다 로컬 editable checkout 실행이 계약이라서, 경로와 seed 재현성 검증이 중요했다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋았다.

## Archived ideas (재활성화 전까지 실행 대상 아님)

### 2026-04-18 - 시즌 스냅샷 매니페스트

Status: archived (2026-06-04 toto 아카이브 정책에 따라 보류)

Why now: 대시보드가 읽기전용 스켈레톤인 만큼, 같은 시즌을 다시 시드했을 때 같은 행 수와 같은 결과가 나오는지 확인할 수 있어야 한다.

First slice: 시드 대상 시즌의 원본 파일, 행 수, 체크섬, 예상 요약값을 기록한 매니페스트를 만들고 `bun run seed` 결과와 비교한다.

### 2026-04-18 - 데이터 공급자 어댑터 분리

Status: archived (2026-06-04 toto 아카이브 정책에 따라 보류)

Why now: 지금은 로컬 스켈레톤이지만, 나중에 CSV/fixture/API 중 무엇을 쓰든 UI는 같은 계약만 보면 되게 만들어야 유지보수가 쉽다.

First slice: 경기 결과와 순위 조회를 담당하는 얇은 provider 인터페이스를 정의하고, `streamlit_app/Home.py`가 그 인터페이스만 호출하도록 바꾼다.

### 2026-04-18 - 읽기전용 스모크 게이트

Status: archived (2026-06-04 toto 아카이브 정책에 따라 보류)

Why now: 이 저장소의 핵심 가치는 수정이 아니라 재현이므로, 실수로 쓰기 경로나 외부 변조가 들어와도 바로 잡아내는 게 먼저다.

First slice: 앱 부팅, 홈 임포트, `verify` 흐름을 묶은 스모크 테스트를 추가하고, 비정상 쓰기 경로나 경로 드리프트가 있으면 실패하게 만든다.

### 2026-04-25 - gitlink 커밋 및 재현 가능한 클론 게이트

Status: archived (2026-06-04 toto 아카이브 정책에 따라 보류; gitlink 재등록은 재활성화 결정 이후에만 검토)

Why now: `toto`가 `.gitmodules`에 선언돼 있지만 gitlink가 루트 인덱스에 커밋되지 않아서, 신규 클론 시 디렉터리가 없고 `bun run dev:toto`·`bun run verify:toto`를 실행할 수 없다. 재현성을 핵심 가치로 내세운 프로젝트에서 이 비대칭은 가장 먼저 해소해야 할 운영 위험이다.

First slice: 안정 커밋을 골라 gitlink를 루트 인덱스에 커밋하고, `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 순서가 CI에서 그린으로 돌아오면 pinning 완료로 간주한다.
