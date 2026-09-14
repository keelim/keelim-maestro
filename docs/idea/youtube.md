# youtube

Last reviewed: 2026-09-14 KST

## Signals

- `youtube`는 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 루트 uv 워크스페이스(`easy-release-note` 패키지) 양쪽에
  동시에 속한 유일한 autonomous 자식 저장소다.
- `docs/CODEMAPS/WORKSPACE.md`는 "`youtube`는 Bun 워크스페이스 멤버이지만 해당
  디렉터리가 기본 루트 체크아웃에는 존재하지 않는다"고 명시해, 하이드레이션 여부에
  따라 `bun install`/`uv` 명령 결과가 달라질 수 있음을 이미 경고하고 있다.
- 스택이 TypeScript(Remotion 렌더러, 서비스)와 Python(자동화, `>=3.13`)으로 나뉘어
  있어, 두 워크스페이스 중 한쪽에서만 새 패키지가 추가되면 다른 쪽 계약과 조용히
  어긋날 수 있다.
- 지금까지 `docs/idea/`에 전용 파일이 없어, 다른 활성 워크스페이스 멤버(`all`,
  `all-web-ui`, `keelim-vercel`, `rich` 등)와 달리 백로그 커버리지가 없었다.

## Open ideas

### 2026-09-14 - 워크스페이스 하이드레이션 프리플라이트

Status: proposed

Why now: `docs/CODEMAPS/WORKSPACE.md`와 루트 `README.md` 모두 `youtube`(그리고
`all-web-ui`, `rich`)가 로컬에 하이드레이트되어 있어야 `bun install`/uv 워크스페이스
명령이 정상 동작한다고 전제하지만, 실제로 디렉터리가 없는 체크아웃(예: 이번 정리를
수행한 원격 세션)에서는 이 전제가 조용히 깨진다.

First slice: `bun install`/`uv sync` 실행 전에 Bun 워크스페이스 glob
(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)과 uv 워크스페이스
멤버(`youtube`)가 실제로 로컬에 존재하는지 확인하는 프리플라이트 스크립트를 추가하고,
누락 시 하이드레이션 절차(README의 `git clone <private-youtube-remote-or-local-path>
youtube`)를 안내한다.

### 2026-09-14 - TS/Python 이중 워크스페이스 정합성 가드

Status: proposed

Why now: `youtube`는 Remotion/서비스(TypeScript)와 자동화(Python `>=3.13`,
`easy-release-note` 패키지)를 동시에 운영하는 유일한 워크스페이스 멤버라서, 한쪽
워크스페이스에만 새 비디오/서비스 패키지가 추가되고 다른 쪽 매니페스트가 갱신되지
않으면 두 워크스페이스가 서로 다른 상태를 신뢰하게 된다.

First slice: `youtube/services/*`, `youtube/videos/*` 각 패키지의 `package.json`과
대응하는 Python 매니페스트(있는 경우) 존재 여부, 그리고 루트
`tool.uv.constraint-dependencies` 준수 여부를 비교하는 가벼운 리포트를 만들어
`bun run report:baseline`류 검증 흐름에 붙일 후보로 남긴다.
