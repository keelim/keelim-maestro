# youtube 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 2 -->

프로젝트 유형: 자율 저장소 (YouTube Shorts 프로덕션 — Remotion + Easy Release Note)  
코드맵 참조: `docs/CODEMAPS/SUBMODULES.md`, `docs/CODEMAPS/backend.md`

---

## [OPEN] 프라이빗 원격 저장소 설정 및 초기 push

**근거:** `docs/CODEMAPS/SUBMODULES.md` "Autonomous Local Repos"에 `youtube` 항목이 "Private local checkout; not a submodule"으로 명시되어 있다. 원격 없이 로컬에만 존재하는 상태는 데이터 손실 위험이 가장 높은 시나리오다. `docs/CODEMAPS/SUBMODULES.md` "Expansion Blockers" 항목 2에도 직접 언급된다.

**내용:**
1. GitHub에 프라이빗 `keelim/youtube` 저장소를 생성한다.
2. 로컬 `youtube/` 워킹 트리를 clean 상태로 정리한다.
3. `git remote add origin <private-url>` 후 초기 push를 수행한다.
4. 루트 `SUBMODULES.md` 및 `README.md`의 상태 테이블을 갱신한다.
5. 원격 안정화 후 서브모듈 전환 가능 여부를 `bun run report:baseline`으로 확인한다.

**가치:** 운영 리스크 감소 — 유일한 사본이 로컬에만 있는 가장 위험한 상태를 해소한다.

---

## [OPEN] n8n 워크플로우 백업 및 버전 관리 전략

**근거:** `docs/CODEMAPS/backend.md`에 `youtube` n8n 워크플로우가 로컬 Kubernetes PVC에 저장된다고 명시되어 있다. PVC 상태는 K8s 클러스터 삭제 시 손실될 수 있으며, n8n 워크플로우의 Git 버전 관리 전략이 코드맵에 명시되어 있지 않다.

**내용:**
1. n8n 워크플로우를 JSON으로 내보내는 자동화 스크립트를 작성한다.
2. 내보낸 워크플로우 파일을 `youtube` 저장소(원격 설정 후)에 커밋한다.
3. 주기적인 백업 cron을 n8n 자체 또는 루트 자동화 헬퍼에 통합한다.
4. 워크플로우 복원 절차를 `docs/ops/local-automation-stack.md`에 문서화한다.

**가치:** 운영 리스크 감소 — Kubernetes 재구성 시 n8n 워크플로우를 재현 가능하게 복원할 수 있다.
