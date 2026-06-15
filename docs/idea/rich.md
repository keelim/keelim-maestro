# 아이디어: rich (관리자 웹 + 알고 트레이딩 백엔드)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/backend.md, docs/CODEMAPS/SUBMODULES.md, docs/CODEMAPS/architecture.md -->

**유형:** autonomous | **스택:** Python/FastAPI + React 19 (Vite) + Kubernetes (Skaffold)
**원격:** github.com/keelim/rich | **브랜치:** master
**현재 상태:** 더티 워킹 트리 (dirty working tree), origin 대비 ahead/behind 없음

---

## 열린 아이디어

### R-1. 더티 워킹 트리 freeze/split — 서브모듈 등록 블로커 해소 (긴급)

**근거:** SUBMODULES.md와 README.md 모두 `rich`의 더티 워킹 트리가 (1) `all-web-ui` 서브모듈 전환, (2) `rich` 자체 pinning, (3) workspace 확장의 블로커라고 명시한다. 더티 상태가 지속되는 한 루트 workspace topology를 안정화할 수 없다.

**제안:** `rich` 리포 안에서: 더티 파일을 분류해 커밋 가능한 변경과 임시 파일을 분리한다. 커밋 가능한 변경은 feature 브랜치에 커밋하고 origin에 push한다. 임시/생성 파일은 `.gitignore`에 추가한다. 완료 후 `bun run report:baseline`으로 clean 상태 확인.

**우선순위:** 긴급 — workspace 확장 전체의 전제 조건.

---

### R-2. Open Trading API 백테스트 결과 시각화 대시보드

**근거:** `rich/open-trading-api/`는 strategy builder와 backtester 두 서브앱을 포함한다(backend.md). 루트에서 `bun run dev:strategy-builder`, `bun run dev:backtester` 헬퍼가 있지만 백테스트 결과를 시각화하는 인터페이스가 코드맵에 언급되지 않는다.

**제안:** `rich/web` 관리자 대시보드에 백테스트 결과 뷰어 페이지를 추가한다. FastAPI 백엔드에서 백테스트 결과를 JSON API로 노출하고 `rich/web`에서 차트(`recharts` 또는 `all-web-ui` 컴포넌트 활용)로 렌더링한다.

**우선순위:** 보통 — R-1 완료 및 `rich` Kubernetes 환경 안정화 후 진행.

---

### R-3. Python 3.13 의존성 리스크 모니터링

**근거:** `rich`는 Python >=3.13을 요구한다(backend.md). 이는 uv workspace에서 가장 높은 최소 버전 요구사항이며, Python 3.13의 보안 패치와 breaking change에 영향을 받는다. 루트 constraint-dependencies는 여러 패키지를 고정하지만 Python 런타임 버전 갱신 알림이 없다.

**제안:** `scripts/` 아래 `check-python-runtime.sh`를 추가해 로컬 Python 버전과 루트 `requires-python` 제약을 비교한다. `uv run python scripts/verify-python-dependency-constraints.py` 실행 결과를 루트 CI에 포함시킨다.

**우선순위:** 낮음 — 현재 Python 3.13이 안정적이며 즉각 위험 없음.

---

### R-4. Kubernetes Skaffold 로컬 스택 장애 대응 runbook 보강

**근거:** `rich`는 Skaffold로 로컬 Kubernetes에서 실행되며 `bun run automation:local -- start rich`로 시작한다(architecture.md). 그러나 Skaffold 루프 실패, PVC 손상, 포트 충돌 등 장애 시나리오의 대응 절차가 `docs/ops/local-automation-stack.md`에 충분히 기술돼 있는지 코드맵에서 확인 불가.

**제안:** `docs/ops/local-automation-stack.md`에 `rich` Skaffold 장애 대응 섹션을 추가한다: (1) 루프 재시작, (2) PVC 상태 확인, (3) namespace 정리 순서, (4) `standby` 후 재시작 절차. `bun run automation:local -- verify rich`의 기대 출력도 문서화.

**우선순위:** 낮음 — 현재 장애 없지만 on-demand 스택의 공통 운영 리스크.
