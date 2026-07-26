# future

Last updated: 2026-07-26 KST

## Purpose

이 문서는 `docs/idea/<project>.md`로 바로 라우팅하기 전에 잠깐 모아두는 **임시 공용 inbox**다.

- source of truth는 계속 각 `docs/idea/<project>.md`
- 여기는 cross-project 관점에서 한 번 더 묶어보는 곳
- 실행 계획/태스크 분해는 하지 않음
- 비슷한 아이디어는 프로젝트가 여러 개여도 **하나로 통합**해서 적음

## Review rule

- 첫 리뷰 오너: 이번 정리의 lead/synthesizer
- 첫 리뷰 시점: 생성 후 72시간 이내
- 각 항목은 이후 `docs/idea/<project>.md`로 라우팅, 분기, 폐기, 혹은 1회 연장 중 하나를 택함

## 2026-07-26 triage note

이 inbox는 2026-04-16에 마지막으로 채워진 뒤 72시간 리뷰 기한과 1회 연장 기한을 모두 넘긴 채 3개월 이상 방치되어 있었다. 이번 점검에서 각 항목을 해당 시점 기준 `docs/idea/<project>.md` 내용과 대조한 결과, 절반 가량은 이미 프로젝트별 파일에 사실상 동일한 항목으로 존재해 **폐기**했다(아래 목록). 근접 중복 2건은 하나로 통합했다. 나머지는 어느 프로젝트 파일에도 1:1로 대응되지 않는 cross-project 관찰이라 계속 inbox에 남기되, 다음 정리에서는 반드시 라우팅하거나 폐기해야 한다 — 이 문서의 목적은 상시 보관함이 아니라 72시간짜리 대기열이다.

폐기된 항목(이미 프로젝트 파일에 라우팅된 중복으로 확인):
- 계약 드리프트 관제 레이어 → `all`/`all-web-ui`/`android-support`/`keelim-vercel`의 개별 드리프트 검사 항목과 중복
- Android 릴리스 계약 매니페스트 & 롤아웃 정책 레지스트리 → `android-support`의 Localized rollout guardrails / 액션 계약 드리프트 검사와 중복
- 실행 증적·재생·복구를 하나로 묶는 운영 ledger → `rich`의 Execution ledger, `android-support`의 릴리스 증적 번들과 중복
- 워크스페이스 지식 미러와 변화 다이제스트 → `Keelim-Knowledge-Vault`의 워크스페이스 지시문 미러 / 일일 변화 다이제스트와 중복
- 공용 토큰·프리미티브 소비 영향 가시화 → `all-web-ui`의 내보내기 계약 스냅샷·토큰 폐기 예고판, `keelim-vercel`의 공용 UI 어댑터 계약 스냅샷과 중복
- 앱/도구 전반의 다음 행동 추천 루프 → `keelim-vercel`의 Next-best-action feed와 중복
- 공유 스킬 생태계 catalog + 회귀 검증면 → `keelim-plugin`의 catalog/smoke-test 항목과 중복
- 릴리스 준비도와 빌드 병목을 함께 보는 control tower → `all`의 Release readiness radar / 빌드 병목 열지도와 중복
- workspace trusted-baseline scoreboard와 safe-set pinning gate → `Keelim-Knowledge-Vault`의 워크스페이스 신뢰 기준선 보드와 중복
- workspace backlink + stale-note resurfacer hub → `Keelim-Knowledge-Vault`의 Project-to-note backlink hub / Weekly resurfacer와 중복

## Temporary inbox (여전히 미라우팅 상태)

### 2026-04-16 - 재사용 가능한 프로필·시나리오 작업공간

Type: product

Why now: 금융 계산, 체크인, 운영 리뷰 표면이 같은 전제값을 반복해서 묻기 시작했기 때문에, 공통 프로필과 named scenario를 여러 도구가 공유하는 구조가 점점 더 중요해지고 있다.

Likely homes: `keelim-vercel`, `rich`

Refs: `keelim-vercel/lib/tax-benefit-storage.ts`, `keelim-vercel/lib/social-freshman-guide-storage.ts`, `keelim-vercel/lib/gift-tax-storage.ts`, `keelim-vercel/NEW_FEATURES_PLAN.md`

