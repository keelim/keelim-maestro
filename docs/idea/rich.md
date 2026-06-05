# rich

Last reviewed: 2026-06-05 KST

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
- `open-trading-api/` 아래에 KIS Code Assistant MCP, Kis Trading MCP, 백테스터(프론트+백엔드),
  전략 빌더(프론트+백엔드)가 별도 서비스 레이어로 존재한다(2026-05-27 코드맵 기준 전체 1,834개 파일).
  이 표면은 기존 admin API·PyKRX 흐름과 독립적으로 움직이고 있어서 운영 가시성을 별도로 확보해야 한다.

## Open ideas

### 2026-04-12 - 실패 복구 cockpit 및 실행 ledger

Status: proposed

Why now: `rich`는 cron 잡, 수동 실행, Slack 리마인더, Google 재연결, PyKRX 수집을 함께 돌리는데 실패·재시도·이력이 흩어진 로그에만 남아서 복구 비용이 크다. 실행 이력을 정규화된 타임라인에 남기면 어떤 흐름이 깨졌는지, 재시도나 복구에 무엇이 필요한지를 한 화면에서 볼 수 있다.

First slice: 각 실행·재시도·실패 이벤트를 정규화된 로그에 저장하고, 실패 항목에 대한 정확한 재시도 또는 수동 복구 액션을 함께 표시하는 타임라인 패널을 만든다.

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

### 2026-06-05 - Open Trading API MCP 서비스 운영 가시화

Status: proposed

Why now: `rich/open-trading-api/` 아래에 KIS Code Assistant MCP, Kis Trading MCP, 백테스터(프론트+백엔드), 전략 빌더(프론트+백엔드)가 독립적인 서비스 레이어로 실행된다. 이 표면은 기존 `rich/app` admin API·PyKRX 흐름과 별도로 움직이고 있어서, MCP 서버 상태·거래 실행 결과·백테스트 이력을 현재 관제 화면에서 확인할 수 없고 장애 감지도 늦어진다.

First slice: KIS Trading MCP·KIS Code Assistant MCP의 현재 엔드포인트와 인증 경계를 정리하고, 백테스터/전략 빌더 백엔드와의 데이터 흐름을 기존 admin 관제 표면에서 확인할 수 있는 최소 상태 패널을 만든다.
