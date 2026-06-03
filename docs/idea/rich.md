# rich

Last reviewed: 2026-06-03 KST

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
- `open-trading-api/` 하위 표면이 1,124개 파일 규모로 성장해 KIS MCP 서버 2개(Docker), 전략 빌더 프론트/백엔드, 백테스터(황금 파일 기반 테스트)를 포함하며, `rich/web`에는 `strategy-lab` 라우트 패밀리와 `work-triage` 표면이 이미 연결돼 있다.

## Open ideas

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

### 2026-04-12 - Execution ledger, replay timeline, and recovery queue

Status: proposed

Why now: The admin surface runs manual workflows, cron-triggered ingestion, and
review flows, but execution history and recovery actions are scattered across
endpoints and logs — so a failed run that needs a specific retry or repair
is hard to find and reproduce.

First slice: Persist every run/retry/failure into a normalized log and render a
timeline that links each event back to the affected workflow; surface failed or
partial runs in a recovery queue with the exact retry action and affected
workflow link.

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

### 2026-06-03 - open-trading-api MCP·전략·백테스터 통합 건강도 게이트

Status: proposed

Why now: `open-trading-api/`가 1,124개 파일 규모로 성장해 KIS MCP 서버 2개(Docker), 전략 빌더 프론트/백엔드, 백테스터(황금 파일 기반 테스트)를 포함하며, `rich/web`의 `strategy-lab` 라우트 패밀리가 이 계층에 의존한다. 그러나 이 하위 계층의 서비스 기동·API 연결·백테스터 결과 일관성을 확인하는 공통 건강도 게이트가 없어서, 회귀가 main admin 표면에 늦게 드러날 수 있다.

First slice: KIS MCP 서버 기동 가능성, 전략 빌더 백엔드 ping, 백테스터 황금 파일 smoke 검증을 묶은 통합 건강도 스크립트(`scripts/smoke_open_trading_api_kis.py` 확장)를 만들고, `rich/web`의 `strategy-lab` 운영자 피드백 패널에서 결과를 표시하게 연결한다.
