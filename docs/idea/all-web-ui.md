# all-web-ui

Last reviewed: 2026-08-06 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- 루트에는 이미 `bun run report:shared-ui`(읽기 전용 계약 리포트)와
  `scripts/verify-all-web-ui-integration.sh --full`(정적 계약 검증 + keelim-vercel/
  rich-web 런타임 검증 + GitHub Packages 게시 확인)이 구현돼 있다. 다만 루트 저장소에
  `.github/workflows`가 전혀 없어서, 이 검증들은 PR마다 자동으로 도는 CI 게이트가 아니라
  사람이 수동으로 실행해야 하는 로컬 도구로만 남아 있다.

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

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.

### 2026-04-18 - 공유 UI 계약 검증을 CI 게이트로 승격

Status: proposed

Why now: export/theme 계약 스냅샷과 `keelim-vercel`/`rich/web` 대상 다운스트림 빌드 카나리는
이미 `bun run report:shared-ui`와 `scripts/verify-all-web-ui-integration.sh --full`(GitHub
Packages 게시 확인 포함)로 루트에 구현돼 있다. 남은 위험은 이 도구들이 사람이 로컬에서
직접 실행할 때만 도는 정적 스크립트라서, 루트 저장소에 `.github/workflows`가 없는 한
`all-web-ui` 변경이 배포 전 자동으로 게이트되지 않는다는 점이다.

First slice: `bun run typecheck:web`/`bun run build:web`과
`scripts/verify-all-web-ui-integration.sh --full`을 묶은 최소 CI 워크플로를 루트에 추가하고,
실패 시 어떤 export/테마 파일과 어떤 소비자 저장소가 영향받는지 요약으로 보여준다.
