# youtube

Last reviewed: 2026-09-24 KST

## Signals

- `youtube/`는 root Bun workspace의 활성 멤버로, `youtube/remotion`(Remotion 렌더러),
  `youtube/services/*`, `youtube/videos/*` glob 패턴으로 편입되어 있다
  (`docs/CODEMAPS/frontend.md`, `docs/CODEMAPS/WORKSPACE.md`).
- 동시에 root uv workspace의 Python >=3.13 멤버(`easy-release-note` 패키지)이기도
  하며, root `tool.uv.constraint-dependencies`를 따라야 한다
  (`docs/CODEMAPS/backend.md`, root `AGENTS.md`).
- Autonomous local repo로, 신선한 root 체크아웃에는 기본으로 존재하지 않는다.
  `bun install`이나 uv 명령을 돌리기 전에 로컬 hydration이 필요하다
  (`docs/CODEMAPS/WORKSPACE.md`).
- TypeScript(Remotion 렌더러·서비스) + Python(자동화 스택) 혼합 구조라서, 워크스페이스
  멤버십 선언(glob 패턴)과 실제 하이드레이션 상태가 어긋나면 조용히 스킵될 위험이 있다.
- 아직 `docs/CODEMAPS/projects/youtube.md`가 없고, 이전 idea 리뷰(2026-05-16)에서도
  누락되어 있었다 — 워크스페이스 멤버 목록과 idea 백로그 사이의 커버리지 갭이었다.

## Open ideas

### 2026-09-24 - 워크스페이스 하이드레이션·멤버십 드리프트 점검

Status: proposed

Why now: `youtube`는 Bun workspace와 uv workspace 양쪽의 선언된 멤버지만 root
체크아웃에는 기본으로 존재하지 않으므로, `bun install`이나 `uv` 명령이 멤버 누락을
에러 없이 조용히 건너뛸 수 있다. 이는 다른 workspace 멤버(`all-web-ui`, `rich`)와
같은 유형의 위험이지만 `youtube`에는 아직 대응하는 검증이 없다.

First slice: root `package.json`의 workspace glob과 root `pyproject.toml`의
`tool.uv.workspace.members`를 실제 로컬 디렉터리 존재 여부와 비교하는 점검을
`bun run report:baseline` 계열 스크립트에 추가하고, `youtube`가 하이드레이션되지
않은 상태에서 관련 명령이 실행되면 명확히 경고한다.

### 2026-09-24 - Remotion·서비스·비디오 프로젝트 계약 인벤토리

Status: proposed

Why now: `youtube/remotion`, `youtube/services/*`, `youtube/videos/*`는 glob
패턴으로 워크스페이스에 편입되므로, 서비스나 비디오 프로젝트가 늘어날수록 실제로
무엇이 빌드·배포 대상인지 root에서 한눈에 보기 어렵다.

First slice: 각 서브패키지 경로의 `package.json`/`pyproject.toml` 존재 여부와
glob 매칭 결과를 비교하는 인벤토리 리포트를 만들어, 워크스페이스에 잡히지 않는
프로젝트나 매니페스트 누락 후보를 표시한다.
