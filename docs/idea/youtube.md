# youtube

Last reviewed: 2026-10-13 KST

## Signals

- 비공개 자율 저장소이며 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(`easy-release-note`)에 모두 참여한다.
- 기본 루트 체크아웃에는 디렉터리가 없어서, hydrate 없이 `bun install`/uv 명령을 실행하면 실패할 수 있다(WORKSPACE.md 선행조건).
- `bun run automation:local -- ...`이 `youtube` n8n Kubernetes 자동화를 위임 대상으로 이미 색인한다.
- 이번 리뷰에서는 자식 저장소가 hydrate되지 않아 README/AGENTS 대신 루트 codemap·README만 근거로 사용했다.

## Open ideas

### 2026-10-13 - 워크스페이스 멤버 hydrate 사전 점검

Status: proposed

Why now: `youtube`는 Bun/uv 워크스페이스 멤버지만 기본 체크아웃에 없어, 루트 설치 실패 원인이 "코드 문제"인지 "미hydrate"인지 구분하기 어렵다. `all-web-ui`, `rich`도 같은 선행조건을 공유한다.

First slice: `all-web-ui`, `rich`, `youtube`의 존재 여부와 선언된 패키지 경로 glob 해석 결과를 출력하는 읽기전용 preflight를 `bun run report:baseline` 옆에 두고, 누락 시 명확한 hydrate 안내만 출력한다.

### 2026-10-13 - n8n 자동화 메서드 단위 준비 증적

Status: proposed

Why now: 루트 가이드는 로컬 MCP/자동화 준비 상태를 health 초록불이 아니라 메서드 호출 증적으로 증명하라고 요구한다. `automation:local`이 `youtube` n8n을 위임하지만 준비 증적을 남기는 경로는 codemap에 없다.

First slice: `automation:local`에 `youtube` n8n 대상의 읽기전용 상태 점검(워크플로 목록 호출 결과 요약)을 추가하고 결과를 `docs/ops/`에 날짜별 한 줄 로그로 남긴다.