### 2026-04-16 - 네비게이션·라우트 인벤토리 동기화 가드

Type: mixed

Why now: `rich`는 `admin-route-inventory.ts`로 admin/public/legacy 경로를 명시적으로 관리하고, `keelim-vercel`은 `menu-config.ts` + `changelog-data.ts` + `verify-project-rules.ts`로 노출 메뉴와 신규 배지 규칙을 강하게 묶고 있어서, 두 제품 모두 실제 라우트·네비게이션·공지 표면이 쉽게 어긋날 수 있다. `keelim-vercel` 쪽은 이미 라우트 계약 드리프트 감시로 라우팅됐지만, `rich`의 admin-route-inventory 쪽은 아직 대응 항목이 없다.

Likely homes: `rich`, `keelim-vercel`

Refs: `rich/web/src/features/admin/admin-route-inventory.ts`, `keelim-vercel/lib/menu-config.ts`, `keelim-vercel/lib/changelog-data.ts`, `keelim-vercel/scripts/verify-project-rules.ts`

### 2026-04-16 - 실행 결과 패널과 알림 토스트를 연결하는 operator feedback layer

Type: mixed

Why now: `rich`의 `FlowPanel`은 run result, streak snapshot, loading 상태를 한 패널에서 보여주고, `keelim-vercel`은 `DeploymentNotification`으로 changelog 기반 업데이트 토스트를 띄우며, `all-web-ui`는 단계형 `LoadingStatus`를 제공하므로, 장기적으로는 실행 결과·진행 상태·배포 공지를 같은 operator feedback layer로 통합할 수 있다.

Likely homes: `rich`, `keelim-vercel`, `all-web-ui`

Refs: `rich/web/src/features/admin/components/flow-panel.tsx`, `rich/web/src/features/admin/components/google-agenda-auth-panel.tsx`, `keelim-vercel/components/deployment-notification.tsx`, `all-web-ui/src/components/loading-status.tsx`

### 2026-04-16 - 운영 변화 공지와 quick-open 탐색을 연결하는 discoverability loop

Type: mixed

Why now: `keelim-vercel`은 `DeploymentNotification`이 `CHANGELOG_DATA`를 읽어 새 기능 공지를 띄우고, `rich`는 `admin-quick-sitemap`과 route inventory로 운영 경로를 빠르게 찾게 하므로, 변경 공지와 실제 재진입 탐색 표면을 연결하면 기능 추가 후 발견성과 복귀성이 함께 좋아진다.

Likely homes: `keelim-vercel`, `rich`

Refs: `keelim-vercel/components/deployment-notification.tsx`, `keelim-vercel/lib/changelog-data.ts`, `rich/web/src/features/admin/components/admin-quick-sitemap.tsx`, `rich/web/src/features/admin/admin-route-inventory.ts`, `rich/web/src/app/admin/layout.tsx`

### 2026-04-16 - 통합 신선도·헬스·이상징후 watchdog (범위 확장)

Type: mixed

Why now: 데이터 신선도, 외부 연동 상태, 업스트림 auth drift, 갑작스러운 지표 이상을 따로따로 보지 말고 하나의 운영 건강도 관점에서 다뤄야 침묵 실패를 줄일 수 있다. `rich` 쪽은 이미 Data freshness/anomaly watchdog와 Integration health console로 라우팅됐지만, 이번 관찰은 `keelim-vercel`의 시장 데이터 신선도까지 같은 관점으로 묶자는 확장 제안이라 별도로 남긴다.

Likely homes: `rich`, `keelim-vercel`

Refs: `rich/app/main.py`, `rich/app/core/settings.py`, `rich/README.md`, `keelim-vercel/lib/queries/market.ts`

### 2026-04-16 - 개인 운영 상태 버전 레지스트리와 triage funnel

Type: mixed

Why now: `rich`는 personal inbox → loop → weekly review로 이어지는 운영 흐름을 이미 갖고 있고, `keelim-vercel`은 bookmarks·tool ranking·profile/scenario 저장소와 별도 `storage-version-registry.ts`를 유지하고 있어서, 개인 운영 상태가 여러 도구에 흩어질수록 저장 포맷·triage 단계·재진입 경험을 함께 다루는 공통 레이어가 필요하다.

