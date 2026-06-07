# rich

Last reviewed: 2026-06-07 KST

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
- `open-trading-api/` 서브시스템(1,100개 이상 파일)이 추가됐으며 KIS MCP 서버 2종,
  백테스터, 전략 빌더, Docker 컨테이너를 포함한다. 서브시스템 전용 AGENTS.md나 코드맵이
  없어 기존 `app/`, `web/`, `supabase/` 경계와의 관계가 불명확하다.

## Open ideas

### 2026-04-12 - 실행 복구 cockpit과 증적 타임라인

Status: proposed

Why now: `rich`는 cron 잡, 수동 실행, Slack 알림, Google 재연결, pykrx 수집 등 실패 비용이 큰 흐름을 섞어 운영하며, 각 실행의 입력·결과·재시도 힌트가 흩어져 있어 복구 판단이 늦어진다. 단일 큐와 정규화된 타임라인이 함께 있어야 재실행·감사·복구가 빨라진다.

First slice: 실패하거나 부분 완료된 실행을 단일 큐에 모으고, 각 항목에 재시도 또는 수리 행동을 붙인다. 동시에 run/retry/failure를 정규화된 로그에 남겨 영향 워크플로우로 바로 왕복하는 타임라인을 만든다.

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

### 2026-06-07 - `open-trading-api` 서브시스템 코드맵·AGENTS 경계 정립

Status: proposed

Why now: `rich` 저장소에 1,100개 이상의 파일을 담은 `open-trading-api/` 서브시스템(KIS MCP 서버 2종, 백테스터, 전략 빌더, Docker 컨테이너)이 추가됐지만, 이 서브시스템 전용 `AGENTS.md`나 코드맵 문서가 없어서 기존 `rich/app` FastAPI 경계, `rich/web` 관리자 UI, Supabase 연동과의 관계가 불명확하다. 트레이딩 API처럼 실패 비용이 큰 경계에서 문서 격차는 운영 위험이 된다.

First slice: `open-trading-api/`의 상위 진입점(MCP server, backtester, strategy_builder, kis_mcp)을 정리한 경량 코드맵 노트를 만들고, 기존 `app/`, `web/`, `supabase/` 경계와의 연결점·격리 지점을 표로 정리한다. `open-trading-api/AGENTS.md`가 없다면 최소 진입점 규칙을 문서화하는 초안을 제안한다.
