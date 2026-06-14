# `all` 아이디어 백로그

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

**유형:** 등록 서브모듈 | **상태:** clean vs origin/develop (pinned `0643bab4`) | **우선순위:** 낮음

---

## 열린 아이디어

### ALL-001 · 서브모듈 초기화 후 codemap 파일 카운트 갱신
**우선순위:** 낮음 | **근거:** `all.md` — "—" 파일 카운트; 초기화 필요

서브모듈을 초기화(`git submodule update --init all`)한 후 `scripts/refresh-codemaps.py`를 실행하여 Android 멀티모듈 앱 구조(모듈 목록, Gradle 파일 수, 주요 소스 경로)를 codemap에 반영한다.

---

### ALL-002 · agentgateway MCP 연동 시나리오 탐색
**우선순위:** 낮음 | **근거:** `architecture.md` — agentgateway MCP가 워크스페이스 공유 엔드포인트

`all` Android 앱의 개발 워크플로우(예: 빌드 트리거, 테스트 실행)에서 `agentgateway` MCP 도구를 활용하는 시나리오를 탐색한다. 현재 MCP 연동은 Python/TS 프로젝트 중심이며 Android 쪽은 미검토.

---

## 닫힌 아이디어

_없음_
