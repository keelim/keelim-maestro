# all

Last reviewed: 2026-08-09 KST

## Signals

- Multi-module Android/KMP workspace with six app modules and a wide shared core.
- Strong platform surface already exists in `core:*`, `feature:*`, widgets, and
  custom Gradle build logic.
- Release and quality risk scale quickly when several apps move in parallel.
- Module-level `AGENTS.md` files define concrete contracts for navigation,
  repositories, KMP entities, Compose components, and Gradle convention plugins.

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

Why now: 루트와 모듈별 `AGENTS.md`에 날짜·금액·타이머 포맷, typed navigation, repository 경계, KMP entity, convention plugin 규칙이 흩어져 있어서 릴리스 전에 drift를 한 번에 봐야 한다.

First slice: 실제 소스 트리의 모듈별 `AGENTS.md` 규칙과 알려진 마이그레이션 대상 파일을 함께 인덱싱해 위반 후보와 영향 모듈을 보여주는 리포트를 만든다.

### 2026-04-15 - 빌드 병목 열지도와 CI 분할 계획기

Status: proposed

Why now: 앱이 6개이고 공유 모듈도 많아서, Gradle 빌드·테스트 병목을 보지 않으면 무엇을 먼저 쪼개고 병렬화할지 계속 감으로만 판단하게 된다.

First slice: CI에서 앱·모듈별 Gradle task 시간을 수집해 병목 열지도를 만들고, 오래 걸리는 구간을 기준으로 분할·병렬화 후보를 제안한다.

### 2026-04-25 - KMP·iOS·Rust 플랫폼 빌드 게이트

Status: proposed

Why now: `all`은 Android Gradle 빌드 외에 `composeApp/`(Compose Multiplatform), `allIos/`(iOS Xcode 프로젝트, `all.xcodeproj`), `all-rust-lib/`(Cargo 프로젝트)를 함께 갖고 있다. 최신 코드맵 기준 `.github/workflows/`에는 `app_arducon.yml`, `app_cnubus.yml`, `app_comssa.yml`, `app_my_grade.yml`, `app_nanda.yml`, `app_deploy.yml`, `ci.yml`, `release.yml` 등 앱별 Android 워크플로만 있고 iOS·Rust·Compose Multiplatform 전용 워크플로는 하나도 없어서, 세 플랫폼 중 하나가 독립적으로 깨져도 지금 CI 구성만으로는 감지되지 않는다.

First slice: `all-rust-lib/scripts/build.sh`(Cargo), `allIos/all.xcodeproj`(Xcode), `composeApp/build.gradle.kts`(Compose Multiplatform)를 각각 최소 실행해 성공/실패를 확인하고, 기존 Android PR 게이트 옆에 플랫폼별 빌드 상태를 한 번에 보이는 요약 표를 추가한다.
