# rich

Last reviewed: 2026-06-27 KST

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

### 2026-04-12 - 실패 복구 대기열 및 실행 타임라인

Status: proposed

Why now: `rich`는 cron 작업, 수동 실행, Slack 리마인더, Google 재연결, pykrx 수집이 섞여 있어서, 실패·부분 실행 기록과 재시도/수복 경로를 한 곳에서 볼 수 없으면 복구 비용이 커진다.

First slice: 모든 실행·재시도·실패를 정규화된 로그로 저장하고, 각 항목에 정확한 재시도 또는 수복 액션을 연결하는 타임라인 뷰를 만든다. 영향받은 워크플로우로 바로 연결되는 링크를 포함한다.

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

### 2026-06-27 - 서브모듈 전환 준비 — 로컬 dirty/ahead 상태 해소

Status: proposed

Why now: SUBMODULES.md의 expansion blockers 항목에 `rich`의 dirty working tree와 origin 앞선 커밋이 명시되어 있다. 이 상태가 해소되지 않으면 `all-web-ui` 포함 워크스페이스 전체의 서브모듈 핀닝이 막히는 운영 위험이다.

First slice: `rich` 로컬 브랜치의 ahead 커밋과 dirty 파일 목록을 확인하고, upstream push → freeze → root gitlink 커밋 순서로 해소하는 단계별 체크리스트를 만든다.
