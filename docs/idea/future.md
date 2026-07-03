# future

Last updated: 2026-07-03 KST

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

## Routing log - 2026-07-03

2026-04-16에 쌓인 24개 항목을 이번 라운드에서 처음으로 리뷰했다 (72시간 규칙을 이미 크게 넘겼음을 인지).

- **라우팅 완료로 제거 (11개):** 계약 드리프트 관제 레이어, 실행 증적·재생·복구 ledger, 워크스페이스 지식 미러와 변화 다이제스트, 공용 토큰·프리미티브 소비 영향 가시화, 앱/도구 전반 다음 행동 추천 루프, 통합 신선도·헬스·이상징후 watchdog, 공유 스킬 생태계 catalog + 회귀 검증면, 릴리스 준비도와 빌드 병목 control tower, workspace trusted-baseline scoreboard, workspace backlink + stale-note resurfacer hub. 각각 `all.md`, `all-web-ui.md`, `android-support.md`, `Keelim-Knowledge-Vault.md`, `keelim-plugin.md`, `keelim-vercel.md`, `rich.md`의 2026-04-12~04-18 항목으로 이미 구체화되어 있어 중복이므로 이 inbox에서는 제거한다.
- **신규 라우팅 (1개):** "Android 릴리스 계약 매니페스트 & 롤아웃 정책 레지스트리" → `android-support.md`로 승격 (2026-07-03 항목, `all` 교차 참조 포함).
- **통합 후 1회 연장 (9→1개로 압축):** 실행 결과 패널/토스트 feedback layer, 운영 변화 공지 discoverability loop, 개인 운영 상태 triage funnel, capture artifact workflow, operator collection kit, admin surface kit, review cadence registry, public capture handoff rail, 재사용 가능한 프로필·시나리오 작업공간 — 9개 모두 "`rich`/`keelim-vercel`/`all-web-ui`의 운영자 UI 표면을 하나로 묶자"는 같은 관찰의 변형이라 하나의 통합 노트로 압축했다. 아래 유지 항목 참고.
- **1회 연장 (그대로 유지, 2개):** 워크플로우 publishing loop, dry-run·cache·force execution mode contract registry, human summary + machine artifact proof bundle contract — 근거는 분명하지만 대상 프로젝트(`keelim-plugin`, `rich`, `all`, `android-support`)가 모두 idea 상한(6개)에 이미 도달해 있어 이번 라운드에는 승격하지 않는다.

## Temporary inbox

### 2026-04-16 (1회 연장 -> 2026-07-03) - `rich`·`keelim-vercel`·`all-web-ui` 운영자 UI 표면 통합

Type: mixed

Why now: 지난 라운드에서 실행 결과 패널, discoverability loop, capture/collection kit, admin surface kit, nav/route 동기화, review cadence, public capture handoff, 프로필/시나리오 작업공간까지 서로 겹치는 변형 아이디어 9개가 개별 항목으로 쌓였다. 공통 원인은 하나다: `rich`의 admin 패널 군(`FlowPanel`, todo/inbox/loop/profit-note panel, `admin-route-inventory`, `admin-quick-sitemap`)과 `keelim-vercel`의 저장·알림·북마크 표면(`DeploymentNotification`, `smart-bookmark-manager`, `storage-version-registry`)이 같은 "운영자 UI 프리미티브" 계층으로 수렴하고 있는데, 아직 어느 프로젝트가 1차 소유자인지 정해지지 않았다.

Likely homes: `rich`, `keelim-vercel`, `all-web-ui` (1차 소유자 미정 - 승격 전 단일 프로젝트로 스코프를 좁혀야 함)

Refs: `rich/web/src/features/admin/components/flow-panel.tsx`, `rich/web/src/features/admin/components/todo-panel.tsx`, `rich/web/src/features/admin/components/bucket-list-panel.tsx`, `rich/web/src/features/admin/admin-route-inventory.ts`, `rich/web/src/features/admin/components/admin-quick-sitemap.tsx`, `rich/web/src/features/inbox/inbox-hooks.ts`, `rich/web/src/features/loop/loop-hooks.ts`, `rich/web/src/features/weekly-review/weekly-review-page-content.tsx`, `rich/supabase/functions/slack-review-reminder/index.ts`, `keelim-vercel/components/deployment-notification.tsx`, `keelim-vercel/components/smart-bookmark-manager.tsx`, `keelim-vercel/lib/changelog-data.ts`, `keelim-vercel/lib/storage-version-registry.ts`, `keelim-vercel/lib/bookmark-storage.ts`, `all-web-ui/src/components/loading-status.tsx`, `all-web-ui/src/components/panel.tsx`, `all-web-ui/src/components/empty-state.tsx`

