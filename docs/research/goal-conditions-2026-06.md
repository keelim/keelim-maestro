# `/goal` 실행용 atomic 조건 카탈로그

*Source: `docs/research/feature-enhancement-research-2026-06.md` · Target: Claude Code `/goal` (v2.1.139+) · Generated: 2026-06-04*

## 사용법

`/goal`은 **단일 자연어 완료 조건**을 받아 충족까지 자율 반복하는 기능이다(파일/배치 로드 불가, 세션 스코프). 이 카탈로그의 각 항목은 그대로 붙여넣어 실행할 1개의 `/goal` 조건이다.

- **실행 순서**: Preconditions(수동) → Wave 1 → 2 → 3. `depends`가 있으면 선행 항목을 먼저 완료한다.
- **한 번에 하나씩**: `/goal <조건>` 붙여넣기 → 완료되면 `/goal clear` 후 다음 항목. 또는 `claude -p "/goal <조건>"`로 순차 스크립트.
- **체크 명령 주의**: 각 조건의 `verify:` 명령은 해당 repo에 실재하는 스크립트를 기준으로 한다. repo의 실제 script 명이 다르면 첫 실행 시 조정하라(자율 루프가 존재하지 않는 명령을 영원히 재시도하지 않도록).
- **안전절**: 모든 조건에 `or stop after N turns`를 넣어 평가가 수렴하지 않을 때 멈춘다.

조건 1줄 포맷: `<측정가능한 end-state> ; verify: \`<command>\` exits 0 ; constraints: <유지 불변식> ; or stop after <N> turns`

---

## Preconditions (실행 전 수동 처리 — `/goal` 아님)

사람 판단/위험 영역이라 자율 goal로 돌리지 않는다. 아래를 먼저 손으로 처리한 뒤 Wave 1을 시작한다.

- **P1 · rich 더티 트리 + freeze/split 결정**: `rich`의 더티 변경(`docs/words/*.md`, `web/tsconfig.tsbuildinfo`)을 직접 검토해 커밋/스태시하고, "freeze vs split" 아키텍처 결정을 내린다. (자동 커밋 금지 — 미완성 변경 위험.)
- **P2 · keelim-vercel 더티 트리 정리**: `keelim-vercel` 더티 변경을 검토 후 커밋.
- **P3 · toto 서브모듈 핀 대상 선택·정렬**: 인덱스(`5897ef44`)↔체크아웃(`b94974b4`) 중 의도한 커밋을 골라 `git add toto` 정렬. (게이트링크는 이미 커밋됨 — 대상 선택이 사람 판단.)
- **P4 · android-support 서브모듈 핀 대상 선택·정렬**: 인덱스(`485a2e40`)↔체크아웃(`06843399`) 정렬.

---

## Wave 0 — 자동화 가능한 선결 (공통 의존)

### W0-rich-01 — rich in-process APScheduler 스캐폴드
**`/goal`**: `rich 백엔드에 in-process APScheduler 스케줄러 계층을 추가해 주기 작업 등록 진입점(app/services/scheduler.py)을 만들고, FastAPI lifespan에서 start/shutdown 되게 배선하며, 더미 주기 잡 1개와 그 등록 테스트를 통과시킨다 ; verify: `cd rich && uv run pytest tests/test_scheduler.py` exits 0 ; constraints: 기존 라우트/서비스 동작 불변, APScheduler 외 새 의존성 금지, 더미 잡은 부작용 없음 ; or stop after 18 turns`
- **진입점**: `rich/app/main.py`(lifespan), 신규 `rich/app/services/scheduler.py`, 신규 `rich/tests/test_scheduler.py`
- **수용 체크리스트**:
  - [ ] `scheduler.py`에 AsyncIOScheduler 싱글턴 + `register_job(func, trigger)` 래퍼
  - [ ] FastAPI lifespan에서 `start()`/`shutdown()` 호출
  - [ ] 더미 주기 잡 등록 + 등록 여부 단언 테스트
  - [ ] APScheduler를 `pyproject.toml` 의존성에 추가
- **depends**: P1
- *(공통 선결: W2-rich-01, W2-rich-03, W3-rich-01이 이 계층에 의존)*

---

## Wave 1 — 빠른 승리 (S, 코드 준비 완료)

