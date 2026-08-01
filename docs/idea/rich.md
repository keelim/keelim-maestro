# rich

Last reviewed: 2026-08-01 KST

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

### 2026-04-12 - 실행 복구 콘솔과 재생 타임라인 (병합: Recovery cockpit + Execution ledger)

Status: proposed

Why now: `rich`는 cron 작업, 수동 실행, Slack 리마인더, Google 재연결, pykrx 수집이 뒤섞여 있어서 복구 작업이 흩어진 로그 대신 한 곳에서 이뤄져야 한다. 동시에 관리자 화면은 이미 수동 워크플로, cron 수집, 리뷰 플로우를 실행하지만 무엇이 언제 일어났는지는 여러 엔드포인트와 로그에 흩어져 있다.

First slice: 모든 run/retry/failure를 정규화된 로그에 남기고, 실패/부분 실행 항목을 정확한 재시도·복구 액션과 연결한 큐 겸 타임라인 뷰로 렌더링한다.

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

### 2026-08-01 - 프리즈-분할 후 서브모듈 편입 준비도 리포트

Status: proposed

Why now: 루트 `docs/CODEMAPS/SUBMODULES.md`와 `rich` 코드맵이 이미 pinning 전에 필요한 순서(dirty 상태 정리 → origin 대비 ahead 커밋 push → clean 상태 확인 → `bun run report:baseline`)를 문서화하고 있지만, 현재 상태가 그 조건을 얼마나 충족했는지는 매번 사람이 다시 확인해야 한다. `all-web-ui`의 서브모듈 전환도 이 정리가 끝나야 풀리는 선행 블로커다.

First slice: `rich`의 dirty 파일 목록, origin/master 대비 ahead 커밋 수, `bun run report:baseline` 결과를 모아 pin-ready 여부를 한 줄 상태로 보여주는 리포트를 추가하고, 조건이 모두 충족되면 `.gitmodules` 등록 다음 단계를 안내한다.
