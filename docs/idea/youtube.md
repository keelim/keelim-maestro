# youtube

Last reviewed: 2026-09-12 KST

## Signals

- `AGENTS.md`는 `youtube`를 아홉 개 자율 자식 저장소 중 하나로 명시하고, `/youtube` 정책 절에서
  YouTube Shorts / Easy Release Note 제작용 비공개 자율 저장소로 규정한다.
- `docs/CODEMAPS/WORKSPACE.md`는 `youtube`를 Bun 워크스페이스(`youtube/remotion`,
  `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(`easy-release-note` 패키지)
  양쪽 모두의 활성 멤버로 기록하면서, 동시에 "youtube is a Bun workspace member but its
  directory is not present in the root checkout by default"라고 명시한다.
- `docs/CODEMAPS/backend.md`, `frontend.md`, `architecture.md`도 동일하게 `youtube`를
  Remotion 렌더러 + 서비스 + 비디오 프로젝트로 구성된 활성 워크스페이스 멤버로 설명한다.
- 반면 `docs/CODEMAPS/projects/README.md`의 "Generated Snapshots" 표와
  `docs/CODEMAPS/projects/` 디렉터리에는 `youtube`용 프로젝트 코드맵이 아예 없다 —
  `all`, `all-web-ui`, `android-support`, `Keelim-Knowledge-Vault`, `keelim-plugin`,
  `keelim-vercel`, `rich`, `toto`는 모두 스냅샷이 있는데 `youtube`만 빠져 있다.
- 지금까지 루트 idea 백로그(`docs/idea/`)에도 `youtube` 전용 파일이 없어서, 활성 워크스페이스
  멤버인데도 백로그 커버리지가 비어 있는 문서 격차가 있다.

## Open ideas

### 2026-09-12 - 워크스페이스 하이드레이션 상태 가드

Status: proposed

Why now: `youtube`는 Bun과 uv 워크스페이스 양쪽에 동시에 등록돼 있지만 신규 루트 클론에는
디렉터리가 존재하지 않는다. 이 상태에서 `bun install`이나 `uv run` 계열 명령을 돌리면 워크스페이스
멤버가 조용히 누락된 채로 넘어갈 수 있어, `rich`의 pre-pinning 요구사항이나 (이제 보관된) `toto`의
gitlink 드리프트 문제와 같은 종류의 운영 위험이 반복될 수 있다.

First slice: `./scripts/update-subrepos.sh status`(또는 `bun run report:baseline`) 출력에
`youtube` 디렉터리 존재 여부를 명시적으로 표시하고, 없을 때 `bun install` / uv 워크스페이스
명령 전에 하이드레이션이 필요하다는 경고를 내도록 루트 헬퍼 스크립트를 보강한다.

### 2026-09-12 - youtube 프로젝트 코드맵 커버리지 격차 해소

Status: proposed

Why now: 다른 7개 자식 저장소(`all`, `all-web-ui`, `android-support`,
`Keelim-Knowledge-Vault`, `keelim-plugin`, `keelim-vercel`, `rich`)는 모두
`docs/CODEMAPS/projects/*.md` 스냅샷을 갖고 있는데, 활성 Bun+uv 워크스페이스 멤버인 `youtube`만
빠져 있다. 이 비대칭은 워크스페이스 문서 커버리지 갭으로, `youtube`를 로컬에서 다룰 때 다른
프로젝트와 달리 참고할 생성 스냅샷이 없다는 뜻이다.

First slice: `youtube`가 로컬에 하이드레이션된 세션에서 `python3 scripts/refresh-codemaps.py`를
실행해 `docs/CODEMAPS/projects/youtube.md`를 생성하고, `projects/README.md`의 "Generated
Snapshots" 표에 행을 추가한다.