### W1-vercel-01 — 메뉴 배지 예산 게이트
**`/goal`**: `keelim-vercel lib/menu-config.ts의 isNew:true 항목이 4개를 초과하면 비0으로 종료하는 검사 스크립트를 추가하고, lib/changelog-data.ts 날짜와 대조해 오래된 배지를 리포트한다 ; verify: `cd keelim-vercel && bun run typecheck && node scripts/check-badge-budget.mjs` exits 0 ; constraints: menu-config.ts의 실제 isNew 값은 변경하지 않음(검사만 추가), 기존 lint/build 통과 유지 ; or stop after 12 turns`
- **진입점**: `keelim-vercel/lib/menu-config.ts`, `lib/changelog-data.ts`, `app/changelog/page.tsx`; 신규 `scripts/check-badge-budget.mjs`
- **수용 체크리스트**:
  - [ ] `isNew:true` 항목 추출 + 카운트
  - [ ] 4 초과 시 비0 종료, 목록 출력
  - [ ] changelog 날짜와 대조해 stale 배지 표시
  - [ ] `package.json` 스크립트 등록
- **depends**: P2

### W1-vercel-02 — 스토리지 키 레지스트리 드리프트 게이트
**`/goal`**: `keelim-vercel의 lib/*storage*.ts에 선언된 STORAGE_KEY 상수 목록과 lib/storage-version-registry.ts 등록 목록을 대조해, 누락·불일치·stale 마이그레이션을 비0으로 리포트하는 검사 스크립트를 추가한다 ; verify: `cd keelim-vercel && bun run typecheck && node scripts/check-storage-registry.mjs` exits 0 ; constraints: 실제 저장 키/마이그레이션 정의는 변경하지 않음, 검사 스크립트만 추가 ; or stop after 14 turns`
- **진입점**: `keelim-vercel/lib/storage-version-registry.ts`, `lib/*storage*.ts`, `lib/storage-versioning.ts`; 신규 `scripts/check-storage-registry.mjs`
- **수용 체크리스트**:
  - [ ] `lib/*storage*.ts`에서 키 상수 추출(정규식/AST)
  - [ ] registry 배열과 양방향 diff
  - [ ] 누락/잉여/stale 마이그레이션 분류 출력
  - [ ] 불일치 시 비0 종료, `package.json` 등록
- **depends**: P2

### W1-webui-01 — 다운스트림 사용 매트릭스
**`/goal`**: `all-web-ui의 src/manifest.ts 컴포넌트 목록과, keelim-vercel·rich/web의 @keelim/all-web-ui import 지점을 교차해 (컴포넌트 × 소비자 × 사용수) 매트릭스 JSON을 생성하는 스크립트를 추가한다 ; verify: `cd all-web-ui && bun run build && node scripts/usage-matrix.mjs --check` exits 0 ; constraints: 컴포넌트 export/소스 변경 금지(분석만), 결과는 dist 또는 docs에 JSON으로 출력 ; or stop after 16 turns`
- **진입점**: `all-web-ui/src/manifest.ts`, `src/index.ts`; (read) `keelim-vercel`, `rich/web` import; 신규 `all-web-ui/scripts/usage-matrix.mjs`
- **수용 체크리스트**:
  - [ ] manifest에서 export 컴포넌트 목록 파싱
  - [ ] 소비자 repo import grep(경로 인자화)
  - [ ] 매트릭스 JSON 생성
  - [ ] `--check` 모드에서 manifest에 없는 export 사용 시 비0
- **depends**: —

### W1-rich-01 — 통합 헬스 콘솔
**`/goal`**: `rich에 /api/admin/integrations/health 엔드포인트와 app/services/integration_health.py를 추가해 Supabase·KRX 로그인·GitHub 토큰·PyKRX last-run의 상태를 집계 반환하고, 각 통합의 last-success/repair 힌트를 포함시킨다 ; verify: `cd rich && uv run pytest tests/test_integration_health.py` exits 0 ; constraints: 외부 호출은 모킹된 테스트로 검증, 기존 라우트 불변, 비밀값 로깅 금지 ; or stop after 18 turns`
- **진입점**: 신규 `rich/app/services/integration_health.py`, `rich/app/api/...`(admin 라우터), 신규 `rich/tests/test_integration_health.py`
- **수용 체크리스트**:
  - [ ] 통합별 status 체크 함수(주입 가능한 클라이언트)
  - [ ] 집계 응답 모델(last_success, reconnect_state, repair_hint)
  - [ ] `/api/admin/integrations/health` 라우트
  - [ ] 모킹 기반 단위 테스트
