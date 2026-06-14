# `keelim-plugin` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 등록 서브모듈 | **상태:** clean vs origin/main (pinned `a3463396`) | **우선순위:** 중간

---

## 열린 아이디어

### PLUGIN-001 · codemap 자동 갱신 CI 통합
**우선순위:** 높음 | **근거:** `projects/README.md` — 모든 프로젝트 codemap이 `—` 파일 카운트 상태

`scripts/refresh-codemaps.py`는 `keelim-plugin/skills/codebase-codemap/scripts/generate_codemap.py`를 호출한다. 현재 서브모듈이 초기화되지 않으면 codemap 파일 카운트가 `—`으로 남는다. CI 스케줄(예: 주간)에 서브모듈 초기화 → codemap 갱신 → 변경사항 커밋 파이프라인을 추가한다.

**작업 순서:**
```bash
git submodule update --init keelim-plugin
python3 scripts/refresh-codemaps.py
git diff docs/CODEMAPS/
```

---

### PLUGIN-002 · 아이디어 가드너 스킬 추가
**우선순위:** 낮음 | **근거:** `keelim-plugin.md` — 현재 codemap 생성기 스킬만 존재

`keelim-plugin`에 아이디어 백로그 유지보수를 자동화하는 스킬을 추가한다. codemap을 읽고 `docs/idea/` 파일을 업데이트하는 루틴을 Claude/Codex 스킬로 패키징한다.

---

## 닫힌 아이디어

_없음_
