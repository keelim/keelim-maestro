# youtube

Last reviewed: 2026-09-02 KST

## Signals

- 루트 `docs/CODEMAPS/architecture.md`, `backend.md`, `frontend.md`, `WORKSPACE.md`가
  모두 `youtube`를 활성 워크스페이스 멤버로 기록한다: root Bun workspace의
  `youtube/remotion`, `youtube/services/*`, `youtube/videos/*`, 그리고 root uv
  workspace의 Python 멤버.
- `youtube`는 autonomous local repo(비-submodule)이며, 이 checkout에는 디렉터리 자체가
  존재하지 않는다. 로컬에 hydrate된 뒤에만 `bun install`·`uv` 명령이 완전히 동작한다.
- `all`, `all-web-ui`, `rich`와 달리 `docs/CODEMAPS/projects/`에 `youtube` 전용 코드맵
  스냅샷이 아직 없다 — 다른 autonomous repo들은 hydration 전에도 placeholder 코드맵을
  갖고 있는데 `youtube`만 빠져 있다.
- Remotion 렌더러, services 자동화, 개별 video 프로젝트라는 세 종류의 워크스페이스
  glob 멤버가 하나의 자동화 파이프라인(YouTube Shorts / Easy Release Note 제작)을
  구성한다고 root AGENTS.md가 설명한다.

## Open ideas

### 2026-09-02 - youtube 프로젝트 코드맵 공백 메우기

Status: proposed

Why now: `youtube`는 root Bun workspace(3개 경로)와 root uv workspace 양쪽의 활성
멤버로 4개 root 코드맵에서 반복 언급되지만, `docs/CODEMAPS/projects/youtube.md`가
없다. `all-web-ui`, `rich`처럼 hydration 전에도 placeholder 코드맵(원격 URL, 워크스페이스
역할, 재생성 커맨드)을 남겨두는 관례가 `youtube`에는 적용되지 않아, 다음에 이 저장소를
다루는 세션이 매번 root 코드맵 4곳을 다시 짜맞춰야 한다.

First slice: `all-web-ui.md`/`rich.md`와 같은 형식으로 `docs/CODEMAPS/projects/youtube.md`
placeholder를 만들고, `docs/CODEMAPS/projects/README.md`의 Generated Snapshots 표에
행을 추가한다. `youtube`가 로컬에 hydrate되면 `scripts/refresh-codemaps.py`로 실제
스냅샷을 채운다.

### 2026-09-02 - services/videos 자동화 실행 상태 요약

Status: proposed

Why now: `youtube/services/*`(자동화 서비스)와 `youtube/videos/*`(개별 영상 프로젝트)가
각각 별도 Bun workspace glob 멤버로 흩어져 있어서, 어떤 서비스 실행이 실패했는지 root
에서 자식 저장소에 들어가지 않고는 알 수 없다. `rich`의 "Recovery cockpit"/"Execution
ledger" 아이디어와 같은 문제의식이지만 `youtube`에는 아직 대응 항목이 없다.

First slice: `youtube/services/*` 패키지가 실행 종료 시 성공/실패/소요시간을 담은 얇은
run-status 매니페스트를 남기도록 정의하고, root에서 그 매니페스트만 모아 보여주는 요약
커맨드(child repo 소스는 건드리지 않는 root-owned 리포터)를 추가한다.
