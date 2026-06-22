# toto

Last reviewed: 2026-06-22 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.
- 루트 `.gitmodules`에 커밋 `5897ef44`로 pinning이 완료되어, Bun 워크스페이스·uv 워크스페이스·gitlink 포인터 세 표면이 함께 움직인다.

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

### 2026-06-22 - bun+uv 이중 워크스페이스 정합성 게이트

Status: proposed

Why now: `toto`가 루트 서브모듈(`5897ef44`)로 pinning 완료되면서 Bun 워크스페이스, uv 워크스페이스, gitlink 포인터 세 표면이 동시에 관리 대상이 되었다. 패키지 버전이나 Python 의존성이 바뀔 때 세 표면이 모두 일치하는지 확인하지 않으면 신규 클론에서 조용히 깨질 수 있다.

First slice: `git submodule status toto`, `bun run test`, `uv lock --check`를 묶은 통합 정합성 검사를 만들고, 세 표면 중 하나라도 어긋나면 명시적 오류를 출력해 CI에서 잡히게 한다.
