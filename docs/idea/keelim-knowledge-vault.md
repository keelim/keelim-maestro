# 아이디어: Keelim-Knowledge-Vault (지식 볼트)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/data.md, docs/CODEMAPS/SUBMODULES.md -->

**유형:** 서브모듈 | **스택:** Markdown / Obsidian
**원격:** github.com/keelim/Keelim-Knowledge-Vault | **브랜치:** main | **핀:** `15b29c11`

---

## 열린 아이디어

### KKV-1. GBrain 임포트 자동화 파이프라인 구축

**근거:** data.md에 따르면 Knowledge Vault는 GBrain(`~/brain` 리포)의 "curated import source"이지만 동기화는 수동 연산자 행위에 의존한다. 루트 `docs/knowledge/source-targets.md`가 임포트 풀을 정의하지만 자동화 스크립트가 없다.

**제안:** `scripts/` 아래 `sync-knowledge-vault.sh`(또는 keelim-plugin 스킬)를 추가한다. Knowledge Vault 서브모듈 핀 갱신 → GBrain 임포트 실행 → 임포트 결과 검증의 3단계를 자동화한다. `bun run automation:local -- start gbrain` 흐름에 통합하면 최적.

**우선순위:** 보통 — GBrain MCP 컨텍스트 품질에 직접 영향.

---

### KKV-2. 프론트매터 검증 스크립트 루트 자동화 통합

**근거:** `scripts/improvements/verify_knowledge_vault_*.py` 스크립트가 존재하지만(data.md 언급) 루트 `bun run test`나 CI에 포함되지 않는다. 서브모듈 핀 갱신 후 vault 정합성을 자동으로 검증하지 않는다.

**제안:** 루트 `package.json`에 `verify:knowledge-vault` 스크립트를 추가하고 `uv run python scripts/improvements/verify_knowledge_vault_*.py`를 호출한다. 이를 `update-subrepos.sh` 완료 후 선택적 post-hook으로 등록한다.

**우선순위:** 낮음 — 현재 vault 상태가 main과 동기된 경우 즉각적 위험 없음.
