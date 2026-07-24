# all-web-ui

Last reviewed: 2026-07-24 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- `scripts/report-shared-ui-contract.sh`와 `scripts/verify-all-web-ui-integration.sh`
  (`--full` 포함)가 이제 provider/consumer 계약 검증과 소비자 빌드 확인을 커버하지만,
  둘 다 root에 `.github/workflows`가 없어 로컬 수동 실행에만 의존한다.

## Open ideas

### 2026-04-12 - Token playground and theme diff lab

Status: proposed

Why now: Shared theme tokens are more valuable when consumers can preview what a
token change will do before publishing it into downstream apps.

First slice: Build a tiny docs/demo page that renders each primitive under the
existing themes and highlights token deltas side by side.

### 2026-04-12 - Visual regression and accessibility gate pack

Status: proposed

Why now: A shared component package becomes much safer to evolve when visual and
 accessibility regressions are caught before they break `keelim-vercel` or
 `rich/web`.

First slice: Add snapshot coverage for the exported primitives plus a minimal
accessibility check in CI for the demo surface.

### 2026-04-12 - Downstream usage matrix

Status: proposed

Why now: The package already powers multiple web apps, so changes are safer
when the consumer graph and upgrade surface are visible in one place.

First slice: Generate a matrix of exported primitives vs downstream import
sites, then attach a short upgrade checklist for each consumer repo.

### 2026-04-13 - 내보내기 계약 스냅샷 & 다운스트림 빌드 카나리

Status: in-progress — 스크립트로 구현됨, CI 연결 남음

Why now: 공유 UI는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 공개 export·theme
파일·빌드가 깨지면 소비자 쪽 회귀가 바로 생긴다.

Evidence: `scripts/report-shared-ui-contract.sh`(provider/consumer 계약 테이블,
read-only)와 `scripts/verify-all-web-ui-integration.sh --full`(all-web-ui/rich-web/
keelim-vercel의 typecheck·test·build까지 실행하는 엄격 게이트)이 이미 이 아이디어의
first slice를 구현했다. 두 스크립트 모두 `all-web-ui`의 export/manifest/style
entrypoint와 소비자 dependency·lockfile·import 경계를 함께 검사한다.

First slice (남은 것): 두 스크립트를 CI 워크플로로 승격해 PR마다 자동 실행하고, 실패
시 소비자 영향 요약을 코멘트로 남긴다. 시각 회귀는 여전히 스크립트 자체가 "MANUAL no
automated visual gate"로 보고하므로 아래 "Visual regression and accessibility gate
pack" 항목으로 이어진다.

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.
