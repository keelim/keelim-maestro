# youtube

Last reviewed: 2026-09-21 KST

## Signals

- YouTube Shorts / Easy Release Note 제작을 담당하는 private autonomous child
  repo. 루트 `AGENTS.md`와 `docs/CODEMAPS/{architecture,frontend,backend,WORKSPACE}.md`
  전부가 이 프로젝트를 다루지만, 지금까지 `docs/idea/`에는 전용 파일이 없었다 —
  코드맵 커버리지와 백로그 커버리지 사이의 명확한 gap.
- Bun 워크스페이스에 `youtube/remotion`, `youtube/services/*`, `youtube/videos/*`
  세 개의 glob 멤버로 참여하고(top-level 패키지 아님), uv 워크스페이스에는
  `easy-release-note` 패키지명으로 참여한다 — 두 워크스페이스 시스템에 동시에
  걸쳐 있는 유일한 자율 child repo다.
- 루트 codemap(`keelim-maestro.md`, `WORKSPACE.md`)이 반복해서 명시: "youtube not
  physically present in this checkout; hydrate locally before running `bun
  install` or uv commands" — 즉 워크스페이스 선언과 실제 로컬 상태가 기본적으로
  어긋나 있는 것이 알려진 전제 조건이다.
- 루트 `AGENTS.md`는 `youtube`의 child-local 의존성 선언이 루트
  `tool.uv.constraint-dependencies`와 정렬을 유지해야 standalone fallback 설치가
  정직하게 동작한다고 명시하며, `youtube/simple`은 별도 lockfile/호환 범위를 가진
  채 uv 워크스페이스 밖에 의도적으로 남아 있다.

## Open ideas

### 2026-09-21 - 워크스페이스 하이드레이션 가드

Status: proposed

Why now: `youtube`는 루트 `package.json`의 workspaces 배열과 `pyproject.toml`의
uv workspace members 양쪽에 선언돼 있지만, fresh root checkout에는 디렉터리 자체가
없다. 이 상태에서 `bun install`이나 uv 명령을 그대로 돌리면 실패 원인이 "워크스페이스
멤버 누락"이 아니라 알아보기 어려운 하위 에러로 나타날 위험이 있다.

First slice: `bun install` / `uv lock --check` 전에 선언된 워크스페이스 glob
(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`, uv의 `youtube`
member)이 실제로 로컬에 존재하는지 확인하는 사전 점검 스크립트를 추가하고, 누락 시
`git clone`/hydration 안내 메시지와 함께 조기에 실패하게 만든다.

### 2026-09-21 - Bun/uv 이중 멤버십 계약 정합성 점검

Status: proposed

Why now: `youtube`는 Bun 워크스페이스(TypeScript: remotion/services/videos)와 uv
워크스페이스(Python: `easy-release-note`) 양쪽에 동시에 걸친 유일한 child repo라서,
한쪽 워크스페이스만 보고 변경하면 다른 쪽 계약을 조용히 깨뜨리기 쉽다. 루트
`AGENTS.md`도 child-local 의존성 선언을 루트 constraint와 정렬하라고 명시하지만
자동 검증 대상은 아직 명확하지 않다.

First slice: `scripts/verify-python-dependency-constraints.py`를 `youtube`의
child-local `pyproject.toml`/lockfile까지 포함해 실행하고, Bun 쪽은
`bun run typecheck:web` 대상에 `youtube/remotion`을 포함해 두 워크스페이스 계약이
동시에 통과하는지 한 리포트로 보여준다.
