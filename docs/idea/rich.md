# rich

Last reviewed: 2026-07-04 KST

## Signals

- Bridges FastAPI admin services, a Next.js web surface, Supabase, GitHub
  workflow control, Google integrations, and market data ingestion.
- Already has strong operational surfaces around PyKRX, weekly review, Google-connected agenda,
  and personal inbox/loop items.
- Reliability and operator leverage are at least as important as new UI pages.
- Shared UI consumption and admin route inventory now add frontend contract drift
  to the existing backend/workflow reliability surface.
- `docs/words/AGENTS.md` defines a raw-source/wiki/schema split for an investing
  LLM wiki, so durable review insights can be routed back into knowledge pages.
- 루트 `scripts/all-web-ui-rich-allowed-drift.txt`가 `rich/web`에서 아직 `all-web-ui` 공용
  프리미티브로 옮겨가지 못한 파일 11개를 명시적으로 허용목록화하고 있고,
  `scripts/verify-all-web-ui-integration.sh`의 `rich_web_generic_drift_is_allowlisted`
  체크가 이 목록과 실제 drift 파일 집합이 정확히 일치할 때만 통과한다.

## Open ideas

### 2026-04-12 - 실행·재시도 통합 콘솔 (구 "Recovery cockpit" + "Execution ledger and replay timeline" 통합)

Status: proposed

Why now: `rich`는 cron ingestion, 수동 실행, Slack 리마인더, Google 재연결까지 여러 실행 경로를 섞어 쓰는데, 실패/재시도 이력이 로그 여기저기 흩어져 있어서 복구 액션과 실행 타임라인을 따로 관리하던 두 아이디어(복구 큐, 재생 타임라인)는 사실상 같은 표면이 필요하다.

First slice: 모든 run/retry/failure를 정규화된 로그로 남기고, 실패·부분 실행 항목은 정확한 재시도/복구 액션과 함께 큐 형태로, 전체 이력은 타임라인 형태로 같은 데이터에서 렌더링한다.

### 2026-04-12 - Daily review cockpit

Status: proposed

Why now: `rich` already contains the ingredients for a strong operator ritual,
but they appear to live across separate endpoints and pages.

First slice: Create one dashboard view that combines agenda, inbox priorities,
 PyKRX flow highlights, weekly review carry-over items, journal prompts, and
 links for filing durable insights into `docs/words`.

### 2026-04-12 - 데이터 신선도·연동 헬스 워치독 (구 "Data freshness and anomaly watchdog" + "Integration health console" 통합)

Status: proposed

Why now: 스케줄 ingestion, 외부 데이터, Supabase 상태, edge-function 워크플로우, 그리고 Supabase/Google/GitHub CLI/pykrx 연동까지 침묵 실패 지점이 여러 개인데, "데이터가 오래됐다"와 "연동이 끊겼다"를 따로 보면 원인 파악이 늦어진다. 두 워치독 아이디어를 하나의 운영 헬스 패널로 합친다.

First slice: 데이터셋 신선도, 실패한 job, 누락된 스냅샷, 이상 지표 점프와 함께 Supabase/Google/GitHub CLI/pykrx 각 연동의 last-success 시각·재연결 상태·복구 액션을 한 패널에서 보여준다.

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.

### 2026-07-04 - rich/web 잔여 drift 허용목록 축소 로드맵

Status: proposed

Why now: `scripts/all-web-ui-rich-allowed-drift.txt`가 `rich/web`에서 로컬 프리미티브·Radix 직접 사용·테이블/패널/버튼 클래스를 아직 자체 소유 중인 파일 11개(`money/quant/page.tsx`, `google-agenda-auth-panel.tsx`, `profit-note-panel.tsx`, `review-flagged-profit-note-panel.tsx`, `money-dividend-page-content.tsx`, `money-sentiment-page-content.tsx`, `profit-calendar.tsx`, `support-funds-page-content.tsx`, `today-day-trade-amount-panel.tsx`, `work-triage-page-content.tsx`, `weekly-review-page-content.tsx`)를 명시적으로 나열하고, 검증 스크립트는 이 목록과 실제 drift 파일 집합이 "정확히 같을 때만" 통과시킨다. 즉 마이그레이션이 멈춰 있다는 사실 자체가 이미 게이트로 드러나 있는데, 그 목록을 줄여나가는 로드맵은 아직 없다.

First slice: 허용목록 11개 파일을 우선순위(가장 많이 재사용되는 패턴부터)로 정렬한 마이그레이션 순서를 정하고, 파일 하나를 `all-web-ui` 프리미티브로 옮길 때마다 허용목록에서 제거해 검증 스크립트가 잔여 drift 축소를 그대로 측정하게 만든다.
