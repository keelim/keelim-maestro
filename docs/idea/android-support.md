# `android-support` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 등록 서브모듈 (detached) | **상태:** pinned `485a2e40` (v0.0.8-4), 로컬 upstream 없음 | **우선순위:** 낮음

---

## 열린 아이디어

### AS-001 · v0.0.8-4 이후 신규 릴리스 평가
**우선순위:** 낮음 | **근거:** `android-support.md` — detached at v0.0.8-4; 로컬 upstream 추적 브랜치 없음

`android-support` 리포에 v0.0.8-4 이후 신규 릴리스가 있는지 확인하고, 업그레이드 필요성을 평가한다. 루트 서브모듈 포인터 업데이트 전에 `bun run report:baseline`으로 워크스페이스 상태를 확인한다.

**확인 방법:**
```bash
git submodule update --init android-support
cd android-support
git fetch origin
git log HEAD..origin/main --oneline
```

---

### AS-002 · upstream 추적 브랜치 복원 검토
**우선순위:** 낮음 | **근거:** `android-support.md` — "no local upstream tracking branch (detached state is intentional)"

현재 intentional detached 상태이나, 신규 릴리스 평가(AS-001) 완료 후 업그레이드 결정 시 추적 브랜치를 복원하고 안전한 서브모듈 핀 업데이트 절차를 수행한다.

---

## 닫힌 아이디어

_없음_
