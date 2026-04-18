# future

Last updated: 2026-04-16 09:56 KST

## Purpose

이 문서는 `idea/<project>.md`로 바로 라우팅하기 전에 잠깐 모아두는 **임시 공용 inbox**다.

- source of truth는 계속 각 `idea/<project>.md`
- 여기는 cross-project 관점에서 한 번 더 묶어보는 곳
- 실행 계획/태스크 분해는 하지 않음
- 비슷한 아이디어는 프로젝트가 여러 개여도 **하나로 통합**해서 적음

## Review rule

- 첫 리뷰 오너: 이번 정리의 lead/synthesizer
- 첫 리뷰 시점: 생성 후 72시간 이내
- 각 항목은 이후 `idea/<project>.md`로 라우팅, 분기, 폐기, 혹은 1회 연장 중 하나를 택함

## Temporary inbox

### Exploration note

현재 라운드는 **원본 워크스페이스**(`/Users/keelim/Desktop/keelim-maestro`)를 read-only로 계속 훑으면서 `idea/future.md`를 직접 보강하는 timed exploration이다. 1시간 조건은 `2026-04-16 09:19:45 KST` 시작 / `2026-04-16 10:19:45 KST` 종료 기준으로 강제하고, 그 전에는 완료로 간주하지 않는다.

### 2026-04-16 - 계약 드리프트 관제 레이어

Type: mixed

Why now: `all`, `all-web-ui`, `android-support`, `keelim-vercel` 전부에서 export/input/route/convention 계약이 따로 움직이고 있어서, 문서·설정·실제 구현 사이의 drift를 늦게 발견하는 비용이 커지고 있다.

Likely homes: `all`, `all-web-ui`, `android-support`, `keelim-vercel`

Refs: `/Users/keelim/Desktop/keelim-maestro/android-support/action.yml`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/input-validation.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/scripts/verify-project-rules.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/AGENTS.md`


### 2026-04-16 - Android 릴리스 계약 매니페스트 & 롤아웃 정책 레지스트리

Type: technical

Why now: `android-support`가 `track`, `status`, `userFraction`, `whatsNewDirectory` 같은 typed input 경계를 이미 가지고 있고, `all`은 여러 앱과 release workflow를 같이 돌리기 때문에 앱별 Play 정책과 action input이 어긋나면 늦게 깨질 위험이 크다.

Likely homes: `all`, `android-support`

Refs: `/Users/keelim/Desktop/keelim-maestro/android-support/action.yml`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/main.ts`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/input-validation.ts`, `/Users/keelim/Desktop/keelim-maestro/all/.github`, `/Users/keelim/Desktop/keelim-maestro/all/build-logic`

### 2026-04-16 - 실행 증적·재생·복구를 하나로 묶는 운영 ledger

Type: technical

Why now: Play 업로드, cron/수동 실행, 데이터 수집, 리뷰 플로우처럼 실패 비용이 큰 흐름이 늘어나서, 입력·결과·재시도 힌트를 같은 표면에서 남기고 다시 재생할 수 있어야 운영 복구가 빨라진다.

Likely homes: `android-support`, `rich`

Refs: `/Users/keelim/Desktop/keelim-maestro/android-support/README.md`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/edits.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/README.md`, `/Users/keelim/Desktop/keelim-maestro/rich/app/api/admin.py`

### 2026-04-16 - 워크스페이스 지식 미러와 변화 다이제스트

Type: mixed

Why now: Vault, AGENTS, CODEMAPS, idea 인덱스, automation memory가 모두 가치가 큰데 진입점이 흩어져 있어, 활성 프로젝트가 다시 참고할 수 있는 연결 허브와 변화 요약이 필요하다.

Likely homes: `Keelim-Knowledge-Vault`, `rich`

Refs: `/Users/keelim/Desktop/keelim-maestro/Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 3 - Turning a Multi-Repo Workspace Into a Reproducible Superproject.md`, `/Users/keelim/Desktop/keelim-maestro/docs/CODEMAPS/WORKSPACE.md`, `/Users/keelim/Desktop/keelim-maestro/docs/CODEMAPS/SUBMODULES.md`

### 2026-04-16 - 공용 토큰·프리미티브 소비 영향 가시화

Type: technical

