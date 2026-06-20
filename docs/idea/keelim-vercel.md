# keelim-vercel 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 2 -->

프로젝트 유형: 등록 서브모듈 (Next.js 16 / App Router, Vercel 배포)  
코드맵 참조: `docs/CODEMAPS/projects/keelim-vercel.md`, `docs/CODEMAPS/frontend.md`

---

## [OPEN] Vercel / CI 환경 NODE_AUTH_TOKEN 설정 검증 자동화

**근거:** `docs/CODEMAPS/projects/keelim-vercel.md`에 "Requires `.npmrc` scope mapping for `@keelim` + `NODE_AUTH_TOKEN` in CI/Vercel builds"가 명시되어 있다. 이 설정이 누락되면 `@keelim/all-web-ui` 패키지 읽기 실패로 빌드가 중단된다. 현재 자동 검증 메커니즘이 코드맵에 확인되지 않는다.

**내용:**
1. Vercel 프로젝트 설정에서 `NODE_AUTH_TOKEN` 환경 변수가 구성되어 있는지 확인한다.
2. GitHub Actions CI 워크플로에 인증 토큰 유효성 단계를 추가한다.
3. `.npmrc`의 `@keelim` 스코프 매핑이 standalone 설치 시에도 동작하는지 검증한다.
4. 인증 실패 시 명확한 오류 메시지와 해결 가이드를 CI 로그에 포함시킨다.

**가치:** 운영 리스크 감소 — Vercel 배포 실패를 사전에 차단하고 온보딩 마찰을 줄인다.

---

## [OPEN] all-web-ui 신규 버전 릴리즈 시 의존성 업그레이드 자동 감지

**근거:** `docs/CODEMAPS/frontend.md`에 `keelim-vercel`이 `@keelim/all-web-ui@0.1.4`를 소비자로 사용한다고 명시되어 있다. `all-web-ui`가 새 버전을 릴리즈하면 `keelim-vercel`의 의존성 선언을 수동으로 갱신해야 하며, 이 절차가 자동화되지 않으면 버전 drift가 발생한다.

**내용:**
1. Dependabot 또는 Renovate Bot을 통해 `@keelim/all-web-ui` GitHub Packages 버전 업데이트를 자동 감지한다.
2. 신규 버전 PR이 생성되면 `bun run typecheck:web`과 `bun run build:web`이 자동 실행되도록 CI를 구성한다.
3. all-web-ui 아이디어 파일과 연계하여 릴리즈 케이던스를 조율한다.

**가치:** 자동화 기회 — 수동 추적 없이 공유 UI 라이브러리 최신 상태를 유지한다.
