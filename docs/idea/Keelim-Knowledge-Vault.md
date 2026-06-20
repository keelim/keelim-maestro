# Keelim-Knowledge-Vault 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 2 -->

프로젝트 유형: 등록 서브모듈 (Obsidian/Markdown 지식 볼트)  
코드맵 참조: `docs/CODEMAPS/projects/Keelim-Knowledge-Vault.md`, `docs/CODEMAPS/data.md`

---

## [OPEN] 볼트 검증 스크립트 루트 CI 연동

**근거:** `docs/CODEMAPS/projects/Keelim-Knowledge-Vault.md`에 세 가지 검증 스크립트가 명시되어 있다: `verify_knowledge_vault_automation.py`, `verify_knowledge_vault_frontmatter.py`, `verify_knowledge_vault_links.py`. 이 스크립트들이 루트 CI에 자동 실행되는지 코드맵에서 확인되지 않는다.

**내용:**
1. 루트 CI 파이프라인에 볼트 검증 스크립트 단계를 추가한다.
2. 서브모듈이 초기화된 경우에만 실행되도록 조건을 설정한다.
3. 프론트매터 오류, 깨진 내부 링크, 자동화 위반 항목을 CI에서 리포트한다.
4. 검증 실패 시 PR 차단 여부를 정책으로 결정한다.

**가치:** 자동화 기회 — 수동 검토 없이 볼트 건강 상태를 지속적으로 보장한다.

---

## [OPEN] GBrain 임포트 풀 확장 및 소스 타겟 최신화

**근거:** `docs/CODEMAPS/data.md`에 Knowledge Vault가 GBrain의 "curated import source"임이 명시되어 있고, `docs/knowledge/source-targets.md`에 임포트 풀과 제외 목록이 관리된다. 서브모듈 핀이 `15b29c11`로 고정된 채 볼트가 성장하면 GBrain의 지식 커버리지에 gap이 생긴다.

**내용:**
1. 현재 서브모듈 핀(`15b29c11`)과 `origin/main` HEAD 사이의 새 노트/카테고리를 확인한다.
2. `docs/knowledge/source-targets.md`의 큐레이션 풀에 추가할 새 타겟을 검토한다.
3. 불필요한 제외 항목을 정리하거나 이유를 명시한다.
4. GBrain sync 후 `docs/knowledge/verification-contract.md`의 기대 결과와 일치하는지 검증한다.

**가치:** 문서/코드맵 커버리지 갭 해소 — 볼트의 최신 지식이 GBrain 질의에 반영된다.
