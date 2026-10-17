# youtube

Last reviewed: 2026-10-17 KST

## Signals

- 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스 멤버(`easy-release-note`)로 동시에 참여한다.
- `docs/CODEMAPS/WORKSPACE.md`에 따르면 기본 루트 체크아웃에는 `youtube/`가 없어서 `bun install` 전에 로컬 하이드레이션이 필요하다.
- 자식 저장소는 비공개이며 서브모듈로 고정되지 않았으므로, 워크스페이스 전제 조건은 문서로만 보장되고 있다.
- 이번 리뷰는 루트 코드맵 기준이며 `youtube` 자체의 README/AGENTS는 읽지 못했다(미하이드레이션).

## Open ideas

### 2026-10-17 - 워크스페이스 하이드레이션 사전 점검

Status: proposed

Why now: 코드맵이 `youtube/` 부재 시 설치 전 수동 하이드레이션을 요구하는데, 이 전제를 확인하는 자동 점검이 없어 `bun install`/`uv lock`이 불명확하게 실패할 수 있다.

First slice: `bun run report:baseline` 또는 루트 계약 검증에 `youtube`, `all-web-ui`, `rich` 경로 존재 여부를 확인해 누락 시 하이드레이션 안내를 출력하는 읽기전용 점검을 추가한다.

### 2026-10-17 - Bun/uv 공유 제약 정렬 리포트

Status: proposed

Why now: `youtube`는 TypeScript와 Python 양쪽 워크스페이스에 걸쳐 있고, 루트 `constraint-dependencies`와 자식 로컬 선언이 어긋나면 단독 설치 폴백이 거짓이 된다.

First slice: 기존 `scripts/verify-python-dependency-constraints.py`가 `youtube` 선언을 포함해 점검하는지 확인하고, 빠진 항목을 요약하는 리포트 한 줄을 추가한다.
