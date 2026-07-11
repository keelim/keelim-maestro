# toto

Last reviewed: 2026-07-11 KST

## Signals

- 로컬 read-only Streamlit 스켈레톤이라서, UI 확장보다 재현성과 입력 계약이 먼저다.
- `bun run bootstrap`, `bun run seed`, `bun run dev`, `bun run test`, `bun run compile`, `bun run verify`가 이미 실행 경로를 정해준다.
- wheel 배포보다 로컬 editable checkout 실행이 현재 계약이라서, 경로와 seed 재현성 검증이 더 중요하다.
- KBO win1loss 대시보드는 시즌/경기 데이터가 조금만 흔들려도 표가 달라지므로, 시드와 공급자 경계를 분리해 두는 편이 좋다.
- `toto` gitlink는 이제 루트 인덱스에 커밋되어 있다(`git ls-files --stage`의 `160000 5897ef44… toto`, `docs/CODEMAPS/SUBMODULES.md` 등록 서브모듈 표), 커밋 `d7e4535`("Repair root pin contracts after final review", 2026-05-17) 기준. 남은 위험은 이 pin이 CI에서 계속 재현 가능한 상태로 유지되는지다.

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

### 2026-04-18 - 서브모듈 pin 고정 CI 재현성 게이트

Status: proposed

Why now: gitlink 커밋이 완료되어 `toto`는 이제 등록된 서브모듈로 pin 되어 있다(`docs/CODEMAPS/SUBMODULES.md` `5897ef44…`). 하지만 pin이 살아있다는 사실과 그 pin에서 `bootstrap`→`seed`→`verify` 흐름이 실제로 그린인지는 다른 문제이며, 아직 이를 정기적으로 확인하는 CI 단계가 없다.

First slice: fresh-clone을 흉내 내는 CI 잡을 추가해 `git submodule update --init toto` → `bun run bootstrap` → `bun run verify:toto`를 순서대로 실행하고, 실패 시 pin 드리프트(오래된 커밋, 깨진 seed, 컴파일 실패)로 표시한다.

## Resolved ideas

### 2026-04-25 - gitlink 커밋 및 재현 가능한 클론 게이트

Status: resolved (2026-07-11)

Resolution: 루트 인덱스에 `toto` gitlink가 커밋되어 `git ls-files --stage`에서 `160000 5897ef44… toto`로 확인된다. 커밋 `d7e4535`("Repair root pin contracts after final review", 2026-05-17)에서 pin 계약이 정리됐고, `docs/CODEMAPS/SUBMODULES.md`도 동일 커밋을 등록 서브모듈로 표시한다. 후속 과제는 이 pin이 CI에서 계속 재현 가능한지 검증하는 것이며, 위 "서브모듈 pin 고정 CI 재현성 게이트" 항목으로 이어진다.