- **depends**: P1

### W1-android-01 — 액션 계약 드리프트 검사
**`/goal`**: `android-support에 action.yml의 inputs/outputs, src/main.ts의 파라미터 사용, README.md 입력 표를 대조해 불일치 시 비0으로 종료하는 CI 검사 scripts/check-contract-drift.ts를 추가한다 ; verify: `cd android-support && npm run build && npx ts-node scripts/check-contract-drift.ts` exits 0 ; constraints: action.yml/소스 인터페이스 변경 금지(검사만), lib/index.js 빌드 전에 실행 가능해야 함 ; or stop after 14 turns`
- **진입점**: `android-support/action.yml`, `src/main.ts`, `README.md`; 신규 `scripts/check-contract-drift.ts`
- **수용 체크리스트**:
  - [ ] action.yml inputs/outputs 파싱(YAML)
  - [ ] main.ts에서 참조되는 입력 추출
  - [ ] README 입력 표 파싱
  - [ ] 3자 비교 후 불일치 비0 종료
- **depends**: P4

### W1-toto-01 — 읽기전용 스모크 게이트
**`/goal`**: `toto에 앱 부팅·Home import·verify 흐름을 묶고 실행 중 SQLite 파일이 변경되지 않음을 단언하는 읽기전용 스모크 테스트를 추가하고, verify 스크립트에 포함시킨다 ; verify: `cd toto && bun run verify` exits 0 ; constraints: 쓰기 경로/시드 로직 변경 금지, 테스트는 부작용 0 ; or stop after 12 turns`
- **진입점**: 신규 `toto/tests/test_smoke_readonly.py`; `toto/streamlit_app/Home.py`, `src/kbo_dashboard/bootstrap.py`; `package.json` verify
- **수용 체크리스트**:
  - [ ] Home import + `get_repository()` 부팅
  - [ ] 실행 전후 `.data/dashboard.sqlite3` mtime/해시 동일 단언
  - [ ] 경로 드리프트 시 실패
  - [ ] `bun run verify`에 연결
- **depends**: P3

### W1-plugin-01 — 생성형 스킬 카탈로그
**`/goal`**: `keelim-plugin에서 skills/*/SKILL.md 메타(name·description)를 파싱해 태그·설치 명령(CLI/symlink) 매트릭스가 포함된 카탈로그(CATALOG.md 또는 catalog.json)를 생성하는 스크립트를 추가하고, README 목록과의 불일치를 비0으로 표시한다 ; verify: `cd keelim-plugin && node scripts/gen-catalog.mjs --check` exits 0 ; constraints: SKILL.md 내용 변경 금지(읽기·생성만) ; or stop after 14 turns`
- **진입점**: `keelim-plugin/skills/*/SKILL.md`, `README.md`; 신규 `scripts/gen-catalog.mjs`
- **수용 체크리스트**:
  - [ ] 각 SKILL.md frontmatter/헤더 파싱
  - [ ] 설치 명령 매트릭스(CLI vs symlink) 구성
  - [ ] 카탈로그 산출(MD/JSON)
  - [ ] `--check`에서 README와 폴더 불일치 시 비0
- **depends**: —

### W1-vault-01 — 프로젝트-노트 백링크 허브
**`/goal`**: `Keelim-Knowledge-Vault에 projects/keelim-maestro.md 노트를 만들어 각 repo를 핵심 아키텍처/운영/결정 노트·코드맵 하이라이트·루트 idea index로 연결하고, Index.md에서 링크되게 한다 ; verify: `cd Keelim-Knowledge-Vault && bash scripts/check-backlinks.sh` exits 0 ; constraints: 기존 노트 내용 변경 최소화(허브 노트·인덱스 링크만 추가), 모든 링크는 존재하는 파일 대상 ; or stop after 14 turns`
- **진입점**: 신규 `Keelim-Knowledge-Vault/projects/keelim-maestro.md`, `Index.md`, `ops/domain-map.md`; 신규 `scripts/check-backlinks.sh`
- **수용 체크리스트**:
  - [ ] repo→노트 매핑 허브 노트 작성
  - [ ] `Index.md`에서 허브로 링크
  - [ ] 링크 유효성 검사 스크립트(깨진 링크 비0)
  - [ ] 루트 idea index 역링크
