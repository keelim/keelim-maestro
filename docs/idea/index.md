# Workspace Idea Index

Last updated: 2026-07-14 KST

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
| `all` | [all.md](./all.md) | 2026-07-14 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-07-14 KST | 6 | 기존 계약 검증 스크립트(`report:shared-ui`, `verify-all-web-ui-integration.sh`, `typecheck:web`, `build:web`)를 CI 게이트로 승격하고 시각·접근성 커버리지를 채우는 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-07-14 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-07-14 KST | 6 | 워크스페이스 기준선과 실제로 채워진(비어있지 않은) 코드맵 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-07-14 KST | 6 | 스킬 카탈로그, 설치·회귀 검증, CodeGraph 디스패처 문서-구현 정합성을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-07-14 KST | 6 | 후속 행동 루프, 저장소 계약, 공용 UI 어댑터 CI 게이트를 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-07-14 KST | 6 | 운영 복구와 외부 연동 상태를 한곳에서 다루는 관리자 허브 |
| `toto` | [toto.md](./toto.md) | 2026-07-14 KST | 3 | gitlink pinning은 완료됨(2026-07-14 확인); 시즌 재현성과 데이터 공급자 계약 분리에 집중하는 KBO 대시보드 허브 |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
| `quant` | 원격 저장소가 없는 로컬 전용 quantitative research repo (`AGENTS.md`의 `/quant policy`, `docs/CODEMAPS/architecture.md`에서 명시적으로 제외 대상). 원격이 생기기 전까지는 서브모듈로 등록하거나 백로그 대상으로 승격하지 않는다 |
