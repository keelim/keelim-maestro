# youtube

Last reviewed: 2026-09-06 KST

## Signals

- `youtube`는 YouTube Shorts 및 Easy Release Note 제작을 위한 private autonomous
  child repo이며, 루트 README.md(407-409줄)에 따르면 원격/업스트림조차 아직 없는
  로컬 전용 checkout이다.
- 그럼에도 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 uv 워크스페이스(`easy-release-note` 패키지) 멤버로 이미
  편입되어 있다 (`docs/CODEMAPS/WORKSPACE.md`, `docs/CODEMAPS/frontend.md`,
  `docs/CODEMAPS/backend.md`).
- `docs/CODEMAPS/WORKSPACE.md`는 "youtube는 Bun 워크스페이스 멤버이지만 루트
  checkout에 기본적으로 존재하지 않는다"고 명시하며, 루트 README.md
  333-339줄은 `bun install` 전에 별도 clone이 필요하다고 안내한다.
- `scripts/local-automation.sh`(`bun run automation:local`)가 `rich`, `youtube`
  n8n, `tools/agentgateway`를 하나의 인덱스에서 위임하지만, youtube n8n
  워크플로우나 Remotion 렌더 상태를 모아 보여주는 리포트는 아직 없다.
- 기존 root idea 백로그에는 `youtube` 항목이 없어 문서/백로그 커버리지 공백으로
  남아 있었다.

## Open ideas

### 2026-09-06 - 워크스페이스 하이드레이션 프리플라이트

Status: proposed

Why now: `youtube`는 원격조차 없는 로컬 전용 checkout인데 루트 Bun/uv 워크스페이스
멤버(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`, uv
`easy-release-note`)로 이미 선언돼 있어서, 신선한 루트 클론에서 `bun install`이나
`uv sync`를 돌리면 해당 패키지가 조용히 빠지거나 뒤늦게 실패로 드러날 위험이 있다.

First slice: 루트 `bun install` / uv 명령 실행 전에 `youtube/remotion`,
`youtube/services/*`, `youtube/videos/*`와 uv 멤버 `youtube` 디렉터리 존재 여부를
확인하는 프리플라이트 스크립트를 추가하고, 없으면 실패 대신 README의 hydration
절차(operator-approved clone 경로)를 안내하는 명확한 skip 메시지를 출력한다.

### 2026-09-06 - 유튜브 자동화 상태 통합 리포트

Status: proposed

Why now: `bun run automation:local`이 rich·youtube n8n·agentgateway 런타임을 한
인덱스에서 위임하지만, 실제 n8n 워크플로우 헬스, Remotion 렌더 성공/실패,
per-video 패키지 목록은 각 런타임에 흩어져 있어 루트에서 한눈에 확인할 방법이
없다.

First slice: `automation:local` 델리게이터가 이미 아는 런타임 목록을 기반으로,
youtube n8n 워크플로우 상태·최근 Remotion 렌더 결과·`youtube/videos/*` 패키지
목록을 모으는 읽기 전용 상태 리포트를 추가한다.
