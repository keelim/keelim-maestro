# rich

Last reviewed: 2026-05-30 KST

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
- `open-trading-api/` 하위 트리(1,124 파일)에 KIS Code Assistant MCP, Kis Trading MCP, backtester, strategy_builder가 있으며, 루트 스크립트 `dev:strategy-builder`·`dev:backtester`로 진입할 수 있으나 각 표면의 운영 건강도와 진입 전제가 아직 문서화되지 않았다.

## Open ideas

### 2026-04-12 - Recovery cockpit for failed runs

Status: proposed

Why now: `rich` now mixes cron jobs, manual runs, Slack reminders, Google reconnects, and pykrx ingestion, so recovery work needs one place to live instead of scattered logs.

First slice: Collect failed or partial runs into a single queue with the exact retry or repair action, then link each item back to the affected workflow.

### 2026-04-12 - Daily review cockpit

Status: proposed

Why now: `rich` already contains the ingredients for a strong operator ritual,
but they appear to live across separate endpoints and pages.

First slice: Create one dashboard view that combines agenda, inbox priorities,
 PyKRX flow highlights, weekly review carry-over items, journal prompts, and
 links for filing durable insights into `docs/words`.

### 2026-04-12 - 연동 건강도·데이터 신선도 통합 관제판

Status: proposed

Why now: `rich`는 Supabase, Google, GitHub CLI, pykrx/KRX 연동과 크론 수집, 엣지 함수에 동시에 의존하므로, 연동 auth drift와 데이터 신선도 저하가 서로 다른 증상으로 나타난다. 두 문제를 같은 패널에서 다뤄야 침묵 실패를 빠르게 구분할 수 있다.

First slice: 업스트림별 마지막 성공 시각·재연결 상태와 수집 데이터 신선도·실패 잡 목록을 한 패널로 결합하고, 이상 징후 임계값을 초과하면 복구 행동 링크를 함께 표시한다.

### 2026-04-12 - Execution ledger and replay timeline

Status: proposed

Why now: The admin surface already runs manual workflows, cron-triggered
ingestion, and review flows, but the history of what happened is still
scattered across endpoints and logs.

First slice: Persist every run/retry/failure into a normalized log and render a
timeline that links each event back to the affected workflow and recovery
action.

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.

### 2026-05-30 - 오픈 트레이딩 API 모듈 진입점 smoke 게이트

Status: proposed

Why now: `open-trading-api/`는 KIS Code Assistant MCP, Kis Trading MCP, backtester, strategy_builder를 포함한 1,124 파일 규모의 하위 트리로, 루트에서 `dev:strategy-builder`·`dev:backtester` 스크립트로 노출된다. 그러나 각 서비스의 KIS 인증 전제, Docker 의존, MCP 프로토콜 요구사항이 문서화 없이 흩어져 있어서, 어느 표면이 실제로 동작하는지 클론 직후에 파악하기 어렵다.

First slice: 각 진입점(MCP 서버 `health_check`, backtester `/health`, strategy_builder `/health`)을 순서대로 확인하는 smoke 스크립트를 만들고, 루트 `verify` 스크립트 그룹에 포함해 환경 미설정 여부와 실행 가능 표면을 한 줄 요약으로 출력한다.
