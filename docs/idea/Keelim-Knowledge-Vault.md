# 아이디어 — Keelim-Knowledge-Vault

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `Keelim-Knowledge-Vault`  
스택: Obsidian / Markdown — 플랫 노트 + 메타데이터  
상태: 서브모듈 (`main` 브랜치, 핀 `15b29c11`)  
오픈 아이디어: 2

---

## 열린 아이디어

### [KKV-001] GBrain 동기화 주기 및 소스 타겟 문서화 공백

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 문서화 / 운영 위험 감소
- **근거:** `docs/CODEMAPS/data.md`. GBrain이 `~/brain` 별도 저장소를 사용하며 `Keelim-Knowledge-Vault`가 큐레이션된 임포트 소스임. 루트에는 `docs/knowledge/` 계약 문서가 있어야 하지만 이 체크아웃에서 해당 디렉토리가 없음(MAESTRO-001 참조).

Knowledge Vault에서 GBrain으로 콘텐츠가 어떤 기준으로, 어떤 주기로 동기화되는지 루트 수준에서 파악하기 어렵다. `docs/knowledge/source-targets.md`(현재 누락)가 이를 다뤄야 하지만 없는 상태다. 임시방편으로 Knowledge Vault 저장소의 `AGENTS.md`에 GBrain 연동 계약(가져오기 대상 폴더, 제외 항목, 갱신 주기)을 요약해두면 에이전트가 동기화 상태를 확인할 수 있다.

---

### [KKV-002] 프론트매터 / 링크 검증 스크립트 CI 미연동

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 자동화 기회 / 문서 품질
- **근거:** `docs/CODEMAPS/SCRIPTS.md`. `scripts/improvements/verify_knowledge_vault_frontmatter.py`, `verify_knowledge_vault_links.py`, `verify_knowledge_vault_automation.py`가 존재하지만 CI 파이프라인에 연결되어 있지 않음.

Knowledge Vault에 노트가 추가될 때 프론트매터 규격(필수 키, 날짜 형식)과 내부 링크 유효성이 자동으로 검사되지 않는다. `Keelim-Knowledge-Vault` 저장소의 GitHub Actions 워크플로우에 이 세 스크립트를 포함시키면 품질 게이트를 자동화할 수 있다. 루트에서 직접 실행(`uv run python scripts/improvements/verify_knowledge_vault_frontmatter.py`)할 수 있는지 확인 후 연동한다.

---

## 닫힌 아이디어

_없음_
