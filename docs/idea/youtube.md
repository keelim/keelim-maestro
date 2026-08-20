# youtube

Last reviewed: 2026-08-20 KST

## Signals

- `youtube`는 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 루트 uv 워크스페이스(`rich`, `youtube` 멤버) 양쪽에 실제로 등록된 자율 child repo다.
- 루트 체크아웃에는 기본적으로 디렉터리가 존재하지 않아, `bun install`이나 uv 명령 전에 로컬 하이드레이션이 먼저 필요하다.
- `bun run automation:local -- ...`가 `rich`, `youtube` n8n, `tools/agentgateway`를 함께 다루는 로컬 자동화 인덱서/딜리게이터 역할을 한다.
- 다른 자율/서브모듈 리포(`all`, `all-web-ui`, `keelim-plugin`, `keelim-vercel`, `rich`, `Keelim-Knowledge-Vault`, 심지어 archived된 `toto`)는 모두 `docs/CODEMAPS/projects/<name>.md` 코드맵을 갖고 있지만, `youtube`만 대응 코드맵이 없다.

## Open ideas

### 2026-08-20 - youtube 프로젝트 코드맵 스냅샷 생성

Status: proposed

Why now: `youtube`는 Bun/uv 워크스페이스 멤버로 문서상 이미 활성 상태지만, `docs/CODEMAPS/projects/`에 대응 코드맵이 없어서 다른 자율 리포와 달리 구조·진입점·검증 표면을 원격 세션에서 파악할 방법이 없다.

First slice: `youtube`를 로컬에 하이드레이션한 뒤 기존 codemap 생성 스크립트를 실행해 `docs/CODEMAPS/projects/youtube.md`를 만들고, `WORKSPACE.md`/`architecture.md`/`backend.md`/`frontend.md`에서 이미 걸려 있는 참조와 맞춰 링크를 확인한다.

### 2026-08-20 - youtube 하이드레이션 상태 점검 자동화

Status: proposed

Why now: `youtube`는 루트 체크아웃에 기본적으로 존재하지 않아 `bun install`/uv 명령 전에 하이드레이션이 필요하지만, `rich`나 `all-web-ui`와 달리 이 상태를 확인하는 절차가 백로그에 아직 없어서 remotion/services/videos 패키지가 실제로 설치 가능한지 매번 수동으로 확인해야 한다.

First slice: `./scripts/update-subrepos.sh status`(또는 동등한 헬퍼)의 출력에 `youtube` 하이드레이션 여부를 포함시켜, 워크스페이스 멤버 패키지 경로가 실제로 존재하는지 한 번에 보여준다.
