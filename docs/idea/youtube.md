# youtube

Last reviewed: 2026-09-01 KST

## Signals

- `youtube`는 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 uv 워크스페이스(`youtube` 패키지, Python >=3.13) 양쪽에
  등록된 활성 자율 child repo다.
- 신규 root 체크아웃에는 디렉터리가 기본으로 존재하지 않아, 로컬에 hydrate하기
  전까지 `bun install`/`uv sync`가 이 멤버를 건너뛴다(`WORKSPACE.md`에 명시).
- `docs/CODEMAPS/projects/`에는 아직 `youtube` 전용 코드맵이 없어서, 다른
  코드맵 파일(`architecture.md`, `backend.md`, `frontend.md`)의 교차 참조만으로
  구조를 추정해야 한다.
- Remotion 렌더러, 여러 자동화 서비스(`services/*`), 개별 비디오 프로젝트
  (`videos/*`)로 구성이 나뉘어 있어, 하위 폴더 수가 늘어날수록 워크스페이스
  glob 결과와 실제 산출물이 조용히 어긋날 여지가 있다.

## Open ideas

### 2026-09-01 - youtube 전용 코드맵 베이스라인

Status: proposed

Why now: `architecture.md`, `backend.md`, `frontend.md`, `WORKSPACE.md`는 모두
`youtube`를 활성 Bun+uv 워크스페이스 멤버로 언급하지만, `docs/CODEMAPS/projects/`에는
다른 child repo들과 달리 `youtube` 전용 코드맵이 없어 이번 아이디어 정원 작업에서도
실제 소스 근거 없이 교차 참조에만 의존해야 했다.

First slice: `youtube`를 로컬에 hydrate한 뒤 `python3 scripts/refresh-codemaps.py`로
`docs/CODEMAPS/projects/youtube.md`를 생성하고, `projects/README.md`의 Generated
Snapshots 표에도 추가한다.

### 2026-09-01 - 워크스페이스 glob 멤버 무음 실패 감시

Status: proposed

Why now: `youtube/services/*`와 `youtube/videos/*`는 glob 패턴 멤버라서, 디렉터리가
비어 있거나 하위 프로젝트가 없어도 `bun install`이 에러 없이 조용히 아무 패키지도
찾지 못한 채 넘어갈 수 있다. `WORKSPACE.md`가 이미 "디렉터리가 root 체크아웃에
기본으로 존재하지 않는다"고 명시하고 있어, 이 무음 실패 경로는 실제로 발생 가능하다.

First slice: `bun run report:baseline` 또는 별도의 가벼운 검사에 `youtube/remotion`,
`youtube/services/*`, `youtube/videos/*` glob이 최소 1개 이상의 실제 패키지로
해석되는지 확인하는 체크를 추가하고, 비어 있으면 하이드레이션이 필요하다는 경고를
명확히 출력한다.
