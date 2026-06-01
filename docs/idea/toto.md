# toto

Last reviewed: 2026-06-01 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win/loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.
- 2026-05-31 코드맵 기준 `.gitmodules`에 pinned commit(`5897ef44`)으로 등록 완료 — gitlink 운영 위험이 해소됐다.
- 코드맵이 provider 인터페이스가 이미 CSV/fixture/API 소스를 분리하고 있음을 확인했으므로, 다음 과제는 공급자별 교체 안정성 검증이다.

## Open ideas

### 2026-04-18 - 시즌 스냅샷 매니페스트

Status: proposed

Why now: 대시보드가 읽기전용 스켈레톤인 만큼, 같은 시즌을 다시 시드했을 때 같은 행 수와 같은 결과가 나오는지 확인할 수 있어야 한다.

First slice: 시드 대상 시즌의 원본 파일, 행 수, 체크섬, 예상 요약값을 기록한 매니페스트를 만들고 `bun run seed` 결과와 비교한다.

### 2026-04-18 - 데이터 공급자 어댑터 분리

Status: 진행 중

Why now: 2026-05-31 코드맵에서 provider 인터페이스가 이미 CSV/fixture/API 소스를 분리하고 있음이 확인됐다. 남은 과제는 각 공급자 구현체를 독립적으로 교체할 때 UI 회귀가 없음을 자동으로 검증하는 것이다.

First slice: 각 provider 구현체(CSV/fixture/API)를 독립 교체하는 최소 픽스처 테스트를 추가하고, `bun run verify:toto`에서 공급자별 smoke 결과를 함께 보고하도록 확장한다.

### 2026-04-18 - 읽기전용 스모크 게이트

Status: proposed

Why now: 이 저장소의 핵심 가치는 수정이 아니라 재현이므로, 실수로 쓰기 경로나 외부 변조가 들어와도 바로 잡아내는 게 먼저다.

First slice: 앱 부팅, 홈 임포트, `verify` 흐름을 묶은 스모크 테스트를 추가하고, 비정상 쓰기 경로나 경로 드리프트가 있으면 실패하게 만든다.
