# Keelim-Knowledge-Vault

Last reviewed: 2026-07-18 KST

## Signals

- The vault is already organized by technical domains and acts as a workspace
  knowledge base.
- It has high strategic value when project work can pull actionable notes from
  it instead of treating it as passive storage.
- The root workspace also now carries codemaps, idea backlogs, and automation
  memory worth linking back into the vault.
- Generated code maps and workspace guidance should be preserved as linkable
  snapshots, not only as one-off references.
- Root docs already define a trusted set, excluded set, and pinning blockers,
  so the vault can mirror that baseline instead of re-deriving it every run.

## Open ideas

### 2026-04-12 - Project-to-note backlink hub

Status: proposed

Why now: The workspace spans several repos, so it is easy for useful notes to
 exist in the vault without being discoverable from the active project surface.

First slice: Create a project index note that maps each repo to its most useful
architecture notes, operating docs, recurring decision references, current
codemap highlights, and links back to the root idea index and automation
memory.

### 2026-04-12 - Weekly resurfacer for stale high-value notes

Status: proposed

Why now: A knowledge vault compounds when strong notes re-enter active work, not
 when they remain buried in old folders.

First slice: Add a weekly review note or script that surfaces recently untouched
high-value notes, open questions, and notes linked to active repos.

### 2026-04-13 - 코드맵·지시문·다이제스트 통합 미러 (병합: 코드맵 스냅샷 보관소 + 워크스페이스 지시문 미러 + 일일 변화 다이제스트)

Status: proposed

Why now: 루트에 생성된 CODEMAPS/WORKSPACE 문서와 AGENTS, idea 인덱스, automation memory가 각각 따로 움직이는데, 이를 세 개의 비슷한 vault 아이디어(스냅샷 보관·지시문 미러·일일 다이제스트)로 나눠 다루면 서로 겹치기만 하고 어느 것도 완성되지 않는다. 2026-07-18 기준 CODEGRAPH.md, SCRIPTS.md 같은 신규 코드맵 문서도 늘어나 미러 대상이 계속 넓어지고 있다.

First slice: 코드맵 갱신 시점마다 파일 수·핵심 결합점·새로 생긴 운영 규칙을 요약하고, 루트 AGENTS/CODEMAPS/idea 인덱스로의 링크와 그날의 변경 다이제스트를 함께 담은 단일 인덱스 노트를 만들어 프로젝트 인덱스에서 바로 왕복 연결한다.

### 2026-04-16 - 워크스페이스 신뢰 기준선 보드

Status: proposed

Why now: 루트 AGENTS/CODEMAPS가 이미 신뢰 가능한 repo 집합, 제외 대상, pinning blocker를 정의하고 있어서, 이를 vault에 복원 가능한 한 장의 기준선 보드로 남기면 다음 작업에서 다시 해석하지 않아도 된다.

First slice: 현재 trusted set, excluded set, pinning blocker, 마지막 검증 시각을 묶은 노트를 만들고 루트 workspace 문서와 상호 링크한다.
