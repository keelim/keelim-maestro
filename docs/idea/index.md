# Workspace Idea Index

Last updated: 2026-07-11 KST

This folder tracks feature, product, and workflow ideas for the top-level
projects inside `/Users/keelim/Desktop/keelim-maestro`.

## Update rules

- Treat the immediate child directories with a `.git` file or directory as
  project candidates, then keep the maintained set aligned to root codemaps,
  README/AGENTS context, and workspace policy.
- Keep machine-local utility repos that should not become root project files in
  an observed-only note unless they are promoted into the maintained set.
- Update only files inside `docs/idea/` from the root workspace.
- Keep each `docs/idea/<project>.md` file as the source of truth for that project.
- Append new ideas when they are genuinely new; tighten or extend existing
  entries instead of creating near-duplicates.
- Keep this index in sync with per-project counts and review dates.

## Projects

| Project | File | Last reviewed | Open ideas | Current focus |
| --- | --- | --- | --- | --- |
| `all` | [all.md](./all.md) | 2026-07-11 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-07-11 KST | 6 | 공용 토큰·프리미티브 계약, 다운스트림 영향, 서브모듈 승격 준비 신호를 함께 보는 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-07-11 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-07-11 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-07-11 KST | 6 | 스킬 카탈로그·설치 회귀 검증에 더해 루트 코드맵 생성기 의존성 신뢰성을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-07-11 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-07-11 KST | 6 | 운영 복구와 외부 연동 상태에 더해 서브모듈 승격 병목(dirty/ahead 정리)을 함께 다루는 관리자 허브 |
| `toto` | [toto.md](./toto.md) | 2026-07-11 KST | 4 | pin 유지 검증부터 시즌 재현성까지 다루는 KBO 대시보드 허브 |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
