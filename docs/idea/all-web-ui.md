# 아이디어: all-web-ui (공유 UI 컴포넌트 라이브러리)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/frontend.md, docs/CODEMAPS/SUBMODULES.md, docs/CODEMAPS/architecture.md -->

**유형:** autonomous (public remote, 서브모듈 전환 대기) | **스택:** React 19 + Tailwind 4 + TypeScript
**원격:** github.com/keelim/all-web-ui | **브랜치:** main | **현재 버전:** `@keelim/all-web-ui@0.1.4`

---

## 열린 아이디어

### AWU-1. 서브모듈 전환 준비 및 블로커 추적

**근거:** SUBMODULES.md에서 `all-web-ui`는 "pending submodule conversion"이며, 전환 블로커로 `rich`의 더티 워킹 트리와 workspace 안정화가 명시돼 있다. 전환이 완료되면 루트 cloner가 `all-web-ui`를 자동으로 hydrate할 수 있어 온보딩 마찰이 대폭 감소한다.

**제안:** `docs/idea/keelim-maestro.md` 또는 `docs/ops/`에 전환 블로커 체크리스트를 작성한다: (1) `rich` freeze/split 완료, (2) `bun run report:baseline` 이상 없음, (3) `all-web-ui` 원격 URL 검증, (4) `.gitmodules` 추가 + 루트 gitlink 커밋. [rich.md R-1](rich.md)과 연계.

**우선순위:** 보통 — `rich` 더티 상태 해소 후 즉시 실행 가능.

---

### AWU-2. 패키지 버전 범프 및 GitHub Packages publish 자동화

**근거:** 현재 버전 `0.1.4`는 수동으로 범프하고 publish하는 것으로 보인다. 루트 `scripts/` 또는 `package.json` 스크립트에 publish 커맨드가 없다. publish 실패 시 `keelim-vercel`과 `rich/web`의 새 소비자 설치가 중단된다.

**제안:** `all-web-ui` 내에 버전 범프 + `npm publish --registry https://npm.pkg.github.com` + GitHub Release 태그 생성을 하나의 커맨드로 실행하는 스크립트를 추가한다. 루트 `bun run publish:all-web-ui` 래퍼를 통해 호출할 수 있도록 한다.

**우선순위:** 보통 — 다음 패키지 릴리즈 전에 선행 필요.

---

### AWU-3. 소비자별 통합 테스트 범위 확장

**근거:** `scripts/verify-all-web-ui-integration.sh`가 정적 검증을 수행하지만 `rich/web`과 `keelim-vercel`에서 실제 컴포넌트를 렌더링하는 통합 테스트가 없다. `@keelim/all-web-ui` API 변경 시 소비자 런타임 오류가 사전에 감지되지 않는다.

**제안:** `bun run test:web`에 `rich/web` Vitest 스위트를 확장해 `@keelim/all-web-ui` 컴포넌트의 기본 렌더 테스트를 추가한다. `all-web-ui` 자체 스토리북(있는 경우) 또는 Vitest 테스트를 루트 `bun run test:web` 파이프라인에 포함시킨다.

**우선순위:** 낮음 — 현재 정적 타입 검증이 주요 회귀를 잡고 있음.
