# 아이디어 — youtube

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `youtube`  
스택: TypeScript + Python / Remotion, n8n (K8s), Easy Release Note  
상태: 자율 저장소 — 프라이빗 리모트 없음  
오픈 아이디어: 2

---

## 열린 아이디어

### [YTB-001] 프라이빗 리모트 없음 — 재해 복구 불가 상태

- **상태:** 열림
- **우선순위:** P1
- **카테고리:** 운영 위험 감소
- **근거:** `docs/CODEMAPS/SUBMODULES.md` "Autonomous Local Repos": `youtube`가 "private (no upstream yet)"으로 명시. SUBMODULES.md의 서브모듈 확장 블로커 항목 2번.

`youtube`는 YouTube Shorts 영상 렌더링(Remotion), Easy Release Note 자동화, n8n 워크플로우를 포함하는 프로덕션 저장소인데, 로컬에만 존재한다. 로컬 환경 장애 시 복구가 불가능하다. 우선 운영자 승인 하에 프라이빗 GitHub 리포지토리를 생성하고, `git remote add origin <url>` 후 첫 push를 진행해야 한다. 이 작업이 완료되면 SUBMODULES.md의 블로커 항목 2번이 해소된다.

---

### [YTB-002] n8n 워크플로우 버전 관리 부재 — 로컬 K8s 상태에만 의존

- **상태:** 열림
- **우선순위:** P2
- **카테고리:** 운영 위험 감소 / 문서화
- **근거:** `docs/CODEMAPS/backend.md`. n8n 워크플로우가 로컬 Kubernetes PVC에 저장됨. K8s 네임스페이스 삭제나 PVC 손실 시 워크플로우 복구 방법이 문서화되어 있지 않음.

n8n 워크플로우는 `bun run automation:local -- standby`로 스케일 다운해도 PVC에 남아 있지만, PVC 자체가 삭제되거나 K8s 환경이 초기화되면 워크플로우가 사라진다. n8n의 내보내기(`n8n export:workflow --all`) 기능을 활용해 워크플로우 JSON을 `youtube` 저장소에 주기적으로 커밋하는 방안을 도입하면 리모트 백업(YTB-001 해소 후)과 결합해 완전한 재현 가능성을 확보할 수 있다.

---

## 닫힌 아이디어

_없음_
