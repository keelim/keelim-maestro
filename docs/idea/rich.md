# rich

Last reviewed: 2026-07-01 KST

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

First slice: Persist every run/retry/failure into a normalized log, collect failed or partial runs into a single queue with the exact retry or repair action, and render a timeline that links each event back to the affected workflow (2026-07-01: merged in the former "Execution ledger and replay timeline" entry as this idea's data layer).

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

### 2026-07-01 - 서브모듈 승격 전 정리(freeze/split) 체크리스트

Status: proposed

Why now: `docs/CODEMAPS/SUBMODULES.md`의 Expansion Blockers는 `rich`의 dirty 작업 트리와 origin 대비 ahead 커밋 상태를 root submodule 승격의 1순위 차단 요인으로 명시한다. `rich`는 root Bun/uv 워크스페이스 멤버이자 `all-web-ui`의 컨슈머이기도 해서, 이 상태가 정리되지 않으면 `all-web-ui`의 submodule 전환까지 함께 막힌다(연쇄 차단).

First slice: `rich` 프로젝트 코드맵의 Pre-Pinning Requirements(dirty 트리 freeze/split → origin 대비 ahead 커밋 push → clean 상태 확인 → `bun run report:baseline` 통과)를 순서대로 실행하는 체크리스트를 만들고, 각 단계 완료 여부를 root에서 재확인할 수 있는 자기 점검 스크립트로 남긴다.
