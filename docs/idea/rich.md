# rich

Last reviewed: 2026-08-02 KST

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

Why now: `rich` now mixes cron jobs, manual runs, Slack reminders, Google reconnects, and pykrx ingestion, so recovery work needs one place to live instead of scattered logs — and the run/retry/failure history behind those recoveries is still scattered across endpoints and logs. (Merged 2026-08-02 from the former separate "Recovery cockpit for failed runs" and "Execution ledger and replay timeline" entries — they described the same underlying data from two angles.)

First slice: Persist every run/retry/failure into a normalized log, then surface it two ways from one source: a triage queue of failed/partial runs with the exact retry or repair action, and a timeline view for replay that links each event back to the affected workflow.

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

### 2026-08-02 - rich 드리프트 프리즈 → 서브모듈 pinning 게이트

Status: proposed

Why now: `docs/CODEMAPS/SUBMODULES.md`의 Expansion Blockers가 "`rich` dirty/ahead 상태 — freeze/split before pinning"과 "`all-web-ui` — pending reconciliation of workspace blockers"를 나란히 명시하고 있고, `rich` 자체 codemap의 Pre-Pinning Requirements도 동일한 4단계(freeze/split → ahead 커밋 push → clean 확인 → `report:baseline` 재검증)를 반복해서 요구한다. 지금은 이 절차가 문서로만 존재해서, `rich`를 pin하지 못하는 상태가 `all-web-ui`의 서브모듈 전환까지 함께 막고 있다는 사실이 실행 시점에는 드러나지 않는다.

First slice: `bun run report:baseline` 출력을 기준으로 `rich`의 dirty 파일과 `origin/master` 대비 ahead 커밋을 "즉시 push 가능"과 "freeze/split 필요"로 나누는 체크리스트를 만들고, 그 결과를 `all-web-ui` pinning 판단에도 그대로 재사용할 수 있게 두 항목을 같은 리포트에서 보여준다.