Why now: `all-web-ui`의 토큰/프리미티브 변화가 `keelim-vercel`과 다른 소비자 앱에 늦게 전파되므로, 시각 회귀뿐 아니라 실제 소비 경로와 교체 비용을 같이 보여주는 표면이 필요하다.

Likely homes: `all-web-ui`, `keelim-vercel`

Refs: `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/components/shared/all-web-ui-adapters.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/AGENTS.md`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src`

### 2026-04-16 - 앱/도구 전반의 다음 행동 추천 루프

Type: product

Why now: `keelim-vercel`과 `rich` 모두 계산기·리뷰·운영 표면이 넓어져서, 사용자가 다음에 무엇을 해야 할지 추천해주는 루프가 개별 페이지 추가보다 더 큰 가치가 있다.

Likely homes: `keelim-vercel`, `rich`

Refs: `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/ranking-actions.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/bookmark-storage.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/app/api/admin.py`, `/Users/keelim/Desktop/keelim-maestro/rich/README.md`

### 2026-04-16 - 재사용 가능한 프로필·시나리오 작업공간

Type: product

Why now: 금융 계산, 체크인, 운영 리뷰 표면이 같은 전제값을 반복해서 묻기 시작했기 때문에, 공통 프로필과 named scenario를 여러 도구가 공유하는 구조가 점점 더 중요해지고 있다.

Likely homes: `keelim-vercel`, `rich`

Refs: `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/tax-benefit-storage.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/social-freshman-guide-storage.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/gift-tax-storage.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/NEW_FEATURES_PLAN.md`


### 2026-04-16 - 네비게이션·라우트 인벤토리 동기화 가드

Type: mixed

Why now: `rich`는 `admin-route-inventory.ts`로 admin/public/legacy 경로를 명시적으로 관리하고, `keelim-vercel`은 `menu-config.ts` + `changelog-data.ts` + `verify-project-rules.ts`로 노출 메뉴와 신규 배지 규칙을 강하게 묶고 있어서, 두 제품 모두 실제 라우트·네비게이션·공지 표면이 쉽게 어긋날 수 있다.

Likely homes: `rich`, `keelim-vercel`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/admin-route-inventory.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/menu-config.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/changelog-data.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/scripts/verify-project-rules.ts`



### 2026-04-16 - 실행 결과 패널과 알림 토스트를 연결하는 operator feedback layer

Type: mixed

Why now: `rich`의 `FlowPanel`은 run result, streak snapshot, loading 상태를 한 패널에서 보여주고, `keelim-vercel`은 `DeploymentNotification`으로 changelog 기반 업데이트 토스트를 띄우며, `all-web-ui`는 단계형 `LoadingStatus`를 제공하므로, 장기적으로는 실행 결과·진행 상태·배포 공지를 같은 operator feedback layer로 통합할 수 있다.

Likely homes: `rich`, `keelim-vercel`, `all-web-ui`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/flow-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/google-agenda-auth-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/components/deployment-notification.tsx`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/components/loading-status.tsx`

### 2026-04-16 - 운영 변화 공지와 quick-open 탐색을 연결하는 discoverability loop

Type: mixed

Why now: `keelim-vercel`은 `DeploymentNotification`이 `CHANGELOG_DATA`를 읽어 새 기능 공지를 띄우고, `rich`는 `admin-quick-sitemap`과 route inventory로 운영 경로를 빠르게 찾게 하므로, 변경 공지와 실제 재진입 탐색 표면을 연결하면 기능 추가 후 발견성과 복귀성이 함께 좋아진다.

Likely homes: `keelim-vercel`, `rich`

Refs: `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/components/deployment-notification.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/changelog-data.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/admin-quick-sitemap.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/admin-route-inventory.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/app/admin/layout.tsx`

### 2026-04-16 - 통합 신선도·헬스·이상징후 watchdog

Type: mixed

Why now: 데이터 신선도, 외부 연동 상태, 업스트림 auth drift, 갑작스러운 지표 이상을 따로따로 보지 말고 하나의 운영 건강도 관점에서 다뤄야 침묵 실패를 줄일 수 있다.

Likely homes: `rich`, `keelim-vercel`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/app/main.py`, `/Users/keelim/Desktop/keelim-maestro/rich/app/core/settings.py`, `/Users/keelim/Desktop/keelim-maestro/rich/README.md`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/queries/market.ts`


