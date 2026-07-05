# rich

Last reviewed: 2026-07-05 KST

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
- `docs/CODEMAPS/SUBMODULES.md`(2026-07-05)는 `rich`가 origin/master 대비 dirty/ahead
  상태라 pinning이 막혀 있고, 이 상태가 풀리기 전까지 `all-web-ui`의 서브모듈 전환도
  순서대로 막혀 있다고 명시한다.

## Open ideas

### 2026-04-12 - 실행 원장과 복구 대기열 (Execution ledger + recovery cockpit, 병합 2026-07-05)

Status: proposed

Why now: `rich` now mixes cron jobs, manual runs, Slack reminders, Google reconnects, and pykrx ingestion, so recovery work needs one place to live instead of scattered logs. 기존에 별도 항목이었던 "Recovery cockpit"과 "Execution ledger and replay timeline"은 같은 문제(흩어진 실행 이력)를 데이터 레이어와 뷰 레이어로 나눠 다루던 것이라 하나의 흐름으로 합친다.

First slice: 모든 run/retry/failure 이벤트를 정규화된 로그로 남기고, 그 로그에서 실패·부분 성공 항목만 골라 정확한 재시도/복구 액션과 함께 큐로 보여주는 타임라인+대기열 뷰를 만든 뒤 각 항목을 해당 워크플로로 다시 링크한다.

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

### 2026-07-05 - dirty/ahead 정리로 서브모듈 전환 경로 확보

Status: proposed

Why now: `docs/CODEMAPS/SUBMODULES.md`의 Expansion Blockers와 `rich` 코드맵 모두 `rich`가 `origin/master` 대비 ahead + dirty 상태라서 pinning이 막혀 있다고 명시하고, 이 상태가 풀리기 전까지 `all-web-ui`의 서브모듈 전환도 순서대로 막혀 있다. 두 저장소가 autonomous 상태로 오래 남을수록 워크스페이스 재현성과 `bun run report:baseline` 신뢰도가 계속 낮게 유지된다.

First slice: `rich`의 dirty diff를 origin에 반영할 변경과 로컬 전용 변경(freeze/split 대상)으로 나누고, ahead 커밋을 `origin/master`에 푸시한 뒤 `bun run report:baseline`으로 clean 상태를 확인해 `rich` → `all-web-ui` 순서의 서브모듈 승격 체크리스트를 남긴다.
