# `rich` 아이디어 백로그

<!-- 마지막 검토: 2026-06-19 | 열린 아이디어: 2 -->

**유형:** 자율 저장소 (서브모듈 아님)
**스택:** Python >=3.13 / FastAPI + React 19 / Vite + Kubernetes (Skaffold)
**코드맵 출처:** `docs/CODEMAPS/projects/rich.md`
**현재 상태:** 더티 워킹 트리, origin 대비 커밋 앞섬 — 서브모듈 고정 불가

---

## 열린 아이디어

### RICH-01: 워킹 트리 정리 및 origin 동기화로 서브모듈 고정 해제

**근거:** `docs/CODEMAPS/projects/rich.md` — "Dirty working tree; commits ahead of origin; do not pin until reconciled"
**유형:** 운영 리스크 감소
**우선순위:** 높음

`rich` 저장소가 더티 상태이고 origin 대비 커밋이 앞서 있어 루트에서 서브모듈로 고정할 수 없다.
`all-web-ui` 서브모듈 전환과 `youtube` 원격 등록도 이 블로커 해소를 기다린다.
(`docs/CODEMAPS/SUBMODULES.md`: "Expansion Blockers — rich dirty/ahead state — freeze/split before pinning")

**실행 단계:**
1. `bun run report:baseline` 으로 현재 상태 스냅샷 확인
2. `rich` 저장소 내에서 변경사항 커밋 또는 스태시 처리
3. ahead-of-origin 커밋을 `origin/master` 에 푸시
4. `./scripts/update-subrepos.sh status` 로 clean 상태 확인
5. `bun run report:baseline` 재실행 후 루트 서브모듈 고정 진행

**차단 조건:** 없음 (자체 해결 가능)
**해제 후 효과:** `all-web-ui` 서브모듈 전환 및 `youtube` 원격 등록 언블로킹

---

### RICH-02: 로컬 수화 후 rich 코드맵 전체 재생성

**근거:** `docs/CODEMAPS/projects/rich.md` — "Full codemap requires local hydration. Re-run scripts/refresh-codemaps.py after cloning."
**유형:** 코드맵/문서 커버리지 갭
**우선순위:** 중간

현재 `docs/CODEMAPS/projects/rich.md` 는 루트 스텁 수준이다.
Strategy Builder, Backtester, FastAPI 엔드포인트, K8s 매니페스트 구조가 코드맵에 없어
교차 프로젝트 참조와 의존성 분석에 사각지대가 생긴다.

**실행 단계:**
1. RICH-01 완료 후 `rich` 저장소 로컬 수화 확인
2. `scripts/refresh-codemaps.py` 재실행
3. `docs/CODEMAPS/projects/rich.md` 업데이트 결과 검토

**차단 조건:** RICH-01 선행 필요