- **depends**: —

---

## Wave 2 — 중간 빌드 (M)

### W2-vercel-01 — 도구 사용 히트맵 & 데드 표면 리포트
**`/goal`**: `keelim-vercel에서 Supabase tool_clicks를 집계해 도구를 entry/view/complete 기준으로 랭크하고 장기 미사용 라우트를 통합 후보로 표시하는 주간 리포트 생성기를 추가한다 ; verify: `cd keelim-vercel && bun run typecheck && node scripts/tool-usage-report.mjs --dry-run` exits 0 ; constraints: 운영 데이터 쓰기 금지(읽기 집계만), 자격증명은 env로만 ; or stop after 18 turns`
- **진입점**: `keelim-vercel/lib/ranking-actions.ts`, `lib/tool-tracking.ts`, `lib/menu-config.ts`; 신규 `scripts/tool-usage-report.mjs`
- **수용 체크리스트**:
  - [ ] tool_clicks 집계 쿼리(이벤트 타입별)
  - [ ] menu-config 인벤토리와 조인해 미사용 라우트 식별
  - [ ] 랭킹 + 통합 후보 리포트 출력
  - [ ] `--dry-run`은 네트워크 없이 스키마/쿼리 검증
- **depends**: W1-vercel-01

### W2-vercel-02 — 라우트 계약 드리프트 리포트
**`/goal`**: `keelim-vercel에서 (dashboard) 네비/메뉴 항목, app/api 엔드포인트, app/sitemap.ts·robots.ts 출력을 대조해 stale 라우트·누락 네비·미문서 API를 리포트하는 스크립트를 추가한다 ; verify: `cd keelim-vercel && bun run typecheck && node scripts/route-drift-report.mjs` exits 0 ; constraints: 라우트/네비 정의 변경 금지(분석만) ; or stop after 18 turns`
- **진입점**: `keelim-vercel/app/(dashboard)/layout.tsx`, `lib/menu-config.ts`, `app/api/`, `app/sitemap.ts`, `app/robots.ts`; 신규 `scripts/route-drift-report.mjs`
- **수용 체크리스트**:
  - [ ] 실제 라우트 트리 수집(app 디렉터리 스캔)
  - [ ] 메뉴/네비 항목 수집
  - [ ] sitemap/robots 커버리지 대조
  - [ ] orphan/누락/미문서 분류 출력
- **depends**: —

### W2-rich-01 — 데이터 신선도 워치독
**`/goal`**: `rich에 app/services/freshness_monitor.py와 /api/admin/freshness/status를 추가해 테이블별 stale 임계·PyKRX 캐시 age·KRX last-fetch를 점검하고, W0의 스케줄러로 주기 등록한다 ; verify: `cd rich && uv run pytest tests/test_freshness_monitor.py` exits 0 ; constraints: 외부 호출 모킹 검증, 임계값은 설정으로 분리, 기존 동작 불변 ; or stop after 18 turns`
- **진입점**: 신규 `rich/app/services/freshness_monitor.py`, admin 라우트; `rich/app/services/scheduler.py`(W0); 신규 테스트
- **수용 체크리스트**:
  - [ ] 소스별 신선도 임계 설정
  - [ ] stale 판정 + 사유 반환
  - [ ] `/api/admin/freshness/status` 라우트
  - [ ] 스케줄러 주기 등록 + 테스트
- **depends**: W0-rich-01

### W2-rich-02 — 일일 리뷰 콕핏
**`/goal`**: `rich/web에 agenda·inbox·PyKRX fear-greed·주간리뷰 carry-over·저널 링크를 한 페이지로 모으는 일일 리뷰 뷰를 추가하고, web/src/lib/api.ts에 통합 조회 계약을 정의한다 ; verify: `cd rich/web && bun run typecheck && bun run build` exits 0 ; constraints: 기존 admin API 계약 불변(집계만), 신규 페이지는 기존 라우팅에 추가 ; or stop after 20 turns`
- **진입점**: `rich/web/src/lib/api.ts`, 신규 `rich/web/app/.../daily-review/page.tsx`; 기존 `/api/admin/weekly-review/summary`, `/api/admin/pykrx/fear-greed`
- **수용 체크리스트**:
  - [ ] api.ts 통합 조회 타입/함수
  - [ ] 일일 리뷰 페이지 컴포넌트
  - [ ] 섹션별 카드(agenda/inbox/fear-greed/carry-over)
  - [ ] typecheck/build 통과
