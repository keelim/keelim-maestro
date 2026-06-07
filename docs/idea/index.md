# Workspace Idea Index

Last updated: 2026-06-06 KST

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
| `all` | [all.md](./all.md) | 2026-06-06 KST | 12 | 빌드/릴리스 허브 + (신규) 6개 앱 사용자 기능 백로그 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-06-06 KST | 9 | 공용 토큰·프리미티브 계약 + (신규) 텔레메트리 스키마·온보딩·성능 예산 |
| `android-support` | [android-support.md](./android-support.md) | 2026-05-16 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-05-16 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-05-16 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-06-06 KST | 9 | 후속 행동 루프·저장소 계약 + (신규) 금융 어시스턴트·온보딩·성능 예산 |
| `rich` | [rich.md](./rich.md) | 2026-06-06 KST | 8 | 운영 복구·외부 연동 + (신규) 투자 위키 Q&A(P1 블록)·성능 예산 |

## Cross-project inbox

| 문서 | 날짜 | 내용 |
| --- | --- | --- |
| [future.md](./future.md) | 2026-04-16 | 초기 cross-project 종합 inbox |
| [net-new-2026-06-06.md](./net-new-2026-06-06.md) | 2026-06-06 | 기존 백로그가 다루지 않은 빈 영역(제품·보안·성능·LLM·텔레메트리·온보딩) net-new 시드 7개 (N1~N7). N2/N3/N4 root 시드는 이 문서가 source. |

## Archived projects

| Project | File | Archived | Root treatment |
| --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | 2026-06-04 KST | historical notes only; no new root idea gardening unless explicitly reactivated |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
