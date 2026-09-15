# Workspace Idea Index

Last updated: 2026-09-15 KST

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
| `all` | [all.md](./all.md) | 2026-09-15 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-09-15 KST | 6 | 공용 토큰·프리미티브 계약과 다운스트림 영향 가시화 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-09-15 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-09-15 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-09-15 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-09-15 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-09-15 KST | 6 | 운영 복구와 외부 연동 상태를 한곳에서 다루는 관리자 허브 |
| `youtube` | [youtube.md](./youtube.md) | 2026-09-15 KST | 2 | 워크스페이스 하이드레이션 공백과 코드맵/백로그 부재를 먼저 메우는 정합성 허브 |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
| `quant` | `AGENTS.md`의 `/quant policy`에 따라 remote가 없고 root superproject/submodule 범위에서 의도적으로 제외된 저장소라서, 근거로 삼을 codemap/README 문서가 없다. 명시적 요청 없이는 백로그에 편입하지 않는다 |

## Archived projects

| Project | File | Archived | Why |
| --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | 2026-06-04 (per `AGENTS.md` `/toto` archive policy) | 루트 코디네이션 레이어에서 더 이상 능동적으로 다루지 않는 저장소. 기존 4건의 열린 아이디어는 파일에 보존하되, 사용자가 명시적으로 재활성화를 요청하기 전까지 위 활성 프로젝트 표·신규 아이디어 편성 대상에서 제외한다 |
