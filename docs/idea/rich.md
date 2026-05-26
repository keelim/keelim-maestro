# rich

Last reviewed: 2026-05-26 KST

## Signals

- Bridges FastAPI admin services, a Next.js web surface, Supabase, GitHub
  workflow control, Google integrations, and market data ingestion.
- Already has strong operational surfaces around PyKRX, weekly review, Google-connected agenda,
  and personal inbox/loop items.
- `open-trading-api/`가 1,000+ 파일의 독립 서브시스템으로 성장했고, KIS MCP 서버 2개
  (KIS Code Assistant MCP, Kis Trading MCP), backtester, strategy builder 프론트엔드와
  FastAPI 백엔드를 포함한다. `web/src/app/api/open-trading/[service]/[...path]` 프록시
  라우트가 admin web과 이 서브시스템을 연결한다.
- `web/` admin 표면이 strategy-lab, work-triage, dividends, journal, sentiment, signals,
  support-funds 등 새 페이지와 workspace-dashboard API 라우트로 크게 확장됐다.
- Reliability and operator leverage are at least as important as new UI pages.
- Shared UI consumption and admin route inventory now add frontend contract drift
  to the existing backend/workflow reliability surface.
- `docs/words/AGENTS.md` defines a raw-source/wiki/schema split for an investing
  LLM wiki, so durable review insights can be routed back into knowledge pages.

## Open ideas

### 2026-04-12 - Recovery cockpit for failed runs

Status: proposed

Why now: `rich` now mixes cron jobs, manual runs, Slack reminders, Google reconnects, and pykrx ingestion, so recovery work needs one place to live instead of scattered logs.

First slice: Collect failed or partial runs into a single queue with the exact retry or repair action, then link each item back to the affected workflow.

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

### 2026-04-12 - Execution ledger and replay timeline

Status: proposed

Why now: The admin surface already runs manual workflows, cron-triggered
ingestion, and review flows, but the history of what happened is still
scattered across endpoints and logs.

First slice: Persist every run/retry/failure into a normalized log and render a
timeline that links each event back to the affected workflow and recovery
action.

### 2026-04-12 - Integration health console

Status: proposed

Why now: `rich` depends on Supabase, Google, GitHub CLI, and pykrx/KRX access,
so auth or connection drift needs to be visible separately from stale data or
failed runs.

First slice: Add a compact health panel that shows last-success time, reconnect
state, and repair action for each upstream integration.

### 2026-05-26 - open-trading-api 운영 경계와 MCP 서버 게이트

Status: proposed

Why now: `open-trading-api/`가 1,000+ 파일의 독립 서브시스템으로 성장했고 KIS MCP 서버
2개(KIS Code Assistant MCP, Kis Trading MCP)와 backtester·strategy builder를 포함한다.
`web/src/app/api/open-trading/[service]/[...path]` 프록시 라우트가 admin web과 이
서브시스템을 연결하지만, 이 경계가 조용히 깨져도 지금은 감지 수단이 없어서 전체
trading 워크플로우가 영향을 받는다.

First slice: `open-trading-api` 백엔드 healthcheck, KIS MCP 서버 가용성 확인, 프록시
라우트 계약을 묶어 한 번에 확인하는 slim integration gate를 만들고, `rich/app` admin
API와의 경계 계약을 명시한다.
