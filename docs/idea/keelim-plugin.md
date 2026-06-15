# 아이디어: keelim-plugin (Claude/Codex 스킬 플러그인)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/architecture.md, docs/CODEMAPS/SUBMODULES.md, docs/CODEMAPS/keelim-maestro.md -->

**유형:** 서브모듈 | **스택:** Python
**원격:** github.com/keelim/keelim-plugin | **브랜치:** main | **핀:** `a3463396`

---

## 열린 아이디어

### KP-1. 서브모듈 업데이트 후 코드맵 자동 갱신 훅

**근거:** 현재 코드맵(`docs/CODEMAPS/*.md`)은 2026-06-14에 수동 생성된 스냅샷이다. keelim-plugin이 코드맵 생성기를 포함한다고 알려져 있지만, `update-subrepos.sh` 또는 서브모듈 핀 업데이트 후 자동으로 코드맵을 재생성하는 훅이 없다.

**제안:** `update-subrepos.sh update` 완료 후 `bun run cg:status`와 코드맵 갱신 커맨드를 순차 실행하는 post-update 훅을 추가한다. keelim-plugin의 codemap 스킬을 MCP(`agentgateway`)를 통해 호출하는 방식이 이상적.

**우선순위:** 높음 — 코드맵 신선도가 에이전트 의사결정 품질에 직결됨.

---

### KP-2. 사용 가능한 스킬 카탈로그 루트 문서화

**근거:** keelim-plugin이 "Claude/Codex skill plugin (codemap generator, etc.)"으로 명시돼 있지만 어떤 스킬이 있는지 루트 docs에 노출되지 않는다. 에이전트가 어떤 스킬을 호출할 수 있는지 루트 AGENTS.md나 codemaps에서 확인 불가.

**제안:** `docs/CODEMAPS/keelim-plugin.md`(또는 SCRIPTS.md 확장)에 플러그인이 제공하는 스킬 목록을 열거한다: 이름, 입력/출력, 호출 방법(agentgateway 경로 포함). 코드맵 갱신 스킬은 반드시 포함.

**우선순위:** 보통 — 신규 에이전트 세션 컨텍스트 품질 개선.

---

### KP-3. 서브모듈 핀 동기화 스킬 통합

**근거:** 루트 `update-subrepos.sh`는 서브모듈 상태를 보고하지만 핀(gitlink)을 자동으로 업데이트하고 커밋하는 워크플로가 없다. keelim-plugin에서 이를 자동화하는 스킬을 제공하면 여러 서브모듈의 핀 갱신을 에이전트가 안전하게 조율할 수 있다.

**제안:** keelim-plugin 내에 "submodule-pin-update" 스킬을 추가한다: (1) `git submodule status` 파싱, (2) 각 서브모듈의 업스트림 최신 커밋 확인, (3) 드라이런 결과 출력 → 승인 후 커밋. 위험 작업이므로 드라이런이 필수.

**우선순위:** 보통 — KP-1과 연계해 코드맵 자동화 완성.
