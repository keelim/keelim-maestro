# rich

Last reviewed: 2026-06-24 KST

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

### 2026-04-12 - 실행 증적·복구 통합 코크핏

Status: proposed (2026-04-12 제안; 2026-06-24 병합·확장)

Why now: cron 잡, 수동 실행, PyKRX 수집, Slack 리마인더, Google 재연결처럼 실패 비용이 큰 흐름이 늘어나서, 입력·결과·재시도 힌트를 같은 표면에서 남기고 다시 재생할 수 있어야 운영 복구가 빨라진다. 현재는 실행 타임라인이 흩어진 로그와 엔드포인트에 분산되어 있어 원인 역추적 비용이 크다.

First slice: 모든 실행·재시도·실패를 정규화된 로그에 저장하고 타임라인으로 보여주는 단일 패널을 만들고, 각 항목에서 영향받은 워크플로우와 복구 행동으로 바로 연결한다.

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

### 2026-06-24 - 알고 트레이딩 서브앱 운영 상태 가시화

Status: proposed

Why now: `rich`의 open trading API는 `strategy_builder`와 `backtester` 두 서브앱을 독립적으로 실행하는데(`bun run dev:strategy-builder`, `bun run dev:backtester`), 각 서브앱의 실행 상태·마지막 성공 시각·오류 원인이 메인 admin 대시보드에서 보이지 않아 운영 사각지대가 생긴다.

First slice: 두 서브앱의 마지막 실행 시각, 상태, 오류 요약을 admin 대시보드 헬스 패널에 통합하고, 개별 서브앱 로그로 바로 이동할 수 있는 링크를 추가한다.
