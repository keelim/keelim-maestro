# 아이디어 — keelim-vercel

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `keelim-vercel`  
스택: Next.js 16 (App Router) / TypeScript — Vercel 배포  
상태: 서브모듈 (`develop` 브랜치, 핀 `8d29b510`)  
오픈 아이디어: 2

---

## 열린 아이디어

### [KVCL-001] 패키지 로컬 `bun.lock` 드리프트 — 루트 워크스페이스와 불일치 위험

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 운영 위험 감소
- **근거:** `docs/CODEMAPS/frontend.md` "Vercel Deployment". `keelim-vercel`에 독립 `bun.lock`이 있으며 Vercel은 이 파일을 읽는다. 루트 워크스페이스가 의존성을 업그레이드할 때 `keelim-vercel/bun.lock`이 자동으로 갱신되지 않을 수 있음.

루트 `bun install` 후 `keelim-vercel/bun.lock`이 변경되지 않으면 Vercel 빌드는 이전 버전의 패키지를 사용하게 된다. 특히 `@keelim/all-web-ui` 버전이 올라갔을 때 Vercel 빌드가 구버전을 계속 참조하는 상황이 발생할 수 있다. CI에서 `keelim-vercel/bun.lock`의 드리프트를 감지하는 단계를 추가하거나, `bun install --frozen-lockfile` 결과를 루트와 비교하는 검증 스텝을 도입한다.

---

### [KVCL-002] `@keelim/all-web-ui` GitHub Packages 인증 — Vercel 재빌드 시 취약점

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 운영 위험 감소
- **근거:** `docs/CODEMAPS/frontend.md` "Registry Requirements". AWUI-003과 연관. `keelim-vercel`이 `@keelim/all-web-ui`를 `https://npm.pkg.github.com`에서 받아야 하므로 Vercel 환경 변수에 `NODE_AUTH_TOKEN`이 설정되어야 함.

Vercel 팀/조직 변경, 토큰 만료, 또는 새 Vercel 프로젝트 연결 시 빌드가 즉시 실패한다. 현재 `scripts/verify-all-web-ui-integration.sh --full`이 로컬에서 레지스트리 접근을 검증하지만 Vercel 환경은 별도다. Vercel 대시보드의 환경 변수 목록을 루트 문서에 체크리스트로 문서화하고, 토큰 만료 전 알림 시스템(GitHub Secret 갱신 알림 등)을 설정한다.

---

## 닫힌 아이디어

_없음_
