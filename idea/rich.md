# rich

Last reviewed: 2026-05-04 KST

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
- `open-trading-api/`(1,100 파일)에 KIS Code Assistant MCP, Kis Trading MCP, 전략
  빌더(frontend+backend), 백테스터(frontend+backend)가 존재하며, 이 거래 서비스 계층은
  현재 아이디어 백로그에 완전히 미반영 상태다.

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

### 2026-05-04 - open-trading-api KIS 거래 서비스 상태 게이트

Status: proposed

Why now: `rich/open-trading-api/`는 KIS Code Assistant MCP, Kis Trading MCP,
전략 빌더, 백테스터로 구성된 1,100 파일 규모의 거래 서비스 계층인데, 현재 아이디어
백로그에는 이 표면에 대한 헬스·계약·신선도 감시가 없다. KIS API 연결 상태, MCP
서버 기동 여부, 전략 실행 결과 정합성을 추적하지 않으면 장애가 침묵으로 진행될 수
있다.

First slice: `scripts/smoke_open_trading_api_kis.py`를 기준으로 KIS 연결 상태,
MCP 서버 응답, backtester/strategy_builder 실행 경로를 묶은 최소 헬스 체크를 만들고,
결과를 기존 통합 헬스 콘솔과 연결한다.
