# toto

Last reviewed: 2026-05-11 KST

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

Status: gitlink 핀 완료(a942e6b) — CI 게이트 검증 잔여

Why now: gitlink는 루트 인덱스에 `a942e6b`로 커밋된 상태이나, `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 전 과정이 CI 게이트에서 그린으로 돌아오는지는 아직 확인이 필요하다. 재현성이 핵심 가치인 프로젝트에서 클론-부트스트랩-검증 경로가 CI 단위에서 통과해야 pinning이 완료된다.

First slice: CI에서 `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto` 순서를 순차 실행하고, 전 과정이 에러 없이 그린으로 완료되는지 확인한다.

### 2026-05-11 - Python·Bun 이중 의존성 고정 재현성 검사

Status: proposed

Why now: toto는 Streamlit(Python) 런타임과 Bun 래퍼 스크립트를 함께 쓰는데, Python 패키지 버전 고정은 Bun lockfile과 별개로 관리된다. `requirements.txt` 또는 `pyproject.toml`이 정확하게 고정되지 않으면 같은 시드·같은 커밋에서도 Streamlit 렌더링 결과가 달라질 수 있어서, 재현성 약속이 Python 런타임 레이어에서 조용히 깨질 수 있다.

First slice: `bun run verify:toto` 흐름에 Python 의존성 고정 파일 존재 여부와 버전 고정 형식(핀 없는 `>=` 범위 등) 확인을 추가해, 고정이 누락된 경우를 부트스트랩 단계에서 잡는다.
