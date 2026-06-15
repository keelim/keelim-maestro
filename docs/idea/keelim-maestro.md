# 아이디어: keelim-maestro (루트 코디네이션 레이어)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/architecture.md, docs/CODEMAPS/WORKSPACE.md, docs/CODEMAPS/keelim-maestro.md -->

**유형:** 루트 superproject | **스택:** Bun workspace + uv workspace + 서브모듈
**원격:** github.com/keelim/keelim-maestro

---

## 열린 아이디어

### M-1. Autonomous Repo Hydration 스크립트 자동화

**근거:** fresh clone 후 루트 Bun workspace를 사용하려면 `all-web-ui`, `rich`, `youtube`를 수동으로 clone해야 한다(README.md). 현재 이 hydration 절차는 README.md에 예시 명령어로만 기술돼 있고 실행 가능한 스크립트가 없다. 신규 개발자나 CI 환경에서 온보딩 마찰이 크다.

**제안:** `scripts/hydrate-workspace.sh`를 신설한다: (1) `git submodule update --init --recursive`, (2) 각 autonomous repo(`all-web-ui`, `rich`, `youtube`)의 존재 여부 확인 후 부재 시 clone, (3) `bun install` 실행. dry-run 모드(`--dry-run`)를 기본 포함한다. `README.md`에서 이 스크립트를 one-liner로 참조.

**우선순위:** 높음 — 온보딩 및 CI 환경 재구성 시 직접 영향.

---

### M-2. 통합 workspace 상태 대시보드 (`bun run status`)

**근거:** 현재 상태 확인 명령어가 분산돼 있다: `git submodule status`, `bun run report:baseline`, `./scripts/update-subrepos.sh status`, `bun run automation:local -- status`. 루트에서 전체 workspace 상태(submodule 다이버전스, autonomous repo 상태, Kubernetes 런타임, Vercel 배포)를 한 번에 보는 방법이 없다.

**제안:** `bun run status` 스크립트를 추가한다. 내부적으로 `report:baseline` + `update-subrepos.sh status` + `automation:local -- status`를 순차 실행하고 결과를 섹션별로 집계 출력한다. 개별 스크립트는 유지하고 이 커맨드는 read-only 집계 래퍼로만 동작한다.

**우선순위:** 보통 — 에이전트와 운영자 모두의 daily check 효율 향상.

---

### M-3. 코드맵 자동 갱신 CI 워크플로 추가

**근거:** `docs/CODEMAPS/*.md`는 2026-06-14에 마지막으로 생성됐다. keelim-plugin의 코드맵 생성기가 존재하지만 정기적 또는 이벤트 기반 자동 갱신이 없다. 서브모듈 핀이 변경되거나 autonomous repo 상태가 바뀌면 코드맵이 stale 상태가 된다.

**제안:** GitHub Actions 워크플로(`.github/workflows/update-codemaps.yml`)를 추가한다. 트리거: (1) 루트 `package.json` 또는 `.gitmodules` 변경 push, (2) 주 1회 cron. 코드맵 생성 후 변경이 있으면 자동 commit + push (`[skip ci]` 태그 포함). keelim-plugin의 codemap 스킬을 MCP 없이 직접 CLI로 호출하도록 설계.

**우선순위:** 보통 — KP-1(keelim-plugin 코드맵 훅)과 연계해 구현하면 중복 최소화.
