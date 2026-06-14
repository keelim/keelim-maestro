# `rich` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 자율 child repo | **상태:** dirty working tree, origin/master 앞서감 | **우선순위:** 높음

---

## 열린 아이디어

### RICH-001 · dirty working tree 해소 및 origin 푸시
**우선순위:** 긴급 | **근거:** `rich.md` — dirty 상태가 `all-web-ui` 서브모듈 변환을 차단

`rich` 리포의 미커밋 변경사항을 정리하고, origin/master보다 앞서 있는 커밋을 푸시한다.
이 작업이 완료돼야 `all-web-ui` 공식 서브모듈 변환 및 추후 `rich` 자체 서브모듈 등록이 가능해진다.

**작업 순서:**
1. `rich/` 내부에서 `git status`, `git diff` 확인
2. 변경사항 커밋 또는 stash (freeze/split 원칙 준수)
3. `git push origin master`
4. 루트에서 `bun run report:baseline` 재실행하여 상태 확인

**완료 기준:** `bun run report:baseline` 결과에서 `rich`가 clean 상태로 보고됨.

---

### RICH-002 · Open Trading API 통합 검증 자동화
**우선순위:** 중간 | **근거:** `backend.md` — strategy_builder / backtester 두 서브앱이 독립적으로 존재

전략 빌더(`rich/open-trading-api/strategy_builder/`)와 백테스터(`rich/open-trading-api/backtester/`)의 FastAPI 엔드포인트에 대한 통합 테스트를 추가한다. 현재 루트 uv 워크스페이스에 `pytest rich/tests`만 있고, Open Trading API 서브앱별 테스트는 별도로 확인되지 않음.

**검토할 것:**
- `rich/tests/` 범위가 Open Trading API를 포함하는지 확인
- 포함하지 않으면 `rich/open-trading-api/*/tests/` 경로 추가 검토

---

### RICH-003 · Kubernetes Skaffold 스택 문서화 보강
**우선순위:** 낮음 | **근거:** `backend.md` — 로컬 K8s는 Skaffold 관리이나 루트 계약 문서가 `docs/ops/`에만 존재

`rich/` 내 Skaffold 매니페스트, PVC 레이아웃, Secret 구성을 `docs/ops/local-automation-stack.md`와 연결하는 계약 문서를 보강한다. 운영 리스크 감소가 목적.

---

## 닫힌 아이디어

_없음_
