# Workspace Idea Index

Last updated: 2026-09-20 KST

This folder tracks feature, product, and workflow ideas for the top-level
projects inside the `keelim-maestro` workspace root.

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
- Do not add an archived or explicitly excluded project (see below) back into
  this table without an explicit request to reactivate it.

## Projects

| Project | File | Last reviewed | Open ideas | Current focus |
| --- | --- | --- | --- | --- |
| `all` | [all.md](./all.md) | 2026-09-20 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-09-20 KST | 6 | 공용 토큰·프리미티브 계약과 다운스트림 영향 가시화 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-09-20 KST | 6 | Play Console 입력 검증·릴리스 증적과 루트 코드맵 등록 격차 해소를 함께 다루는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-09-20 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-09-20 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-09-20 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-09-20 KST | 6 | 운영 복구와 외부 연동 상태를 한곳에서 다루는 관리자 허브 |
| `youtube` | [youtube.md](./youtube.md) | 2026-09-20 KST | 1 | 루트 Bun/uv 워크스페이스 멤버십 대비 루트 검증(typecheck/build/test) 커버리지 격차 추적 (초기 항목; 로컬 미하이드레이트 상태에서 루트 문서만으로 작성됨) |

## Archived / excluded projects

이 표의 프로젝트는 루트 `AGENTS.md` 정책에 따라 이 백로그의 활성 관리 대상에서
제외된다. 명시적인 재활성화 요청이 없는 한 다시 위 표에 추가하지 않는다.

| Project | File | Status | Reason |
| --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | Archived (2026-06-04) | 루트 `AGENTS.md` `/toto` archive policy — 더 이상 root submodule/workspace/CodeGraph/idea gardener 대상이 아님. 기존 항목은 이력 참고용으로만 보존 |
| `quant` | — (파일 없음) | Excluded | 루트 `AGENTS.md` `/quant` policy — 원격 저장소가 없어 초기 root superproject/submodule 및 idea 백로그 범위에서 의도적으로 제외 |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
