# keelim-maestro 서브프로젝트 기능·개선 리서치 리포트

*Generated: 2026-06-04 KST · Scope: 8 sub-projects · Method: code-grounding (3 Explore agents) + bounded external web research · Confidence: High (code-grounded) / Medium (external-pattern recommendations)*

## Executive Summary

이 리포트는 `keelim-maestro` 워크스페이스의 8개 서브프로젝트 각각에 대해 (1) 기존 `docs/idea/<project>.md` 백로그를 실제 코드 진입점에 묶어 **심화**하고, (2) 백로그를 넘어선 **신규 기능**을 발굴하고, (3) 운영 블로커와 영향/노력을 함께 고려한 **우선순위 로드맵**을 제시한다.

핵심 발견 3가지:

1. **기존 백로그는 "신뢰성/드리프트 감시 리포트"에 강하게 편향**돼 있다(계약 스냅샷, 신선도 워치독, 채택 맵). 사용자 요청의 "신규 기능 발굴"은 이 편향 밖, 즉 사용자/제품 가치 쪽을 의도적으로 채워야 한다.
2. **운영 블로커가 로드맵의 시작점을 강제**한다 — `rich`/`keelim-vercel` 더티 트리, `rich` 스케줄러 부재, `all-web-ui` 미등록 서브모듈. (`toto`/`android-support`는 서브모듈 *포인터 드리프트* — 인덱스 기록 커밋과 체크아웃 커밋 불일치 — 로 가벼운 동기화 항목이며, 초기 백로그가 주장한 "gitlink 미커밋/빈 클론"은 **사실이 아님**. `git ls-files --stage`가 두 repo 모두 `160000` 게이트링크를 반환해 커밋 확인됨.) 영향/노력과 무관하게 *언제* 착수 가능한지를 결정한다.
3. **`rich`의 공유 선결 조건**: 코드에 스케줄러/오케스트레이션 계층이 없다(APScheduler/Celery import 부재). execution ledger·freshness watchdog·data-portal feed 세 기능이 조용히 이 계층에 의존하므로, 기능별이 아니라 **공통 선결 작업**으로 빼야 한다.

가장 빠른 승리(코드 준비 완료, S 노력): `keelim-vercel` 메뉴 배지/스토리지 레지스트리 드리프트 게이트, `all-web-ui` 다운스트림 사용 매트릭스, `rich` 통합 헬스 콘솔, `android-support` 액션 계약 드리프트 검사, `toto` 읽기전용 스모크 게이트(핀 이후), `keelim-plugin` 생성 카탈로그, vault 프로젝트-노트 백링크 허브.

---

## 0. 교차 운영 블로커 (로드맵 선결 게이트)

| 블로커 | 영향 | 해소 작업 | 노력 |
| --- | --- | --- | --- |
| `toto`·`android-support` 서브모듈 포인터 드리프트 | 루트 인덱스 기록 커밋(`toto 5897ef44`, `android-support 485a2e40`)과 체크아웃 커밋(`b94974b4`, `06843399`) 불일치 → ` M`로 표시. **빈 클론 아님** — 게이트링크는 커밋됨(`git ls-files --stage`가 `160000` 반환). 가벼운 핀 정렬 항목 | 의도한 커밋으로 정렬: `git add toto android-support` 후 검증, 또는 체크아웃을 인덱스 커밋으로 리셋 | S |
| `rich` 더티 트리 (M `docs/words/...md`, `web/tsconfig.tsbuildinfo`) + "freeze/split before modernization" 정책 | 스키마/라우트를 건드리는 기능 머지 전 커밋/스태시 필요 | 더티 변경 커밋·정리, freeze/split 결정 확정 | S |
| `rich` 스케줄러/오케스트레이션 계층 부재 (APScheduler/Celery import 없음) | execution ledger·freshness watchdog·data-portal feed가 모두 의존 | in-process APScheduler 먼저 도입(소규모), 추후 Celery 승격 평가 | M |
| `keelim-vercel` 더티 트리 (docs/CODEMAPS, scripts 등) | 기능 작업 전 로컬 드리프트 확인 | 더티 변경 커밋 | S |
| `all-web-ui` 미등록 서브모듈(자율 로컬 repo) | 루트 핀/CI 카나리 통합 시점 제약 | 잔여 워크스페이스 블로커 해소 후 등록 평가 | — |

