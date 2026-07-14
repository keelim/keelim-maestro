# all-web-ui

Last reviewed: 2026-07-14 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- `docs/CODEMAPS/frontend.md`(2026-07-12)로 확인한 결과, 루트에 `bun run report:shared-ui`
  (버전/의존성/스타일 계약 리포트), `scripts/verify-all-web-ui-integration.sh`(export 개수,
  manifest exportPath, 소비자별 import 히트, boundary 체크를 pass/fail로 검증), `bun run
  typecheck:web`, `bun run build:web`이 이미 존재한다. 다만 루트에 `.github/workflows`가
  없어(2026-07-14 확인) 이 검증들은 전부 로컬 수동 실행에 의존하는 상태다.

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

Status: proposed (2026-07-14 갱신 — 정적 검증은 이미 구현됨)

Why now: 공유 UI는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 공개 export와 theme 파일이 깨지면 소비자 쪽 회귀가 바로 생긴다. `scripts/verify-all-web-ui-integration.sh`가 이미 `package.json` export 개수, `src/manifest.ts`의 exportPath 목록, 소비자별 import 코드 히트 수, 테마/스타일 import 상태를 pass/fail로 검증하고 있어 계약 스냅샷의 핵심 로직은 이미 구현돼 있다.

First slice: 새 manifest를 처음부터 만들기보다, 기존 `verify-all-web-ui-integration.sh --full`과 `bun run report:shared-ui` 출력을 사람이 보기 쉬운 diff/표 형태로 다듬어 배포 전 리뷰에 붙인다. 시각/접근성 검사는 별도 항목("Visual regression and accessibility gate pack")에서 다루므로 이 아이디어에서는 제외한다.

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.

### 2026-04-18 - 다운스트림 빌드 카나리

Status: proposed (2026-07-14 갱신 — 로컬 명령은 이미 존재, CI 게이트만 남음)

Why now: `all-web-ui`는 실제로 두 개의 다운스트림 앱에 붙어 있으니, export나 theme 파일 변경이 배포 전에 빌드 단위에서 먼저 깨지는지 확인해야 회귀 비용이 낮아진다. `docs/CODEMAPS/frontend.md`로 확인한 결과 `bun run typecheck:web`(all-web-ui+keelim-vercel+rich-admin-web 타입체크)과 `bun run build:web`(keelim-vercel+rich-admin-web 빌드)이 매트릭스 빌드 역할을 이미 하고 있다. 남은 문제는 루트에 `.github/workflows`가 없어 이 명령이 PR마다 자동으로 도는 게이트가 아니라는 점이다.

First slice: 새 fixture를 만들기보다, 기존 `bun run typecheck:web` / `bun run build:web`을 `all-web-ui` 변경 PR에서 자동 실행하는 CI 게이트로 승격하고, 실패를 소비자별(keelim-vercel/rich-admin-web) 영향 경고로 구분해 보여준다.
