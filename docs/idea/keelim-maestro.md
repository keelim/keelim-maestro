# 아이디어 — keelim-maestro

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `keelim-maestro`  
역할: 워크스페이스 슈퍼프로젝트 / 조율 레이어  
오픈 아이디어: 3

---

## 열린 아이디어

### [MAESTRO-001] `docs/knowledge/` 누락으로 인한 루트 테스트 실패 위험

- **상태:** 열림
- **우선순위:** P1
- **카테고리:** 운영 위험 감소
- **근거:** `scripts/test-workspace.sh` L118-122에서 `docs/knowledge/README.md`, `docs/knowledge/gbrain.md`, `docs/knowledge/source-targets.md`, `docs/knowledge/operator-runbook.md`, `docs/knowledge/verification-contract.md` 존재 여부를 검사. 현재 이 체크아웃에서 `docs/knowledge/` 자체가 없음.

`bun run test`가 knowledge 문서 파일 5개의 존재를 하드코딩으로 검사한다. 이 파일들이 없으면 루트 워크스페이스 계약 테스트가 실패한다. GBrain 문서(`~/brain` 레포 기반)가 정상 운영 환경에는 있을 수 있지만, 이 체크아웃에서는 해당 디렉토리가 없다. 스텁 파일을 루트에 추가하거나, 테스트 스크립트를 파일이 없을 경우 경고만 내도록 완화해야 한다.

---

### [MAESTRO-002] 자율 저장소 수동 하이드레이션 — 온보딩 자동화 필요

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 워크플로우 통합 / 자동화 기회
- **근거:** `README.md` "Bun workspace prerequisites" 섹션. `all-web-ui`, `rich`, `youtube`가 `.gitmodules` 미등록 자율 저장소이므로, 새 클론 후 `bun install` 전에 수동으로 `git clone`해야 한다.

fresh clone 후 `bun install`이 실패하는 이유가 세 자율 저장소의 로컬 경로 의존 때문이다. 현재 README에 hydration 예시가 있지만, 스크립트화되어 있지 않아 `youtube`처럼 프라이빗 리모트가 없는 경우 재현이 불가능하다. `scripts/bootstrap.sh` 같은 대화형 부트스트랩 스크립트를 추가하면 온보딩 마찰을 줄일 수 있다. `youtube` 리모트 확보(youtube.md P1) 이후에 실행 가능.

---

### [MAESTRO-003] 코드맵 자동 갱신 — `refresh-codemaps.py` CI 연동 누락

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 자동화 기회 / 문서 적시성
- **근거:** `scripts/refresh-codemaps.py`가 존재하고 `docs/CODEMAPS/` 파일들에 `Generated: 2026-06-16` 타임스탬프가 있으나, 스크립트가 CI 파이프라인에 연결되어 있지 않음. 코드맵은 수동으로만 갱신된다.

`docs/CODEMAPS/` 파일들이 워크스페이스 상태를 반영하지 못하면 에이전트(Claude, Codex)가 오래된 정보로 작업하게 된다. `refresh-codemaps.py`를 주기적 GitHub Actions 워크플로우(예: 매일 새벽 또는 루트 파일 변경 시)에 연결하면 코드맵 신선도를 자동 유지할 수 있다. `keelim-plugin`이 이미 스킬/스크립트 자동화를 담당하므로 해당 저장소에서 구현을 주도할 수 있다.

---

## 닫힌 아이디어

_없음_
