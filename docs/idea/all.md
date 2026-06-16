# 아이디어 — all

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `all`  
스택: Android / Kotlin — 멀티모듈 Gradle  
상태: 서브모듈 (`develop` 브랜치, 핀 `0643bab4`)  
오픈 아이디어: 2

---

## 열린 아이디어

### [ALL-001] 서브모듈 핀 갱신 자동화 — `develop` 브랜치 추적 누락

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 자동화 기회 / 워크플로우 통합
- **근거:** `docs/CODEMAPS/SUBMODULES.md`. `all` 서브모듈이 `develop` 브랜치를 추적하지만 루트에 핀된 커밋은 `0643bab4`로 고정되어 있음. `./scripts/update-subrepos.sh update`가 자동 패스트포워드를 지원하지만 수동 실행 필요.

`develop`에 새 기능이 머지될 때마다 루트의 서브모듈 포인터를 수동으로 업데이트해야 하는 부담이 있다. 루트 GitHub Actions 워크플로우에 `git submodule update --remote all` 후 드리프트 감지 및 PR 자동 생성 단계를 추가하면 핀 갱신 주기를 줄일 수 있다. `./scripts/update-subrepos.sh`의 기존 `dry-run` 모드를 활용해 변경 내용을 미리 확인한다.

---

### [ALL-002] CodeGraph 초기화 상태 미확인 — 에이전트 코드 탐색 불가

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 문서화 / 크로스프로젝트 레버리지
- **근거:** `docs/CODEMAPS/CODEGRAPH.md`. `all`의 `.codegraph/` 존재 여부가 "unknown — submodule not initialized in this checkout"으로 표시됨.

루트 CodeGraph 디스패처(`bun run cg -- context all "..."`)가 동작하려면 `all` 저장소에 `.codegraph/`가 초기화되어 있어야 한다. 서브모듈을 체크아웃한 후 `codegraph init -i`로 초기화하고 상태를 `docs/CODEMAPS/CODEGRAPH.md` 테이블에 업데이트한다. 멀티모듈 Gradle 프로젝트의 경우 build 산출물과 `.gradle/` 디렉토리를 CodeGraph ignore 패턴에 포함시켜야 한다.

---

## 닫힌 아이디어

_없음_
