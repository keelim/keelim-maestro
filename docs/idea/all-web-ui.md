# all-web-ui

Last reviewed: 2026-07-09 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- `scripts/verify-all-web-ui-integration.sh` and `bun run report:shared-ui` now
  give a static export/import contract gate (see Resolved), so remaining gaps
  are about visual/accessibility regression and submodule-conversion readiness,
  not export-matrix visibility.

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

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.

### 2026-07-09 - 서브모듈 전환 준비 게이트

Status: proposed

Why now: `docs/CODEMAPS/projects/all-web-ui.md`는 `all-web-ui`가 origin 대비 clean 상태이며 전환을 막는 건 `rich`의 dirty/ahead-of-origin 상태뿐이라고 밝히고 있다. `toto`는 이미 gitlink pinning + `bun run verify:toto` 패턴으로 같은 문제를 풀었으므로, 같은 재현 가능한 클론 게이트 절차를 `all-web-ui`(그리고 뒤이어 `rich`)에도 적용할 준비를 미리 해 둘 가치가 있다.

First slice: `bun run report:baseline`과 `SUBMODULES.md`의 Expansion Blockers를 주기적으로 확인해 `rich`가 clean해지는 시점을 감지하고, 감지 즉시 `all-web-ui`를 `.gitmodules`에 등록·pin·검증까지 이어갈 체크리스트를 `toto` 사례를 본떠 정리한다.

## Resolved

- 2026-07-09 — Downstream usage matrix (2026-04-12), 내보내기 계약 스냅샷 (2026-04-13),
  다운스트림 빌드 카나리 (2026-04-18): `scripts/verify-all-web-ui-integration.sh`
  (export manifest 비교, adapter-safe import 경계, `keelim_components_ui_is_shim_only`
  등)와 `scripts/report-shared-ui-contract.sh`(`bun run report:shared-ui`), 그리고
  `bun run typecheck:web` / `bun run build:web`가 export 계약·다운스트림 import·빌드
  카나리를 이미 정적으로 검증하고 있어 별도 신규 작업 없이 해소됨. 근거:
  `docs/CODEMAPS/frontend.md`, `package.json`(`report:shared-ui`, `typecheck:web`,
  `build:web`).
