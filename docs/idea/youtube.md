# youtube

Last reviewed: 2026-09-13 KST

## Signals

- `youtube`는 private autonomous child repo로, YouTube Shorts와 Easy Release Note
  제작 작업을 담당한다.
- 루트 Bun 워크스페이스에 `youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*` glob 멤버로 참여하고, 루트 uv 워크스페이스에는
  `easy-release-note` 패키지로 참여한다.
- 루트 체크아웃에는 기본적으로 하이드레이션되어 있지 않아, `bun install`이나
  uv 명령을 실행하기 전에 로컬 클론이 선행되어야 한다.
- `youtube/simple`은 자체 lockfile과 호환 범위를 가진 별도 프로젝트로, 명시적으로
  승격되기 전까지는 루트 uv 워크스페이스 밖에 있어야 한다.
- 지금까지 워크스페이스 idea 백로그에 이 프로젝트 항목이 없었다는 점 자체가
  문서 커버리지 공백이었다.

## Open ideas

### 2026-09-13 - 워크스페이스 하이드레이션 정합성 게이트

Status: proposed

Why now: 루트 `package.json`의 Bun 워크스페이스는 `youtube/remotion`,
`youtube/services/*`, `youtube/videos/*`를 멤버로 선언하고 `pyproject.toml`의 uv
워크스페이스는 `youtube`를 멤버로 선언하지만, 저장소가 로컬에 하이드레이션되어
있지 않으면 이 선언들이 실제로 무엇과 매칭되는지 확인할 방법이 없어
`bun install`/`uv` 명령이 조용히 부분 실패하거나 예상과 다른 결과를 낼 수 있다.

First slice: 저장소 하이드레이션 여부, Bun glob 멤버의 실제 매칭 디렉터리 수,
uv 패키지명(`easy-release-note`) 일치 여부를 확인하는 상태 점검을 추가하고,
`bun run report:baseline`류 루트 점검 결과에 노출한다.

### 2026-09-13 - uv 워크스페이스 경계 드리프트 점검

Status: proposed

Why now: 루트 문서는 `youtube`가 uv 워크스페이스에 `easy-release-note` 패키지로
참여하되 자체 lockfile을 가진 `youtube/simple`은 명시적으로 승격되기 전까지
워크스페이스 밖에 있어야 한다고 정하고 있지만, 이 경계를 실제로 검증하는
자동화된 확인 절차는 아직 없어 향후 리팩터링에서 경계가 조용히 깨질 위험이 있다.

First slice: `scripts/verify-python-dependency-constraints.py` 실행 결과에
`youtube`(`easy-release-note`) 패키지가 포함되고 `youtube/simple`은 제외되어
있는지 확인하는 체크를 추가해, 경계 이탈이 생기면 바로 드러나게 한다.
