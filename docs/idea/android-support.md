# android-support

Last reviewed: 2026-08-06 KST

## Signals

- Play Console 업로드와 서명 흐름을 담당하는 TypeScript GitHub Action이다.
- 실패 비용이 큰 릴리스 작업을 다루며, 문제를 늦게 발견할수록 영향이 커진다.
- track, staged rollout, release notes, artifact 입력이 이미 노출되어 있다.
- `action.yml`, README, `src/*`, `lib/index.js`가 함께 맞아야 하는 번들형 Action이다.
- `action.yml`/README/소스 간 입력 계약 드리프트와 커밋된 번들(`lib/index.js`) 최신성은
  `scripts/check-contract-drift.mjs`, `scripts/check-ci-release-workflows.mjs`,
  `git diff --exit-code -- lib/index.js`로 CI(`test.yml`)에서 이미 자동 검증된다.
  `userFraction`/`status` 호환성도 `validateStatus`가 검증한다.

## Open ideas

### 2026-04-12 - Release preflight validator

Status: proposed

Why now: Most release automation pain comes from bad inputs, missing files, or
mismatched package and track configuration before the real upload even starts.

First slice: Add a dry-run validation mode that checks artifact paths, package
 metadata, auth material, track/status combinations, and a release diff against
 the last successful upload before performing any mutating Play API call.

### 2026-04-12 - 로케일 커버리지 가드레일

Status: proposed

Why now: `userFraction`/`status` 조합 검증은 이미 `validateStatus`로 처리되지만,
`whatsNewDirectory`의 로케일 커버리지 자체는 검증 대상이 아니다. `readLocalizedReleaseNotes`는
패턴에 맞는 파일을 그대로 읽어 올릴 뿐이라, 특정 로케일 노트가 빠지거나 이전 릴리스에서
그대로 남아 있어도 조용히 통과한다.

First slice: 최소 로케일 집합(예: `en-US`, `ko-KR`)을 기준으로 `whatsNewDirectory`를 점검해
누락된 로케일이나 직전 성공 업로드와 내용이 동일한(즉, 갱신되지 않은) 로케일을 경고하는
단계를 `dryRun` 검증 경로에 추가한다.

### 2026-04-13 - 릴리스 증적 번들

Status: proposed

Why now: Play Console 업로드는 성공/실패 원인 파악이 늦어질수록 비싸지므로, 실제 업로드와 dry-run의 입력·검증·응답을 한 묶음으로 남기면 복구와 감사가 쉬워진다.

First slice: 실행마다 JSON 증적 파일을 남겨 입력값, 검증 결과, track/status, 업로드 응답 URL, 경고 목록을 저장하고, 실패 시 재실행에 쓸 최소 정보를 포함한다.

### 2026-04-15 - Play API 재생 harness

Status: proposed

Why now: 이 action은 릴리스 핵심 경로를 직접 건드리는데, 현재 테스트는 입력 검증에 비해 실제 Play API 편집 생명주기 검증이 약해서 사소한 변경도 실배포까지 밀려갈 수 있다.

First slice: sign/upload/internal sharing/staged rollout 응답을 대표 fixture로 기록하고, 이를 CI에서 재생해 Play Console에 닿지 않고도 전체 edit lifecycle을 검증한다.
