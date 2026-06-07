# keelim-vercel

Last reviewed: 2026-05-16 KST

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

Why now: dashboard route, public page, API route, sidebar navigation, discovery
output이 따로 움직이면 실제로 열리는 표면과 사용자가 찾을 수 있는 표면이 쉽게 어긋난다.

First slice: `app/`, `app/api/`, `app/(dashboard)/layout.tsx`,
`app/(dashboard)/nav-item.tsx`, 그리고 sitemap/robots 출력이 생긴 경우까지
비교해 stale route, 누락된 navigation entry, 문서화되지 않은 API 후보를 주간
리포트로 표시한다.

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

### 2026-06-06 - 금융 어시스턴트(자연어 → 도구 라우팅) (net-new N5b)

Status: proposed

Why now: 50+ 계산기 카탈로그가 넓어 사용자가 "내 상황에 맞는 도구"를 매번 직접 찾는다.
기존 Next-best-action(룰기반 *추천 패널*)과 달리, 이건 **자연어 질의 → 적합 계산기
라우팅 + 입력값 제안**이라는 다른 축이다(리서치 §1.44의 LLM 스코어링 승격과도 구별).
(출처: `net-new-2026-06-06.md`)

First slice: 계산기 메타 인덱스를 만들고 LLM이 질의→도구를 선택해 진입 폼을 프리필한다.
Grounding: `lib/menu-config.ts`·계산기 라우트 구조에서 도구 메타 스키마 확정.

### 2026-06-06 - 첫 실행·온보딩 여정 (net-new N7)

Status: proposed

Why now: 표면이 넓어 신규 진입 사용자가 길을 잃는다. operator collection kit(컴포넌트
추출)과 달리 진입 여정 자체를 다룬다. (출처: `net-new-2026-06-06.md`)

First slice: 첫 방문 시 프로필/관심사 기반 추천 온보딩 + 빈 상태 가이드.
`all-web-ui` 온보딩 프리미티브(N6/N7)를 소비한다.

### 2026-06-06 - 웹 성능 예산 게이트 (net-new N4)

Status: proposed

Why now: `build-bottleneck`은 `all` Gradle 전용이고, 이 앱에는 번들 사이즈/Web Vitals
예산이 없어 성능 회귀가 늦게 드러난다. (출처: `net-new-2026-06-06.md`)

First slice: 빌드 산출물 번들 사이즈를 예산 임계와 대조해 초과 시 비0 종료하는 검사.
Lighthouse/Web Vitals는 헤드리스 브라우저(인프라) 필요.
