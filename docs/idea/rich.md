# rich

Last reviewed: 2026-06-13 KST

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

### 2026-06-13 - 오픈트레이딩 전략 빌더·백테스터 운영 가시화

Status: proposed

Why now: `rich/open-trading-api/strategy_builder`와 `rich/open-trading-api/backtester`가 루트 워크스페이스의 `dev:strategy-builder`·`dev:backtester` 스크립트로 노출되어 새로운 운영 표면으로 성장하고 있다. 이 서비스들의 실행 상태·API 경계·기존 PyKRX 및 weekly-review 흐름과의 데이터 의존성이 아직 운영 관제 표면에 통합되지 않아 장애나 데이터 품질 이상이 늦게 드러날 수 있다.

First slice: strategy_builder·backtester의 최신 실행 결과와 상태를 기존 recovery cockpit 또는 daily review cockpit 패널에 추가해, 다른 rich 운영 흐름과 같은 화면에서 모니터링할 수 있게 한다.
