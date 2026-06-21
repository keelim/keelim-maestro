# 아이디어 — youtube

<!-- 마지막 검토: 2026-06-21 -->

## 프로젝트 개요

`youtube`는 YouTube Shorts 영상 프로덕션 전용 자율 자식 레포지터리.
TypeScript(Remotion 렌더러, 서비스 툴, 에피소드 패키지)와 Python(`easy-release-note` 패키지) 혼합 스택.
로컬 Kubernetes에서 n8n 워크플로우 자동화를 실행.
루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(`easy-release-note` 패키지) 양쪽에 참여.

**현재 상태:** 프라이빗 로컬 체크아웃 — 리모트 없음 — 루트 서브모듈 확장 블로커 2번

## 열린 아이디어

### IDEA-001: 프라이빗 리모트 설정 및 클린 워킹트리 확보

**우선순위:** 높음
**근거:** `docs/CODEMAPS/SUBMODULES.md` 확장 블로커 #2. README 및 AGENTS.md에서 "프라이빗 리모트와 클린 워킹트리 확보 전까지 `.gitmodules` 제외" 명시. 리모트가 없으면 재현 가능한 클론 워크플로우가 불가능하고 서브모듈 등록이 차단됨.

1. GitHub에 프라이빗 레포지터리 생성
2. `youtube` 로컬 체크아웃을 해당 리모트에 연결 및 초기 푸시
3. 워킹트리 클린 상태 확인 후 루트에서 원격 URL 기반 서브모듈 등록 진행

**완료 기준:**
- `git remote -v` 결과에 `origin` 항목 존재
- `git status --short` 깨끗함
- `docs/CODEMAPS/SUBMODULES.md`의 "Expansion Blockers"에서 `youtube` 항목 제거

---

### IDEA-002: n8n 워크플로우 백업·버전 관리 자동화

**우선순위:** 중간
**근거:** `docs/CODEMAPS/backend.md`에서 n8n이 로컬 Kubernetes PVC 기반으로 상태를 보관 중임을 확인. PVC 데이터는 `bun run automation:local -- standby` 시 보존되지만, Git 추적 대상이 아님. 워크플로우 변경 이력이 없으면 롤백 불가.

n8n 내보내기 API 또는 CLI를 활용해 워크플로우 JSON을 주기적으로 `youtube/` 레포지터리의 `workflows/` 디렉터리에 커밋하는 자동화 스크립트 작성.

**완료 기준:**
- 워크플로우 JSON 파일이 레포지터리에 버전 관리됨
- 내보내기 스크립트가 로컬에서 idempotent하게 실행됨
