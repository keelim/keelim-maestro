# 아이디어 — all-web-ui

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `all-web-ui`  
스택: React 19 / Tailwind 4 / TypeScript — GitHub Packages에 `@keelim/all-web-ui` 게시  
현재 버전: `0.1.4`  
상태: 자율 저장소 (origin/main 대비 클린) — 서브모듈 전환 대기 중  
오픈 아이디어: 3

---

## 열린 아이디어

### [AWUI-001] 서브모듈 전환 준비 — rich 정리 및 youtube 리모트 확보 후 진행

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 크로스프로젝트 레버리지 / 워크플로우 통합
- **근거:** `docs/CODEMAPS/SUBMODULES.md` "Expansion Blockers" 항목 3번. `all-web-ui`는 이미 퍼블릭 리모트가 있고 origin/main 대비 클린하지만, rich 더티 상태(RICH-001)와 youtube 리모트 없음(YTB-001) 해소 전까지 서브모듈 전환이 보류 중.

`all-web-ui`를 `.gitmodules`에 등록하면 루트 클론만으로 UI 라이브러리를 재현할 수 있어 온보딩이 단순해진다. 현재 자율 저장소로 남아 있어 `bun install` 전 수동 클론이 필요하다(MAESTRO-002 참조). 선결 조건(RICH-001, YTB-001)이 해소되면 `git submodule add https://github.com/keelim/all-web-ui.git all-web-ui`로 전환 가능. 전환 시 루트 `.gitignore`의 `/all-web-ui/` 항목을 제거해야 한다.

---

### [AWUI-002] 패키지 버전 범프 프로세스 미문서화 — 소비자 업그레이드 마찰

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 문서화 / 워크플로우 통합
- **근거:** `docs/CODEMAPS/frontend.md`. `@keelim/all-web-ui@0.1.4`가 `keelim-vercel`과 `rich/web` 두 소비자에서 사용됨. 버전이 올라가면 두 소비자 모두 `package.json`을 수동으로 수정해야 함.

`0.1.4` 이후 버전이 게시될 때 `keelim-vercel`의 `package.json`과 `rich/web`의 `package.json`을 동기화하는 절차가 명시되어 있지 않다. GitHub Packages에 새 버전이 게시되면 소비자 저장소에 PR을 자동으로 여는 Dependabot 설정이나, 버전 동기화 스크립트(`scripts/bump-shared-ui.sh` 등)를 추가하면 마찰을 줄일 수 있다.

---

### [AWUI-003] NODE_AUTH_TOKEN 미설정 시 Vercel / CI 빌드 실패 위험

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 운영 위험 감소
- **근거:** `docs/CODEMAPS/frontend.md` "Registry Requirements". 독립 소비자(`keelim-vercel` Vercel 빌드, CI)는 `@keelim` 스코프에 대한 `.npmrc` 매핑과 `NODE_AUTH_TOKEN`이 없으면 GitHub Packages에서 패키지를 받지 못함. `scripts/verify-all-web-ui-integration.sh --full`이 레지스트리 접근을 검증하지만, Vercel 환경 변수 설정 여부는 별도로 검증하지 않음.

신규 Vercel 프로젝트 연결 또는 CI 환경 재구성 시 `NODE_AUTH_TOKEN` 미설정으로 빌드가 실패하는 사례가 발생할 수 있다. `keelim-vercel`의 README나 루트 문서에 Vercel 환경 변수 설정 가이드와 CI 시크릿 체크리스트를 추가한다.

---

## 닫힌 아이디어

_없음_
