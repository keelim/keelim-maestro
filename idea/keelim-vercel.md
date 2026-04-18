# keelim-vercel

Last reviewed: 2026-04-18 14:38 KST

## Signals

- Large Next.js finance product with many calculator and dashboard routes.
- Mixes Supabase-backed content, market data, newsletter flows, and persistent
  client storage.
- The current surface is wide, which makes cross-tool continuity more valuable
  than adding isolated single-purpose pages forever.
- 최근 도구 사용 추적과 목표 체크인 표면이 붙고 있어서, 단순 페이지 확장보다 후속 행동 루프를 강화하는 쪽이 더 크다.
- `all-web-ui`가 로컬 sibling repo로 붙어 있어, 어댑터와 실제 import 경로가 어긋나면 소비자 앱에서 늦게 깨질 수 있다.

## Open ideas

### 2026-04-12 - Tool usage heatmap and dead-surface cleanup

Status: proposed

Why now: The app already tracks `tool_clicks` and exposes a wide route inventory, so usage data can drive pruning and promotion instead of manual guesswork.

First slice: Produce a weekly report that ranks tools by real usage, flags long-unused surfaces, and suggests consolidation candidates.

### 2026-04-12 - Next-best-action feed across finance tools

Status: proposed

Why now: The product has enough calculators, market widgets, and saved surfaces
  that users would benefit from guidance on what to do next instead of choosing
  from a long catalog every time, especially after a tool run or goal check-in.

First slice: Build a small recommendation panel that uses recent tool history,
  bookmarks, and a few profile signals to suggest the next relevant workflow or
  goal-check-in card.

### 2026-04-13 - 라우트 계약 드리프트 감시

Status: proposed

Why now: `/admin`, `/login`, `/agenda`, `/tqqq-checklist`, `/review` 같은
별칭과 `sitemap.xml`, admin route inventory가 분리돼 있어서 실제 라우트와
문서/색인 사이에 drift가 생기기 쉽다.

First slice: `web/src/features/admin/admin-route-inventory.ts`,
`web/src/app/sitemap.xml`, legacy redirect 라우트, 실제 app directory를
비교해 stale alias와 누락/중복 경로를 주간 리포트로 표시한다.

### 2026-04-14 - 신규 기능 배지 예산 감시

Status: proposed

Why now: `AGENTS.md`에 `isNew: true`가 정확히 4개만 유지돼야 한다는 규칙이 있어서, 기능이 늘어날수록 메뉴 배지와 changelog가 서로 어긋나기 쉽다.

First slice: `lib/menu-config.ts`의 신규 배지 개수, `app/changelog/page.tsx`의 최신 추가 항목, 실제 라우트 노출을 비교해서 오래된 배지를 먼저 내리고 새 기능 승격 후보를 표시한다.

### 2026-04-14 - 공용 UI 어댑터 계약 스냅샷

Status: proposed

Why now: `all-web-ui`를 로컬 sibling repo로 쓰는 동안 adapter export와 실제 import 경로가 조금만 어긋나도 `keelim-vercel` 쪽에서 런타임보다 늦게 회귀가 드러난다.

First slice: `components/shared/all-web-ui-adapters.tsx`와 downstream import 지점을 스캔해, 사용 중인 primitive와 경로를 한 장의 manifest로 묶고 변경 diff를 보여준다.

### 2026-04-18 - 스토리지 키 레지스트리 드리프트 게이트

Status: proposed

Why now: `lib/*storage.ts`와 `storage-version-registry.ts`가 실제로 같은 저장 키 계약을 지켜야 하므로, 레지스트리 누락이나 stale sidecar가 생기면 사용자 설정이 조용히 깨질 수 있다.

First slice: 저장소 키 상수와 registry 등록 목록을 비교하는 보고서를 만들고, 누락/불일치/정체된 마이그레이션 후보를 주간 점검에 띄운다.
