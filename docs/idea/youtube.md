# youtube

Last reviewed: 2026-08-24 KST

## Signals

- Private autonomous child repo for YouTube Shorts and Easy Release Note
  production work (`AGENTS.md` `/youtube` policy).
- Unlike other autonomous child repos (`all-web-ui`, `rich`), `youtube` has no
  origin/upstream remote yet (`README.md` subrepo status table), so root
  workspace tooling assumes a hydration path that does not exist for a fresh
  clone.
- Participates in both the root Bun workspace (`youtube/remotion`,
  `youtube/services/*`, `youtube/videos/*` package globs) and the root uv
  workspace (`easy-release-note` package), and is one of three runtimes under
  the root-owned local automation audit alongside `rich` (local Kubernetes)
  and `tools/agentgateway`: `rich` local Kubernetes and `youtube` n8n
  Kubernetes (`docs/ops/local-automation-stack.md`, `bun run automation:local`).
- `youtube/videos/*` is an open-ended glob for per-episode packages, so the
  root Bun lockfile shifts whenever an episode folder is added or removed.
- `youtube/simple` is intentionally excluded from the root uv workspace and
  keeps its own `pyproject.toml`/`uv.lock`.

## Open ideas

### 2026-08-24 - 원격 부재 상태의 워크스페이스 참여 가드

Status: proposed

Why now: `youtube`는 `rich`·`all-web-ui`와 달리 origin/upstream이 아직 없는데도
루트 Bun/uv 워크스페이스 패키지 경로에 이미 포함돼 있어서, 신선한 클론에서
`bun install`이나 uv 명령을 실행하면 원격 클론이 아니라 운영자 로컬 경로
하이드레이션에 의존하게 된다. 이 비대칭이 문서에만 남아 있고 자동 점검이
없으면, 신규 환경에서 실패 원인을 매번 다시 진단해야 한다.

First slice: `./scripts/update-subrepos.sh status` 또는 `bun run report:baseline`
경로에 `youtube` 디렉터리 존재 여부와 원격 등록 상태를 함께 표시하고, 부재 시
운영자 승인 하이드레이션 경로(`AGENTS.md` 안내)를 바로 알려주는 안내 문구를
추가한다.

### 2026-08-24 - n8n 로컬 자동화 상태 가시화

Status: proposed

Why now: `docs/ops/local-automation-stack.md`가 `rich` 로컬 Kubernetes,
`youtube` n8n Kubernetes, `tools/agentgateway`를 하나의 루트 감사 계약으로
묶고 있지만, `rich`는 이미 idea 백로그에 통합 상태/복구 아이디어가 있는 반면
`youtube` n8n 워크플로 상태는 별도로 다뤄지지 않고 있다.

First slice: `bun run automation:local -- status`(또는 동등 경로)가 `youtube`
n8n 스택의 마지막 성공 시각과 실패 워크플로를 함께 보여주도록, `rich` 쪽
Integration health console 아이디어와 같은 얇은 상태 패널을 확장한다.
