# youtube

Last reviewed: 2026-08-23 KST

## Signals

- YouTube Shorts / Easy Release Note 제작을 담당하는 비공개 자율 child repo이며, 이 워크스페이스 사본에는 아직 origin/upstream이 없다 (`README.md` child repo 표).
- `all-web-ui`, `rich`와 달리 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(파이썬 패키지) 양쪽에 동시에 속한 유일한 child repo다 (`docs/CODEMAPS/WORKSPACE.md`).
- `youtube/simple`은 의도적으로 루트 uv 워크스페이스 밖에 있으며 자체 lockfile과 호환 범위를 쓴다 (`AGENTS.md` Python uv workspace policy).
- `youtube` n8n Kubernetes가 `rich` local Kubernetes와 함께 로컬 자동화 런타임으로 문서화되어 있다 (`README.md`).
- `youtube/videos/*` glob은 새 비디오 폴더가 추가될 때마다 루트 Bun lockfile을 변경시킬 수 있다고 이미 문서화되어 있다 (`README.md`).
- 이번 루트 체크아웃에는 디렉터리가 물리적으로 존재하지 않아, 로컬 hydration 이후에만 실제 상태 검증이 가능하다.
- 지금까지 `docs/idea/`에 전용 백로그 파일이 없었다는 점 자체가 문서/코드맵 커버리지 공백이었다.

## Open ideas

### 2026-08-23 - 신규 비디오 프로젝트 워크스페이스 드리프트 가드

Status: proposed

Why now: `youtube/videos/*` glob 패턴이 새 비디오 폴더가 추가될 때마다 루트 Bun lockfile을 변경시킨다는 점이 이미 문서화돼 있어서, 워크스페이스 멤버십과 실제 하위 디렉터리 사이 드리프트를 미리 잡아야 루트 `bun install`이 조용히 깨지지 않는다.

First slice: `youtube/videos/*`, `youtube/services/*` 실제 디렉터리 목록과 루트 `package.json` workspace 선언·`bun.lock` 항목을 비교하는 점검 스크립트를 추가해, 신규/제거된 패키지가 루트에 반영됐는지 `bun run test` 계열 검증에 포함시킨다.

### 2026-08-23 - 로컬 자동화 런타임(n8n·rich) 상태 콘솔

Status: proposed

Why now: `youtube` n8n Kubernetes와 `rich` local Kubernetes가 나란히 로컬 자동화 런타임으로 문서화돼 있지만, 두 런타임의 기동/정지 상태와 마지막 성공 실행 시각을 한 곳에서 확인할 수 있는 표면은 아직 없다.

First slice: `bun run automation:local` 상태 조회를 확장해 `agentgateway`·`rich`·`youtube n8n` 세 런타임의 기동 여부와 마지막 성공 실행 시각을 한 표로 보여주는 read-only 리포트를 만든다.

### 2026-08-23 - Bun·uv 이중 워크스페이스 버전 정합성 스냅샷

Status: proposed

Why now: `youtube`는 Bun 워크스페이스와 uv 워크스페이스 양쪽에 동시에 속하고, `youtube/simple`은 의도적으로 루트 uv 워크스페이스 밖에서 별도 lock·호환 범위를 쓰기 때문에, 루트 constraint-dependencies와 하위 패키지 선언이 조용히 어긋날 위험이 다른 child repo보다 크다.

First slice: `uv run python scripts/verify-python-dependency-constraints.py` 결과와 `youtube/remotion`·`services/*`·`videos/*`의 `package.json` 버전, `youtube/simple`의 별도 lock을 함께 비교하는 리포트를 만들어 정합성 이탈 항목을 표로 표시한다.
