# `Keelim-Knowledge-Vault` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 등록 서브모듈 | **상태:** clean vs origin/main (pinned `15b29c11`) | **우선순위:** 중간

---

## 열린 아이디어

### VAULT-001 · 루트 검증 스크립트 CI 통합
**우선순위:** 중간 | **근거:** `Keelim-Knowledge-Vault.md` — 루트 소유 검증 스크립트 3개 존재, CI 연결 미확인

루트가 소유한 vault 검증 스크립트를 CI에 통합하여 정기 실행을 보장한다.

- `scripts/improvements/verify_knowledge_vault_automation.py`
- `scripts/improvements/verify_knowledge_vault_frontmatter.py`
- `scripts/improvements/verify_knowledge_vault_links.py`

**검토할 것:**
- GitHub Actions 워크플로우에 이 스크립트 실행 단계 존재 여부
- 미존재 시 `uv run python scripts/improvements/verify_knowledge_vault_*.py` 주간 스케줄 추가

---

### VAULT-002 · GBrain source-targets 큐레이션 워크플로우 문서화
**우선순위:** 중간 | **근거:** `data.md`, `docs/knowledge/source-targets.md` — import pool이 curated지만 갱신 루틴 미문서화

`docs/knowledge/source-targets.md`의 import pool 및 exclusions를 정기적으로 검토하는 워크플로우를 `docs/knowledge/operator-runbook.md`에 명시한다. GBrain 브레인 repo(`~/brain`)와의 동기화 빈도 및 트리거 조건을 기록한다.

---

### VAULT-003 · Obsidian 노트 내부 링크 무결성 자동 확인
**우선순위:** 낮음 | **근거:** `Keelim-Knowledge-Vault.md` — `verify_knowledge_vault_links.py`가 존재하나 실행 주기 불명

`verify_knowledge_vault_links.py`를 vault 변경이 있을 때마다 실행되도록 서브모듈 업데이트 훅 또는 CI 조건부 단계로 연결한다. broken link가 GBrain import에 포함되지 않도록 방지한다.

---

## 닫힌 아이디어

_없음_