> 스케줄러 선택은 외부 패턴과 일치한다: 동일 FastAPI 앱 객체/소규모 주기 작업은 APScheduler in-process, 분산·재시도·모니터링이 필요한 무거운 처리는 Celery로 승격 ([FastAPI Scheduling guide](https://medium.com/@rasifrazak123/fastapi-scheduling-background-tasks-backgroundtasks-vs-apscheduler-vs-celery-complete-guide-ff90d6be524b), [APScheduler+FastAPI](https://ahaw021.medium.com/scheduled-jobs-with-fastapi-and-apscheduler-5a4c50580b0e)).

---

## 1. keelim-vercel (Next.js 금융 웹 — DEEP)

**현재 상태**: `app/(dashboard)/*` 라우트 그룹에 ~19개 도구 + 50+ 계산기, 네비게이션은 `lib/menu-config.ts`(140+줄, `isNew:true` 4개). 데이터 계층은 Supabase(`lib/supabase.ts`) + Drizzle(`lib/db.ts`), 클라이언트 영속 저장 70+ `*-storage.ts`. 도구 추적이 이미 라이브: `lib/tool-tracking.ts` + `lib/ranking-actions.ts`가 Supabase `tool_clicks`(entry/view/complete, 15 source)에 기록. 스토리지 레지스트리 `lib/storage-version-registry.ts`(82키) + `lib/storage-versioning.ts`. 공유 UI 어댑터 `components/shared/all-web-ui-adapters.tsx`(Badge/Button/Card 3개만 포워딩). `app/sitemap.ts`·`app/robots.ts` 존재.

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 메뉴 배지 예산 강제 | deepen | `lib/menu-config.ts`(`isNew:` 스캔) ↔ `lib/changelog-data.ts`(날짜) ↔ `app/changelog/page.tsx` | S | 배지 4개 규칙 위반·stale 배지 자동 감지, pre-commit 가능 | 없음 (regex+diff) |
| 스토리지 키 레지스트리 드리프트 게이트 | deepen | `lib/storage-version-registry.ts`(82키) ↔ `lib/*storage*.ts` 상수 ↔ `lib/storage-versioning.ts` | S | 레지스트리 누락/stale 마이그레이션 → 사용자 설정 조용한 손상 방지 | 없음 (추출기+배열 diff) |
| 공유 UI 어댑터 스냅샷·diff | deepen | `components/shared/all-web-ui-adapters.tsx`(3 export) ↔ downstream import grep ↔ `all-web-ui/src/manifest.ts`(34 컴포넌트) | M | export 변경 CI 게이트; 어댑터 얇아 표면 작음 | cross-repo grep + manifest 빌드 |
| 도구 사용 히트맵 & 데드 표면 정리 | deepen | `lib/ranking-actions.ts`(Supabase `tool_clicks` 쿼리) + `lib/menu-config.ts` 인벤토리 | M | 50+ 도구를 실사용 기준 랭크, 장기 미사용 라우트 통합 후보화 | 집계 쿼리 계층 + 주간 잡(스케줄러 없음) |
| 라우트 계약 드리프트 리포트 | deepen | `app/(dashboard)/layout.tsx` + nav ↔ `app/api/` 인벤토리 ↔ `app/sitemap.ts`/`robots.ts` | M | 메뉴·실라우트·API·sitemap 정합성 주간 리포트로 orphan 표시 | 빌드타임 스크립트 미통합 |
| **Next-best-action 피드** (신규) | new | `lib/tool-tracking.ts` 히스토리 + `lib/household-goal-checkin-storage.ts` + `lib/favorite-tools-storage.ts`; `/dashboard` 또는 신규 `/next-action` | M–L | 긴 카탈로그 대신 "다음 행동" 추천 → 후속 행동 루프 강화(백로그 Signals와 정합) | 룰기반/LLM 스코어링 + Supabase 프로필 스키마 |

**신규 기능 노트**: Next-best-action 피드는 도구 히스토리·북마크·목표 체크인 표면이 이미 존재해 코드 앵커가 분명하다. 1차는 룰기반(최근 도구 시퀀스 + 즐겨찾기 + 프로필 신호)으로 시작하고, 효과 검증 후 LLM 스코어링으로 승격하는 점진 경로 권장.

**Operational blockers**: 더티 트리; `tool_clicks` 테이블 스키마 코드 미검증(히트맵 집계 쿼리 부재); 어댑터가 34개 중 3개만 미러 → 롤아웃 미완.

---

## 2. all-web-ui (공유 React UI 패키지 — LIGHT)

**현재 상태**: `@keelim/all-web-ui`로 퍼블리시되는 34+ 프리미티브 + 테마 토큰. `src/index.ts` export, `src/manifest.ts`의 `ComponentManifestEntry`(stable/deprecated/removed 라이프사이클 + replacement/removalTarget). 테마 CSS 2종(`src/styles/themes/admin-bw.css`, `finance.css`) + `src/lib/cn.ts`. 소비자: `keelim-vercel`(어댑터 확인) + `rich/web`(`styles.css` import, transpilePackages). `.stitch/metric-card-migration-candidates.md`가 진행 중 마이그레이션 추적.

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 다운스트림 사용 매트릭스 | deepen | `@keelim/all-web-ui` import grep(keelim-vercel + rich/web) ↔ `src/manifest.ts` 크로스레퍼런스 | S | (컴포넌트 × 소비자 × 사용수) 매트릭스 → deprecation 영향 가시화 | grep + TS AST, 인프라 비용 낮음 |
| 시각 회귀 & 접근성 게이트 팩 | new | `tests/visual-*.test.ts`(Playwright) + axe-core; 테마별 베이스라인 스냅샷; CI 통합 | M | Button/Badge/Card 드리프트를 소비자 도달 전 차단; 대비 회귀 방지 | CI(GitHub Actions) + Chromatic/Percy 또는 자체 스냅샷 |
| 토큰 플레이그라운드 & 테마 diff 랩 | new | `src/docs/theme-lab.tsx`; 각 프리미티브를 두 테마로 병렬 렌더 + 토큰 델타 강조; `src/lib/cn.ts` 토큰 변수 | M | 퍼블리시 전 토큰 변경 미리보기 → 다운스트림 깜짝 회귀 감소 | 데모 페이지 인프라(Storybook 부재) |

**외부 패턴 참조**: 디자인 시스템 표준 스택은 **Storybook(격리 개발) + Chromatic(컴포넌트 단위 시각 회귀) + axe-core CI(WCAG 위반 시 머지 차단)** 조합이며, 토큰은 **Style Dictionary**로 CSS/Swift/Kotlin 다중 플랫폼 변환한다(W3C Design Tokens 사양 2025-10 안정화) ([Chromatic for Storybook](https://www.chromatic.com/storybook), [Storybook+Chromatic VRT](https://bug0.com/knowledge-base/storybook-visual-regression-testing-chromatic), [A11y in design systems](https://a11ypros.com/blog/accessibility-in-design-systems)). 두 테마(admin-bw/finance)를 이미 보유하므로 토큰 랩 + 시각 게이트가 가장 자연스러운 진입.

**Operational blockers**: manifest가 34개를 stable로 보지만 `.stitch/`는 진행 중 마이그레이션 시사 → manifest-실제 불일치; 다운스트림 카나리(소비자 빌드 전체 CI) 부재; 미등록 서브모듈.

---

## 3. rich (FastAPI 관리자 + Next.js 웹 — DEEP)

**현재 상태**: FastAPI(`app/main.py` + `/api/admin` 라우터), 서비스 계층 `app/services/{weekly_review,market_fear_greed,quality_screener,krx_daily_price_cache,krx_data_portal_client}.py`. 라우트 `/api/admin/pykrx/{fear-greed,quality-screener}`, `/api/admin/weekly-review/{summary,generate-ai,save}`, 에러 엔벨로프(PykrxIngestionError, WeeklyReviewError). 프런트 계약 `web/src/lib/api.ts`(FearGreedFreshness 등). wiki는 `docs/words`(raw-source/wiki/schema split). 통합: PyKRX, KRX 공공포털, Supabase, Google, GitHub CLI.

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 통합 헬스 콘솔 | new | 신규 `/api/admin/integrations/health` + `app/services/integration_health.py`(Supabase ping, KRX 로그인 상태, GitHub 토큰, PyKRX last-run 래핑) | S | Supabase/Google/GitHub/KRX 연결 드리프트 실시간 가시화 → 다운스트림 실패 전 복구 | 신규 서비스 모듈; Supabase 시스템 테이블/캐시 타임스탬프 |
| 데이터 신선도 워치독 | new | `app/services/freshness_monitor.py`(테이블별 stale 임계, PyKRX 캐시 age, KRX last-fetch) + `/api/admin/freshness/status` | S–M | 조용한 staleness(KRX 다운/지연)를 review 왜곡 전 감지 | **스케줄러 선결**; `as_of_date` 일관성 |
| 일일 리뷰 콕핏 | deepen | `web/src/lib/api.ts` + 신규 페이지; `/weekly-review/summary` + `/pykrx/fear-greed/overview` + docs/words 라우팅 집계 | M | agenda·inbox·PyKRX·저널을 하나의 랜딩 의식으로 → 컨텍스트 스위칭 감소 | 통합 쿼리 계약 + 페이지 스캐폴드 |
| 공공데이터 카탈로그 변경 피드 | new | `app/services/krx_data_portal_client.py` 카탈로그-export differ; Supabase `data_portal_changes`; `/api/admin/data-portal/changes` → weekly-review 큐 | M | 정적 인벤토리를 watchable 피드로 → API deprecation·필드 rename 조기 포착 | **스케줄러 선결**; diff 알고리즘; client 리팩터 |
| 실행 원장 + 리플레이 타임라인 | deepen | Supabase `execution_events` + `app/services/execution_ledger.py`(에러 핸들러/크론 훅에서 정규화) + `/api/admin/executions` | L | 모든 run/retry/failure 가시화 + 워크플로 역링크 | alembic 마이그레이션, 서비스 계측, RLS; **스케줄러 선결** |
| 실패 run 복구 콕핏 | deepen | 에러 핸들러 계측 → Supabase `failed_runs`; `app/services/recovery.py`(실패유형별 remediation) + `/api/admin/recovery/queue` | L | 흩어진 로그를 단일 큐 + 정확한 재시도/복구 액션으로 | execution_ledger 의존; 서비스별 remediation 로직 |

**외부 패턴 참조**: 실행 원장은 **Transactional Outbox 패턴**과 정합한다 — 상태/타임스탬프가 있는 outbox 행이 라이프사이클 추적·감사 추적을 제공하며, `processed_at IS NULL` 인덱스 쿼리는 저렴하다 ([Transactional Outbox – AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), [Event Sourcing+CQRS with FastAPI/Celery](https://dev.to/markoulis/how-i-learned-to-stop-worrying-and-love-raw-events-event-sourcing-cqrs-with-fastapi-and-celery-477e)). 단, 개인 운영 도구 규모에서는 풀 event-sourcing보다 **단순 append-only 이벤트 테이블 + 인덱스 폴링**으로 시작 권장.

**Operational blockers**: 더티 트리(스키마/라우트 변경 전 커밋/스태시); 스케줄러 부재(3개 기능 공통 의존).

---

## 4. all (Android/KMP 멀티모듈 — DEEP)

**현재 상태**: 6 앱(grade/deeplink/health/bus/finance/senior), 14 `core:*` + 5 `feature:*`, KMP shared 모듈(89파일). 멀티플랫폼: `composeApp/`(Compose MP), `allIos/`(Xcode), `all-rust-lib/`(Cargo JNI). 빌드 인프라 `build-logic/convention/`(17 컨벤션 플러그인) + `gradle/libs.versions.toml` 단일 의존 소스. CI `.github/workflows/ci.yml`(변경 앱 감지), `app_deploy.yml`. 계약은 루트 + 모듈별 `AGENTS.md`(포맷/네비/repository/KMP entity).

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 공유 모듈 채택 맵 | deepen | `settings.gradle.kts` 모듈 목록 + `gradle/libs.versions.toml` + Gradle 모델 파싱 | M | 6앱 reuse/중복 가시화 → 통합 우선순위를 감이 아닌 데이터로 | Gradle 모델(subprojects deps) 파싱 |
| 크로스앱 피처 플래그 레지스트리 | new | 스키마 `core:data-api/`, 캐시/repo `core:data/`(Hilt 기존), 화면 `feature:ui-setting/` | M | 공유 아키텍처 위 롤아웃 컨트롤을 여러 앱 동시 적용 | 없음(기존 DataStore 패턴과 정합) |
| 릴리스 레디니스 레이더 | new | 앱별 `build.gradle.kts`(versionCode/Name) + `.github/workflows/*.yml` 상태 + `docs/topics/Release-Note.md` | M | 버전/QA/changelog 드리프트를 한 리포트로 → stalled 릴리스 방지 | CI가 빌드/테스트 상태 노출 필요 |
| 빌드 병목 열지도 & CI 분할 계획기 | new | `.github/workflows/ci.yml` Gradle 호출에 타이밍 계측 + task 그래프 파싱 | M | 6앱×14모듈 조합 복잡도 → 무엇을 쪼개/병렬화할지 데이터화 | CI 계측 |
| KMP/iOS/Rust 플랫폼 빌드 게이트 | new | `ci.yml`에 iOS Xcode(`allIos/all.xcodeproj`) + Cargo check(`all-rust-lib`) + Compose MP 스텝 → PR 요약 표 | M | Android-only CI가 가리는 플랫폼별 독립 실패를 머지 전 노출 | 러너 Xcode/Cargo 툴체인, iOS 빌드 시크릿 |
| 컨벤션 드리프트 대시보드 | deepen | 모듈별 `AGENTS.md` 규칙 인덱싱 + `core/*`·`feature/*` 소스 스캔(날짜 포맷·하드코딩 통화) | L | 8개 AGENTS.md 규칙이 릴리스 QA 전까지 조용히 드리프트 | 탐지용 AST/regex 패턴 |

**외부 패턴 참조**: 빌드 병목은 **Build Scan으로 베이스라인 → `--parallel`(실측 평균 40% 단축) → 병목 task 식별**이 정석이며, `gradle-profiler`로 벤치마크한다 ([Gradle performance docs](https://docs.gradle.org/current/userguide/performance.html), [gradle-profiler](https://github.com/gradle/gradle-profiler), [Develocity build observability](https://gradle.com/blog/optimize-your-gradle-and-maven-builds-with-resource-usage-data/)). 무료 경로(gradle-profiler + `--scan`)로 시작하고 규모 확장 시 Develocity 평가 권장.

**Operational blockers**: CI에 플랫폼별 빌드 게이트 없음(iOS/Cargo 수동); 컨벤션 드리프트 탐지 수동; Gradle task 타이밍 미계측.

---

## 5. toto (KBO Streamlit 대시보드 — DEEP, 소형)

**현재 상태**: Streamlit(`streamlit_app/Home.py` → `kbo_dashboard.streamlit_support.prepare_page()`), SQLite(`.data/dashboard.sqlite3`), dataclass 계약(`src/kbo_dashboard/contracts.py`: DashboardFilters, PredictionCardDTO 등). 서비스 `src/kbo_dashboard/repository.py`(DashboardRepository) + `bootstrap.py`(`get_repository(reset=)`). bun 스크립트(bootstrap/seed/dev/test/verify/compile), `verify = pytest && compileall`.

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 서브모듈 포인터 핀 정렬 + 재현 클론 게이트 | housekeeping | 게이트링크는 이미 커밋됨(`160000 5897ef44`); 인덱스↔체크아웃 커밋 정렬 후 CI: `submodule update --init toto → bun run bootstrap → verify:toto` | S | 포인터 드리프트 해소 + 재현 클론 그린 검증 (※ 초기 백로그의 "빈 클론" 주장은 오류) | 의도 커밋 선택만 |
| 읽기전용 스모크 게이트 | new | `tests/test_smoke_readonly.py`(Home import + bootstrap + verify, write-path 부작용 0 assert) → `verify` 스크립트 | S | 재현이 핵심 가치 → 우발적 쓰기/경로 드리프트 차단 | 핀 이후; 파일 상태 pre/post 추적 |
| 시즌 스냅샷 매니페스트 | deepen | `toto/manifest.json`(season/source/row_count/sha256/expected) + `bootstrap.py` seed 확장 + `tests/test_repository.py` 재시드 diff | M | 동일 시드가 다른 행수/요약 → 즉시 실패(데이터 손상 조기 감지) | 결정적 시드(외부 API 핀/픽스처) |
| 데이터 공급자 어댑터 분리 | deepen | `repository.seed_demo_data()` → `GameResultProvider`/`RankingProvider` Protocol 추출; `Home.py`는 repository만 호출 | M | UI/데이터소스 분리 → CSV/fixture/API 피벗 시 UI 무변경 | DTO/내부모델 분리; `_LocalFixtureProvider` 추출 |

**Operational blockers**: 서브모듈 포인터 드리프트(인덱스 `5897ef44` vs 체크아웃 `b94974b4`) → 루트에서 ` M toto`. 게이트링크 자체는 커밋돼 있어 빈 클론은 아니며, 핀 정렬만 하면 됨. (초기 `docs/idea/toto.md`(2026-04-25)의 "gitlink 미커밋" 기재는 stale·부정확.)

---

## 6. android-support (TS GitHub Action — LIGHT)

**현재 상태**: TS 액션(`src/main.ts` → `lib/index.js`), `action.yml` 20+ 입력 + 13 서명 출력. 입력 검증 `src/input-validation.ts`(validateUserFraction/Status/InAppUpdatePriority/ReleaseFiles), 업로드 `src/edits.ts`(runUpload, Play API edit 라이프사이클), 서명 `src/signing.ts`. 테스트 8개(`__tests__/*.test.ts`).

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 액션 계약 드리프트 검사(CI) | new | `scripts/check-contract-drift.ts`: `action.yml` ↔ `src/main.ts` 파라미터 ↔ `README.md` 표 비교, 불일치 시 CI 실패 | S | action.yml 추가 입력이 main.ts 미연결/문서 stale → 워크플로 깜짝 방지 | YAML 파서 + TS AST/regex; 빌드 전 실행 |
| 릴리스 프리플라이트 검증(dry-run) | new | `action.yml`에 `dryRun` 입력 + `src/preflight.ts`(아티팩트 존재/패키지 메타/auth/track-status enum) — Play API 미호출 | M | 비싼 Play API mutation 전 입력 오류 차단 | input-validation.ts 로직 중복 회피 |

**외부 패턴 참조**: 레퍼런스 액션(`r0adkll/upload-google-play`)의 알려진 함정 — `status`(completed/inProgress/halted/draft), `changesNotSentForReview`, 그리고 **외부 변경 후 stale edit → 항상 fresh edit 생성** 필요. 프리플라이트는 `packageName` 사전 존재·track 조합·드래프트 상태를 검증해야 한다 ([r0adkll/upload-google-play](https://github.com/r0adkll/upload-google-play), [action.yml](https://github.com/r0adkll/upload-google-play/blob/master/action.yml)).

**Operational blockers**: 코드 자체는 클린(테스트 존재, action.yml/lib 동기)이나, 루트에서 서브모듈 포인터 드리프트(인덱스 `485a2e40` vs 체크아웃 `06843399`) → ` M android-support`. 핀 정렬 필요(§0 참조).

---

## 7. keelim-plugin (개인 스킬 저장소 — LIGHT)

**현재 상태**: 8 스킬 `skills/*/SKILL.md`(+ 선택 `agents/openai.yaml` Codex 메타). 듀얼 설치(Vercel skills CLI + 수동 symlink). 루트 `AGENTS.md`/`README.md`(스킬 목록·설치).

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 생성형 스킬 카탈로그 + 설치 매트릭스 | new | `skills/*/SKILL.md` 메타 파싱 → 태그(라이프사이클/플랫폼/목적) + 설치 명령 매트릭스(CLI vs symlink) | S | 스킬 증가 → 수기 README stale; 라이프사이클 태그로 미검증 스킬 오용 방지 | frontmatter 파싱 + 템플릿 |
| 스킬 스모크 테스트 하네스 | new | 각 스킬 필수 파일/설치 명령 검증 + Codex/Claude 설치 패리티 비교 | S | 두 설치 경로 유효성·툴 간 패리티 갭을 PR 전 노출 | skills CLI + Claude 환경 |

**Operational blockers**: 라이프사이클 메타 부재; README 기반 발견이 스킬 수 증가로 드리프트; 툴 간 패리티 불투명. (bespoke 개인 도구 — 외부 비교군 없음, 코드 앵커 있는 2건만 권장)

---

## 8. Keelim-Knowledge-Vault (LLM 위키 — LIGHT)

**현재 상태**: Obsidian형 위키, 13 도메인 허브 + ops/schema. Layer 분리(raw/wiki/schema), 네비 계약(도메인 허브 `index.md`, 루트 `Index.md`, `log.md` append-only, `schema/`). 진입점: `Index.md`, `ops/domain-map.md`, `log.md`.

| Feature | Type | Concrete entry point | Effort | Impact | Blockers/deps |
| --- | --- | --- | --- | --- | --- |
| 프로젝트-노트 백링크 허브 | new | 신규 `projects/keelim-maestro.md` — 각 repo → 아키텍처/운영/결정 노트 + 코드맵 하이라이트 + 루트 idea index/automation memory 역링크 | S | 워크스페이스가 활성 표면에서 vault 노트를 발견 못함 → 재진입 비용 감소 | 수동 링크 큐레이션 + 동기 코드맵/idea |
| 주간 stale 노트 리서페이서 | new | `ops/` 스크립트 — `log.md`에서 30일+ 미변경 고가치 노트 필터 → 주간 요약 노트 | S | 묻힌 고가치 노트를 활성 작업에 재진입 | 스케줄러; 일관된 `log.md` 타임스탬프 |

**Operational blockers**: 루트 loose 노트 30+ 중 `ops/domain-map.md`가 ~18만 커버 → orphan; 코드맵 스냅샷 보존 메커니즘 부재; 일일 다이제스트 부재. (bespoke — 로그 규율/수동 큐레이션 의존, 코드 통합 아님)

---

## 9. 교차 프로젝트 우선순위 로드맵

영향/노력만이 아니라 **운영 블로커가 착수 가능 시점을 강제**한다는 점을 반영한 웨이브 구성.

### Wave 0 — 언블록 (먼저, 모두 S–M)
1. `rich` 더티 트리 커밋 + freeze/split 결정 (S) — rich 스키마 작업 게이트
2. `rich` in-process APScheduler 도입 (M) — 3개 rich 기능 공통 선결
3. `keelim-vercel` 더티 트리 커밋 (S)
4. `toto`·`android-support` 서브모듈 포인터 핀 정렬 (S) — 가벼운 housekeeping(빈 클론 아님). 해당 repo 기능 착수 전 정렬 권장이나 임계 경로는 아님

### Wave 1 — 빠른 승리 (코드 준비된 S, 즉시 가치)
- `keelim-vercel`: 메뉴 배지 예산(S), 스토리지 레지스트리 드리프트 게이트(S)
- `all-web-ui`: 다운스트림 사용 매트릭스(S)
- `rich`: 통합 헬스 콘솔(S)
- `android-support`: 액션 계약 드리프트 검사(S)
- `toto`: 읽기전용 스모크 게이트(S, 핀 이후)
- `keelim-plugin`: 생성형 스킬 카탈로그(S)
- `vault`: 프로젝트-노트 백링크 허브(S)

### Wave 2 — 중간 빌드 (M, Wave 0/1 위에)
- `keelim-vercel`: 도구 사용 히트맵(M), 라우트 계약 드리프트(M)
- `rich`: 데이터 신선도 워치독(S–M), 일일 리뷰 콕핏(M), 데이터포털 변경 피드(M)
- `all`: 공유 모듈 채택 맵(M), 피처 플래그 레지스트리(M), 릴리스 레디니스 레이더(M)
- `all-web-ui`: 시각 회귀 + a11y 게이트(M)
- `android-support`: 프리플라이트 검증(M)
- `toto`: 시즌 스냅샷 매니페스트(M), 공급자 어댑터(M)
- `keelim-plugin`: 스모크 테스트 하네스(S); `vault`: 주간 리서페이서(S)

### Wave 3 — 깊은 투자 (L 또는 신규 제품 표면)
- `keelim-vercel`: Next-best-action 피드(M–L, 신규 제품 가치)
- `rich`: 실행 원장(L), 복구 콕핏(L)
- `all`: 빌드 병목 열지도 + CI 분할(M), KMP/iOS/Rust 플랫폼 게이트(M), 컨벤션 드리프트 대시보드(L)
- `all-web-ui`: 토큰 플레이그라운드(M)

**제품 vs 신뢰성 균형**: Wave 1–2는 백로그의 신뢰성/드리프트 편향을 빠르게 소진하고, Wave 3의 `keelim-vercel` Next-best-action 피드가 유일하게 큰 신규 *사용자* 표면이다. 사용자 가치 우선순위가 높다면 이 항목을 Wave 2로 끌어올리는 것을 권장.

---

## 외부 리서치 소스

1. [Gradle Performance docs](https://docs.gradle.org/current/userguide/performance.html) — 빌드 베이스라인·`--parallel`
2. [gradle-profiler](https://github.com/gradle/gradle-profiler) — 빌드 벤치마킹 도구
3. [Develocity build observability](https://gradle.com/blog/optimize-your-gradle-and-maven-builds-with-resource-usage-data/) — 리소스 사용 기반 최적화
4. [Chromatic for Storybook](https://www.chromatic.com/storybook) / [Storybook+Chromatic VRT](https://bug0.com/knowledge-base/storybook-visual-regression-testing-chromatic) — 컴포넌트 시각 회귀
5. [Accessibility in Design Systems](https://a11ypros.com/blog/accessibility-in-design-systems) — axe-core CI 게이트
6. [FastAPI Scheduling guide](https://medium.com/@rasifrazak123/fastapi-scheduling-background-tasks-backgroundtasks-vs-apscheduler-vs-celery-complete-guide-ff90d6be524b) / [APScheduler+FastAPI](https://ahaw021.medium.com/scheduled-jobs-with-fastapi-and-apscheduler-5a4c50580b0e)
7. [Transactional Outbox – AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) / [Event Sourcing+CQRS with FastAPI/Celery](https://dev.to/markoulis/how-i-learned-to-stop-worrying-and-love-raw-events-event-sourcing-cqrs-with-fastapi-and-celery-477e)
8. [r0adkll/upload-google-play](https://github.com/r0adkll/upload-google-play) + [action.yml](https://github.com/r0adkll/upload-google-play/blob/master/action.yml) — Play 업로드 레퍼런스·함정

## Methodology

- **코드 그라운딩**: 3개 Explore 에이전트가 8개 repo를 병렬 조사, 통일 스키마(Feature | Type | Concrete entry point | Effort | Impact | Blockers)로 반환. 모든 기능 후보는 실제 파일/함수 진입점에 묶임.
- **외부 리서치**: 활성·비-bespoke 스택(Gradle/KMP, 디자인 시스템, FastAPI 관측성, Play Action)에 한해 4개 타깃 WebSearch. bespoke 개인 도구(toto/keelim-plugin/vault)는 비교군 부재로 일반론 주입을 의도적으로 회피.
- **로드맵**: 교차 프로젝트 랭킹은 단일 합성 단계에서 수행(서브에이전트는 각자 한 슬라이스만 보므로 불가). 운영 블로커를 선행 게이트로 명시.
- **한계**: Supabase 테이블 스키마, CI 러너 toolchain 가용성, 시드 결정성은 코드만으로 미확정 — 해당 기능 착수 전 검증 필요.
