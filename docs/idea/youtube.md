# youtube

Last reviewed: 2026-09-16 KST

## Signals

- `youtube`는 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 루트 uv 워크스페이스(`easy-release-note` 패키지) 양쪽에
  동시에 등록된, 실제로 활성 상태인 autonomous child repo다.
- 여러 코드맵(`architecture.md`, `frontend.md`, `backend.md`, `WORKSPACE.md`)이
  일관되게 "신선한 root checkout에는 `youtube/` 디렉터리가 물리적으로 없고,
  `bun install`/uv 명령 전에 로컬에서 먼저 hydrate해야 한다"고 명시한다.
- 루트 `AGENTS.md`는 `bun run automation:local -- ...`을 `rich`, `youtube` n8n,
  `tools/agentgateway`용 로컬 자동화 delegator로 지정하고, readiness를 주장할 때는
  health 상태만이 아니라 `initialize`/`tools/list`/`tools/call` 같은
  method-level 호출로 증명하라고 요구한다.
- Remotion 렌더러(`youtube/remotion/`), 자동화 서비스(`youtube/services/`),
  영상 프로젝트(`youtube/videos/`)가 각각 별도 워크스페이스 멤버로 선언돼 있어,
  실제 서비스/영상 목록과 루트 워크스페이스 선언이 어긋나기 쉬운 구조다.
- 지금까지 `docs/idea/`에 `youtube` 전용 파일이 없었다. 워크스페이스 통합 범위에
  비해 백로그 커버리지가 비어 있던 문서 공백이라 이번에 신규로 채운다.

## Open ideas

### 2026-09-16 - 워크스페이스 hydration 상태 게이트

Status: proposed

Why now: 여러 코드맵이 반복해서 "`youtube/`가 신선한 checkout에는 없다"고
경고하는데도, 이를 사전에 감지하는 자동 점검은 없다. `bun install`이나 uv
명령이 `youtube`를 조용히 건너뛰면 워크스페이스 멤버 선언과 실제 상태가
말없이 어긋난 채로 남을 수 있다.

First slice: 루트 `bun install` / `uv lock --check` 실행 전에 `youtube/`,
`youtube/remotion/`, `youtube/services/`, `youtube/videos/` 디렉터리 존재 여부와
각 `package.json`/`pyproject.toml` 유무를 확인하는 사전 점검 스크립트를 추가하고,
누락 시 hydrate 명령(`git clone https://github.com/keelim/youtube.git youtube`)을
안내한다.

### 2026-09-16 - 영상/서비스 카탈로그 리포트

Status: proposed

Why now: `youtube/services/*`와 `youtube/videos/*`는 glob 패턴 워크스페이스
멤버로만 선언돼 있어서, 실제로 몇 개의 서비스·영상 프로젝트가 활성 상태인지,
어떤 것이 오래 방치됐는지 루트에서 한눈에 볼 방법이 없다. 이는 `all-web-ui`,
`keelim-plugin`에서 이미 검증된 "카탈로그화" 패턴과 동일한 leverage를 가진다.

First slice: `youtube/services/*`, `youtube/videos/*`를 스캔해 각 패키지의
이름·최근 수정 시각·`package.json` 스크립트 유무를 모으는 짧은 리포트를 만들고,
루트 `bun run` 스크립트로 노출한다.

### 2026-09-16 - n8n 자동화 method-level 콜러빌리티 증적

Status: proposed

Why now: 루트 `AGENTS.md`는 로컬 MCP/agentgateway readiness를 주장할 때 health
상태만으로는 부족하고 `initialize`/`tools/list`/`tools/call` 같은 실제 호출로
증명해야 한다고 명시하는데, `youtube` n8n 자동화 경로는 아직 이 기준을 충족하는
전용 검증 산출물이 없다.

First slice: `bun run automation:local -- ...`을 통해 `youtube` n8n 워크플로에
대해 JSON-RPC `initialize`/`tools/list` 호출 결과를 기록하는 최소 스모크
스크립트를 추가하고, 결과를 짧은 증적 파일로 남긴다.
