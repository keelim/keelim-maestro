# youtube

Last reviewed: 2026-08-18 KST

## Signals

- `youtube`는 autonomous 로컬 리포지토리이면서 루트 Bun 워크스페이스(`youtube/remotion`,
  `youtube/services/*`, `youtube/videos/*`)와 루트 uv 워크스페이스(`youtube` 멤버, 패키지명
  없음)에 모두 등록된 활성 워크스페이스 멤버다.
- `docs/CODEMAPS/WORKSPACE.md`와 `docs/CODEMAPS/keelim-maestro.md`가 공통적으로 "youtube는
  신선한 root checkout에 기본으로 존재하지 않으며, `bun install`/uv 명령 전에 로컬에서
  hydrate해야 한다"고 명시한다.
- `docs/CODEMAPS/backend.md`, `frontend.md`, `architecture.md`는 Remotion 렌더러(TS),
  services(자동화 백엔드), videos(프로젝트별 glob 패키지)로 이루어진 혼합
  TypeScript+Python 스택이라고 설명한다.
- `rich`는 이미 `bun run dev:rich-web`, `dev:strategy-builder`, `dev:backtester` 같은 루트
  편의 래퍼를 갖고 있지만, 동일하게 autonomous·활성 워크스페이스 멤버인 `youtube`에는
  대응하는 루트 헬퍼가 아직 없다.

## Open ideas

### 2026-08-18 - 워크스페이스 하이드레이션 가드

Status: proposed

Why now: `youtube`는 Bun과 uv 워크스페이스 멤버 목록에 모두 올라 있지만 신선한 루트
checkout에는 디렉터리 자체가 없어서, hydrate하지 않은 상태로 `bun install`이나 uv
명령을 돌리면 워크스페이스가 부분적으로만 해석되며 원인이 불명확한 실패로 이어지기
쉽다.

First slice: `bun install`/`uv sync` 계열 명령 실행 전에 `youtube/`, `youtube/remotion`,
`youtube/services`, `youtube/videos`가 실제로 존재하는지 확인하고, 없으면 clone 안내와
함께 조기에 실패하는 가벼운 사전 점검 스크립트를 추가한다.

### 2026-08-18 - 렌더러·서비스·비디오 프로젝트 의존성 인벤토리

Status: proposed

Why now: `youtube/remotion`(렌더러), `youtube/services/*`(자동화 서비스),
`youtube/videos/*`(비디오별 프로젝트)가 모두 glob 기반으로 늘어날 수 있는 구조라서,
어떤 video 프로젝트가 어떤 service와 렌더러 버전에 의존하는지 한눈에 보이지 않으면
프로젝트가 늘어날수록 회귀 지점을 찾기 어려워진다.

First slice: `youtube/services/*`와 `youtube/videos/*` 패키지 매니페스트를 스캔해
video → service → remotion 의존 관계를 매트릭스로 만들고, 버전 불일치나 끊어진 참조를
표시한다.

### 2026-08-18 - 루트 편의 래퍼 격차 해소

Status: proposed

Why now: `rich`는 이미 `dev:rich-web`, `dev:strategy-builder`, `dev:backtester` 같은 루트
래퍼로 로컬 진입 비용을 낮추고 있는데, 같은 정책(autonomous 유지, 루트는 편의 래퍼만
제공)을 따르는 `youtube`에는 대응 래퍼가 없어서 hydrate 이후에도 실행 경로를 매번
다시 찾아야 한다.

First slice: hydrate된 `youtube`를 전제로 Remotion 렌더러와 대표 서비스 하나를 기동하는
최소 `bun run dev:youtube-*` 래퍼를 추가하고, 기존 `rich` 래퍼와 동일하게 child repo의
독립적인 설치·실행 책임은 그대로 둔다.
