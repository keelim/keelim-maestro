# rich

Last reviewed: 2026-07-11 KST

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
- `docs/CODEMAPS/SUBMODULES.md`는 `rich`가 dirty/ahead-of-origin 상태를 해소해야
  서브모듈로 승격될 수 있다고 명시한다(freeze/split → push → `origin/master` 대비
  clean 확인 → `bun run report:baseline`). `all-web-ui`의 서브모듈 등록도 이 상태 해소를
  기다리고 있어, `rich`의 워킹트리 위생이 워크스페이스 전체의 pinning 진행을 막는 병목이다.

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

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.
