# rich

Last reviewed: 2026-07-23 KST

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
- `docs/CODEMAPS/architecture.md`는 `rich`가 Skaffold로 관리되는 로컬 Kubernetes 스택의 유일한 on-demand 워크로드이고, 모든 MCP 호출이 `agentgateway`(항상 실행 상태 유지 필요)를 통과한다고 기록한다. 이 로컬 스택 자체의 기동 상태는 지금까지 어떤 idea에도 반영되지 않았다.

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

### 2026-04-12 - Integration health console (+ 로컬 K8s/agentgateway 상태)

Status: proposed

Why now: `rich` depends on Supabase, Google, GitHub CLI, and pykrx/KRX access,
so auth or connection drift needs to be visible separately from stale data or
failed runs. 여기에 더해 `agentgateway`(항상 실행 유지)와 `rich`의 Skaffold 로컬 K8s
루프(on-demand start/standby)가 실제로 기대 상태인지도 같은 운영 건강도 표면에서
봐야, MCP 라우팅 실패의 원인이 외부 연동인지 로컬 스택 자체인지 빠르게 구분할 수 있다.

First slice: Add a compact health panel that shows last-success time, reconnect
state, and repair action for each upstream integration. 같은 패널에 `agentgateway`
기동 여부와 `rich` Skaffold 스택의 start/standby 상태를 추가해, 로컬 인프라 문제를
외부 연동 장애와 구분해서 보여준다.

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.
