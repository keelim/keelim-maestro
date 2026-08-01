# android-support

Last reviewed: 2026-08-01 KST

## Signals

- Play Console 업로드와 서명 흐름을 담당하는 TypeScript GitHub Action이다.
- 실패 비용이 큰 릴리스 작업을 다루며, 문제를 늦게 발견할수록 영향이 커진다.
- track, staged rollout, release notes, artifact 입력이 이미 노출되어 있다.
- `action.yml`, README, `src/*`, `lib/index.js`가 함께 맞아야 하는 번들형 Action이다.
- `AGENTS.md`가 스스로 `manual-build.yml`을 "Fragile CI Setup"으로 지목하고 있다: 버전 관리에 `awk`/`sed`를 쓰고, 캐시 키에 정의되지 않은 매트릭스 변수 `${{ matrix.bun }}`를 참조한다.

## Open ideas

### 2026-04-12 - Release preflight validator

Status: proposed

Why now: Most release automation pain comes from bad inputs, missing files, or
mismatched package and track configuration before the real upload even starts.

First slice: Add a dry-run validation mode that checks artifact paths, package
 metadata, auth material, track/status combinations, and a release diff against
 the last successful upload before performing any mutating Play API call.

### 2026-04-12 - Localized rollout guardrails

Status: proposed

Why now: The action already accepts staged rollout and localized "What's New"
 data, which makes it a good place to prevent partial or risky release setups.

First slice: Validate locale coverage in `whatsNewDirectory` and warn or fail on
suspicious staged-rollout inputs such as missing `userFraction` or conflicting
release status.

### 2026-04-13 - 액션 계약 드리프트 검사

Status: proposed

Why now: `action.yml`, README, 소스, 번들 산출물이 쉽게 서로 어긋날 수 있고, 입력 변경 시 인터페이스와 문서를 함께 맞춰야 하는 부담이 이미 드러나 있다.

First slice: `action.yml`, `README.md`, `src/main.ts`, `lib/index.js`의 입력·출력 선언을 비교하는 가벼운 검사를 추가해 릴리스 전에 계약 불일치를 잡는다.

### 2026-04-13 - 릴리스 증적 번들

Status: proposed

Why now: Play Console 업로드는 성공/실패 원인 파악이 늦어질수록 비싸지므로, 실제 업로드와 dry-run의 입력·검증·응답을 한 묶음으로 남기면 복구와 감사가 쉬워진다.

First slice: 실행마다 JSON 증적 파일을 남겨 입력값, 검증 결과, track/status, 업로드 응답 URL, 경고 목록을 저장하고, 실패 시 재실행에 쓸 최소 정보를 포함한다.

### 2026-04-15 - Play API 재생 harness

Status: proposed

Why now: 이 action은 릴리스 핵심 경로를 직접 건드리는데, 현재 테스트는 입력 검증에 비해 실제 Play API 편집 생명주기 검증이 약해서 사소한 변경도 실배포까지 밀려갈 수 있다.

First slice: sign/upload/internal sharing/staged rollout 응답을 대표 fixture로 기록하고, 이를 CI에서 재생해 Play Console에 닿지 않고도 전체 edit lifecycle을 검증한다.

### 2026-08-01 - CI 캐시 키 결함 수정

Status: proposed

Why now: 저장소 자체 `AGENTS.md`가 `manual-build.yml`을 "Fragile CI Setup"으로 명시하고 있다. `awk`/`sed`로 `package.json` 버전을 직접 조작하고, 캐시 키가 정의되지 않은 매트릭스 변수 `${{ matrix.bun }}`를 참조해서 캐시가 항상 미스하거나 워크플로 문법 오류로 조용히 깨질 수 있다. 릴리스 액션 자체의 CI가 불안정하면 이 액션을 쓰는 `all`의 여러 앱 배포까지 영향을 받는다.

First slice: `manual-build.yml`의 매트릭스 정의와 캐시 키 표현식을 대조해 실제 사용 가능한 변수로 고치고, 버전 범프 단계를 `awk`/`sed` 대신 `package.json`을 직접 읽고 쓰는 스크립트로 교체한 뒤 워크플로 문법과 캐시 히트 여부를 한 번 더 확인한다.