Likely homes: `rich`, `keelim-vercel`

Refs: `rich/web/src/features/inbox/inbox-hooks.ts`, `rich/web/src/features/loop/loop-hooks.ts`, `rich/web/src/features/weekly-review/weekly-review-page-content.tsx`, `keelim-vercel/lib/storage-version-registry.ts`, `keelim-vercel/lib/bookmark-storage.ts`, `keelim-vercel/lib/ranking-actions.ts`

### 2026-04-16 - 개인 캡처·첨부·내보내기·복기를 묶는 operator collection kit (2건 통합)

Type: mixed

Why now: `rich`는 profit note(이미지 첨부, review flag), bucket list, todo, loop 같은 개인 운영 입력 표면을 이미 여러 panel로 나눠 갖고 있고, `keelim-vercel`도 smart bookmark manager처럼 저장·검색·분류·TSV 내보내기·재탐색 흐름을 가진 개인 캡처 도구를 별도로 운영하고 있어서, 입력/첨부 미디어/내보내기/후속 복기/빈 상태/로딩 패턴을 공용 operator collection kit로 추출할 여지가 크다. (이전의 "capture artifact workflow"와 "operator collection kit" 두 항목을 하나로 통합함.)

Likely homes: `rich`, `keelim-vercel`, `all-web-ui`

Refs: `rich/web/src/features/admin/profit-note-panel.tsx`, `rich/web/src/features/admin/profit-note-attachment-hooks.ts`, `rich/web/src/features/admin/profit-note-types.ts`, `rich/web/src/features/admin/components/bucket-list-panel.tsx`, `rich/web/src/features/admin/components/todo-panel.tsx`, `keelim-vercel/components/smart-bookmark-manager.tsx`, `keelim-vercel/lib/bookmark-storage.ts`, `keelim-vercel/lib/insight-clipper-storage.ts`, `all-web-ui/src/components/loading-status.tsx`, `all-web-ui/src/components/input.tsx`

### 2026-04-16 - 운영 UI 프리미티브 계약면과 admin surface kit

Type: mixed

Why now: `all-web-ui`는 `Panel`, `EmptyState`, `LoadingStatus` 같은 얇은 공용 primitive를 export하고 있고, `rich`는 admin shell·quick sitemap·todo/inbox/loop panel에서 이 표면을 반복 사용하고 있어서, 운영 UI가 커질수록 admin 전용 composition kit와 primitive 계약 검증이 같이 필요하다.

Likely homes: `all-web-ui`, `rich`

Refs: `all-web-ui/src/index.ts`, `all-web-ui/src/components/panel.tsx`, `all-web-ui/src/components/empty-state.tsx`, `rich/web/src/features/admin/components/todo-panel.tsx`, `rich/web/src/features/admin/components/admin-quick-sitemap.tsx`, `rich/web/src/features/admin/components/admin-shell.test.tsx`

### 2026-04-16 - 워크플로우를 skill·문서·설치 경로로 동시 출판하는 publishing loop

Type: mixed

Why now: Vault의 AI harness 시리즈가 반복 워크플로우를 skill과 superproject 규칙으로 승격하는 과정을 이미 설명하고 있고, `keelim-plugin`은 실제로 `SKILL.md` + `agents/openai.yaml` + Vercel skills CLI/manual symlink 설치 경로를 함께 갖고 있어서, 새 워크플로우를 문서·skill·설치 검증까지 한 번에 승격하는 공통 loop를 만들 여지가 크다.

Likely homes: `Keelim-Knowledge-Vault`, `keelim-plugin`

Refs: `Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 1 - Turning a Repetitive Release Process Into a Skill.md`, `Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 2 - Turning Planning and Parallel Execution Into a Reusable Workflow.md`, `keelim-plugin/README.md`, `keelim-plugin/skills/release-automation/SKILL.md`, `keelim-plugin/skills/ralplan-team/agents/openai.yaml`

### 2026-04-16 - review cadence를 Slack·agenda·changelog로 묶는 operator rhythm registry

Type: mixed

