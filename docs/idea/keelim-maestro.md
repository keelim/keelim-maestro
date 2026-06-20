# keelim-maestro 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 3 -->

프로젝트 유형: 루트 조율 레이어  
코드맵 참조: `docs/CODEMAPS/architecture.md`, `docs/CODEMAPS/SUBMODULES.md`, `docs/CODEMAPS/WORKSPACE.md`

---

## [OPEN] rich dirty 상태 해소 → 서브모듈 확장 차단 해제

**근거:** `docs/CODEMAPS/SUBMODULES.md` "Expansion Blockers" 및 `docs/CODEMAPS/projects/rich.md` "Pre-Pinning Requirements"에 명시된 최우선 차단 항목.  
`rich` 워킹 트리의 dirty 상태와 origin/master 대비 앞선 커밋이 `all-web-ui` 서브모듈 전환과 전체 워크스페이스 확장을 막고 있다.

**내용:**
1. `rich` 워킹 트리에서 uncommitted 변경 사항을 freeze/split 방식으로 정리한다.
2. origin/master 대비 앞선 커밋을 push한다.
3. `bun run report:baseline`으로 clean 상태를 확인한다.
4. 차단 해소 후 `all-web-ui` 서브모듈 전환 검토를 재개한다.

**가치:** 교차 프로젝트 레버리지 — 이 한 작업이 `all-web-ui` 공식 등록과 워크스페이스 전체 신뢰성 향상으로 이어진다.

---

## [OPEN] youtube 프라이빗 원격 저장소 설정 및 서브모듈 전환 계획

**근거:** `docs/CODEMAPS/SUBMODULES.md` "Autonomous Local Repos" — `youtube`는 원격 없이 로컬 프라이빗 체크아웃 상태이며, `README.md`에 "no upstream yet"으로 명시되어 있다.

**내용:**
1. `youtube` 저장소를 위한 프라이빗 GitHub 원격을 생성/등록한다.
2. 로컬 워킹 트리를 clean 상태로 정리한 후 최초 push를 수행한다.
3. 원격이 안정화되면 `.gitmodules` 등록 가능 여부를 `bun run report:baseline`으로 검증한다.
4. n8n 워크플로우와 Remotion 렌더러가 포함된 private 원격 접근 권한 정책을 문서화한다.

**가치:** 운영 리스크 감소 — 원격 없는 저장소는 머신 장애 시 데이터 손실 위험이 있다.

---

## [OPEN] all-web-ui 공식 서브모듈 등록 (rich 해소 후 차순위)

**근거:** `docs/CODEMAPS/projects/all-web-ui.md` "Submodule Conversion Blockers" — 퍼블릭 원격(`github.com/keelim/all-web-ui`)이 이미 존재하지만 `rich` dirty 상태 해소 전까지 `.gitmodules` 등록이 차단된 상태다.

**내용:**
1. `rich` dirty 상태 해소 이슈가 완료된 후 진행한다.
2. `./scripts/update-subrepos.sh status`로 all-web-ui 상태를 확인한다.
3. 원격 URL(`https://github.com/keelim/all-web-ui`)만 사용하여 `.gitmodules`에 추가한다.
4. `scripts/verify-all-web-ui-integration.sh --full`로 통합 검증을 실행한다.

**가치:** 워크플로우 통합 — 공식 gitlink 등록으로 루트 클론 즉시 all-web-ui를 초기화할 수 있다.
