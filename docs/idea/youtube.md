# `youtube` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 자율 child repo (private) | **상태:** remote 없음, 로컬 전용 | **우선순위:** 중간

---

## 열린 아이디어

### YT-001 · Private remote 설정 및 서브모듈 등록 사전 요건 충족
**우선순위:** 중간 | **근거:** `SUBMODULES.md` — "private (no upstream yet)"; 서브모듈 등록 차단 중

`youtube` 리포의 private remote를 설정하고, 워킹트리를 클린 상태로 유지하는 것이 향후 `.gitmodules` 등록의 전제 조건이다.

**작업 순서:**
1. GitHub에 private remote 리포 생성
2. `youtube/` 내부에서 `git remote add origin <private-url>`
3. `git push -u origin <branch>`
4. 클린 상태 확인 후 루트 `SUBMODULES.md` Expansion Blockers 업데이트

**주의:** 루트 `.gitmodules`에 로컬 경로가 아닌 remote URL만 사용.

---

### YT-002 · n8n 워크플로우 및 로컬 K8s 계약 문서화
**우선순위:** 중간 | **근거:** `backend.md` — `youtube` n8n이 로컬 K8s에서 실행되나 루트 계약 문서가 얕음

`docs/ops/local-automation-stack.md`의 `youtube` n8n 섹션을 보강한다. 현재 "on-demand" 런타임으로만 기술되어 있으며, n8n 워크플로우 목록, PVC 레이아웃, 시작/종료 명령이 명시적으로 문서화되어 있지 않다.

---

### YT-003 · easy-release-note Python 패키지 테스트 커버리지 확인
**우선순위:** 낮음 | **근거:** `backend.md` — `uv run --package easy-release-note --group dev pytest youtube/tests` 명령 존재

`youtube/tests/` 디렉토리의 테스트 존재 여부와 커버리지 현황을 확인하고, CI에서 안정적으로 실행되도록 보장한다. `youtube/simple`은 루트 uv 워크스페이스에서 의도적으로 제외된 상태임을 유의.

---

## 닫힌 아이디어

_없음_
