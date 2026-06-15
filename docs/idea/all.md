# 아이디어: all (Android 앱)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/architecture.md, docs/CODEMAPS/SUBMODULES.md -->

**유형:** 서브모듈 | **스택:** Android / Kotlin (multi-module Gradle)
**원격:** github.com/keelim/all | **브랜치:** develop | **핀:** `0643bab4`

---

## 열린 아이디어

### A-1. android-support 서브모듈 핀 최신화 프로세스 구축

**근거:** `android-support`는 현재 `v0.0.8-4`(커밋 `485a2e40`)에 detached된 상태다. `all` 앱이 이 라이브러리를 사용한다면 업스트림 패치와 단절될 위험이 있다. 루트 코드맵(SUBMODULES.md)은 이 고정 상태를 언급하지만 핀 갱신 절차가 없다.

**제안:** `all` 내에서 `android-support` 의존성 버전을 명시적으로 추적하고, `update-subrepos.sh` 실행 후 핀 갱신 커밋이 필요한 경우를 감지하는 루트 스크립트 훅을 추가한다.

**우선순위:** 보통 — 현재 detached 상태가 빌드 실패를 유발하는지 확인 필요.

---

### A-2. 루트에서 Android CI 빌드 상태 가시화

**근거:** keelim-maestro 루트는 `bun run test`, `bun run typecheck:web` 등 웹 프론트엔드 검증 스크립트를 보유하지만, Android 빌드 상태를 확인하는 루트 레벨 커맨드가 없다. `all`이 서브모듈이므로 루트에서 빌드 상태를 빠르게 파악할 수 없다.

**제안:** `scripts/` 아래에 `check-android-status.sh`(또는 `bun run report:android`) 추가. GitHub Actions CI 결과를 polling하거나 서브모듈 상태 + 브랜치 다이버전스만 출력하는 경량 스크립트로 시작한다.

**우선순위:** 낮음 — 루트 test suite와 독립적으로 동작하는 CI가 이미 있을 가능성.

---

### A-3. 멀티모듈 Gradle 모듈 경계 코드맵 추가

**근거:** `all`은 "multi-module Gradle" 구조라고 명시돼 있지만 루트 코드맵(architecture.md)에는 모듈 목록이 없다. 어떤 Gradle 모듈이 있는지 루트에서 파악 불가.

**제안:** `docs/CODEMAPS/architecture.md` 또는 `docs/CODEMAPS/all.md`에 `all`의 주요 Gradle 모듈을 열거한다 (`:app`, `:feature:*`, `:core:*` 등). keelim-plugin의 코드맵 생성기를 통해 자동화할 수 있다.

**우선순위:** 낮음 — 코드맵 커버리지 개선 항목.