### 2026-04-16 - 개인 운영 상태 버전 레지스트리와 triage funnel

Type: mixed

Why now: `rich`는 personal inbox → loop → weekly review로 이어지는 운영 흐름을 이미 갖고 있고, `keelim-vercel`은 bookmarks·tool ranking·profile/scenario 저장소와 별도 `storage-version-registry.ts`를 유지하고 있어서, 개인 운영 상태가 여러 도구에 흩어질수록 저장 포맷·triage 단계·재진입 경험을 함께 다루는 공통 레이어가 필요하다.

Likely homes: `rich`, `keelim-vercel`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/inbox/inbox-hooks.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/loop/loop-hooks.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/weekly-review/weekly-review-page-content.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/storage-version-registry.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/bookmark-storage.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/ranking-actions.ts`




### 2026-04-16 - 첨부·내보내기·복기를 한 번에 다루는 capture artifact workflow

Type: mixed

Why now: `rich`의 profit note는 이미지 첨부와 review flag를 함께 다루고, `keelim-vercel`의 bookmark/insight/storage 계열은 TSV export와 재탐색 흐름이 반복되므로, 기록 입력·첨부 미디어·내보내기·후속 복기까지 이어지는 공통 capture artifact workflow를 만들면 개인 운영 데이터의 재사용성과 회고 품질이 올라간다.

Likely homes: `rich`, `keelim-vercel`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/profit-note-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/profit-note-attachment-hooks.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/profit-note-types.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/components/smart-bookmark-manager.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/bookmark-storage.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/insight-clipper-storage.ts`

### 2026-04-16 - 개인 캡처 표면을 재사용 가능한 operator collection kit로 묶기

Type: mixed

Why now: `rich`는 profit note, bucket list, todo, loop 같은 개인 운영 입력 표면을 이미 여러 panel로 나눠 갖고 있고, `keelim-vercel`도 smart bookmark manager처럼 저장·검색·분류·복사 흐름을 가진 개인 캡처 도구를 별도로 운영하고 있어서, 입력/빈 상태/로딩/후속 액션 패턴을 공용 operator collection kit로 추출할 여지가 크다.

Likely homes: `rich`, `keelim-vercel`, `all-web-ui`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/profit-note-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/bucket-list-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/todo-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/components/smart-bookmark-manager.tsx`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/components/loading-status.tsx`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/components/input.tsx`

### 2026-04-16 - 운영 UI 프리미티브 계약면과 admin surface kit

Type: mixed

Why now: `all-web-ui`는 `Panel`, `EmptyState`, `LoadingStatus` 같은 얇은 공용 primitive를 export하고 있고, `rich`는 admin shell·quick sitemap·todo/inbox/loop panel에서 이 표면을 반복 사용하고 있어서, 운영 UI가 커질수록 admin 전용 composition kit와 primitive 계약 검증이 같이 필요하다.

Likely homes: `all-web-ui`, `rich`

Refs: `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/index.ts`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/components/panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/components/empty-state.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/todo-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/admin-quick-sitemap.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/admin-shell.test.tsx`

### 2026-04-16 - 워크플로우를 skill·문서·설치 경로로 동시 출판하는 publishing loop

Type: mixed

Why now: Vault의 AI harness 시리즈가 반복 워크플로우를 skill과 superproject 규칙으로 승격하는 과정을 이미 설명하고 있고, `keelim-plugin`은 실제로 `SKILL.md` + `agents/openai.yaml` + Vercel skills CLI/manual symlink 설치 경로를 함께 갖고 있어서, 새 워크플로우를 문서·skill·설치 검증까지 한 번에 승격하는 공통 loop를 만들 여지가 크다.

Likely homes: `Keelim-Knowledge-Vault`, `keelim-plugin`

Refs: `/Users/keelim/Desktop/keelim-maestro/Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 1 - Turning a Repetitive Release Process Into a Skill.md`, `/Users/keelim/Desktop/keelim-maestro/Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 2 - Turning Planning and Parallel Execution Into a Reusable Workflow.md`, `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/README.md`, `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/skills/release-automation/SKILL.md`, `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/skills/ralplan-team/agents/openai.yaml`

