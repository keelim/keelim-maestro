# 아이디어 — keelim-plugin

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `keelim-plugin`  
스택: Python — Claude/Codex 스킬, 코드맵 생성기, 자동화 스크립트  
상태: 서브모듈 (`main` 브랜치, 핀 `a3463396`)  
오픈 아이디어: 2

---

## 열린 아이디어

### [KPLG-001] `refresh-codemaps.py` CI 자동 실행 — 코드맵 신선도 자동 유지

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 자동화 기회 / 문서 적시성
- **근거:** `docs/CODEMAPS/SCRIPTS.md`. `scripts/refresh-codemaps.py`가 존재하며 `docs/CODEMAPS/` 파일들에 `Generated: 2026-06-16` 타임스탬프가 기록되어 있다. 현재 이 스크립트는 수동으로만 실행됨. MAESTRO-003과 연관.

`keelim-plugin`이 Claude/Codex 스킬과 자동화 스크립트를 담당하는 저장소이므로, 코드맵 갱신 트리거 스킬이나 GitHub Actions 워크플로우를 이 저장소에서 구현하는 것이 자연스럽다. 루트 파일 변경(`.gitmodules`, `package.json`, `pyproject.toml` 등) 감지 시 `refresh-codemaps.py`를 실행하고 결과를 루트에 커밋하는 워크플로우를 추가하면, 에이전트가 항상 최신 코드맵을 참조할 수 있다.

---

### [KPLG-002] 스킬 인벤토리 문서화 부재 — 에이전트 스킬 발견 가능성 저하

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 문서화 / 크로스프로젝트 레버리지
- **근거:** `docs/CODEMAPS/architecture.md`. `keelim-plugin`이 "Claude/Codex skill plugin (codemap generator, etc.)"으로 명시되지만, 루트 코드맵에서 어떤 스킬이 존재하는지 목록이 없음. `bun run cg -- context keelim-plugin "skill inventory"`로 조회해야만 확인 가능.

현재 어떤 스킬이 있는지 루트에서 빠르게 파악할 수 없다. `keelim-plugin` 저장소에 `SKILLS.md` 또는 `README.md` 스킬 인벤토리 테이블을 추가하면, 에이전트와 개발자 모두 활용 가능한 스킬을 즉시 파악할 수 있다. 루트 코드맵이 갱신될 때 이 테이블도 함께 최신화되도록 `refresh-codemaps.py`에 포함시킨다.

---

## 닫힌 아이디어

_없음_
