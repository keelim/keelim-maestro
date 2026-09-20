# youtube

Last reviewed: 2026-09-20 KST

## Signals

- `youtube/`는 루트 `AGENTS.md`가 명시하는 활성 최상위 child repo(YouTube Shorts /
  Easy Release Note 제작용, private, autonomous)이지만, 이번 워크스페이스
  스냅샷에는 디렉터리가 하이드레이트되어 있지 않아 하위 README/AGENTS.md를 직접
  읽을 수 없었다. 이 파일의 근거는 루트 `docs/CODEMAPS/*`와 root `package.json`
  / `pyproject.toml`뿐이며, 저장소가 로컬에 있을 때 다시 검증해야 한다.
- 루트 `package.json`의 `workspaces`에 `youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`가 명시돼 있고, 루트 `pyproject.toml`의 uv workspace
  members에도 `youtube`가 포함돼 있어 Bun·uv 양쪽에서 동시에 활성 워크스페이스
  멤버다.
- 그런데 `bun run typecheck:web`, `bun run build:web`, `bun run test:web`은
  `all-web-ui` / `keelim-vercel` / `rich-admin-web`만 다루고 `youtube/*` 패키지는
  포함하지 않는다 (`package.json` scripts, `docs/CODEMAPS/frontend.md`,
  `docs/CODEMAPS/SCRIPTS.md` 확인). `rich`에는 `dev:rich-web`,
  `dev:strategy-builder`, `dev:backtester` 같은 루트 헬퍼가 있지만 `youtube`에는
  대응하는 루트 dev/verify 헬퍼가 없다.

## Open ideas

### 2026-09-20 - youtube 워크스페이스 패키지 루트 검증 커버리지 격차

Status: proposed

Why now: `youtube/remotion`, `youtube/services/*`, `youtube/videos/*`는 루트
Bun workspace와 uv workspace 양쪽에 이미 등록된 활성 멤버인데, 루트에서 실행하는
`typecheck:web` / `build:web` / `test:web`은 이들을 전혀 검증하지 않는다. 즉
`youtube` 쪽 패키지가 깨져도 루트 레벨 명령으로는 감지되지 않고, `rich`처럼
전용 `dev:*` 헬퍼도 없어 로컬에서 무엇을 실행해야 하는지도 root 문서만으로는
알 수 없다.

First slice: `youtube`를 로컬에 하이드레이트한 뒤 실제 하위 `package.json` /
`pyproject.toml` 스크립트를 확인하고, `typecheck:web` 계열에 `youtube/remotion`
및 `youtube/services/*`를 포함할지, 아니면 별도의 `typecheck:youtube` /
`test:youtube` 루트 스크립트를 추가할지 결정한다. 결정 후 `docs/CODEMAPS/frontend.md`와
`docs/CODEMAPS/SCRIPTS.md`도 함께 갱신한다 (이 파일들은 `docs/idea/` 밖이므로 이번
실행에서는 격차만 기록한다).
