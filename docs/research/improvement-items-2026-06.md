# Keelim Maestro Improvement Backlog — 2026-06

8개 하위 프로젝트에서 **각 100건씩, 총 800건**의 개선 항목을 수집한 통합 백로그 요약.

- 전체 리포트: [improvement-items-2026-06.html](./improvement-items-2026-06.html) (오프라인 단일 HTML, 프로젝트별 100행 테이블 + P1 하이라이트)
- 전체 데이터: [improvements-2026-06/improvements.json](./improvements-2026-06/improvements.json)
- 차원별 원본: [improvements-2026-06/raw/](./improvements-2026-06/raw/) (48개 체크포인트)

## 요약

| 항목 | 값 |
|---|---|
| 총 항목 | 800 (프로젝트당 정확히 100) |
| P1 (즉시 조치) | 193 |
| P2 (중요) | 607 |
| 수집 후보 | 1,119건 → 중복 제거·우선순위 컷으로 800건 선별 (P3는 전량 컷) |
| 검증 | 필수 필드·file_path 실존·ID 유일성·오프라인 HTML 계약 모두 통과 |

## 프로젝트별 하이라이트

### all — Kotlin 멀티 Android 앱 모노레포 (P1 21)
상위 차원: architecture 24, security 18, testing 16
- **ALL-001** core:common-android가 data/network/domain 상위 계층에 의존
- **ALL-002** core:data가 core:network를 api로 전이 노출
- **ALL-003** feature:ui-setting umbrella가 core:data 구현체에 직접 의존

### android-support — Play Store 배포 GitHub Action (P1 28)
상위 차원: ci-release 19, error-handling 18, testing 18
- **ASUP-001** PR CI에서 ncc build를 실행하지 않는다
- **ASUP-002** main push 검증 워크플로우가 없다
- **ASUP-003** release 태그가 버전 PR보다 먼저 만들어진다

### Keelim-Knowledge-Vault — Obsidian 지식 저장소 (P1 17)
상위 차원: naming 21, content-quality 19, structure 19
- **KKV-001** 링크 검사가 단일 허브 노트에 고정됨
- **KKV-002** 운영 스키마의 lint workflow가 자동화 명령으로 구현되지 않음
- **KKV-003** Android 2026 업데이트 노트가 재확인 상태를 닫지 않음

### keelim-plugin — Claude Code 스킬 플러그인 (P1 28)
상위 차원: script-quality 21, testing-evals 19, security 17
- **KPLG-001** README 수동 설치 경로가 현재 체크아웃과 다름
- **KPLG-002** CI workflow가 없어 로컬 검증이 자동화되지 않음
- **KPLG-003** evals와 SkillOpt 운영 스크립트가 ignore되어 소스 관리에서 빠짐

### keelim-vercel — Next.js 16 관리 대시보드 (P1 36 — 최다)
상위 차원: api-correctness 20, security 17, testing 15
- **KVCL-001** ranking action이 raw interaction rows를 두 번 읽고 JS에서 집계함
- **KVCL-002** CSV import가 파일 크기와 행 수를 제한하지 않음
- **KVCL-003** OG parser가 외부 요청 대상의 scheme·host를 제한하지 않음 (SSRF)

### rich — FastAPI + Next.js 주식 정량분석 (P1 18)
상위 차원: api-security 21, reliability 19, testing 18
- **RICH-001** Admin API 라우터에 인증 dependency가 없음
- **RICH-002** KIS quote 호출이 요청자 권한과 분리됨
- **RICH-003** Open Trading 라우트를 인증 래퍼 없이 같은 앱에 등록

### youtube — Python CLI + Remotion 영상 자동화 (P1 19)
상위 차원: testing 21, ci-automation 18, reliability 18
- **YTB-001** CI 진입점이 패키지 메타데이터에 정의되어 있지 않음
- **YTB-002** Playwright 의존성이 pyproject에 선언되어 있지 않음
- **YTB-003** 명시 후보 경로가 repo 내부로 제한되지 않음

### all-web-ui — React 19 공유 UI 라이브러리 (P1 26)
상위 차원: testing 19, api-design 17, docs 17
- **AWUI-001** Progress가 Radix Root에 value를 전달하지 않음
- **AWUI-002** async sink 실패를 await/catch하지 않음
- **AWUI-003** telemetry payload의 알 수 없는 필드를 통과시킴

## 방법론

1. **수집**: (project × dimension) 48쌍, 쌍당 전담 분석 에이전트가 Codex(`codex:codex-rescue` 위임)로 소스를 직접 읽고 20~24건씩 과수집 → raw JSON 체크포인트 저장
2. **집계** (`scripts/improvements/aggregate_improvements.py`): 필수 필드·file_path 실존 검증 → 2단계 중복 제거(정확 키 + 제목 토큰 Jaccard ≥ 0.6) → 프로젝트별 우선순위 컷(severity → effort → 차원 라운드로빈)으로 정확히 100건
3. **렌더링** (`keelim-plugin/skills/html-report-generator`): 블록모델 JSON → 오프라인 단일 HTML (`--validate` 통과: CDN/외부 통신/원격 URL 0건)
4. **검증** (`scripts/improvements/check_counts.py`): 프로젝트별 ==100, 총 ==800, ID 유일, file_path 실존, 테이블 행수 일치

### Severity 기준
- **P1**: 버그·보안·데이터 정합성 등 즉시 조치 필요
- **P2**: 품질·유지보수성에 중요한 영향
- **P3**: 점진적 개선 (이번 컷에서는 P1/P2 후보가 충분해 전량 제외)
