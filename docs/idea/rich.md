# 아이디어 — rich

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `rich`  
스택: Python >=3.13 + FastAPI, React (Vite), Open Trading API, Skaffold / K8s  
상태: 자율 저장소 — 워킹트리 더티, origin/master 대비 드리프트 없음  
오픈 아이디어: 3

---

## 열린 아이디어

### [RICH-001] 워킹트리 더티 상태 동결/분할 — 서브모듈 등록 전제조건

- **상태:** 열림
- **우선순위:** P1
- **카테고리:** 운영 위험 감소 / 크로스프로젝트 레버리지
- **근거:** `docs/CODEMAPS/SUBMODULES.md` "Expansion Blockers" 및 `docs/CODEMAPS/keelim-maestro.md`. 루트가 `rich`의 더티 상태를 서브모듈 확장의 첫 번째 블로커로 명시.

`rich` 워킹트리에 커밋되지 않은 변경이 있어 루트에서 안전하게 핀할 수 없는 상태다. 이 상태가 지속되면 `all-web-ui` 서브모듈 전환도 함께 막힌다. `rich` 자체 저장소에서 미완성 변경을 정리하거나(커밋 또는 stash), 인프라/기능 변경을 별도 브랜치로 분리한 뒤 `origin/master`에 머지해야 한다. 루트 SUBMODULES.md의 "Expansion Blockers"에서 가장 먼저 해소해야 할 항목.

---

### [RICH-002] Open Trading API 하위 앱 루트 워크스페이스 미포함 — 빌드 일관성 위험

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 운영 위험 감소 / 워크플로우 통합
- **근거:** `docs/CODEMAPS/WORKSPACE.md` 및 `docs/CODEMAPS/backend.md`. `rich/open-trading-api/strategy_builder/frontend`와 `rich/open-trading-api/backtester/frontend`는 루트 Bun 워크스페이스 멤버가 아님. 루트는 편의 스크립트(`bun run dev:strategy-builder`, `bun run dev:backtester`)만 제공.

전략 빌더와 백테스터의 프론트엔드가 루트 카탈로그 버전을 사용하지 않아 의존성 드리프트가 발생할 수 있다. `@keelim/all-web-ui` 같은 공유 패키지를 이 하위 앱이 사용한다면 독립 설치로 인해 버전 불일치가 생긴다. 현재 사용 여부를 확인하고, 필요하다면 의존성 정렬 전략(루트 워크스페이스 편입 또는 카탈로그 고정 강제)을 수립해야 한다.

---

### [RICH-003] Python >=3.13 강제 요건 — uv 워크스페이스 일관성 유지 점검

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 운영 위험 감소
- **근거:** `docs/CODEMAPS/backend.md`. `keelim-rich`가 Python >=3.13을 요구하며 루트 uv 워크스페이스의 `requires-python`이 이에 맞춰져 있음. `youtube`는 더 낮은 범위를 선언.

CI 환경 또는 로컬 개발 환경에서 Python 버전이 맞지 않으면 `uv run --package keelim-rich` 명령이 실패한다. `scripts/verify-python-dependency-constraints.py`가 제약 정렬을 확인하지만 Python 버전 자체를 검사하지는 않는다. CI 매트릭스에 Python 3.13 고정 검증 단계를 추가하거나, 루트 테스트 스크립트에 버전 체크를 포함시키는 것을 검토한다.

---

## 닫힌 아이디어

_없음_
