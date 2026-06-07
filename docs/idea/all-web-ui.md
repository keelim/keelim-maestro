# all-web-ui

Last reviewed: 2026-05-16 KST

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

Why now: `all-web-ui`는 실제로 두 개의 다운스트림 앱에 붙어 있으니, export나 theme 파일 변경이 배포 전에 빌드 단위에서 먼저 깨지는지 확인해야 회귀 비용이 낮아진다.

First slice: `keelim-vercel`과 `rich/web`이 쓰는 import 경로를 그대로 재현하는 작은 fixture 또는 매트릭스 빌드를 만들고, 타입체크/빌드 실패를 소비자 영향 경고로 보여준다.

### 2026-06-06 - 통합 사용자 텔레메트리 이벤트 계약 (net-new N6)

Status: proposed

Why now: 사용 추적이 `keelim-vercel`의 `tool-tracking`에만 있어서 rich/apps/webui를
가로지르는 사용 인사이트가 불가능하다. 공유 UI 패키지가 이벤트 스키마의 자연스러운
소유처다. (출처: `net-new-2026-06-06.md`)

First slice: opt-in 공통 이벤트 스키마(타입+페이로드)를 `all-web-ui`에 정의하고,
소비자 1곳을 계측해 점진 확장한다.

### 2026-06-06 - 온보딩 프리미티브 (steps/tour) (net-new N7)

Status: proposed

Why now: 소비자 앱 표면이 넓어 신규 진입 사용자가 길을 잃는데, 공용 온보딩
프리미티브가 없어 각 앱이 진입 여정을 매번 새로 만든다. (출처: `net-new-2026-06-06.md`)

First slice: steps/tour/highlight 프리미티브를 추가하고 두 테마(admin-bw/finance)에서
렌더되게 한 뒤, `keelim-vercel` 온보딩(N7)이 이를 소비한다.

### 2026-06-06 - 웹 성능 예산 게이트 (net-new N4)

Status: proposed

Why now: 공유 UI 패키지 빌드에도 번들 사이즈 예산이 없어, export 증가가 소비자 번들을
조용히 키운다. (출처: `net-new-2026-06-06.md`)

First slice: 패키지 빌드 산출물 번들 사이즈를 예산 임계와 대조해 초과 시 비0 종료.
