# 아이디어 백로그 인덱스

<!-- 마지막 검토: 2026-06-17 -->
<!-- 활성 프로젝트: 8 | 제외: quant, toto -->
<!-- 아이디어 파일 수: 3 | 총 열린 아이디어: 3 -->

워크스페이스 루트(`keelim-maestro`)의 프로젝트별 아이디어·백로그 인덱스.
각 프로젝트 파일은 `docs/idea/<project>.md`에 있다.

## 프로젝트 현황

| 프로젝트 | 유형 | 열린 아이디어 | 마지막 검토 | 포커스 요약 |
| --- | --- | :---: | --- | --- |
| [`all`](all.md) | 서브모듈 · Android | — | — | 서브모듈 미초기화; 코드맵 갱신 필요 |
| [`all-web-ui`](all-web-ui.md) | 자율 · React/Tailwind | 1 | 2026-06-17 | `rich` 동결 후 서브모듈 전환 준비 |
| [`android-support`](android-support.md) | 서브모듈 · Android | — | — | v0.0.8-4 고정(디태치), 업데이트 모니터 필요 |
| [`Keelim-Knowledge-Vault`](Keelim-Knowledge-Vault.md) | 서브모듈 · Obsidian | — | — | GBrain 연동·볼트 건강성 자동화 |
| [`keelim-plugin`](keelim-plugin.md) | 서브모듈 · Python | — | — | 코드맵 생성기 핵심; 서브모듈 최신화 |
| [`keelim-vercel`](keelim-vercel.md) | 서브모듈 · Next.js | — | — | Vercel 배포; `@keelim/all-web-ui` 소비자 |
| [`rich`](rich.md) | 자율 · Python+React | 1 | 2026-06-17 | 워킹트리 동결·원격 동기화 긴급 |
| [`youtube`](youtube.md) | 자율 · TS+Python | 1 | 2026-06-17 | 프라이빗 원격 미설정; 재현 불가 위험 |

## 제외 프로젝트

| 프로젝트 | 사유 |
| --- | --- |
| `quant` | 원격 저장소 없음 — 의도적 제외. 원격 생성 시까지 백로그 대상 아님 |
| `toto` | 2026-06-04 아카이브 — 비활성; 백로그 대상 아님 |

## 다음 검토 우선순위

1. `rich` RICH-001 진행 확인 → `all-web-ui` UI-001 차단 해소 여부 판단
2. `youtube` YT-001 진행 확인 → 원격 설정 후 Bun/uv 워크스페이스 안정화
3. 서브모듈 미초기화 4개(`all`, `android-support`, `Keelim-Knowledge-Vault`, `keelim-plugin`) 코드맵 갱신 후 아이디어 파일 추가
