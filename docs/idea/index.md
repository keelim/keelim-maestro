# Workspace Idea Index

Last updated: 2026-09-21 KST

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
- 루트 `AGENTS.md`가 archived로 지정한 프로젝트(현재 `toto`)는 사용자가 명시적으로
  재활성화를 요청하기 전까지 활성 Projects 표에서 제외하고 Archived projects 섹션에만
  남긴다.

## Projects

| Project | File | Last reviewed | Open ideas | Current focus |
| --- | --- | --- | --- | --- |
| `all` | [all.md](./all.md) | 2026-09-21 KST | 6 | 공통 모듈 채택·크로스 플랫폼(KMP/iOS/Rust) 빌드 게이트·릴리스 리스크를 함께 낮추는 허브 |
| `all-web-ui` | [all-web-ui.md](./all-web-ui.md) | 2026-09-21 KST | 6 | 공용 토큰·프리미티브 계약과 다운스트림 영향 가시화 허브 |
| `android-support` | [android-support.md](./android-support.md) | 2026-09-21 KST | 5 | Play Console 입력 검증과 릴리스 증적을 묶는 자동화 |
| `Keelim-Knowledge-Vault` | [Keelim-Knowledge-Vault.md](./Keelim-Knowledge-Vault.md) | 2026-09-21 KST | 6 | 워크스페이스 기준선과 문서 스냅샷을 다시 찾게 만드는 허브 |
| `keelim-plugin` | [keelim-plugin.md](./keelim-plugin.md) | 2026-09-21 KST | 6 | 스킬 카탈로그와 설치·회귀 검증을 함께 다루는 개인 플러그인 저장소 |
| `keelim-vercel` | [keelim-vercel.md](./keelim-vercel.md) | 2026-09-21 KST | 6 | 후속 행동 루프와 저장소 계약을 함께 다루는 금융 허브 |
| `rich` | [rich.md](./rich.md) | 2026-09-21 KST | 6 | 운영 복구·외부 연동 상태와 Open Trading API(전략 빌더/백테스터) 신뢰성을 함께 다루는 관리자 허브 |
| `youtube` | [youtube.md](./youtube.md) | 2026-09-21 KST | 2 | Bun/uv 이중 워크스페이스 멤버십의 하이드레이션·계약 정합성을 지키는 자동화 허브 |

## Archived projects

루트 `AGENTS.md`의 `/toto` archive policy(2026-06-04)에 따라 아래 프로젝트는
idea gardener 활성 표에서 제외한다. 사용자가 명시적으로 재활성화를 요청하지 않는 한
새 아이디어를 추가하지 않으며, 기존 파일은 이력 참고용으로만 보존한다.

| Project | File | Archived since | Note |
| --- | --- | --- | --- |
| `toto` | [toto.md](./toto.md) | 2026-06-04 (root archive policy) | gitlink 미커밋 상태로 archived됨; 재활성화 전까지 신규 아이디어 추가 금지 |

## Observed local-only utility repos

| Path | Why observed-only |
| --- | --- |
| `tools` | machine-local helper repo ignored by the root; useful as operator context, but not promoted into the project backlog unless it gains a workspace-facing product or policy surface |
