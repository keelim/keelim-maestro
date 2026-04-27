# android-support

Last reviewed: 2026-04-27 KST

## Signals

- Play Console 업로드와 서명 흐름을 담당하는 TypeScript GitHub Action이다.
- 실패 비용이 큰 릴리스 작업을 다루며, 문제를 늦게 발견할수록 영향이 커진다.
- track, staged rollout, release notes, artifact 입력이 이미 노출되어 있다.

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

### 2026-04-27 - 업로드 전 버전코드 비교 검사

Status: proposed

Why now: Play Console은 동일 트랙에 이미 게시된 버전코드를 재업로드하면 즉시 오류로 거부하므로, 서명·빌드 시간이 낭비되고 내부 공유 APK가 취소된다. `action.yml`의 `releaseFiles`·`track`·`status` 입력이 이미 노출되어 있어 dry-run 단계에서 사전 비교가 가능하다.

First slice: dry-run 검증 중 Play API를 통해 타깃 트랙의 현재 최신 버전코드를 조회하고, 업로드 대상 APK/AAB의 versionCode가 그보다 클 때만 실제 업로드로 진행한다.