Note: `rich.md`와 `keelim-vercel.md`가 이미 open ideas 상한(6개)에 도달해 있어 이번 라운드에서는 승격하지 않는다. 다음 리뷰에서 1차 소유 프로젝트를 하나로 정하고, 그 프로젝트의 항목에 여유가 생기면 그 안으로 좁혀서 라우팅한다. 이번이 규칙상 마지막 1회 연장이며, 다음 리뷰에서도 라우팅되지 않으면 폐기한다.

### 2026-04-16 (1회 연장 -> 2026-07-03) - 워크플로우를 skill·문서·설치 경로로 동시 출판하는 publishing loop

Type: mixed

Why now: Vault의 AI harness 시리즈가 반복 워크플로우를 skill과 superproject 규칙으로 승격하는 과정을 이미 설명하고 있고, `keelim-plugin`은 실제로 `SKILL.md` + agent 메타데이터 + Vercel skills CLI/manual symlink 설치 경로를 함께 갖고 있어서, 새 워크플로우를 문서·skill·설치 검증까지 한 번에 승격하는 공통 loop를 만들 여지가 크다.

Likely homes: `Keelim-Knowledge-Vault`, `keelim-plugin`

Refs: `Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 1 - Turning a Repetitive Release Process Into a Skill.md`, `Keelim-Knowledge-Vault/AI/ai-harness/Building My AI Harness, Part 2 - Turning Planning and Parallel Execution Into a Reusable Workflow.md`, `keelim-plugin/README.md`, `keelim-plugin/skills/release-automation/SKILL.md`, `keelim-plugin/skills/ralplan-team/agents/openai.yaml`

Note: `keelim-plugin.md`와 `Keelim-Knowledge-Vault.md` 모두 open ideas 상한(6개)에 도달해 있어 이번 라운드에는 승격하지 않는다. 다음 리뷰에서 두 파일 중 하나에 여유가 생기면(기존 항목 정리/해결 포함) 그 프로젝트로 라우팅한다. 이번이 마지막 1회 연장이며, 다음 리뷰에서도 라우팅되지 않으면 폐기한다.

### 2026-04-16 (1회 연장 -> 2026-07-03) - dry-run·cache·force를 함께 다루는 execution mode contract registry

Type: mixed

Why now: `keelim-plugin`의 release automation은 dry-run / confirm / execute 모드를 명시하고, `rich`의 ingestion run은 cached summary와 `force=true` 재실행 규칙을 따로 가지며, `android-support`는 기존 edit 재사용·track 검증·입력 검증을 통과해야 실제 업로드가 진행되므로, 운영 작업마다 "읽기 전용 확인 → 검증된 실행 → 강제 재실행" 계약을 제각각 배우지 않게 해 주는 execution mode registry가 있으면 배포/수집/운영 작업의 신뢰 경계가 훨씬 또렷해진다.

Likely homes: `keelim-plugin`, `rich`, `android-support`

Refs: `keelim-plugin/skills/release-automation/SKILL.md`, `rich/AGENTS.md`, `rich/app/api/admin.py`, `android-support/src/main.ts`, `android-support/src/edits.ts`

Note: 세 대상 프로젝트(`keelim-plugin`, `rich`, `android-support`) 모두 open ideas 상한에 도달했거나(전자 둘) 이번 라운드에 다른 신규 항목을 이미 받았다(`android-support`). 다음 리뷰에서 여유가 생기는 프로젝트로 라우팅한다. 이번이 마지막 1회 연장이며, 다음 리뷰에서도 라우팅되지 않으면 폐기한다.

### 2026-04-16 (1회 연장 -> 2026-07-03) - human summary와 machine artifact를 함께 남기는 proof bundle contract

Type: mixed

Why now: `all`은 coverage manifest와 trusted participant summary를 JSON 파일로 남기고, `rich`는 weekly review와 공공 API catalog export에서 사람이 읽는 summary와 기계가 읽을 수 있는 수치를 함께 만들며, `android-support`는 업로드/서명 결과를 output·env variable로 다시 노출하므로, 운영 검증 결과를 "사람용 서술 + 기계용 artifact" 한 세트로 표준화하면 배포·데이터 수집·품질 점검 이후의 handoff와 재검증이 훨씬 쉬워진다.

Likely homes: `all`, `rich`, `android-support`

Refs: `all/build.gradle.kts`, `rich/scripts/export_data_go_kr_api_catalog.py`, `rich/app/services/weekly_review.py`, `android-support/src/edits.ts`, `android-support/src/main.ts`

Note: `all.md`와 `rich.md` 모두 open ideas 상한(6개)에 도달해 있고 `android-support.md`는 이번 라운드에 이미 신규 항목을 받았다. 다음 리뷰에서 여유가 생기는 프로젝트로 라우팅한다. 이번이 마지막 1회 연장이며, 다음 리뷰에서도 라우팅되지 않으면 폐기한다.
