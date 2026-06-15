# 아이디어: keelim-vercel (Next.js 웹 앱)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/frontend.md, docs/CODEMAPS/SUBMODULES.md, docs/CODEMAPS/dependencies.md -->

**유형:** 서브모듈 + Vercel 배포 | **스택:** Next.js 16 / TypeScript (App Router)
**원격:** github.com/keelim/keelim-vercel | **브랜치:** develop | **핀:** `8d29b510`

---

## 열린 아이디어

### KV-1. GitHub Packages 인증 토큰 관리 개선

**근거:** `@keelim/all-web-ui`는 `https://npm.pkg.github.com`에서 배포되며, standalone 소비자(`keelim-vercel`)는 `NODE_AUTH_TOKEN`과 `.npmrc` 범위 매핑이 필요하다(frontend.md). Vercel 빌드 환경에서 토큰이 누락되면 빌드가 실패한다. 루트 문서에 이 리스크가 언급돼 있지만 토큰 로테이션이나 실패 감지 절차가 없다.

**제안:** `scripts/` 또는 `docs/ops/`에 Vercel secret 설정 runbook을 추가한다. 루트 `verify-all-web-ui-integration.sh --full`이 인증 실패를 명확히 감지하도록 오류 메시지를 개선하고, CI에서 토큰 만료를 조기에 경보하는 단계를 추가한다.

**우선순위:** 높음 — 토큰 만료 시 Vercel 프로덕션 배포 즉시 실패.

---

### KV-2. Vercel 배포 상태 루트 모니터링 통합

**근거:** `keelim-vercel`은 Vercel에 배포되지만 루트에서 최신 배포 상태(성공/실패, 커밋 SHA)를 확인하는 스크립트가 없다. `bun run report:baseline`은 Git 상태만 보고하며 Vercel 배포 상태는 포함하지 않는다.

**제안:** `bun run automation:local` 또는 별도 스크립트에 Vercel 배포 상태 조회를 추가한다. Vercel CLI(`vercel inspect`)나 GitHub Actions 워크플로 상태를 통해 최신 프로덕션 배포 결과를 루트 상태 리포트에 포함시킨다.

**우선순위:** 낮음 — 현재 Vercel 대시보드에서 직접 확인 가능하지만 루트 통합 시 에이전트 가시성 향상.
