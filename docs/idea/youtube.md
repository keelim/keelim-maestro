# youtube

Last reviewed: 2026-08-17 KST

## Signals

- `youtube`는 원격이 아직 없는 private 로컬 체크아웃이지만, 루트 Bun 워크스페이스(`youtube/remotion`,
  `youtube/services/*`, `youtube/videos/*`)와 루트 uv 워크스페이스(`easy-release-note` 패키지) 양쪽에서
  활성 멤버로 선언돼 있다.
- 이 root 체크아웃에는 `youtube/` 디렉터리 자체가 존재하지 않아서, hydrate하지 않은 채로
  `bun install`이나 uv 계열 명령을 돌리면 워크스페이스 그래프에서 조용히 빠지거나 실패 원인을
  워크스페이스 밖에서 찾게 될 위험이 있다.
- `docs/CODEMAPS/projects/`에는 `all`, `all-web-ui`, `Keelim-Knowledge-Vault`, `keelim-plugin`,
  `keelim-vercel`, `rich`, `toto` 스냅샷은 있지만 `youtube.md`는 아직 없어서, 활성 워크스페이스
  멤버 중 하나만 프로젝트 단위 코드맵 커버리지가 비어 있다.
- `youtube/simple`은 별도 lockfile과 호환 범위를 가진 채 uv 워크스페이스 바깥에 의도적으로 남아 있어,
  루트와 nested 프로젝트의 경계를 계속 지켜야 한다.

## Open ideas

### 2026-08-17 - 하이드레이션 가드 스크립트

Status: proposed

Why now: `youtube`가 루트 Bun·uv 워크스페이스 멤버로 선언돼 있지만 표준 체크아웃에는 물리적으로
존재하지 않는 경우가 있어서, 이 사실을 모르고 `bun install`이나 `uv run` 계열 명령을 돌리면
실패 원인을 워크스페이스 설정 밖에서 찾게 된다.

First slice: 루트 워크스페이스 명령 실행 전에 `youtube/` 존재 여부를 확인하고, 없으면 hydrate
안내(clone 경로, 필요한 mise 툴체인 버전)를 출력한 뒤 종료하는 사전 점검 스크립트를 추가한다.

### 2026-08-17 - youtube 프로젝트 코드맵 스냅샷

Status: proposed

Why now: `all`, `all-web-ui`, `rich` 등 다른 활성 워크스페이스 멤버는 이미
`docs/CODEMAPS/projects/`에 스냅샷이 있는데 `youtube`만 비어 있어서, 같은 수준의 탐색
가능성을 못 갖고 있다.

First slice: `youtube`를 로컬에 hydrate한 뒤 `scripts/refresh-codemaps.py`를 실행해
`docs/CODEMAPS/projects/youtube.md`를 생성하고, `docs/CODEMAPS/projects/README.md`의
스냅샷 표에 등록한다.
