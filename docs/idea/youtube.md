# youtube

Last reviewed: 2026-09-15 KST

## Signals

- `youtube`는 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와
  uv 워크스페이스(`youtube` 멤버, 패키지 `easy-release-note`) 양쪽에 동시에 등록된 활성 멤버다.
- 그런데도 루트 체크아웃에는 기본적으로 하이드레이션되어 있지 않으며, `docs/CODEMAPS/WORKSPACE.md`와
  `docs/CODEMAPS/backend.md`가 각각 "hydrate locally before running bun install / uv commands"를
  별도로 경고하고 있다.
- `docs/CODEMAPS/projects/README.md`의 Generated Snapshots 표에는 `youtube` 항목이 아예 없어서,
  다른 autonomous 저장소(`all-web-ui`, `rich`, `toto`)와 달리 프로젝트 코드맵도, 지금까지는
  `docs/idea/` 백로그 파일도 없었다.
- Remotion 렌더러, 자동화 서비스, per-video 프로젝트 패키지가 함께 움직이는 dual-runtime(TS + Python)
  구조라서, 하이드레이션 누락은 Bun/uv 두 워크스페이스 부트스트랩에 동시에 영향을 준다.

## Open ideas

### 2026-09-15 - 워크스페이스 하이드레이션 프리플라이트

Status: proposed

Why now: 루트 `package.json`과 `pyproject.toml`이 `youtube`를 활성 워크스페이스 멤버로 선언하지만,
로컬에 하이드레이션되어 있지 않으면 `bun install`과 uv 명령이 조용히 해당 glob만 건너뛰어서 누락을
알아채기 어렵다.

First slice: `bun run report:baseline` 또는 별도 체크 스크립트에 `youtube/` 디렉터리 존재 여부와
Bun/uv workspace 멤버 목록 매칭 결과를 비교하는 항목을 추가해, 누락 시 하이드레이션 명령을 바로
안내한다.

### 2026-09-15 - youtube 프로젝트 코드맵·백로그 초기화

Status: proposed

Why now: `all-web-ui`, `rich`, `toto`는 이미 `docs/CODEMAPS/projects/*.md`와 `docs/idea/*.md`를
갖고 있지만, `youtube`는 활성 워크스페이스 멤버인데도 둘 다 없어서 다음 작업자가 구조를 다시
조사하는 비용이 반복된다.

First slice: `youtube`를 로컬에 하이드레이션한 뒤 `python3 scripts/refresh-codemaps.py`를 실행해
`docs/CODEMAPS/projects/youtube.md`를 생성하고, `projects/README.md`의 Generated Snapshots 표에
등록한다.
