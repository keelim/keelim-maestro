# rich

Last reviewed: 2026-06-29 KST

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

### 2026-04-12 - 복구 및 연동 헬스 콘솔

Status: proposed

Why now: `rich`는 cron 작업, 수동 실행, Slack 알림, Google 재연결, pykrx 수집을 함께 돌리면서 Supabase·Google·GitHub·pykrx 연동 상태도 각각 관리하기 때문에, 실패 복구와 외부 연동 상태가 같은 콘솔에서 보이지 않으면 침묵 실패를 늦게 발견한다.

First slice: 실패/부분 실행을 재시도·수리 액션과 연결한 단일 큐로 모으고, 각 업스트림 연동의 마지막 성공 시각·재연결 상태·수리 행동을 같은 패널에 표시한다.

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

### 2026-04-12 - Execution ledger and replay timeline

Status: proposed

Why now: The admin surface already runs manual workflows, cron-triggered
ingestion, and review flows, but the history of what happened is still
scattered across endpoints and logs.

First slice: Persist every run/retry/failure into a normalized log and render a
timeline that links each event back to the affected workflow and recovery
action.

### 2026-06-29 - rich 저장소 상태 정리와 워크스페이스 서브모듈 전환 게이트

Status: proposed

Why now: 루트 SUBMODULES.md가 `rich`의 더티 워킹 트리와 origin 선행 커밋을 워크스페이스 확장 차단 요소로 명시하고 있으며, 이 상태가 해소되지 않으면 `all-web-ui` 서브모듈 전환도 계속 보류된다. 운영 기능 작업보다 저장소 상태 정리가 더 먼저 필요한 시점이다.

First slice: `rich`의 더티 파일과 origin 선행 커밋 목록을 확인하고, freeze/split 경계를 정한 뒤 `bun run report:baseline`이 clean 상태를 보고하도록 만든다. 이후 `all-web-ui` 서브모듈 게이트 해제 여부를 재판단한다.

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.
