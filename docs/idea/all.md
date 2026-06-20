# all 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 1 -->

프로젝트 유형: 등록 서브모듈 (Android 멀티모듈 Gradle 앱)  
코드맵 참조: `docs/CODEMAPS/projects/all.md`

---

## [OPEN] 서브모듈 초기화 후 전체 코드맵 갱신

**근거:** `docs/CODEMAPS/projects/all.md`에 "Not initialized in a fresh root checkout. Run `git submodule update --init all` to hydrate. Full codemap requires child hydration."로 명시되어 있다. 현재 `all` 서브모듈의 내부 모듈 구조, 의존성, 빌드 구성이 루트 코드맵에 전혀 반영되어 있지 않다.

**내용:**
1. `git submodule update --init all`로 서브모듈을 초기화한다.
2. `scripts/refresh-codemaps.py`를 실행하여 `all` 프로젝트의 코드맵을 생성한다.
3. 멀티모듈 Gradle 구조(앱 모듈, 피처 모듈, 공유 라이브러리 모듈)를 코드맵에 기술한다.
4. `android-support`와의 의존성 관계를 코드맵에 명시한다.

**가치:** 문서/코드맵 커버리지 갭 해소 — 가장 큰 Android 앱 코드맵이 누락된 상태를 해소한다.
