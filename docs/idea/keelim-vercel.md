# `keelim-vercel` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 등록 서브모듈 | **상태:** clean vs origin/develop (pinned `8d29b510`) | **우선순위:** 중간

---

## 열린 아이디어

### VERCEL-001 · NODE_AUTH_TOKEN CI/Vercel 인증 자동화
**우선순위:** 높음 | **근거:** `frontend.md`, `keelim-vercel.md` — GitHub Packages `@keelim` 스코프 인증이 CI와 Vercel 빌드 모두 필요

`@keelim/all-web-ui` 패키지를 `https://npm.pkg.github.com`에서 설치하려면 `NODE_AUTH_TOKEN` 또는 GitHub CLI 토큰이 필요하다. 현재 CI/Vercel 빌드 환경에서 이 토큰이 안정적으로 주입되는지 확인되지 않았다.

**검토할 것:**
- Vercel 프로젝트 환경 변수에 `NODE_AUTH_TOKEN` 설정 여부
- GitHub Actions CI에서 `@keelim` 스코프 설치 성공 여부
- `.npmrc` scope mapping 파일 존재 및 내용 확인

---

### VERCEL-002 · App Router 페이지 codemap 갱신
**우선순위:** 낮음 | **근거:** `keelim-vercel.md` — 서브모듈 미초기화로 파일 카운트 `—` 상태

서브모듈 초기화 후 `scripts/refresh-codemaps.py`를 실행하여 Next.js App Router 페이지 구조와 라우트 목록을 codemap에 반영한다.

---

### VERCEL-003 · all-web-ui 버전 핀 검토 주기 설정
**우선순위:** 낮음 | **근거:** `frontend.md` — 패키지 로컬 `bun.lock`이 standalone 소비자 폴백으로 존재

`keelim-vercel/package.json`의 `@keelim/all-web-ui` 버전이 GitHub Packages 최신 출판 버전과 동기화되도록 분기별 검토 루틴을 수립한다.

---

## 닫힌 아이디어

_없음_