- **depends**: —

### W2-rich-03 — 공공데이터 카탈로그 변경 피드
**`/goal`**: `rich에서 krx_data_portal_client의 카탈로그 export를 주기 diff해 title/field/link 변경을 Supabase data_portal_changes에 적재하고 /api/admin/data-portal/changes로 노출하며, W0 스케줄러로 등록한다 ; verify: `cd rich && uv run pytest tests/test_data_portal_changes.py` exits 0 ; constraints: 외부 호출 모킹, diff는 결정적, 기존 client 동작 불변 ; or stop after 20 turns`
- **진입점**: `rich/app/services/krx_data_portal_client.py`, 신규 diff 서비스+라우트, 스케줄러(W0), 신규 테스트
- **수용 체크리스트**:
  - [ ] 카탈로그 fetch 로직 추출(테스트 가능화)
  - [ ] 이전 스냅샷 대비 diff(추가/삭제/변경)
  - [ ] Supabase 적재 + 엔드포인트
  - [ ] 스케줄러 등록 + 모킹 테스트
- **depends**: W0-rich-01

### W2-all-01 — 공유 모듈 채택 맵
**`/goal`**: `all에서 settings.gradle.kts와 gradle/libs.versions.toml, 모듈 의존을 파싱해 (앱 × 모듈) 채택 매트릭스와 중복 후보 랭킹을 생성하는 Gradle task 또는 스크립트를 추가한다 ; verify: `cd all && ./gradlew adoptionMap` exits 0 ; constraints: 모듈 빌드 설정 변경 금지(읽기 분석만), 결과는 build/reports에 출력 ; or stop after 18 turns`
- **진입점**: `all/settings.gradle.kts`, `gradle/libs.versions.toml`, `build-logic/convention/`; 신규 task/스크립트
- **수용 체크리스트**:
  - [ ] subprojects 의존 그래프 수집
  - [ ] 앱×모듈 채택 매트릭스
  - [ ] 중복 흐름/유틸 랭킹
  - [ ] 리포트 산출 + task 등록
- **depends**: —

### W2-all-02 — 크로스앱 피처 플래그 레지스트리
**`/goal`**: `all에 공유 피처 플래그 스키마(core:data-api)와 DataStore 기반 캐시/repository(core:data)를 추가하고, feature:ui-setting에 플래그 토글 화면을 한 앱에서 노출한다 ; verify: `cd all && ./gradlew :core:data:test :feature:ui-setting:test` exits 0 ; constraints: 기존 Hilt/DataStore 패턴 준수, 다른 앱 모듈 변경 금지 ; or stop after 22 turns`
- **진입점**: `all/core/data-api`, `core/data`, `feature/ui-setting`
- **수용 체크리스트**:
  - [ ] 플래그 스키마 정의(data-api)
  - [ ] DataStore 캐시 + repository(data)
  - [ ] 토글 화면(ui-setting)
  - [ ] 단위 테스트
- **depends**: —

### W2-all-03 — 릴리스 레디니스 레이더
**`/goal`**: `all에서 앱별 build.gradle.kts의 versionCode/Name, .github/workflows 상태, Release-Note를 모아 릴리스 드리프트 리포트를 생성하는 task를 추가한다 ; verify: `cd all && ./gradlew releaseRadar` exits 0 ; constraints: 버전/워크플로 변경 금지(수집만), 리포트는 build/reports ; or stop after 18 turns`
- **진입점**: `all/**/build.gradle.kts`, `.github/workflows/*.yml`, `docs/topics/Release-Note.md`; 신규 task
- **수용 체크리스트**:
  - [ ] 앱별 버전 수집
  - [ ] 워크플로/릴리스 상태 파싱
  - [ ] changelog 누락 탐지
  - [ ] 통합 리포트 + task
- **depends**: —

