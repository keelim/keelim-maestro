# rich

Last reviewed: 2026-08-05 KST

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
- `docs/CODEMAPS/SUBMODULES.md` / `projects/rich.md` still flag `rich` as a dirty,
  ahead-of-origin autonomous repo that must be frozen/split before it (and, per the
  same blocker list, `all-web-ui`) can become a pinned root submodule.

## Open ideas

### 2026-08-05 - Recovery cockpit and execution ledger (merged)

Status: proposed

Why now: `rich` mixes cron jobs, manual runs, Slack reminders, Google reconnects, and pykrx ingestion, so recovery work needs one place to live instead of scattered logs. This entry merges the earlier separate "Recovery cockpit for failed runs" and "Execution ledger and replay timeline" ideas, since both ultimately need the same normalized run history plus a recovery action per event.

First slice: Persist every run/retry/failure into a normalized log, surface the failed or partial ones as a queue with the exact retry or repair action, and render the full history as a timeline that links each event back to the affected workflow.

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

### 2026-08-05 - Freeze/split 전환 준비 체크리스트

Status: proposed

Why now: `docs/CODEMAPS/SUBMODULES.md`와 `docs/CODEMAPS/projects/rich.md`가 `rich`를 "dirty working tree; commits ahead of origin — freeze/split before pinning"으로 명시하고 있고, 이 상태가 `rich` 자신의 submodule 전환뿐 아니라 같은 블로커 목록에 묶인 `all-web-ui`의 submodule 전환까지 함께 막고 있다.

First slice: dirty 변경분을 정리해 origin에 반영하고 ahead 커밋을 `origin/master`로 push한 뒤 `bun run report:baseline`으로 clean 상태를 확인하는 체크리스트를 만들어, `rich`와 `all-web-ui` 두 전환 모두의 선행 조건으로 추적한다.