### 2026-04-16 - 공유 스킬 생태계 catalog + 회귀 검증면

Type: technical

Why now: `keelim-plugin`의 가치는 스킬 수 자체보다 설치 가능성, lifecycle 상태, smoke-test 가능성, 재사용 조합이 한눈에 보이느냐에 달려 있어서 catalog와 verification이 같이 자라야 한다.

Likely homes: `keelim-plugin`, `Keelim-Knowledge-Vault`

Refs: `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/README.md`, `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/skills/ralplan-team/SKILL.md`, `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/skills/release-automation/SKILL.md`

### 2026-04-16 - 릴리스 준비도와 빌드 병목을 함께 보는 control tower

Type: technical

Why now: 다중 앱/모듈 빌드 병목과 실제 릴리스 위험은 따로 보면 우선순위를 잘못 잡기 쉬워서, 속도 문제와 배포 위험을 한 화면에서 묶어 보는 관제가 필요하다.

Likely homes: `all`, `android-support`

Refs: `/Users/keelim/Desktop/keelim-maestro/all/build-logic`, `/Users/keelim/Desktop/keelim-maestro/all/benchmarks`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/main.ts`, `/Users/keelim/Desktop/keelim-maestro/android-support/README.md`

### 2026-04-16 - review cadence를 Slack·agenda·changelog로 묶는 operator rhythm registry

Type: mixed

Why now: `rich`는 agenda 요약·today warning·weekly review·Slack review reminder를 각각 따로 갖고 있고, `keelim-vercel`은 changelog 기반 deployment notification으로 변화 알림을 따로 띄우며, `keelim-plugin`은 release workflow 자체를 skill 문서로 운영하고 있어서, 운영자의 하루 리듬(언제 보고·언제 복기하고·언제 배포 상태를 확인할지)을 코드와 문서에 걸쳐 한 번에 설명하는 cadence registry가 있으면 리마인더/리뷰/출시 후 확인 루프가 훨씬 덜 흩어진다.

Likely homes: `rich`, `keelim-vercel`, `keelim-plugin`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/supabase/functions/slack-review-reminder/index.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/agenda/components/agenda-client.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/today/components/today-loop-warnings-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/weekly-review/weekly-review-page-content.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/components/deployment-notification.tsx`, `/Users/keelim/Desktop/keelim-maestro/keelim-vercel/lib/changelog-data.ts`, `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/skills/release-automation/SKILL.md`

### 2026-04-16 - dry-run·cache·force를 함께 다루는 execution mode contract registry

Type: mixed

Why now: `keelim-plugin`의 release automation은 dry-run / confirm / execute 모드를 명시하고, `rich`의 ingestion run은 cached summary와 `force=true` 재실행 규칙을 따로 가지며, `android-support`는 기존 edit 재사용·track 검증·입력 검증을 통과해야 실제 업로드가 진행되므로, 운영 작업마다 "읽기 전용 확인 → 검증된 실행 → 강제 재실행" 계약을 제각각 배우지 않게 해 주는 execution mode registry가 있으면 배포/수집/운영 작업의 신뢰 경계가 훨씬 또렷해진다.

Likely homes: `keelim-plugin`, `rich`, `android-support`

Refs: `/Users/keelim/Desktop/keelim-maestro/keelim-plugin/skills/release-automation/SKILL.md`, `/Users/keelim/Desktop/keelim-maestro/rich/AGENTS.md`, `/Users/keelim/Desktop/keelim-maestro/rich/app/api/admin.py`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/main.ts`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/edits.ts`

### 2026-04-16 - workspace trusted-baseline scoreboard와 safe-set pinning gate

Type: mixed

Why now: 루트 AGENTS와 CODEMAPS는 이미 어떤 child repo가 등록 submodule인지, 어떤 repo는 아직 autonomous로 남겨야 하는지, dirty/ahead-of-remote 상태에서 무엇을 pin하면 안 되는지를 자세히 말해 주고 있고, Vault의 superproject 글도 "지금 내가 함께 신뢰하는 repo 집합이 무엇인지"를 workspace-level로 답할 수 있어야 한다고 강조하므로, root에서 한 번에 trusted set / excluded set / pinning blockers를 보여주는 scoreboard가 있으면 multi-repo 작업 후 결과를 더 설명 가능하게 남길 수 있다.

