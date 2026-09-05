# all-web-ui

Last reviewed: 2026-09-05 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.

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

### 2026-04-13 - 내보내기 계약 스냅샷

Status: proposed

Why now: 공유 UI는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 공개 export와 theme 파일이 깨지면 소비자 쪽 회귀가 바로 생긴다.

First slice: 배포 전 `all-web-ui`의 공개 export 목록과 실제 downstream import 지점을 비교하는 manifest를 만들고, 시각/접근성 검사와 함께 계약 변경을 표시한다.

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.

### 2026-04-18 - 다운스트림 빌드 카나리

Status: proposed

Why now: `bun run report:shared-ui`, `verify-all-web-ui-integration.sh`, `typecheck:web`가 이미 존재하고 `scripts/all-web-ui-rich-allowed-drift.txt`가 `rich/web`에 남은 마이그레이션 대상 파일들을 추적하지만, 루트에 `.github/workflows`가 없어 이 검증들이 PR마다 자동으로 돌지 않는다.

First slice: 위 세 스크립트를 CI 게이트로 묶고, allowlist 파일 수가 줄어들지 않거나 새 파일이 allowlist 등록 없이 drift 패턴에 걸리면 실패하도록 만들어 다운스트림 빌드 카나리를 자동화한다.
