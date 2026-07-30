# rich

Last reviewed: 2026-07-30 KST

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

### 2026-04-12 - Execution ledger and replay timeline

Status: proposed

Why now: The admin surface already runs manual workflows, cron-triggered
ingestion, and review flows, but the history of what happened is still
scattered across endpoints and logs.

First slice: Persist every run/retry/failure into a normalized log and render a
timeline that links each event back to the affected workflow and recovery
action.

### 2026-07-30 - 통합 신선도·연동 헬스 워치독 (2026-04-12 두 아이디어 통합)

Status: proposed

Why now: 이전에는 "데이터 신선도/이상 감시"와 "연동 헬스 콘솔"을 별도 아이디어로 다뤘지만, 둘 다 `rich`가 의존하는
Supabase, Google, GitHub CLI, pykrx/KRX 수집이 조용히 실패하거나 지연될 때 드러나는 같은 운영 위험(침묵 실패)을
다른 각도에서만 보고 있었다. `docs/CODEMAPS/backend.md`와 `data.md`가 확인하듯 스케줄 수집, 외부 데이터, Supabase 상태,
Kubernetes(Skaffold) 로컬 스택이 함께 얽혀 있어 하나의 감시 표면으로 합치는 편이 운영 복구 비용을 줄인다.

First slice: 데이터셋 최신성(마지막 갱신 시각, 예상 대비 지연), 실패/부분 실행, 업스트림 연동별 마지막 성공 시각과
재연결 상태를 한 패널에서 보여주고, 이상 징후(지표 급변, 누락 스냅샷)와 재시도/복구 액션을 함께 노출한다.

### 2026-07-30 - 서브모듈 승격 전 정합성·재현성 게이트

Status: proposed

Why now: `docs/CODEMAPS/SUBMODULES.md`의 Expansion Blockers가 "`rich` dirty/ahead 상태 — pinning 전 freeze/split 필요"를
명시하고 있고, `docs/CODEMAPS/keelim-maestro.md`의 Open Questions도 "`rich` local commits ahead of origin pending
reconciliation before pinning"을 반복해서 남긴다. `rich`는 이미 root Bun/uv 워크스페이스(`rich/web`, `keelim-rich`)에
편입되어 있어서, 정리되지 않은 상태로 오래 둘수록 워크스페이스 재현성 위험이 누적된다.

First slice: origin 대비 ahead 커밋 목록과 dirty 파일 목록을 정기적으로 스냅샷하고, freeze/split 대상 후보(어떤 커밋을
origin에 먼저 반영해야 pin이 안전한지)를 표로 정리해 pinning 준비도를 추적 가능하게 만든다.

### 2026-04-13 - 공공데이터 카탈로그 변경 피드

Status: proposed

Why now: `rich` already exports the data.go.kr API catalog, so the next leverage
point is to turn that static inventory into a watchable change feed instead of a
one-off dump.

First slice: Track a small watchlist of high-value dataset pages, diff title /
field / link changes on each export, and push meaningful updates into the
weekly review or recovery queue.
