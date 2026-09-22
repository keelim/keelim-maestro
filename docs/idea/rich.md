# rich

Last reviewed: 2026-09-22 KST

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

### 2026-04-12 - Recovery cockpit and execution ledger

Status: proposed

Why now: `rich` mixes cron jobs, manual runs, Slack reminders, Google reconnects, and pykrx ingestion, so recovery work and run history both need one place to live instead of scattered logs and endpoints — treating them as two separate cockpits would just duplicate the same underlying run/failure data (merged from the former "Recovery cockpit" and "Execution ledger and replay timeline" entries).

First slice: Persist every run/retry/failure into a normalized log, then render both a recovery queue (exact retry/repair action per item) and a timeline view from that same log, linking each entry back to the affected workflow.

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

### 2026-09-22 - 커밋 프리즈·스플릿 체크리스트

Status: proposed

Why now: `docs/CODEMAPS/SUBMODULES.md`가 `rich`를 "dirty working tree; commits ahead of origin; freeze/split before pinning"로 명시된 확장 차단 요인으로 이미 지목하고 있어서, 서브모듈 전환 전에 정확히 무엇을 freeze/split해야 하는지 보이는 목록이 없으면 같은 차단이 계속 반복된다.

First slice: ahead-of-origin 커밋과 dirty 변경분을 브랜치별로 분류해 즉시 병합 가능/보류/스플릿 필요로 나눈 체크리스트를 만들고, 각 항목에 필요한 후속 작업(리뷰, 스플릿 PR, 폐기)을 표시한다.
