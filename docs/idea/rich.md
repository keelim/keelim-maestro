# 아이디어 — rich

<!-- 마지막 검토: 2026-06-21 -->

## 프로젝트 개요

`rich`는 Python(FastAPI) 기반 어드민 API + React(Vite) 관리 대시보드 + 알고 트레이딩 플랫폼으로 구성된 자율 자식 레포지터리.
루트 Bun 워크스페이스(`rich/web`)와 uv 워크스페이스(`keelim-rich` 패키지) 양쪽에 참여.
로컬 Kubernetes(Skaffold)로 실행되며, 하위에 `strategy_builder`와 `backtester` 두 개의 Open Trading API 서브앱을 보유.

**현재 상태:** 더티 워킹트리 — 루트 서브모듈 확장 블로커 1번

## 열린 아이디어

### IDEA-001: 더티 워킹트리 freeze/split 실행

**우선순위:** 높음
**근거:** `docs/CODEMAPS/SUBMODULES.md` 확장 블로커 #1. `docs/CODEMAPS/architecture.md` 및 README에서 반복 언급. `rich` 더티 상태가 `all-web-ui` 서브모듈 전환과 전체 서브모듈 확장을 막는 공통 전제조건.

미커밋 변경사항을 논리 단위로 분류(freeze)하여 최소 가역적 커밋으로 분리(split) 후 `origin/master`에 푸시.
이후 `bun run report:baseline`으로 상태를 검증하고, 서브모듈 전환 계획을 재평가.

**완료 기준:**
- `git status --short` 결과 깨끗함
- `git log origin/master..HEAD` 앞서는 커밋이 없거나 의도된 것만 남음
- 루트에서 `git submodule status` 실행 시 `rich` 항목이 더 이상 잠재적 더티 상태로 표시되지 않음

---

### IDEA-002: 전략 빌더·백테스터 통합 테스트 자동화

**우선순위:** 중간
**근거:** `docs/CODEMAPS/backend.md`에 `uv run --package keelim-rich --group dev pytest rich/tests` 명령이 명시되어 있으나, CI 트리거 여부가 코드맵에 없음. `strategy_builder`와 `backtester`는 루트 편의 스크립트(`bun run dev:strategy-builder`, `bun run dev:backtester`)로 접근 가능하지만, 자동화 검증 체계가 불명확.

루트 uv 워크스페이스 pytest를 GitHub Actions 또는 로컬 훅으로 자동 트리거하는 CI 설정을 추가.
`strategy_builder` → `backtester` 파이프라인의 엔드-투-엔드 스모크 테스트를 하나 이상 작성.

**완료 기준:**
- `uv run --package keelim-rich --group dev pytest rich/tests` 가 zero-exit로 통과
- CI 실행 증거 또는 pre-push 훅 설정 확인
