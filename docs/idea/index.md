# 아이디어 백로그 인덱스

<!-- 마지막 검토: 2026-06-15 -->
<!-- 검토자: idea-gardener (자동 실행) -->

## 현황 요약

| 프로젝트 | 유형 | 열린 아이디어 | 마지막 검토 | 포커스 요약 |
| --- | --- | --- | --- | --- |
| [all](all.md) | submodule (Android) | 3 | 2026-06-15 | android-support 핀 동기화, CI 빌드 검증 |
| [android-support](android-support.md) | submodule (Android) | 2 | 2026-06-15 | v0.0.8-4 고정 상태 갱신, 릴리즈 프로세스 문서화 |
| [Keelim-Knowledge-Vault](keelim-knowledge-vault.md) | submodule (Obsidian) | 2 | 2026-06-15 | GBrain 동기화 자동화, 프론트매터 검증 통합 |
| [keelim-plugin](keelim-plugin.md) | submodule (Python) | 3 | 2026-06-15 | 코드맵 자동 갱신, 스킬 카탈로그 공개 |
| [keelim-vercel](keelim-vercel.md) | submodule (Next.js) | 2 | 2026-06-15 | GitHub Packages 인증 안정화, 배포 상태 모니터링 |
| [all-web-ui](all-web-ui.md) | autonomous (React) | 3 | 2026-06-15 | 서브모듈 전환 준비, publish 파이프라인 자동화 |
| [rich](rich.md) | autonomous (Python/FastAPI) | 4 | 2026-06-15 | 더티 워킹 트리 freeze, submodule 등록 블로커 해소 |
| [youtube](youtube.md) | autonomous (TS/Python) | 3 | 2026-06-15 | private remote 설정, n8n 백업 자동화 |
| [keelim-maestro](keelim-maestro.md) | root coordination | 3 | 2026-06-15 | hydration 스크립트 개선, 통합 상태 대시보드 |

**전체 열린 아이디어:** 25개 (2026-06-15 기준)

## 운영 위험 (긴급 우선순위)

1. **`rich` 더티 워킹 트리** — `all-web-ui` 서브모듈 전환 및 `rich` pinning 블로커. 해소 전까지 workspace 확장 불가. → [rich.md](rich.md)
2. **`youtube` private remote 부재** — 재현 가능한 클론 워크플로 없음. 원격 장애 시 복구 불가. → [youtube.md](youtube.md)
3. **autonomous repo hydration 미자동화** — fresh clone 후 `all-web-ui`, `rich`, `youtube` 수동 hydration 필요. 온보딩 마찰 큼. → [keelim-maestro.md](keelim-maestro.md)

## 크로스 프로젝트 레버리지

- `keelim-plugin` 코드맵 자동 갱신이 완성되면 → 모든 프로젝트 코드맵 품질 향상
- `rich` freeze/split 완료 → `all-web-ui` 서브모듈 전환 가능 → workspace topology 안정화
- GBrain ↔ Knowledge Vault 자동 동기화 → keelim-plugin 스킬과 연동해 에이전트 컨텍스트 개선

## 메타

- 아이디어 파일 위치: `docs/idea/<project>.md`
- 코드맵 소스: `docs/CODEMAPS/`
- 대상에서 제외: `toto` (2026-06-04 아카이브), `quant` (원격 없음, 의도적 제외)
