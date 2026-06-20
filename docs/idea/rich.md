# rich 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 2 -->

프로젝트 유형: 자율 저장소 (Python + React 어드민 스택)  
코드맵 참조: `docs/CODEMAPS/projects/rich.md`, `docs/CODEMAPS/backend.md`

---

## [OPEN] dirty 워킹 트리 freeze/split 정리

**근거:** `docs/CODEMAPS/projects/rich.md` "Pre-Pinning Requirements"에 명시. 코드맵 전반에서 "dirty working tree" 경고가 반복된다. 이 상태는 루트 서브모듈 확장의 가장 큰 단일 차단 요소다.

**내용:**
1. `rich` 워킹 트리에서 uncommitted 변경 사항을 목적별로 분류한다 (작업 중인 기능 / 설정 파일 / 임시 파일).
2. 활성 작업은 feature 브랜치로 분리하거나 stash한다.
3. 불필요한 파일은 `.gitignore`에 추가하거나 삭제한다.
4. `origin/master` 대비 앞선 커밋을 push한다.
5. 루트에서 `bun run report:baseline`으로 clean 확인 후 keelim-maestro 이슈에 완료 보고한다.

**가치:** 운영 리스크 감소 + 교차 프로젝트 레버리지 — 해소 즉시 all-web-ui, youtube 서브모듈 전환 경로가 열린다.

---

## [OPEN] 알고 트레이딩 API (전략 빌더 / 백테스터) 루트 연동 문서화

**근거:** `docs/CODEMAPS/backend.md`에 `rich/open-trading-api/strategy_builder/` 및 `rich/open-trading-api/backtester/` 경로와 루트 헬퍼 스크립트(`bun run dev:strategy-builder`, `bun run dev:backtester`)가 등록되어 있으나, 이 경로들이 루트 Bun 워크스페이스 멤버가 아님에도 공식 진입점처럼 사용된다. 세부 API 문서와 로컬 Kubernetes 스택과의 연동 방법이 명시된 문서가 없다.

**내용:**
1. `docs/ops/local-automation-stack.md`에 strategy_builder / backtester 로컬 개발 플로우 섹션을 추가한다.
2. 루트 헬퍼 스크립트가 위임하는 실제 child-repo 커맨드를 명시한다.
3. 로컬 K8s(`bun run automation:local -- start rich`) 없이 단독 실행 가능 여부를 확인하고 기록한다.

**가치:** 문서/코드맵 커버리지 갭 해소 — 새 기여자가 트레이딩 API를 독립적으로 실행할 수 있게 된다.
