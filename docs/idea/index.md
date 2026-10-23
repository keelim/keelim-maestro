# Workspace Idea Index

Last updated: 2026-10-23 KST

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
| `all` | [all.md](./all.md) | 2026-05-16 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-05-16 KST | 6 | 공용 토큰·프리미티브 계약과 다운스트림 영향 가시화 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-05-16 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-05-16 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-05-16 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-05-16 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-05-16 KST | 6 | 운영 복구와 외부 연동 상태를 한곳에서 다루는 관리자 허브 |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |

## Archived projects

| Project | File | Last reviewed | Open ideas | Note |
| --- | --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | 2026-10-23 KST | 4 | 2026-06-04 루트에서 아카이브됨; 활성 백로그 대상 아님(재활성화 요청 시에만 복귀) |

## Active projects without an idea file yet

| Project | Why pending |
| --- | --- |
| `youtube` | 루트 Bun/uv 워크스페이스 멤버이자 `easy-release-note` 패키지이지만, 이번 점검(2026-10-23) 환경에 자식 체크아웃이 없어 README/AGENTS 근거를 읽지 못해 아이디어를 만들지 않음 |
| `quant` | 원격이 없는 의도적 제외 대상; 백로그 승격 전까지 observed-only |