### W2-webui-01 — 시각 회귀 + 접근성 게이트
**`/goal`**: `all-web-ui에 export 프리미티브의 테마별 스냅샷 테스트와 axe-core 접근성 검사를 추가하고 CI에서 실행되게 한다 ; verify: `cd all-web-ui && bun run test:visual` exits 0 ; constraints: 컴포넌트 구현 변경 금지(테스트·베이스라인만 추가), 두 테마(admin-bw/finance) 모두 커버 ; or stop after 20 turns`
- **진입점**: `all-web-ui/src/index.ts`, `src/styles/themes/*`; 신규 `tests/visual-*.test.ts`, CI 설정
- **수용 체크리스트**:
  - [ ] 프리미티브 렌더 + 테마별 스냅샷
  - [ ] axe-core 접근성 검사
  - [ ] 베이스라인 생성
  - [ ] `test:visual` 스크립트 + CI 연결
- **depends**: —

### W2-android-01 — 릴리스 프리플라이트 검증(dry-run)
**`/goal`**: `android-support에 dryRun 입력과 src/preflight.ts를 추가해 아티팩트 존재·패키지 메타·auth·track/status 조합을 Play API 호출 없이 검증하고 리포트를 출력한다 ; verify: `cd android-support && npm run build && npm test` exits 0 ; constraints: 기존 input-validation 로직 재사용(중복 금지), dryRun에서 어떤 Play API mutation도 호출 금지 ; or stop after 18 turns`
- **진입점**: `android-support/action.yml`, `src/main.ts`, `src/input-validation.ts`; 신규 `src/preflight.ts`, 테스트
- **수용 체크리스트**:
  - [ ] `dryRun` 입력 추가 + 분기
  - [ ] 아티팩트/메타/auth/track-status 검증
  - [ ] 검증 리포트 출력
  - [ ] dry-run에서 Play API 미호출 테스트
- **depends**: W1-android-01

### W2-toto-01 — 시즌 스냅샷 매니페스트
**`/goal`**: `toto에 시즌별 원본·행수·sha256·기대 요약을 기록한 manifest.json을 만들고, 시드 함수가 이를 생성/검증하며 재시드 시 행수·해시 불일치를 테스트로 잡게 한다 ; verify: `cd toto && bun run verify` exits 0 ; constraints: 시드 결정성 보장(픽스처/핀), UI 변경 금지 ; or stop after 18 turns`
- **진입점**: 신규 `toto/manifest.json`, `src/kbo_dashboard/bootstrap.py`(seed), `tests/test_repository.py`
- **수용 체크리스트**:
  - [ ] manifest 스키마(season/source/row_count/sha256/expected)
  - [ ] seed가 manifest 생성·대조
  - [ ] 재시드 diff 테스트
  - [ ] verify에 연결
- **depends**: W1-toto-01

### W2-toto-02 — 데이터 공급자 어댑터 분리
**`/goal`**: `toto에서 repository의 인라인 시드 로직을 GameResultProvider·RankingProvider Protocol 뒤로 추출하고, Home.py가 repository 인터페이스만 호출하도록 리팩터하며 로컬 픽스처 provider 구현을 추가한다 ; verify: `cd toto && bun run verify` exits 0 ; constraints: UI 계약(DTO) 불변, 동작 동일(스냅샷 매니페스트 통과 유지) ; or stop after 20 turns`
- **진입점**: `toto/src/kbo_dashboard/repository.py`, `contracts.py`, `streamlit_app/Home.py`; 신규 provider 모듈
- **수용 체크리스트**:
  - [ ] Provider Protocol 정의
  - [ ] `_LocalFixtureProvider` 추출
  - [ ] Home.py가 repository만 호출
  - [ ] 기존 테스트/매니페스트 통과
- **depends**: W2-toto-01

### W2-plugin-01 — 스킬 스모크 테스트 하네스
**`/goal`**: `keelim-plugin에 각 skills/*가 필수 파일·설치 명령·에이전트 메타를 갖췄는지 검증하고 Codex/Claude 설치 패리티 갭을 표시하는 verifier를 추가한다 ; verify: `cd keelim-plugin && bash scripts/verify-skills.sh` exits 0 ; constraints: 스킬 내용 변경 금지(검증만), 누락 시 비0 ; or stop after 16 turns`
- **진입점**: `keelim-plugin/skills/*/SKILL.md`, `agents/openai.yaml`, `README.md`; 신규 `scripts/verify-skills.sh`
- **수용 체크리스트**:
  - [ ] 스킬별 필수 파일 존재 확인
  - [ ] README 설치 명령 ↔ 폴더 구조 대조
  - [ ] Codex/Claude 메타 패리티 점검
  - [ ] 갭 비0 종료
- **depends**: W1-plugin-01

