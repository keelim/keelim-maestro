# rich

Last reviewed: 2026-07-21 KST

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

### 2026-07-21 - Dirty/ahead 상태 해소 체크리스트 (freeze-split-reconcile)

Status: proposed

Why now: `rich`의 dirty working tree·ahead-of-origin 상태가 4월부터 지금(2026-07-21)까지 그대로 남아 있고, `docs/CODEMAPS/SUBMODULES.md`의 Expansion Blockers와 `docs/CODEMAPS/projects/all-web-ui.md`의 Submodule Conversion Blockers가 이 상태를 `rich` 자체뿐 아니라 `all-web-ui`의 submodule 전환까지 함께 막는 원인으로 반복 지목하고 있어서, 방치 비용이 두 프로젝트에 걸쳐 커지고 있다.

First slice: `docs/CODEMAPS/projects/rich.md`의 Pre-Pinning Requirements(① 혼재된 dirty 상태 freeze/split ② ahead 커밋 원격 push ③ `origin/master` 대비 clean 상태 확인 ④ `bun run report:baseline` 실행)를 실행 가능한 체크리스트로 만들어 단계별 완료 여부와 남은 ahead 커밋 목록을 추적하고, 완료 시 `all-web-ui` pinning 재개 조건과 바로 연결한다.