Why now: `rich`는 agenda 요약·today warning·weekly review·Slack review reminder를 각각 따로 갖고 있고, `keelim-vercel`은 changelog 기반 deployment notification으로 변화 알림을 따로 띄우며, `keelim-plugin`은 release workflow 자체를 skill 문서로 운영하고 있어서, 운영자의 하루 리듬을 코드와 문서에 걸쳐 한 번에 설명하는 cadence registry가 있으면 리마인더/리뷰/출시 후 확인 루프가 훨씬 덜 흩어진다.

Likely homes: `rich`, `keelim-vercel`, `keelim-plugin`

Refs: `rich/supabase/functions/slack-review-reminder/index.ts`, `rich/web/src/features/agenda/components/agenda-client.tsx`, `rich/web/src/features/today/components/today-loop-warnings-panel.tsx`, `rich/web/src/features/weekly-review/weekly-review-page-content.tsx`, `keelim-vercel/components/deployment-notification.tsx`, `keelim-vercel/lib/changelog-data.ts`, `keelim-plugin/skills/release-automation/SKILL.md`

### 2026-04-16 - dry-run·cache·force를 함께 다루는 execution mode contract registry

Type: mixed

Why now: `keelim-plugin`의 release automation은 dry-run / confirm / execute 모드를 명시하고, `rich`의 ingestion run은 cached summary와 `force=true` 재실행 규칙을 따로 가지며, `android-support`는 기존 edit 재사용·track 검증·입력 검증을 통과해야 실제 업로드가 진행되므로, 운영 작업마다 "읽기 전용 확인 → 검증된 실행 → 강제 재실행" 계약을 제각각 배우지 않게 해 주는 execution mode registry가 있으면 배포/수집/운영 작업의 신뢰 경계가 훨씬 또렷해진다.

Likely homes: `keelim-plugin`, `rich`, `android-support`

Refs: `keelim-plugin/skills/release-automation/SKILL.md`, `rich/AGENTS.md`, `rich/app/api/admin.py`, `android-support/src/main.ts`, `android-support/src/edits.ts`

### 2026-04-16 - human summary와 machine artifact를 함께 남기는 proof bundle contract

Type: mixed

Why now: `all`은 coverage manifest와 trusted participant summary를 JSON 파일로 남기고, `rich`는 weekly review와 공공 API catalog export에서 사람이 읽는 summary와 기계가 읽을 수 있는 수치를 함께 만들며, `android-support`는 업로드/서명 결과를 output·env variable로 다시 노출하므로, 운영 검증 결과를 "사람용 서술 + 기계용 artifact" 한 세트로 표준화하면 배포·데이터 수집·품질 점검 이후의 handoff와 재검증이 훨씬 쉬워진다.

Likely homes: `all`, `rich`, `android-support`

Refs: `all/build.gradle.kts`, `rich/scripts/export_data_go_kr_api_catalog.py`, `rich/app/services/weekly_review.py`, `android-support/src/edits.ts`, `android-support/src/main.ts`

### 2026-04-16 - public capture bridge에서 authenticated admin triage로 이어지는 handoff rail

Type: mixed

Why now: `rich`는 `/capture/inbox`를 브라우저 확장과 외부 진입용 경량 capture surface로 두고, 로그인 후에는 같은 데이터를 `/admin/inbox`와 today/loop 경고 패널에서 다시 triage하게 만들며, Google One Tap과 legacy redirect까지 admin 진입 경로를 세심하게 관리하고 있어서, public capture → signed-in admin triage → next action으로 이어지는 handoff rail을 더 명시적으로 제품화하면 빠른 캡처와 실제 운영 행동 사이의 마찰을 크게 줄일 수 있다.

Likely homes: `rich`, `all-web-ui`

Refs: `rich/AGENTS.md`, `rich/web/extension/src/popup-utils.ts`, `rich/web/src/features/inbox/components/inbox-capture-page-content.tsx`, `rich/web/src/features/today/components/today-loop-warnings-panel.tsx`, `rich/web/src/features/admin/components/google-agenda-auth-panel.tsx`, `all-web-ui/src/components/input.tsx`, `all-web-ui/src/components/button.tsx`
