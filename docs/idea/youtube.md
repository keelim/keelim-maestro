# youtube

Last reviewed: 2026-09-04 KST

## Signals

- YouTube Shorts와 Easy Release Note 제작을 담당하는 private 자율 자식 저장소로,
  `all-web-ui`/`rich`와 같은 "autonomous local repo" 취급을 받는다.
- 루트 Bun 워크스페이스에는 `youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*` 세 개의 glob 멤버로 등록돼 있고, 루트 uv 워크스페이스에는
  `easy-release-note` 패키지로 등록돼 있어 TypeScript/Python 두 계약을 동시에
  진다.
- `bun run automation:local -- ...`은 `rich`, `youtube` n8n, `tools/agentgateway`를
  위한 루트 소유 로컬 자동화 인덱스/딜리게이터이지만, 실제 런타임 구현·매니페스트·
  시크릿은 자식 저장소가 소유한다.
- 기본 루트 체크아웃에는 `youtube/` 디렉터리 자체가 없어(하이드레이션 필요),
  워크스페이스 glob·uv 멤버 선언과 실제 하이드레이션 이후 구조가 어긋나도 이를
  잡아낼 자동 검사가 아직 없다.

## Open ideas

### 2026-09-04 - 워크스페이스 하이드레이션 계약 검증기

Status: proposed

Why now: 루트 `package.json`은 `youtube/remotion`, `youtube/services/*`,
`youtube/videos/*`를 Bun 워크스페이스 멤버로, 루트 `pyproject.toml`은 `youtube`를
`easy-release-note` uv 멤버로 선언하지만, 기본 체크아웃에는 `youtube` 디렉터리가
없어 하이드레이션 여부에 따라 `bun install`/`uv lock --check` 결과가 달라진다.
glob 경로·패키지 이름과 실제 하이드레이션된 디렉터리 구조가 어긋나도 잡아내는
검사가 없다.

First slice: `youtube`가 로컬에 하이드레이션된 상태에서 루트 `package.json`의
workspace glob과 `pyproject.toml`의 uv workspace 멤버 선언이 실제
`remotion/`·`services/*`·`videos/*` 디렉터리 구조 및 `easy-release-note` 패키지
이름과 일치하는지 비교하는 read-only 검증을 `bun run report:baseline`류 헬퍼에
추가한다.

### 2026-09-04 - automation:local n8n 델리게이터 정합성 점검

Status: proposed

Why now: `bun run automation:local -- ...`는 `rich`, `youtube` n8n,
`tools/agentgateway`를 위한 루트 소유 로컬 자동화 인덱스/딜리게이터이지만, 실제
런타임 구현·매니페스트·시크릿은 자식 저장소가 소유한다. 루트 인덱스가
`youtube`의 실제 n8n 워크플로 목록과 어긋나면 로컬 자동화가 조용히 실패할 수
있다.

First slice: `automation:local`의 `youtube` n8n 델리게이트 항목과 하이드레이션된
`youtube` 저장소의 실제 n8n 워크플로/스크립트 목록을 비교하는 read-only 점검을
추가하고, 누락되거나 이름이 바뀐 델리게이트 항목을 경고로 표시한다.
