# youtube

Last reviewed: 2026-08-22 KST

## Signals

- `youtube`는 root Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 root uv 워크스페이스(`easy-release-note` 패키지)에
  동시에 속한 자율 로컬 저장소다.
- `docs/CODEMAPS/WORKSPACE.md`는 `youtube`가 워크스페이스 멤버이면서도 "기본
  루트 체크아웃에는 디렉터리가 없다"고 명시해, `bun install`/`uv sync` 전에
  로컬 hydration이 선행돼야 함을 보여준다.
- `youtube/services/*`, `youtube/videos/*`는 개수가 늘어날 수 있는 glob
  멤버라서, 각 하위 패키지가 root Bun catalog·uv constraint-dependencies
  버전을 벗어나도 지금은 개별적으로만 발견된다.
- 루트 `README.md`는 `youtube`를 원격(upstream) 없는 private 로컬 체크아웃으로
  기록하고 있어, 워크스페이스 선언과 실제 소스 가용성 사이에 간극이 있다.

## Open ideas

### 2026-08-22 - 워크스페이스 멤버십 vs 로컬 hydration 격차 감시

Status: proposed

Why now: `WORKSPACE.md`는 `youtube`가 Bun/uv 워크스페이스 멤버이지만 기본
체크아웃에는 디렉터리가 없다고 명시한다. 이 상태에서 `bun install`이나
`uv sync`를 돌리면 glob 멤버(`youtube/services/*`, `youtube/videos/*`)가
조용히 비거나 실패해도 원인이 바로 드러나지 않는다.

First slice: 루트 workspace 선언(`package.json` workspaces,
`pyproject.toml` uv workspace members)과 실제 로컬 디렉터리 존재 여부를
비교하는 점검 스크립트를 추가해, hydration이 필요한 멤버를 설치 전에 명시적
으로 경고한다.

### 2026-08-22 - glob 패키지 카탈로그·제약 정합성 리포트

Status: proposed

Why now: `youtube/services/*`, `youtube/videos/*`는 개수가 늘어날 수 있는
glob 멤버라서, 각 하위 패키지가 root Bun catalog나 uv
`constraint-dependencies`에서 벗어난 버전을 선언해도 지금은 개별적으로만
발견할 수 있다.

First slice: 각 glob 하위 패키지의 `package.json`/`pyproject.toml` 의존성
버전을 root catalog·constraint 표와 비교하는 리포트를 만들어, 드리프트가
생긴 패키지를 목록으로 보여준다.
