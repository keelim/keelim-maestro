# rich

Last reviewed: 2026-07-20 KST

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
- 2026-07-20: 루트 `docs/CODEMAPS/architecture.md`가 로컬 Kubernetes 스택을 명시했다 —
  `agentgateway`는 항상 켜져 있어야 하는 고정 런타임(`bun run automation:local -- start agentgateway`)이고,
  `rich`는 Skaffold로 관리되는 온디맨드 런타임(`start rich` / `standby`)이다. 두 런타임의 기동 상태 자체가
  `rich`가 의존하는 모든 MCP 연동(Supabase, Google, GitHub CLI, pykrx)보다 앞단에 있는 신뢰 전제다.

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
failed runs. Those integrations all route through `agentgateway` MCP
(`http://localhost:3000/mcp`), and `agentgateway` (always-on) plus `rich`'s own
Skaffold-managed local K8s runtime (on-demand start/standby) are the
lower-level dependency both integration health and data freshness sit on top of.

First slice: Add a compact health panel that shows last-success time, reconnect
state, and repair action for each upstream integration, and surface
`agentgateway`/`rich` Skaffold runtime state (running / standby / stopped) as a
precondition banner above the per-integration rows.

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.
