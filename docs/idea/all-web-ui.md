# all-web-ui

Last reviewed: 2026-07-08 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- 루트에 `scripts/verify-all-web-ui-integration.sh`(정적 계약 + `--full` 런타임
  typecheck/test/build)와 `scripts/report-shared-ui-contract.sh`
  (`bun run report:shared-ui`)가 이미 있어서, export manifest·소비자 의존성·빌드
  카나리는 자동 게이트로 커버된다. 남은 공백은 시각/접근성 회귀와 프리미티브 단위
  사용처 매트릭스, deprecated export 안내다.

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
 `rich/web`. `bun run report:shared-ui`'s own visual-readiness check still
 reports "MANUAL no automated visual gate" for all three surfaces, confirming
 this gap is still open even though build/typecheck/export contracts are now
 automated.

First slice: Add snapshot coverage for the exported primitives plus a minimal
accessibility check in CI for the demo surface.

### 2026-04-12 - Downstream usage matrix

Status: proposed

Why now: `bun run report:shared-ui`'s consumer table already reports
per-consumer dependency/registry/import-hit/style status, but it rolls up to
one row per consumer, not one row per exported primitive, so it's still hard
to see which specific primitives are actually used where before a breaking
change.

First slice: Extend the existing report script to cross-reference
`src/manifest.ts` export paths against per-primitive import hits in each
consumer, then attach a short upgrade checklist for each consumer repo.

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다. 기존 정적 검증기는 현재 export 목록이 존재하는지만 확인할 뿐 deprecated 상태나 교체 경로는 다루지 않는다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.

## Resolved

- **다운스트림 빌드 카나리** (proposed 2026-04-18) — resolved by
  `scripts/verify-all-web-ui-integration.sh --full`, which runs
  typecheck/test/build across `all-web-ui`, `rich/web`, and `keelim-vercel`,
  plus `bun run report:shared-ui`'s build-canary-inventory table.
- **내보내기 계약 스냅샷** (proposed 2026-04-13) — resolved by
  `scripts/verify-all-web-ui-integration.sh`'s `all_web_ui_manifest_lists_exports`,
  boundary-import, and `rich_web_generic_drift_is_allowlisted` checks, which
  already compare public exports against downstream import sites on every run.
  Visual/accessibility coverage from the original idea remains open — see the
  "Visual regression and accessibility gate pack" entry above.
