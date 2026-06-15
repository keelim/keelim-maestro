# 아이디어: android-support (Android 공유 라이브러리)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/architecture.md, docs/CODEMAPS/SUBMODULES.md -->

**유형:** 서브모듈 | **스택:** Android / Kotlin (Gradle 라이브러리)
**원격:** github.com/keelim/android-support | **브랜치:** main | **핀:** `485a2e40` (v0.0.8-4)

---

## 열린 아이디어

### AS-1. 라이브러리 핀 갱신 절차 문서화

**근거:** SUBMODULES.md에 따르면 `android-support`는 `v0.0.8-4`(커밋 `485a2e40`)에 detached된 상태로 "no local upstream"이다. 이 서브모듈을 최신 버전으로 갱신하려면 어떤 절차가 필요한지 루트 문서 어디에도 기술되어 있지 않다.

**제안:** `docs/ops/` 또는 SUBMODULES.md에 서브모듈 핀 갱신 runbook을 추가한다: (1) `git fetch`로 업스트림 확인, (2) `all` 앱에서 호환성 검증, (3) 루트 gitlink 업데이트 + 커밋. 루트 `update-subrepos.sh`가 detached 서브모듈을 감지하고 경고를 출력하도록 확장할 수 있다.

**우선순위:** 보통 — 다음 라이브러리 릴리즈 전에 선행 필요.

---

### AS-2. 라이브러리 릴리즈 버전 루트 가시화

**근거:** `android-support`는 Gradle 라이브러리로 버전 태그(v0.0.8-4)를 관리하지만 keelim-maestro 루트에서 현재 핀 버전과 최신 업스트림 버전을 비교하는 방법이 없다. SUBMODULES.md 수동 편집에 의존한다.

**제안:** `bun run report:baseline` 출력에 서브모듈별 "현재 핀 vs. 업스트림 최신 태그" 비교를 추가하거나, `scripts/` 아래 `check-submodule-versions.sh` 스크립트를 신설한다.

**우선순위:** 낮음 — 코드맵 자동화와 연계해 구현하면 효율적.
