# toto

Last reviewed: 2026-05-02 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
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

### 2026-05-02 - 시즌 전환 파라미터 갱신 게이트

Status: proposed

Why now: KBO 시즌은 매년 바뀌어서 연도 파라미터, 팀 목록, 경기 일정 포맷이 달라질 수 있다. 현재 "시즌 스냅샷 매니페스트" 아이디어는 현재 시즌 데이터의 재현성을 검증하지만, 새 시즌 시작 시 파이프라인이 올바르게 시드되는지는 별도로 확인해야 한다. 재현 가능한 파이프라인(`bun run bootstrap → seed`)을 핵심 가치로 내세운 프로젝트에서 연간 전환 게이트가 없으면 시즌 초 데이터 불일치가 조용히 쌓인다.

First slice: 시즌 연도·팀 수·경기 수를 선언하는 파라미터 파일을 만들고, `bun run seed` 이후 예상값과 실제 시드 결과를 비교하는 assertion을 `bun run verify`에 포함시킨다.

### 2026-05-02 - 루트 Bun 워크스페이스 스크립트 경로 검증

Status: proposed

Why now: 루트 `package.json`은 `bun run dev:toto`, `bun run test:toto`, `bun run verify:toto`를 workspace 스크립트로 선언하고 있다. gitlink가 커밋되기 전에는 이 스크립트가 존재하지 않는 경로를 가리키며, 커밋 이후에도 루트 스크립트가 toto 패키지를 올바르게 타겟하는지·예상 exit code를 반환하는지 검증하는 단계가 없다. SUBMODULES.md가 이 세 가지를 공식 루트 스크립트로 문서화하고 있어 통합 검증의 기준이 이미 정해져 있다.

First slice: gitlink 등록 이후 루트 `bun run verify:toto`가 성공하는지 확인하는 통합 검증 단계를 CI에 추가하고, 스크립트 경로 오류나 의존성 누락으로 실패하는 경우 명확한 오류 메시지를 남기게 만든다.
