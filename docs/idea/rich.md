# rich

Last reviewed: 2026-05-25 KST

## Signals

- FastAPI 어드민 서비스, Next.js 웹 표면, Supabase, GitHub 워크플로우 제어, Google
  연동, 시장 데이터 수집을 함께 다루는 다층 허브다.
- `open-trading-api/`(1124 파일)에 KIS Code Assistant MCP·Kis Trading MCP·백테스터·
  전략 빌더·라이브 트레이딩 백엔드가 추가되면서 운영 표면이 기존 admin API의 두 배 이상으로 확장됐다.
- PyKRX·주간 리뷰·Google 연결 어젠다·개인 inbox/loop 등 기존 운영 루프는 계속 강화 중이다.
- 신뢰성과 운영 레버리지가 새 UI 페이지 추가만큼 중요하다.
- 공유 UI 소비와 admin 라우트 인벤토리가 프런트엔드 계약 드리프트 위험을 더하고 있다.
- `docs/words/AGENTS.md`가 투자 LLM 위키의 raw-source/wiki/schema 분리를 정의해,
  내구 가능한 리뷰 인사이트를 지식 페이지로 라우팅할 수 있다.
- `rich` 더티 워킹 트리와 autonomous 상태는 아직 해소되지 않아 루트 submodule 등록이 보류 중이다.

## Open ideas

### 2026-04-12 - 실행 이력 레저와 복구 콕핏

Status: proposed

Why now: `rich`는 cron 잡, 수동 실행, Slack 리마인더, Google 재연결, pykrx 수집, KIS MCP 호출을 함께 돌리지만, 실행 이력과 실패 큐가 흩어져 있어서 무엇이 깨졌는지와 재실행 방법을 한 화면에서 볼 수 없다.

First slice: 모든 run/retry/failure를 정규화된 로그에 영속 저장하고, 실패 항목별 재시도·복구 액션을 타임라인과 복구 큐 형태로 같이 보여주는 admin 패널을 만든다.

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

### 2026-05-25 - KIS MCP·백테스터·전략 빌더 운영 가시성

Status: proposed

Why now: `open-trading-api/`가 KIS Code Assistant MCP·Kis Trading MCP·백테스터·
전략 빌더·라이브 트레이딩 백엔드를 담으면서 운영 표면이 대폭 확장됐다. 현재 admin
대시보드와 daily review는 PyKRX/Google에 집중돼 있어 KIS MCP 서버 상태·백테스터
최근 실행 결과·전략 빌더 strategy 목록을 같은 admin 화면에서 볼 수 없다. 이 새
표면은 기존 integration health console·recovery cockpit과 같은 맥락에서 다뤄야
운영 가시성이 유지된다.

First slice: KIS MCP 서버 헬스 확인, 가장 최근 백테스트 실행 요약, 전략 빌더
strategy 목록을 읽기 전용 위젯으로 admin 대시보드에 배치하고, 기존 integration
health console과 같은 레이아웃에 붙인다.
