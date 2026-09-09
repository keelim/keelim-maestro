# Workspace Idea Index

Last updated: 2026-09-09 KST

This folder tracks feature, product, and workflow ideas for the top-level
projects inside the `keelim-maestro` workspace.

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
| `all` | [all.md](./all.md) | 2026-09-09 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-09-09 KST | 6 | 공용 토큰·프리미티브 계약과 다운스트림 영향 가시화 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-09-09 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-09-09 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-09-09 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-09-09 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-09-09 KST | 6 | 운영 복구와 외부 연동 상태를 한곳에서 다루는 관리자 허브 |

## Archived projects (not active idea backlog targets)

| Project | File | Archived | Root basis |
| --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | 2026-06-04 | 루트 `AGENTS.md`/`README.md`: submodule·Bun/uv workspace·CodeGraph·codemap·"active idea backlog target" 모두 아님. `.gitmodules`에서도 제거됨. 재활성화 요청 전까지 항목은 참고용으로만 보존. |

## Known coverage gaps

- `youtube`: 루트 Bun/uv workspace의 활성 멤버이자 root README에 "autonomous YouTube Shorts production repo"로 기록돼 있지만, 이 워크스페이스 체크아웃에는 로컬 전용으로만 존재해 `docs/CODEMAPS/projects/`와 `docs/idea/`에 아직 근거 문서가 없다. 저장소가 실제로 hydrate된 세션에서 README/AGENTS 근거로 최초 `docs/idea/youtube.md`를 만들어야 한다(이번 라운드는 실제 코드 근거 없이 지어내지 않기 위해 신규 파일을 만들지 않음).
- `quant`: 원격이 없어 루트 정책상 백로그 대상에서 의도적으로 계속 제외됨(변경 없음, 재확인만).

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
