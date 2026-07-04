# all-web-ui

Last reviewed: 2026-07-04 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- 루트 `bun run report:shared-ui`(`scripts/report-shared-ui-contract.sh`)가 이미
  provider(exports/manifest/style entrypoint), consumer(keelim-vercel·rich/web
  dependency·registry·style import), 정적 검증(`verify-all-web-ui-integration.sh`),
  빌드 카나리, 시각 회귀 준비도까지 하나의 리포트로 묶어서 보여준다. 다만 이
  리포트는 로컬 실행 전용이며, 루트에 `.github/workflows`가 없어 CI에는 아직
  연결돼 있지 않다.

## Open ideas

### 2026-04-12 - Token playground and theme diff lab

Status: proposed

Why now: Shared theme tokens are more valuable when consumers can preview what a
token change will do before publishing it into downstream apps.

First slice: Build a tiny docs/demo page that renders each primitive under the
existing themes and highlights token deltas side by side.

### 2026-04-12 - 시각·접근성 회귀 게이트 자동화 (구 "Visual regression and accessibility gate pack" 갱신)

Status: proposed

Why now: `report:shared-ui`의 `visual_readiness_status` 체크가 `all-web-ui`/`keelim-vercel`/`rich/web` 세 표면 모두를 기본값 "MANUAL no automated visual gate"로 보고한다. 즉 컨트롤타워 리포트가 커버하지 못하는 유일한 축이 시각/접근성 회귀라는 사실이 이미 스크립트 자체로 드러나 있다.

First slice: 세 표면 중 하나에 playwright config 또는 `visual|e2e|playwright|screenshot` 스크립트를 추가해 `visual_readiness_status`가 "READY"로 전환되는지부터 확인하고, exported primitives에 대한 스냅샷 + 최소 접근성 체크를 그 표면에 붙인다.

### 2026-04-12 - 공용 UI 계약 컨트롤타워 — CI 게이트 승격 (구 "Downstream usage matrix" + "내보내기 계약 스냅샷" + "다운스트림 빌드 카나리" 통합)

Status: proposed

Why now: 세 아이디어가 각각 요청했던 "소비자 사용 매트릭스", "export 계약 스냅샷", "다운스트림 빌드 카나리"는 이제 `bun run report:shared-ui` 한 번으로 이미 로컬에서 나온다 — provider identity/exports/manifest, `keelim-vercel`·`rich/web` 소비자별 dependency 버전·registry 매핑·style import, 정적 검증 PASS/FAIL 카운트, 빌드 카나리 표(all-web-ui/rich-web/keelim-vercel typecheck·test·build 스크립트 존재 여부)까지 한 문서에 있다. 남은 진짜 격차는 "이 리포트를 실제로 누가, 언제 돌리느냐"이며, 루트에 `.github/workflows`가 없어 all-web-ui 변경 시 자동으로 실행되지 않는다.

First slice: `all-web-ui` 변경(PR 또는 push)마다 `bun run report:shared-ui`와 `scripts/verify-all-web-ui-integration.sh --full`을 자동 실행하는 CI 워크플로를 추가하고, FAIL이 나오면 머지를 막는 최소 게이트로 승격한다.

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다. `report:shared-ui`는 현재 export 개수·manifest 항목 수만 보여줄 뿐, "무엇이 deprecated인지"는 아직 표시하지 않는다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.
