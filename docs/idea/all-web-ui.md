# all-web-ui

Last reviewed: 2026-07-07 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- `scripts/all-web-ui-rich-allowed-drift.txt`가 `rich/web`에서 아직 로컬
  primitive/클래스 소유권을 쓰는 파일 11개를 임시 예외로 등록해 두고 있고,
  `verify-all-web-ui-integration.sh`는 이 목록에 있는 파일만 drift 검사를
  통과시킨다.

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

### 2026-04-13 - 내보내기 계약 스냅샷 (구 "Downstream usage matrix" 통합)

Status: proposed

Why now: 공유 UI는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 공개 export와 theme 파일이 깨지면 소비자 쪽 회귀가 바로 생긴다. 내보낸 primitive와 실제 downstream import 지점을 매트릭스로 보지 않으면 어떤 소비자가 영향받는지 뒤늦게 알게 된다.

First slice: 배포 전 `all-web-ui`의 공개 export 목록과 실제 downstream import 지점을 비교하는 manifest/매트릭스를 만들고, 소비자별 업그레이드 체크리스트와 시각/접근성 검사 결과를 함께 표시한다.

### 2026-04-14 - 토큰 폐기 예고판

Status: proposed

Why now: `all-web-ui`의 토큰과 프리미티브는 `keelim-vercel`과 `rich/web` 둘 다에 붙어 있어서, 이름을 바꾸거나 내릴 때 소비자 경로를 먼저 보여주지 않으면 회귀가 늦게 드러난다.

First slice: 카탈로그에서 deprecated export를 표시하고, downstream import 지점을 수집해 교체 경로와 함께 보여주는 얇은 마이그레이션 표를 만든다.

### 2026-04-18 - 다운스트림 빌드 카나리

Status: proposed

Why now: `all-web-ui`는 실제로 두 개의 다운스트림 앱에 붙어 있으니, export나 theme 파일 변경이 배포 전에 빌드 단위에서 먼저 깨지는지 확인해야 회귀 비용이 낮아진다.

First slice: `keelim-vercel`과 `rich/web`이 쓰는 import 경로를 그대로 재현하는 작은 fixture 또는 매트릭스 빌드를 만들고, 타입체크/빌드 실패를 소비자 영향 경고로 보여준다.

### 2026-07-07 - 임시 drift 허용목록 소진 추적

Status: proposed

Why now: `scripts/all-web-ui-rich-allowed-drift.txt`가 `rich/web`에서 아직 로컬 primitive/클래스 소유권을 쓰는 파일 11개를 예외로 등록해 두고 있고, `verify-all-web-ui-integration.sh`는 이 목록에 있는 파일만 drift 검사를 통과시킨다. 목록이 조용히 유지되거나 늘어나면 마이그레이션이 실제로는 멈췄는데도 통합 검증은 계속 초록불을 보여줄 위험이 있다.

First slice: `bun run report:shared-ui` 또는 별도 스크립트에서 allowed-drift 목록의 파일 수와 각 항목의 최근 변경 여부를 추적해, 목록이 줄지 않고 정체되거나 늘어나면 경고하는 소진(burn-down) 리포트를 추가한다.
