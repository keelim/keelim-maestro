# `all-web-ui` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 자율 child repo | **상태:** clean vs origin/main, 서브모듈 변환 대기 | **우선순위:** 중간

---

## 열린 아이디어

### UI-001 · 서브모듈 변환 실행 계획 수립
**우선순위:** 중간 | **근거:** `all-web-ui.md` — `rich` 해소 후 즉시 실행 가능한 유일한 전환 대상

`rich` dirty 상태 해소(RICH-001) 이후 `all-web-ui`를 공식 서브모듈로 등록한다.

**전제 조건:**
1. RICH-001 완료 (rich 클린 상태 확인)
2. `bun run report:baseline` 재실행하여 워크스페이스 전체 상태 확인
3. remote URL `https://github.com/keelim/all-web-ui` 사용 (로컬 경로 서브모듈 금지)

**작업 순서:**
```bash
git submodule add https://github.com/keelim/all-web-ui all-web-ui
git submodule update --init all-web-ui
git add .gitmodules all-web-ui
git commit -m "chore: register all-web-ui as submodule"
```

---

### UI-002 · @keelim/all-web-ui 버전 동기화 로드맵
**우선순위:** 중간 | **근거:** `frontend.md` — 현재 0.1.4 출판; keelim-vercel과 rich/web 두 소비자가 존재

소비자(`keelim-vercel`, `rich/web`) 버전 요구사항과 GitHub Packages 출판 버전(현재 0.1.4)의 동기화 상태를 정기적으로 확인한다.
버전 드리프트 발생 전에 패키지 릴리스 루틴을 문서화한다.

**검토할 것:**
- 소비자의 `package.json`에 명시된 `@keelim/all-web-ui` 버전 범위
- `./scripts/verify-all-web-ui-integration.sh --full` 결과 (GitHub Packages 가시성 포함)

---

### UI-003 · 시각적 회귀 테스트 준비도 평가
**우선순위:** 낮음 | **근거:** `frontend.md` — `bun run report:shared-ui`가 visual-regression readiness 항목을 포함

`bun run report:shared-ui` 출력에서 시각적 회귀 준비도 섹션을 검토하고, Storybook 또는 Playwright 기반 스냅샷 테스트 추가 가능성을 평가한다.

---

## 닫힌 아이디어

_없음_
