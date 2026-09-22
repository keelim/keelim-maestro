# youtube

Last reviewed: 2026-09-22 KST

## Signals

- `docs/CODEMAPS/architecture.md`, `frontend.md`, `backend.md`, `WORKSPACE.md`가 모두 `youtube`를 활성 Bun+uv 워크스페이스 멤버로 명시하지만, 지금까지 `docs/idea/`에 이 프로젝트를 위한 백로그 파일이 없었다.
- `docs/CODEMAPS/keelim-maestro.md`의 Open Questions는 "youtube not physically present in this checkout; hydrate locally before running bun install or uv commands"라고 명시해, 워크스페이스 멤버십과 실제 체크아웃 상태가 쉽게 어긋날 수 있음을 이미 지적하고 있다.
- 구성은 `youtube/remotion`(Remotion 렌더러), `youtube/services/*`(자동화 서비스), `youtube/videos/*`(영상별 프로젝트)로 나뉘어 있어, Bun 워크스페이스 glob과 uv 워크스페이스 멤버십이 동시에 걸려 있다.

## Open ideas

### 2026-09-22 - 워크스페이스 하이드레이션 가드

Status: proposed

Why now: 루트 codemap이 이미 "youtube가 체크아웃에 없으면 `bun install`/uv 명령이 조용히 어긋난다"는 위험을 지적하고 있는데도, 이를 실행 전에 잡아주는 검증이 없다.

First slice: 루트 `bun install`/uv 관련 스크립트 실행 전에 `youtube/remotion`, `youtube/services`, `youtube` 쪽 Python 패키지 경로의 존재 여부를 확인하고, 없으면 워크스페이스 멤버십과 실제 체크아웃 상태가 어긋난다는 경고를 명확히 출력하는 가드를 추가한다.

### 2026-09-22 - 영상 프로젝트 카탈로그 가시화

Status: proposed

Why now: `youtube/videos/*`와 `youtube/services/*`가 glob 패턴으로만 워크스페이스에 등록돼 있어서, 실제로 몇 개의 영상 프로젝트와 서비스가 활성 상태인지, 어떤 것이 오래돼서 정리 대상인지 한곳에서 보기 어렵다.

First slice: 각 `youtube/videos/<project>`와 `youtube/services/<service>`의 마지막 수정 시각과 상태를 모은 목록을 생성해, 오래 방치된 영상 프로젝트나 서비스를 정리 후보로 표시한다.