### W2-vault-01 — 주간 stale 노트 리서페이서
**`/goal`**: `Keelim-Knowledge-Vault의 ops/에 log.md 기준 30일+ 미변경 고가치 노트를 골라 주간 요약 노트를 생성하는 스크립트를 추가한다 ; verify: `cd Keelim-Knowledge-Vault && bash scripts/resurface.sh --check` exits 0 ; constraints: 기존 노트 변경 금지(요약 노트만 생성), 모든 링크 유효 ; or stop after 14 turns`
- **진입점**: `Keelim-Knowledge-Vault/log.md`, `ops/`; 신규 `scripts/resurface.sh`
- **수용 체크리스트**:
  - [ ] log.md 타임스탬프 파싱
  - [ ] 30일+ 미변경 + 활성 repo 연관 필터
  - [ ] 주간 요약 노트 생성
  - [ ] 링크 유효성 통과
- **depends**: W1-vault-01

---

## Wave 3 — 깊은 투자 (L / 신규 제품 표면)

### W3-vercel-01 — Next-best-action 피드
**`/goal`**: `keelim-vercel에 최근 도구 히스토리·즐겨찾기·목표 체크인 신호로 다음 워크플로/목표 카드를 추천하는 룰기반 패널을 /next-action 또는 dashboard에 추가한다 ; verify: `cd keelim-vercel && bun run typecheck && bun run test` exits 0 ; constraints: 1차는 룰기반(LLM 호출 없음), 기존 저장 키 계약 준수, 추천 로직 단위 테스트 ; or stop after 24 turns`
- **진입점**: `keelim-vercel/lib/tool-tracking.ts`, `lib/favorite-tools-storage.ts`, `lib/household-goal-checkin-storage.ts`; 신규 추천 모듈 + 패널 + 라우트
- **수용 체크리스트**:
  - [ ] 최근 시퀀스/북마크/체크인 신호 수집
  - [ ] 룰기반 스코어링 + 추천 선정
  - [ ] 추천 패널 UI
  - [ ] 스코어링 단위 테스트
- **depends**: W2-vercel-01

### W3-rich-01 — 실행 원장 + 리플레이 타임라인
**`/goal`**: `rich에 append-only execution_events 테이블과 execution_ledger 서비스를 추가해 모든 run/retry/failure를 정규화 적재하고 /api/admin/executions로 타임라인을 노출하며, 기존 서비스 호출을 계측한다 ; verify: `cd rich && uv run pytest tests/test_execution_ledger.py` exits 0 ; constraints: append-only(이벤트 불변), 마이그레이션 포함, 외부 호출 모킹, 기존 동작 불변 ; or stop after 24 turns`
- **진입점**: 신규 `rich/app/services/execution_ledger.py`, alembic 마이그레이션, admin 라우트, 기존 에러 핸들러 계측; 스케줄러(W0)
- **수용 체크리스트**:
  - [ ] `execution_events` 스키마/마이그레이션
  - [ ] 이벤트 emit 헬퍼 + 서비스 계측 포인트
  - [ ] `/api/admin/executions` 타임라인
  - [ ] 인덱스 폴링 쿼리 + 테스트
- **depends**: W0-rich-01

### W3-rich-02 — 실패 run 복구 콕핏
**`/goal`**: `rich에 failed_runs 적재와 app/services/recovery.py(실패유형별 remediation)·/api/admin/recovery/queue를 추가하고, 각 항목을 영향 워크플로에 링크한다 ; verify: `cd rich && uv run pytest tests/test_recovery.py` exits 0 ; constraints: remediation은 명시적 트리거만(자동 실행 금지), execution_ledger 컨텍스트 재사용, 외부 호출 모킹 ; or stop after 24 turns`
- **진입점**: 신규 `rich/app/services/recovery.py`, 라우트; `execution_ledger`(W3-rich-01), 에러 핸들러
- **수용 체크리스트**:
  - [ ] `failed_runs` 적재(에러 핸들러 연계)
  - [ ] 실패유형별 remediation 정의
  - [ ] 복구 큐 엔드포인트 + 워크플로 링크
  - [ ] 상태 머신 단위 테스트
- **depends**: W3-rich-01

