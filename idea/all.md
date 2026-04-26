# all

Last reviewed: 2026-04-26 KST

## Signals

- Multi-module Android/KMP workspace with six app modules and a wide shared core.
- Strong platform surface already exists in `core:*`, `feature:*`, widgets, and
  custom Gradle build logic.
- Release and quality risk scale quickly when several apps move in parallel.

## Open ideas

### 2026-04-12 - Shared module adoption map

Status: proposed

Why now: Shared Android/KMP modules already span several apps, so the highest-leverage refactors are easier to find when duplication and reuse are visible in one matrix.

First slice: Generate an app-to-module dependency map from the Gradle graph, then rank the duplicate flows or utilities that should be consolidated first.

### 2026-04-12 - Cross-app feature flag registry

Status: proposed

Why now: The workspace already has enough shared architecture that rollout
controls can pay off across several apps at once instead of being rebuilt per
app.

First slice: Define a shared flag schema and local cache, then expose a small
developer-facing screen in one app before promoting it into a shared module.

### 2026-04-12 - Release readiness radar

Status: proposed

Why now: A family of apps plus shared modules creates hidden release drift
around versioning, QA coverage, changelog completeness, and regression risk.

First slice: Generate a single report that gathers per-app version, pending
release notes, test/build status, and any known rollout blockers.

### 2026-04-13 - 컨벤션 드리프트 대시보드

Status: proposed

Why now: `AGENTS.md`에 적힌 날짜·금액·타이머 포맷 규칙과 실제 마이그레이션 대상이 많아서, 규칙 위반을 릴리스 전에 한 번에 보이는 표가 있으면 회귀 비용이 낮아진다.

First slice: 알려진 마이그레이션 대상 파일을 스캔해 날짜/금액/제로패딩 위반과 영향 모듈을 보여주는 리포트를 만들고, 우선순위가 높은 항목부터 정리한다.

### 2026-04-15 - 빌드 병목 열지도와 CI 분할 계획기

Status: proposed

Why now: 앱이 6개이고 공유 모듈도 많아서, Gradle 빌드·테스트 병목을 보지 않으면 무엇을 먼저 쪼개고 병렬화할지 계속 감으로만 판단하게 된다.

First slice: CI에서 앱·모듈별 Gradle task 시간을 수집해 병목 열지도를 만들고, 오래 걸리는 구간을 기준으로 분할·병렬화 후보를 제안한다.

### 2026-04-25 - KMP·iOS·Rust 플랫폼 빌드 게이트

Status: proposed

Why now: `all`은 Android Gradle 빌드 외에 `composeApp/`(Compose Multiplatform), `allIos/`(iOS Xcode 프로젝트), `all-rust-lib/`(Cargo 프로젝트)를 함께 갖고 있어서, 각 플랫폼 빌드가 독립적으로 깨져도 Android CI만 봐서는 감지하기 어렵다.

First slice: iOS Xcode 빌드, Cargo 빌드, Compose Multiplatform 빌드를 각각 최소 실행해 성공/실패를 확인하고, Android CI와 동일한 PR 게이트에서 플랫폼별 빌드 상태를 한 번에 보이는 요약 표를 만든다.
