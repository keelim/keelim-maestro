# rich

Last reviewed: 2026-05-08 KST

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
- `open-trading-api` 서브시스템이 추가되어 backtester(FastAPI + React), strategy builder(FastAPI + React), KIS Code Assistant MCP, KIS Trading MCP 서버까지 운영 표면이 크게 늘었다.

## Open ideas

### 2026-04-12 - 실행 이력·복구 원클릭 레저

Status: proposed

Why now: cron 작업, 수동 실행, Slack 리마인더, Google 재연결, pykrx 수집처럼 실패 비용이 큰 흐름이 늘어나고 있고, 복구 작업이 흩어진 로그와 엔드포인트에 분산되어 있다. 같은 표면에서 이력을 보고 재시도·수리까지 이어져야 운영 속도가 빨라진다.

First slice: 모든 실행/재시도/실패를 정규화된 로그로 남기고 타임라인에서 각 이벤트를 영향받은 워크플로우와 연결한다. 실패 항목마다 정확한 재시도·수리 액션을 한 장에 모아 recovery queue와 execution history를 통합한다.

### 2026-04-12 - Daily review cockpit

Status: proposed

Why now: `rich` already contains the ingredients for a strong operator ritual,
but they appear to live across separate endpoints and pages.

First slice: Create one dashboard view that combines agenda, inbox priorities,
 PyKRX flow highlights, weekly review carry-over items, journal prompts, and
 links for filing durable insights into `docs/words`.

### 2026-04-12 - Data freshness and anomaly watchdog

Status: proposed

Why now: The system depends on scheduled ingestion, external data, Supabase
 state, and edge-function style workflows, so silent staleness is a real risk.

First slice: Add a reliability panel that flags stale datasets, failed jobs,
 missing snapshots, and suspicious metric jumps before they affect downstream
 review flows.

### 2026-04-12 - Integration health console

Status: proposed

Why now: `rich` depends on Supabase, Google, GitHub CLI, pykrx/KRX, and now KIS Trading MCP access,
so auth or connection drift needs to be visible separately from stale data or
failed runs.

First slice: Add a compact health panel that shows last-success time, reconnect state, and repair action for each upstream integration — Supabase, Google, GitHub CLI, pykrx/KRX, and KIS Trading MCP.

### 2026-05-08 - 오픈 트레이딩 API 서브시스템 서비스 경계 검증

Status: proposed

Why now: `open-trading-api` 서브시스템에 backtester(FastAPI + React), strategy builder(FastAPI + React), KIS Code Assistant MCP, KIS Trading MCP 서버가 추가되어 운영 표면이 크게 늘었다. 각 서비스의 API 계약, 인증 drift, MCP 서버 연결 상태가 개별 검증 없이는 침묵 실패로 이어질 수 있다. 루트 `dev:strategy-builder`·`dev:backtester` 스크립트가 이 서브시스템을 직접 다루고 있어 로컬 개발 재현성도 함께 확인해야 한다.

First slice: backtester와 strategy builder의 backend·frontend 계약을 스모크 테스트로 검증하고, KIS MCP 서버 연결 상태와 인증 만료를 Integration health console에서 함께 표시한다.

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.
