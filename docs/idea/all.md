# all

Last reviewed: 2026-05-16 KST

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

Why now: `all`은 Android Gradle 빌드 외에 `composeApp/`(Compose Multiplatform), `allIos/`(iOS Xcode 프로젝트), `all-rust-lib/`(Cargo 프로젝트)를 함께 갖고 있어서, 각 플랫폼 빌드가 독립적으로 깨져도 Android CI만 봐서는 감지하기 어렵다.

First slice: iOS Xcode 빌드, Cargo 빌드, Compose Multiplatform 빌드를 각각 최소 실행해 성공/실패를 확인하고, Android CI와 동일한 PR 게이트에서 플랫폼별 빌드 상태를 한 번에 보이는 요약 표를 만든다.

## 앱 기능 (net-new N1)

지금까지 `all`의 아이디어는 전부 빌드/릴리스 인프라였고 **실제 앱 사용자 기능**
아이디어가 0개였다. 2026-06-06 코드 그라운딩 결과, 6개 앱 모두 *개별 화면은 있으나
화면을 잇는 사용자 여정/연계 기능이 없다*는 공통 갭이 확인됐다. 앱별 1차 후보(실제
화면 기반): (출처: `net-new-2026-06-06.md`)

### 2026-06-06 - app-arducon 도구 파이프라인

Status: proposed

Why now: URL단축·Base64·QR·JSON·딥링크 등 단발 도구가 서로 단절돼, 한 도구 결과를 다음
도구에 다시 붙여 넣어야 한다.

First slice: 한 도구의 출력을 다음 도구 입력으로 잇는 파이프라인 + 최근 실행/핀 도구.

### 2026-06-06 - app-cnubus 막차 카운트다운 + 도착 알림

Status: proposed

Why now: 캠퍼스 버스 앱이 Map/Setting 최소 표면뿐이라, 정작 버스 앱의 핵심 가치(언제
타야 하는가)가 빠져 있다.

First slice: 즐겨찾는 정류장의 막차 카운트다운과 도착 임박 알림.

### 2026-06-06 - app-comssa 경제캘린더 ↔ 플래시카드 복습 연계

Status: proposed

Why now: MarketNotification·Ecocal·FlashCard가 각각 단독으로 존재한다.

First slice: 경제 캘린더 이벤트 알림을 플래시카드 복습 루프와 연결해, 이벤트 전후로
관련 카드를 띄운다.

### 2026-06-06 - app-my-grade 목표 학점 역산 플래너

Status: proposed

Why now: Grade·StudyAnalytics가 *과거* 성적만 보여주고, 목표에서 역산하는 *미래*
플래닝이 없다.

First slice: 목표 GPA 입력 → 남은 과목별 필요 성적을 역산해 제시.

### 2026-06-06 - app-mysenior 첫 사용자 표면 정의

Status: proposed

Why now: `app-mysenior`는 MainActivity만 있는 빈 스켈레톤이라 제품 표면 자체가 없다.

First slice: 큰글씨 복약 알림을 첫 표면으로 정의(app-nanda MedicationScreen 패턴 재사용).

### 2026-06-06 - app-nanda 복약·수분·영양 통합 순응도 리포트

Status: proposed

Why now: Medication·WaterIntake·Nutrient 화면이 따로 놀아, 하루 건강 순응도를 한눈에
볼 수 없다.

First slice: 세 표면을 묶은 데일리 순응도 리포트(목표 대비 달성률).
