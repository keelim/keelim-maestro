# rich

Last reviewed: 2026-04-30 KST

## Signals

- Bridges FastAPI admin services, a Next.js web surface, Supabase, GitHub
  workflow control, Google integrations, and market data ingestion.
- Already has strong operational surfaces around PyKRX, weekly review, agenda,
  and personal inbox/loop items.
- Reliability and operator leverage are at least as important as new UI pages.

## Open ideas

### 2026-04-12 - 실행 이력과 복구 큐를 하나로 묶는 운영 허브

Status: proposed

Why now: `rich`는 cron 실행, 수동 실행, PyKRX 수집, 리뷰 플로우가 함께 돌아가는데, 실행 이력과 복구 행동이 서로 다른 엔드포인트에 흩어져 있어서 실패 원인 파악과 재시도가 늦어진다.

First slice: 실행마다 입력·결과·재시도 힌트를 정규화된 로그로 저장하고, 실패·부분 실행을 단일 복구 큐에 모아 영향을 받은 워크플로우와 연결한 타임라인을 렌더링한다.

### 2026-04-12 - Daily review cockpit

Status: proposed

Why now: `rich` already contains the ingredients for a strong operator ritual,
 but they appear to live across separate endpoints and pages.

First slice: Create one dashboard view that combines agenda, inbox priorities,
 PyKRX flow highlights, weekly review carry-over items, and journal prompts.

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

### 2026-04-30 - 로컬 커밋 정리와 워크스페이스 서브모듈 확장 게이트 해소

Status: proposed

Why now: `docs/CODEMAPS/WORKSPACE.md`가 `rich`에 origin 대비 앞선 로컬 커밋이 있어서 워크스페이스 서브모듈 확장 게이트가 잠겨 있다고 명시한다. 이 상태가 지속되면 `all-web-ui` 서브모듈 전환, `quant` 정리, 다른 자율 저장소 정상화가 모두 블록된다.

First slice: 로컬 커밋을 `origin/master`에 push해 확인하고, `git submodule status`로 워크스페이스 전체 상태를 점검한 뒤 확장 게이트 해소 가능 여부를 `docs/CODEMAPS/WORKSPACE.md`에 기록한다.
