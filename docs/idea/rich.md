# rich

Last reviewed: 2026-06-09 KST

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

### 2026-04-12 - 실행 이력 & 복구 코크핏

Status: proposed

Why now: `rich`는 cron 작업, 수동 실행, Slack 알림, Google 재연결, pykrx 수집 등 다양한 실행 흐름을 섞고 있어서, 실행 이력 타임라인과 실패 복구 큐를 같은 화면에서 관리해야 한다.

First slice: 모든 실행·재시도·실패를 정규화 로그에 저장하고 각 이벤트를 영향받은 워크플로우와 복구 행동에 연결하는 타임라인을 렌더링한다. 실패·미완료 실행은 정확한 재시도·수리 행동과 함께 단일 큐로 묶는다.

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

### 2026-06-09 - 작업 트리 기준선 정리 게이트

Status: proposed

Why now: WORKSPACE.md 서브모듈 확장 게이트가 `rich` 작업 트리의 더티 상태를 명시적 차단 요인으로 기록하고 있다. 이를 해소하지 않으면 `all-web-ui` 등 자율 레포의 `.gitmodules` 승격이 계속 보류된다.

First slice: `rich` 내 더티 파일을 커밋하거나 `.gitignore`에 추가해 클린 상태를 만들고, 루트의 `bun run report:baseline` 결과에서 `rich` 차단 항목이 사라지면 정리 완료로 간주한다.