Likely homes: `docs/CODEMAPS`, `Keelim-Knowledge-Vault`, root workspace helpers

Refs: `/Users/keelim/Desktop/keelim-maestro/AGENTS.md`, `/Users/keelim/Desktop/keelim-maestro/docs/CODEMAPS/WORKSPACE.md`, `/Users/keelim/Desktop/keelim-maestro/docs/CODEMAPS/SCRIPTS.md`, `/Users/keelim/Desktop/keelim-maestro/docs/CODEMAPS/README.md`, `/Users/keelim/Desktop/keelim-maestro/Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 3 - Turning a Multi-Repo Workspace Into a Reproducible Superproject.md`

### 2026-04-16 - human summary와 machine artifact를 함께 남기는 proof bundle contract

Type: mixed

Why now: `all`은 coverage manifest와 trusted participant summary를 JSON 파일로 남기고, `rich`는 weekly review와 공공 API catalog export에서 사람이 읽는 summary와 기계가 읽을 수 있는 수치를 함께 만들며, `android-support`는 업로드/서명 결과를 output·env variable로 다시 노출하므로, 운영 검증 결과를 "사람용 서술 + 기계용 artifact" 한 세트로 표준화하면 배포·데이터 수집·품질 점검 이후의 handoff와 재검증이 훨씬 쉬워진다.

Likely homes: `all`, `rich`, `android-support`

Refs: `/Users/keelim/Desktop/keelim-maestro/all/build.gradle.kts`, `/Users/keelim/Desktop/keelim-maestro/rich/scripts/export_data_go_kr_api_catalog.py`, `/Users/keelim/Desktop/keelim-maestro/rich/app/services/weekly_review.py`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/edits.ts`, `/Users/keelim/Desktop/keelim-maestro/android-support/src/main.ts`

### 2026-04-16 - public capture bridge에서 authenticated admin triage로 이어지는 handoff rail

Type: mixed

Why now: `rich`는 `/capture/inbox`를 브라우저 확장과 외부 진입용 경량 capture surface로 두고, 로그인 후에는 같은 데이터를 `/admin/inbox`와 today/loop 경고 패널에서 다시 triage하게 만들며, Google One Tap과 legacy redirect까지 admin 진입 경로를 세심하게 관리하고 있어서, public capture → signed-in admin triage → next action으로 이어지는 handoff rail을 더 명시적으로 제품화하면 빠른 캡처와 실제 운영 행동 사이의 마찰을 크게 줄일 수 있다.

Likely homes: `rich`, `all-web-ui`

Refs: `/Users/keelim/Desktop/keelim-maestro/rich/AGENTS.md`, `/Users/keelim/Desktop/keelim-maestro/rich/web/extension/src/popup-utils.ts`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/inbox/components/inbox-capture-page-content.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/today/components/today-loop-warnings-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/rich/web/src/features/admin/components/google-agenda-auth-panel.tsx`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/components/input.tsx`, `/Users/keelim/Desktop/keelim-maestro/all-web-ui/src/components/button.tsx`

### 2026-04-16 - workspace backlink + stale-note resurfacer hub

Type: mixed

Why now: `Keelim-Knowledge-Vault`는 이미 프로젝트 인덱스와 고가치 노트를 쌓아 두고 있고, 루트는 `idea/index.md`와 `docs/CODEMAPS`로 현재 워크스페이스 진입점을 따로 관리하므로, 활성 repo에서 바로 관련 노트로 왕복하고 오래 묻힌 핵심 노트를 다시 띄우는 resurfacer hub가 있으면 재진입 비용을 더 줄일 수 있다.

Likely homes: `Keelim-Knowledge-Vault`, `docs/CODEMAPS`, `idea`

Refs: `/Users/keelim/Desktop/keelim-maestro/Keelim-Knowledge-Vault/Index.md`, `/Users/keelim/Desktop/keelim-maestro/docs/CODEMAPS/README.md`, `/Users/keelim/Desktop/keelim-maestro/docs/CODEMAPS/WORKSPACE.md`, `/Users/keelim/Desktop/keelim-maestro/idea/index.md`, `/Users/keelim/Desktop/keelim-maestro/idea/Keelim-Knowledge-Vault.md`
