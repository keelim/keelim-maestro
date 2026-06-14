# 아이디어 백로그 인덱스

<!-- 최종 검토: 2026-06-14 -->
<!-- 다음 검토 예정: 2026-07-14 -->

이 파일은 keelim-maestro 워크스페이스의 아이디어 백로그 인덱스입니다.
각 프로젝트의 상세 아이디어는 `docs/idea/<project>.md`에 있습니다.

## 프로젝트 목록

| 프로젝트 | 유형 | 상태 | 열린 아이디어 | 최종 검토 | 포커스 요약 |
| --- | --- | --- | --- | --- | --- |
| [`all`](all.md) | 서브모듈 | 활성 | 2 | 2026-06-14 | codemap 갱신, MCP 연동 탐색 |
| [`android-support`](android-support.md) | 서브모듈 | 활성 (detached) | 2 | 2026-06-14 | 버전 평가, upstream 추적 복원 |
| [`Keelim-Knowledge-Vault`](Keelim-Knowledge-Vault.md) | 서브모듈 | 활성 | 3 | 2026-06-14 | GBrain 통합 검증, source-targets 큐레이션 |
| [`keelim-plugin`](keelim-plugin.md) | 서브모듈 | 활성 | 2 | 2026-06-14 | codemap 자동 갱신 CI 통합, 스킬 확장 |
| [`keelim-vercel`](keelim-vercel.md) | 서브모듈 | 활성 | 3 | 2026-06-14 | 인증 자동화, 공유 UI 연동 |
| [`all-web-ui`](all-web-ui.md) | 자율 | 활성 (서브모듈 변환 대기) | 3 | 2026-06-14 | 서브모듈 변환, 버전 로드맵 |
| [`rich`](rich.md) | 자율 | 활성 (dirty, 변환 차단) | 3 | 2026-06-14 | dirty 해소가 최우선, 트레이딩 API 안정화 |
| [`youtube`](youtube.md) | 자율 | 활성 (private, remote 없음) | 3 | 2026-06-14 | remote 설정, n8n 문서화, 서브모듈 경로 |

> **참고:** `quant`는 원격 저장소 없음으로 의도적 제외. `toto`는 2026-06-04 아카이브 처리.

## 워크스페이스 긴급 차단 이슈

1. **`rich` dirty 상태** — `all-web-ui` 서브모듈 변환 및 전체 워크스페이스 안정화를 차단 중.
2. **`youtube` remote 미설정** — `.gitmodules` 등록 불가; private remote 필요.
3. **codemap 파일 카운트 전체 미확인** — 서브모듈 미초기화로 모든 프로젝트가 `—` 상태.

## 업데이트 이력

| 날짜 | 변경 내용 |
| --- | --- |
| 2026-06-14 | 최초 생성 — `docs/idea/` 구조 부트스트랩 |
