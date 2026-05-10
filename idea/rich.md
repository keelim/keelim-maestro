# rich

Last reviewed: 2026-05-10 KST

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
- `rich/open-trading-api/`가 신규 추가됨: `strategy_builder`(frontend+backend), `backtester`(frontend+backend+kis_mcp), KIS Code Assistant MCP·Kis Trading MCP 두 서버로 구성된 한국투자증권 자동매매 플랫폼. 루트 워크스페이스에 `dev:strategy-builder`·`dev:backtester` 스크립트로 등록됨.
- `rich`는 여전히 origin 선행 커밋 상태(autonomous repo)로, open-trading-api 서브시스템의 CI 가시성이 없다.

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

### 2026-05-10 - open-trading-api KIS 서비스 계약 검증 게이트

Status: proposed

Why now: `rich/open-trading-api/`에 strategy_builder·backtester·KIS MCP 서버 두 개가 추가됐고 일부는 루트 워크스페이스 멤버로 등록됐다. KIS API 자격증명 계약, MCP 서버 기동 경로, 프론트엔드↔백엔드 통신 규약을 한 곳에서 검증하는 절차가 없어 로컬 실행과 배포 사이에 조용한 불일치가 생길 수 있다.

First slice: `bun run dev:strategy-builder`·`bun run dev:backtester`가 프론트엔드·백엔드를 실제로 기동하는지, KIS MCP 서버 두 개의 `pyproject.toml`이 기동 가능 상태인지 스모크 게이트를 만들고, `rich`의 로컬 origin 선행 커밋을 푸시한 뒤 기동 확인을 포함한다.
