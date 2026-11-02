# youtube

Last reviewed: 2026-11-02 KST

## Signals

- 비공개 자율 child repo이며 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(`easy-release-note`)에 모두 참여한다.
- 코드맵(`WORKSPACE.md`, `keelim-maestro.md`)은 기본 체크아웃에 `youtube/`가 없어 `bun install`·uv 명령 전에 로컬 hydrate가 필요하다고 명시한다.
- `bun run automation:local`이 `youtube` n8n을 `rich`, `agentgateway`와 함께 위임 대상으로 묶는다.
- 서브모듈이 아니므로 핀 포인터가 없고, 상태는 `./scripts/update-subrepos.sh status`로만 드러난다.

## Open ideas

### 2026-11-02 - 워크스페이스 hydrate 사전 점검

Status: proposed

Why now: 루트 Bun/uv 워크스페이스가 `youtube`, `rich`, `all-web-ui`가 이미 존재한다고 가정하지만, 신규 체크아웃에서는 디렉터리가 비어 있어 설치 실패 원인이 바로 보이지 않는다.

First slice: 루트 `scripts/`에 워크스페이스 멤버 경로 존재 여부만 읽기 전용으로 검사해 누락된 child 목록과 hydrate 안내를 출력하는 preflight를 추가하고, `bun run test` 계약 검사에서 호출한다.

### 2026-11-02 - 로컬 자동화 메서드 단위 준비 상태 리포트

Status: proposed

Why now: `automation:local`은 `youtube` n8n을 위임하지만, 준비 완료 주장은 health 상태가 아니라 `initialize` / `tools/list` / `tools/call` 호출 증거가 있어야 한다는 루트 규칙이 있다.

First slice: 각 위임 대상(`rich`, `youtube` n8n, `agentgateway`)에 대해 JSON-RPC 3단계 호출 결과를 한 줄 pass/fail로 모으는 읽기 전용 `status` 서브커맨드를 설계한다.
