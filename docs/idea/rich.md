# rich

Last reviewed: 2026-06-11 KST

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
- `open-trading-api` 서브트리가 KIS MCP 서버 두 개(Code Assistant·Trading), 전략 빌더, 백테스터, Lean 실행기, 독립 FastAPI 백엔드를 포함하며 1100여 파일로 독립적으로 커지고 있어, 기존 admin 서비스와 별도의 운영 경계 관리가 필요하다.

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
 missing snapshots, suspicious metric jumps, and external API catalog drift
 (data.go.kr) before they affect downstream review flows.

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

### 2026-06-11 - open-trading-api 운영 경계 가시화

Status: proposed

Why now: `rich/open-trading-api` 서브트리는 KIS 인증, 마스터 파일 업데이트, 전략 실행, 주문 흐름이 맞물려 있지만 기존 admin 헬스 패널 어디에도 이 경계가 표시되지 않는다. 장애 발생 시 어느 레이어(KIS 인증·마스터 파일·전략 엔진·주문 라우터)가 문제인지 빠르게 파악할 수 없으면 복구 시간이 길어진다.

First slice: KIS 인증 상태, 마스터 파일 최신 여부, 전략 빌더·백테스터 API 가용성을 기존 `Integration health console` 포맷에 추가할 수 있는 패널 초안을 만들고, open-trading-api 독립 배포 여부와 root workspace 연결 상태를 한 장의 운영 경계 스냅샷으로 정리한다.
