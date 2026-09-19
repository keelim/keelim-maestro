# toto

Status: Archived — 2026-06-04부로 root 조정 레이어에서 제외됨 (루트 `AGENTS.md` `/toto` 아카이브 정책 참고)
Last reviewed: 2026-09-19 KST

## Archived 메모

- 루트 `AGENTS.md`는 `/toto`를 2026-06-04부로 archived로 지정하고, 사용자가 명시적으로
  재활성화를 요청하기 전까지 `.gitmodules`, root Bun/uv workspace, CodeGraph dispatch,
  코드맵 리프레시, idea gardener 활성 프로젝트 표에서 제외하도록 명시한다.
- 이에 따라 이 파일은 `docs/idea/index.md`의 `Projects` 표가 아닌 `Archived` 표에서만
  추적하며, 아래 항목은 재활성화 전까지 신규 실행 계획이 아닌 과거 기록으로 보존한다.
- 특히 아래 '2026-04-25 - gitlink 커밋 및 재현 가능한 클론 게이트' 항목은 `/toto`를
  `.gitmodules`에 다시 등록하는 것을 전제로 했으나, 현재 archive 정책상 더 이상 유효한
  실행 계획이 아니다.

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
