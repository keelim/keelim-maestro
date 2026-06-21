# 아이디어 — all-web-ui

<!-- 마지막 검토: 2026-06-21 -->

## 프로젝트 개요

`all-web-ui`는 React 19 + Tailwind 4 기반 공유 UI 컴포넌트 라이브러리.
`@keelim/all-web-ui@0.1.4`로 GitHub Packages에 게시되며, `keelim-vercel`과 `rich/web`이 소비자.
루트 Bun 워크스페이스의 권위 있는 설치/검증 표면.

**현재 상태:** clean vs origin/main — 서브모듈 전환 대기 (`rich` 더티 상태 및 `youtube` 리모트 없음이 선행 블로커)

## 열린 아이디어

### IDEA-001: 루트 서브모듈 정식 등록 준비 완료 체크리스트 작성

**우선순위:** 중간 (선행 블로커 해소 후 높음)
**근거:** `docs/CODEMAPS/SUBMODULES.md` 확장 블로커 #3. AGENTS.md `/all-web-ui` 정책에서 "서브모듈 전환은 `rich` 더티·`youtube` 리모트 블로커 해소 후 원격 URL 기반으로만" 명시. 현재 `all-web-ui`는 공개 리모트를 보유하고 있어 기술적으로 전환 준비가 가장 가까움.

`docs/CODEMAPS/SUBMODULES.md`에 서브모듈 전환 체크리스트를 추가하거나, `idea/all-web-ui.md`에 구체적인 전환 조건을 정리.
조건: (1) `rich` freeze/split 완료, (2) `youtube` 프라이빗 리모트 설정 완료, (3) `bun run report:baseline` 클린 결과.

**완료 기준:**
- 체크리스트의 모든 항목이 충족됨을 `bun run report:baseline`으로 확인
- `git submodule add https://github.com/keelim/all-web-ui.git all-web-ui` 실행 후 `git submodule status`에 정상 등록됨

---

### IDEA-002: `@keelim/all-web-ui` 버전 0.1.5 릴리즈 및 소비자 동기화

**우선순위:** 낮음
**근거:** `docs/CODEMAPS/frontend.md`에서 현재 게시 버전이 `0.1.4`임을 확인. `keelim-vercel`과 `rich/web` 두 소비자가 모두 이 버전을 참조. 루트 Bun 카탈로그는 소비자 버전 드리프트를 막는 공통 검증 표면이므로, 버전 업 시 소비자와의 동기화 절차가 문서화되어야 함.

다음 마이너 버전 릴리즈 시: GitHub Packages 게시 → `keelim-vercel` 및 `rich/web` 의존성 업데이트 → `bun run typecheck:web && bun run build:web` 통과 확인 순서를 CI/릴리즈 체크리스트로 문서화.

**완료 기준:**
- `@keelim/all-web-ui@0.1.5` 이상이 `https://npm.pkg.github.com`에 게시됨
- `./scripts/verify-all-web-ui-integration.sh --full` 통과
- 두 소비자의 의존성 버전이 새 버전으로 업데이트됨
