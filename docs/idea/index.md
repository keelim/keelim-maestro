# 아이디어 백로그 인덱스 — keelim-maestro

<!-- 마지막 검토: 2026-06-16 | 초기 생성 -->

마지막 검토: 2026-06-16  
활성 프로젝트: 8  
전체 오픈 아이디어: 21

## 프로젝트 목록

| 프로젝트 | 주요 스택 | 오픈 | 마지막 검토 | 주요 포커스 |
|---|---|---|---|---|
| [keelim-maestro](keelim-maestro.md) | 워크스페이스 조율 | 3 | 2026-06-16 | 서브모듈 블로커 해소, 온보딩 자동화 |
| [all](all.md) | Android / Kotlin | 2 | 2026-06-16 | 서브모듈 핀 갱신, CodeGraph 초기화 |
| [android-support](android-support.md) | Android / Kotlin | 2 | 2026-06-16 | 업스트림 추적 재개, 의존성 검증 |
| [Keelim-Knowledge-Vault](Keelim-Knowledge-Vault.md) | Obsidian / Markdown | 2 | 2026-06-16 | GBrain 연동 견고화, 프론트매터 CI |
| [keelim-plugin](keelim-plugin.md) | Python (Claude/Codex 스킬) | 2 | 2026-06-16 | 코드맵 자동 갱신, 스킬 인벤토리 문서화 |
| [keelim-vercel](keelim-vercel.md) | Next.js 16 / TypeScript | 2 | 2026-06-16 | all-web-ui 연동 안정성, bun.lock 드리프트 |
| [all-web-ui](all-web-ui.md) | React 19 / Tailwind 4 | 3 | 2026-06-16 | 서브모듈 전환 준비, 버전 범프 프로세스 |
| [rich](rich.md) | Python + FastAPI + React | 3 | 2026-06-16 | **[P1] 워킹트리 더티 동결 필요** |
| [youtube](youtube.md) | TypeScript + Python / Remotion | 2 | 2026-06-16 | **[P1] 리모트 없음 — 재해 복구 위험** |

## 제외 항목

| 프로젝트 | 상태 |
|---|---|
| `quant` | 리모트 없음; 의도적으로 제외 (`.gitmodules` 미등록) |
| `toto` | 2026-06-04 아카이브 완료; 루트 조율 및 백로그에서 제거 |

## 서브모듈 확장 블로커 요약

서브모듈 추가/전환 전에 해소해야 할 선결 조건 (SUBMODULES.md 기준):

1. **rich** — 워킹트리 더티 상태 동결/분할 (`rich.md` P1 참조)
2. **youtube** — 프라이빗 리모트 확보 및 클린 워킹트리 필요 (`youtube.md` P1 참조)
3. **all-web-ui** — 위 두 항목 해소 후 서브모듈 전환 가능 (`all-web-ui.md` P2 참조)
