# all-web-ui

Last reviewed: 2026-08-12 KST

## Signals

- Shared React UI package consumed by multiple web repos.
- Already ships theme tokens, reusable primitives, package exports, and a
  `componentManifest` lifecycle surface, while consumers still sit in a mixed
  migration between sibling-source imports and package exports.
- Shared UI releases create coupling, so downstream impact, export contracts,
  and discoverability matter together.
- `docs/design/design-system.md` (§11 Cross-Platform Canary)는 `all`(Android
  Compose) 토큰 동기화를 이미 "소비자(선택)" 의무로 문서화했지만, 실제
  `scripts/verify-all-web-ui-integration.sh`는 `keelim-vercel`/`rich/web` 웹
  소비자만 검사한다 — 문서화된 정책과 자동화 사이에 실제 gap이 있다.
- `scripts/all-web-ui-rich-allowed-drift.txt`에 `rich/web`의 레거시
  프리미티브/클래스 소유 파일이 11개 남아 있어(2026-08-12 기준), 다운스트림
  마이그레이션이 아직 끝나지 않았음을 구체적으로 보여준다.

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

Why now: `all-web-ui`는 실제로 두 개의 다운스트림 웹 앱과 한 개의 Android 앱에 붙어 있으니, export나 theme 파일 변경이 배포 전에 빌드 단위에서 먼저 깨지는지 확인해야 회귀 비용이 낮아진다. `docs/design/design-system.md`가 이미 Cross-Platform Canary를 정책으로 못 박아 놨는데도 실제 검사 스크립트는 웹 두 개만 커버해서, 정의된 의무와 자동화 사이의 gap이 grounded 리스크다.

First slice: `keelim-vercel`과 `rich/web`이 쓰는 import 경로를 그대로 재현하는 작은 fixture 또는 매트릭스 빌드를 만들고, 타입체크/빌드 실패를 소비자 영향 경고로 보여준다. 이어서 `scripts/verify-all-web-ui-integration.sh`에 `all`(Android Compose) 토큰 동기화 smoke 빌드 단계를 추가해, 문서화된 §11 Cross-Platform Canary 의무를 실제 게이트 하나로 묶는다.
