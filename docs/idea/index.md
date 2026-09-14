# Workspace Idea Index

Last updated: 2026-09-14 KST

This folder tracks feature, product, and workflow ideas for the top-level
projects inside the `keelim-maestro` coordination root.

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
- Do not add an archived project (see `AGENTS.md` archive policy) back into the
  active `Projects` table; keep its file only as a frozen historical record.

## Projects

| Project | File | Last reviewed | Open ideas | Current focus |
| --- | --- | --- | --- | --- |
| `all` | [all.md](./all.md) | 2026-09-14 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-09-14 KST | 6 | 공용 토큰·프리미티브 계약과 다운스트림 영향 가시화 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-09-14 KST | 6 | Play Console 입력 검증·릴리스 증적 자동화와, README·CODEMAPS·`.gitmodules` 사이의 등록 상태 불일치 해소 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-09-14 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-09-14 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-09-14 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-09-14 KST | 6 | 운영 복구와 외부 연동 상태를 한곳에서 다루는 관리자 허브 |
| `youtube` | [youtube.md](./youtube.md) | 2026-09-14 KST | 2 | 루트 Bun/uv 이중 워크스페이스 멤버로서의 하이드레이션 전제조건과 TS/Python 정합성을 다루는 신규 허브 |

## Archived projects

| Project | File | Status | Note |
| --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | archived 2026-06-04 | `AGENTS.md`와 `README.md`("Archived child checkouts") 모두 `toto`를 gitlink·Bun/uv 워크스페이스·CodeGraph·codemap 갱신·활성 idea 백로그 대상에서 제외한다고 명시한다. 이번 정리에서 활성 `Projects` 표에서 제거했고, 파일 자체는 재활성화 요청 전까지 수정하지 않는 동결된 이력 기록으로만 남긴다. |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
