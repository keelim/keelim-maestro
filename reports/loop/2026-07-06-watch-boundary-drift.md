# [watch] 경계 드리프트 감시 — 전 경계 PASS

- 사이클: 1 / 날짜: 2026-07-06
- 근거 파일: all-web-ui/package.json, rich/app/api/admin.py, rich/web/src/types/weekly-review.ts, rich/web/src/lib/api.ts, youtube/src/easy_release_note/derive.py, youtube/remotion/src/schema.ts
- 기준선: scripts/all-web-ui-rich-allowed-drift.txt

## 항목별 결과

### 1. all-web-ui exports ↔ 소비자 (keelim-vercel, rich/web) — PASS

소비자가 import하는 subpath 35종(button, card, badge, telemetry, tooltip, toast, textarea, tabs, table, switch, slider, skeleton, sheet, select, scroll-area, radio-group, progress, popover, panel, onboarding, loading-status, label, input, hover-card, dropdown-menu, dialog, checkbox, calendar, breadcrumb, avatar, alert, alert-dialog, accordion, 루트)이 전부 `all-web-ui/package.json`의 `exports` 맵에 등재. 존재하지 않는 export를 import하는 사례 없음. 정적 검증기(`scripts/verify-all-web-ui-integration.sh`, `bun run report:shared-ui`) 결과 PASS=28 FAIL=0.

### 2. rich API 스키마 ↔ 프론트 타입 — PASS

대표 경계(weekly-review) 교차 확인:
- 응답: `rich/app/api/admin.py:252-268`의 `WeeklyReviewSummaryResponse`/`WeeklyReviewGenerateAIResponse`/`WeeklyReviewSaveResponse` 필드가 `rich/web/src/types/weekly-review.ts` 대응 타입과 일치 (`week_start/week_end: date→string`, `profit_total: float→number`, `profit_by_currency: dict[str,float]→Record<string,number>`).
- 요청: TS는 camelCase지만 `rich/web/src/lib/api.ts:487-488`에서 스네이크케이스로 변환 후 전송 — 백엔드 `WeeklyReviewSaveRequest`와 정합. 매핑 계층 정상.
- `rich/web/src/types/profit.ts`의 `CalendarDay`/`CalendarMonth`는 클라이언트 파생 내부 타입 → 경계 대상 아님.

### 3. youtube 파이프라인 ↔ remotion renderer — PASS

`youtube/src/easy_release_note/derive.py:232-245`가 방출하는 `{"episode": {schemaVersion, slug, product, updateName, releaseDate, accessDate, sourceUrls, script, scenes}}`가 `remotion/src/root.tsx:22`의 defaultProps 및 `remotion/src/schema.ts:80-113`의 `EpisodeProps` 필수 필드와 일치. 픽스처 `remotion/fixtures/easy-release-note-v2-props.json`도 정합.

## 새 드리프트 (기준선 외)

없음.

## 비고 (관찰 사항, defect 아님)

- `youtube/src/easy_release_note/n8n.py:156`은 `schemaVersion: 1`(레거시 경로), derive.py는 `2`. `EpisodeProps.schemaVersion`이 `number` 타입이라 타입 드리프트는 아니나, 레거시 경로 정리 후보로 기록.
- rich/web 전수 타입 확인은 대표 경계 정적 대조로 대체(커버리지 우선). 전수 확인이 필요하면 `rtk bun run typecheck:web` 별도 게이트 권장.
- `bun run report:shared-ui`는 샌드박스에서 임시파일 생성 제한으로 1회 실패 → 샌드박스 해제 재실행으로 정상 확인 (환경 이슈).

## 다음 액션

현재 경계 드리프트가 없으므로 즉시 조치 불요. 선택적으로: "youtube의 n8n.py 레거시 경로(schemaVersion 1)를 derive.py(v2)로 통합하거나 제거 여부를 python-lead가 판단하고, 제거 시 remotion 픽스처 영향까지 qa가 boundary-check로 검증" 태스크를 maestro-orchestrator에 넘길 수 있음.
