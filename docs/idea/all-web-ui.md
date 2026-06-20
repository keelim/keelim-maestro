# all-web-ui 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 2 -->

프로젝트 유형: 자율 저장소 (React 19 + Tailwind 4 공유 UI 라이브러리)  
코드맵 참조: `docs/CODEMAPS/projects/all-web-ui.md`, `docs/CODEMAPS/frontend.md`

---

## [OPEN] GitHub Packages 패키지 버전 다음 마이너 릴리즈 준비

**근거:** `docs/CODEMAPS/frontend.md`에 현재 `@keelim/all-web-ui@0.1.4`가 `https://npm.pkg.github.com`에 게시되어 있고 `keelim-vercel`, `rich/web` 두 소비자가 이 버전에 의존한다. 버전이 고정된 채 오랜 기간 유지되면 소비자와의 drift가 누적된다.

**내용:**
1. `all-web-ui` 내 미릴리즈 변경 사항 목록을 확인한다.
2. 다음 마이너 버전(예: 0.2.0)을 위한 변경 로그 초안을 작성한다.
3. GitHub Packages 배포 CI 파이프라인이 정상 동작하는지 검증한다 (`scripts/verify-all-web-ui-integration.sh --full` 포함).
4. 릴리즈 후 `keelim-vercel`과 `rich/web`의 의존성 선언을 신규 버전으로 업데이트한다.

**가치:** 반복 사용 제품 워크플로우 — 소비자 저장소가 명확한 버전 경계를 기준으로 업그레이드를 선택할 수 있게 된다.

---

## [OPEN] 소비자 통합 검증 CI 게이트 강화

**근거:** `docs/CODEMAPS/frontend.md`에 `./scripts/verify-all-web-ui-integration.sh --full`이 "strict static pass/fail gate"로 명시되어 있으나, 루트 CI와의 자동 연동이 코드맵에 확인되지 않는다. 특히 `NODE_AUTH_TOKEN` 의존성이 CI/Vercel 빌드에서 누락되면 패키지 읽기 실패가 발생한다.

**내용:**
1. 루트 CI 파이프라인에서 `./scripts/verify-all-web-ui-integration.sh`가 자동 실행되는지 확인한다.
2. GitHub Actions에 `NODE_AUTH_TOKEN` 시크릿이 정상 구성되어 있는지 점검한다.
3. Vercel 빌드 환경의 `.npmrc` 스코프 매핑과 인증 토큰 설정을 검증한다.
4. 검증 실패 시 명확한 오류 메시지가 출력되도록 스크립트를 개선한다.

**가치:** 운영 리스크 감소 — 소비자 빌드 실패를 배포 전에 차단한다.
