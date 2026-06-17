# all-web-ui 아이디어 백로그

<!-- 마지막 검토: 2026-06-17 -->
<!-- 열린 아이디어: 1 -->

**저장소:** https://github.com/keelim/all-web-ui  
**유형:** 자율 자식 저장소 (서브모듈 전환 대기)  
**현재 상태:** origin/main과 동기화됨 · 서브모듈 전환 보류

---

## UI-001 서브모듈 전환 준비 체크리스트 관리

**우선순위:** 보통 (RICH-001 완료 후 진행 가능)  
**근거:** `docs/CODEMAPS/projects/all-web-ui.md`에서 "pending submodule conversion; blocked until rich is reconciled and workspace is safe to pin" 확인.
`@keelim/all-web-ui@0.1.4`가 GitHub Packages에 게시되어 `keelim-vercel`과 `rich/web` 두 소비자가 의존 중.
서브모듈 전환 완료 시 루트 초기화 재현성이 높아지고, 소비자 통합 검증이 자동화 가능해진다.

**전환 전 체크리스트:**
1. `rich` RICH-001 완료 확인 (워킹트리 클린·원격 동기화)
2. `./scripts/verify-all-web-ui-integration.sh --full` — GitHub Packages 게시 상태 포함 통과 확인
3. `bun run report:shared-ui` — 소비자(`keelim-vercel`, `rich/web`) 통합 이상 없음 확인
4. `bun run typecheck:web` 및 `bun run build:web` 클린 통과 확인
5. 위 항목 모두 클린 시, 원격 URL(`https://github.com/keelim/all-web-ui`)로 서브모듈 등록 진행

**주의:** 로컬 경로 서브모듈 등록 금지 — 반드시 원격 URL 사용.

**연관 아이디어:** [`rich` RICH-001](rich.md#rich-001-워킹트리-동결-및-원격-동기화)
