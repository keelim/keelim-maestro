# 아이디어: youtube (YouTube Shorts 제작 + Easy Release Note)

<!-- 마지막 검토: 2026-06-15 -->
<!-- 코드맵 근거: docs/CODEMAPS/backend.md, docs/CODEMAPS/SUBMODULES.md, docs/CODEMAPS/frontend.md -->

**유형:** autonomous (private, 원격 없음) | **스택:** TypeScript (Remotion) + Python (Easy Release Note)
**원격:** 없음 (private local checkout) | **브랜치:** —
**현재 상태:** 로컬 private checkout; upstream 없음; 재현 가능한 클론 워크플로 없음

---

## 열린 아이디어

### YT-1. Private Remote 설정 — 재현 가능한 클론 워크플로 확보 (긴급)

**근거:** SUBMODULES.md에 따르면 `youtube`는 원격이 없는 완전한 로컬 checkout이다. 로컬 머신 장애 또는 환경 재구성 시 `youtube` 리포를 복구할 방법이 없다. 루트 README.md도 이를 "다음 안전 단계" 항목으로 언급한다.

**제안:** GitHub에 private 리포를 생성하고(`github.com/keelim/youtube` 또는 private fork), `git remote add origin <private-url>` 및 `git push -u origin <branch>`로 초기 push한다. 이후 `docs/ops/`에 복구 절차를 문서화한다. 서브모듈 전환은 remote 확보 + clean working tree 이후.

**우선순위:** 긴급 — 현재 유일한 복사본이 로컬에만 존재하는 운영 위험.

---

### YT-2. n8n 워크플로 백업 자동화

**근거:** `youtube` n8n은 로컬 Kubernetes PVC에 워크플로 상태를 저장한다(backend.md). PVC는 루트에서 관리하지 않으며 별도 백업이 없다. `bun run automation:local -- standby`로 n8n을 종료해도 PVC는 유지되지만, Kubernetes 네임스페이스 삭제나 클러스터 재구성 시 워크플로 손실 위험이 있다.

**제안:** n8n 워크플로를 JSON으로 export해 `youtube` 리포 내 `workflows/` 디렉터리에 버전 관리하는 스크립트를 추가한다. `bun run automation:local`의 `standby` 또는 `stop n8n` 커맨드 전에 자동 export를 실행하거나, cron 기반으로 주기적으로 실행한다.

**우선순위:** 높음 — YT-1 완료 직후 실행 권장.

---

### YT-3. Easy Release Note 파이프라인 루트 통합

**근거:** `easy-release-note`는 루트 uv workspace 멤버이며 `uv run --package easy-release-note --group dev pytest youtube/tests`로 테스트할 수 있다(backend.md). 그러나 실제 릴리즈 노트 생성 트리거 방법이 루트 docs에 없다. 루트 `bun run automation:local`에도 포함되지 않는다.

**제안:** `bun run automation:local -- start n8n` 이후 n8n 워크플로에서 Easy Release Note를 호출하는 흐름을 문서화한다. 또는 루트 `package.json`에 `release-note:generate` 스크립트를 추가해 `uv run --package easy-release-note`를 래핑한다.

**우선순위:** 낮음 — YT-1 완료 및 리포 안정화 후 진행.