### W3-all-01 — 빌드 병목 열지도 + CI 분할 계획기
**`/goal`**: `all의 ci.yml Gradle 호출에 task 타이밍 계측을 추가하고, 수집된 시간으로 앱·모듈 병목 열지도와 분할/병렬화 후보를 생성하는 리포트를 만든다 ; verify: `cd all && ./gradlew buildBottleneckReport` exits 0 ; constraints: 빌드 산출물/캐시 동작 불변, 계측은 비침습적, 리포트는 build/reports ; or stop after 20 turns`
- **진입점**: `all/.github/workflows/ci.yml`, `build-logic/convention/`; 신규 리포트 task
- **수용 체크리스트**:
  - [ ] task 타이밍 수집(`--profile` 또는 build scan)
  - [ ] 앱/모듈별 집계 열지도
  - [ ] 분할/병렬화 후보 제안
  - [ ] task 등록
- **depends**: W2-all-01

### W3-all-02 — KMP/iOS/Rust 플랫폼 빌드 게이트
**`/goal`**: `all의 ci.yml에 iOS Xcode 빌드(allIos)·Cargo check(all-rust-lib)·Compose Multiplatform(composeApp) 최소 실행 스텝을 추가하고 플랫폼별 성공/실패를 PR 요약 표로 모은다 ; verify: `cd all && cargo check --manifest-path all-rust-lib/Cargo.toml && ./gradlew :composeApp:assemble` exits 0 ; constraints: Android 빌드 동작 불변, iOS 스텝은 러너 가용성에 따라 조건부, 시크릿 노출 금지 ; or stop after 22 turns`
- **진입점**: `all/.github/workflows/ci.yml`, `allIos/`, `all-rust-lib/Cargo.toml`, `composeApp/build.gradle.kts`
- **수용 체크리스트**:
  - [ ] Cargo check 스텝
  - [ ] Compose MP 최소 빌드 스텝
  - [ ] iOS Xcode 빌드(조건부) 스텝
  - [ ] PR 요약 표 집계
- **depends**: —

### W3-all-03 — 컨벤션 드리프트 대시보드
**`/goal`**: `all에서 모듈별 AGENTS.md 규칙(날짜/통화 포맷·typed navigation·repository 경계)을 인덱싱하고 core/*·feature/* 소스에서 위반 후보를 스캔하는 리포트 task를 추가한다 ; verify: `cd all && ./gradlew conventionDriftReport` exits 0 ; constraints: 소스 변경 금지(스캔만), 위반은 경고로 분류 출력 ; or stop after 22 turns`
- **진입점**: `all/**/AGENTS.md`, `core/*`, `feature/*`; 신규 리포트 task
- **수용 체크리스트**:
  - [ ] AGENTS.md 규칙 인덱싱
  - [ ] 위반 탐지 패턴(포맷/네비/경계)
  - [ ] 영향 모듈 매핑
  - [ ] 리포트 + task
- **depends**: —

### W3-webui-01 — 토큰 플레이그라운드 & 테마 diff 랩
**`/goal`**: `all-web-ui에 각 프리미티브를 두 테마로 병렬 렌더하고 토큰 델타를 강조하는 데모/문서 페이지를 추가한다 ; verify: `cd all-web-ui && bun run build` exits 0 ; constraints: 컴포넌트 구현 변경 금지(데모 추가만), 토큰 변수는 src/lib/cn.ts 사용 ; or stop after 20 turns`
- **진입점**: 신규 `all-web-ui/src/docs/theme-lab.tsx`; `src/lib/cn.ts`, `src/styles/themes/*`
- **수용 체크리스트**:
  - [ ] 프리미티브 카탈로그 렌더
  - [ ] admin-bw/finance 병렬 비교
  - [ ] 토큰 델타 강조
  - [ ] 빌드 통과
- **depends**: W2-webui-01

---

## 커버리지 요약

| 프로젝트 | Wave 0 | Wave 1 | Wave 2 | Wave 3 |
| --- | --- | --- | --- | --- |
| keelim-vercel | — | 2 | 2 | 1 |
| all-web-ui | — | 1 | 1 | 1 |
| rich | 1 | 1 | 3 | 2 |
| all | — | — | 3 | 3 |
| toto | — | 1 | 2 | — |
| android-support | — | 1 | 1 | — |
| keelim-plugin | — | 1 | 1 | — |
| Keelim-Knowledge-Vault | — | 1 | 1 | — |

총 `/goal` 항목: **30개** (Preconditions 4개 별도). 8개 프로젝트 모두 ≥1, Wave 0–3 모두 표현.
