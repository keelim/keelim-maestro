# Workspace Idea Index

Last updated: 2026-09-11 KST

This folder tracks feature, product, and workflow ideas for the top-level
projects inside the `keelim-maestro` root workspace.

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
| `all` | [all.md](./all.md) | 2026-09-11 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-09-11 KST | 6 | 공용 토큰·프리미티브 계약과 다운스트림 영향 가시화 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-09-11 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-09-11 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-09-11 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-09-11 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-09-11 KST | 6 | 운영 복구와 외부 연동 상태를 한곳에서 다루는 관리자 허브 |

## Archived projects

| Project | File | Archived | Why |
| --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | 2026-06-04 | 루트 `AGENTS.md`의 `/toto` archive policy에 따라 root 코디네이션 레이어의 활성 대상에서 제외됨. 재활성화를 명시적으로 요청받기 전까지 idea gardener의 활성 프로젝트 표·신규 아이디어 생성 대상에서 제외한다. 과거 아이디어는 참고용으로 [toto.md](./toto.md)에 보존. |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |

## Coverage gap (not actioned this run)

- `youtube`는 루트 Bun/uv 워크스페이스의 활성 멤버(`docs/CODEMAPS/architecture.md`, `WORKSPACE.md`, `backend.md`)이지만 `docs/idea/`에 대응 파일이 없다. 이번 실행에서는 실제 `youtube/README.md`·`AGENTS.md` 근거 없이 새 프로젝트 파일을 만들지 않았다(근거 없는 항목 생성 금지 규칙). 다음 idea gardener 실행에서 `youtube` 저장소를 hydrate한 뒤 근거 기반으로 신규 파일 추가를 검토할 것.
