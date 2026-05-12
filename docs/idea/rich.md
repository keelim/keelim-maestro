# rich

Last reviewed: 2026-05-12 KST

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
- `open-trading-api/` 서브시스템이 추가되어 KIS Code Assistant MCP·KIS Trading MCP 서버 2개와 backtester·strategy_builder(각각 FastAPI 백엔드 + Next.js 프론트엔드)가 Docker 기반으로 운영된다. 기존 admin API와 별개의 KIS API 인증·런타임 경로를 갖는다.

## Open ideas

### 2026-04-12 - 복구 코크핏·실행 원장

Status: proposed

Why now: `rich`는 크론 작업, 수동 실행, Slack 알림, Google 재연결, pykrx 수집이 뒤섞여 있어서, 실패·부분 실행을 단일 큐에 모으고 입력·재시도·복구 힌트를 타임라인으로 남겨야 운영 복구가 빨라진다.

First slice: 실패하거나 일부만 완료된 실행을 단일 큐로 수집해 정확한 재시도·복구 행동과 함께 보여주고, 모든 실행·재시도·실패를 정규화된 로그에 저장해 영향 받은 워크플로우로 바로 연결되는 타임라인으로 렌더링한다.

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
failed runs. `open-trading-api/` 서브시스템이 추가되면서 KIS API 인증 및 두 MCP 서버 연결 상태도 같은 관점에서 관리해야 한다.

First slice: Add a compact health panel that shows last-success time, reconnect
state, and repair action for each upstream integration — Supabase, Google,
GitHub CLI, pykrx/KRX, KIS API (backtester/MCP 경로 포함).

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.

### 2026-05-12 - open-trading-api 서브시스템 격리 smoke gate

Status: proposed

Why now: `open-trading-api/`는 두 개의 MCP 서버(KIS Code Assistant MCP, KIS Trading MCP)와 backtester·strategy_builder 백엔드·프론트엔드를 포함하는 독립 서브시스템으로, root Bun 워크스페이스에 `dev:backtester`·`dev:strategy-builder` 경로가 등록되어 있지만 기존 admin API 헬스체크와 분리된 상태다. `scripts/smoke_open_trading_api_kis.py`가 이미 존재하므로 이를 확장하면 최소 비용으로 서브시스템 전체를 검증할 수 있다.

First slice: `scripts/smoke_open_trading_api_kis.py`를 기반으로 backtester·strategy_builder 백엔드 기동 여부, MCP 서버 응답, KIS API 연결 상태를 묶은 서브시스템 smoke gate를 만들고, root `bun run dev:backtester`·`dev:strategy-builder` 실행 경로와 함께 CI에서 확인한다.
