# rich

Last reviewed: 2026-05-07 KST

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
- `open-trading-api` 하위에 `strategy_builder`와 `backtester` 서비스가 루트 Bun 워크스페이스 멤버로 등록되어 `dev:strategy-builder`·`dev:backtester` 스크립트로 노출되어 있지만, `rich`는 아직 `origin/master`보다 앞선 로컬 커밋 상태라 이 두 서비스의 재현성이 루트에서 검증되지 않았다.

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

### 2026-05-07 - open-trading-api 서비스 경계 정의와 루트 워크스페이스 격리 게이트

Status: proposed

Why now: `rich/open-trading-api/strategy_builder`와 `rich/open-trading-api/backtester`가 루트 Bun 워크스페이스 멤버로 등록되어 `dev:strategy-builder`·`dev:backtester` 스크립트로 이미 노출되어 있다. 그러나 `rich` 레포는 아직 `origin/master`보다 앞선 로컬 커밋 상태라서, 이 두 서비스의 API/프론트엔드 계약이 루트에서 안전하게 재현되는지 검증되지 않았다.

First slice: `rich/open-trading-api` 하위 `strategy_builder`·`backtester`가 각각 어떤 API와 프론트엔드 계약을 갖는지 문서화하고, `rich` reconciliation 전까지 루트 워크스페이스 dev 스크립트가 이 두 서비스에 의존하는 경우의 실패 조건을 명시적으로 기록한다.
