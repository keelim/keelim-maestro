# android-support 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 1 -->

프로젝트 유형: 등록 서브모듈 (Android 공유 지원 라이브러리, detached)  
코드맵 참조: `docs/CODEMAPS/projects/android-support.md`

---

## [OPEN] v0.0.8-4 detach 상태 검토 및 업스트림 추적 전략 수립

**근거:** `docs/CODEMAPS/projects/android-support.md`에 "Pinned at v0.0.8-4; no local upstream tracking branch (detached state is intentional)."로 명시되어 있다. detached 핀 전략은 안정성을 보장하지만, `origin/main`에 새 릴리즈가 쌓이면 `all` 앱과의 호환성 gap이 발생할 수 있다. 의도적 detach인지 업그레이드 계획이 있는지 명시된 기록이 없다.

**내용:**
1. `origin/main`에서 v0.0.8-4 이후 릴리즈 목록과 변경 로그를 확인한다.
2. `all` Android 앱이 현재 핀 버전 이상을 요구하는지 의존성 선언을 검토한다.
3. 업그레이드 필요성이 없으면 코드맵에 "의도적 detach, 업그레이드 불필요" 이유를 명시한다.
4. 업그레이드가 필요하면 루트 `bun run report:baseline` 실행 후 새 태그로 핀을 갱신한다.

**가치:** 운영 리스크 감소 — detach 이유를 명시하면 불필요한 업그레이드 시도를 방지하고 실제 필요 시 경로를 명확히 한다.
