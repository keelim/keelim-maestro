# Keelim-Knowledge-Vault

Last reviewed: 2026-04-30 KST

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

### 2026-04-13 - 코드맵 스냅샷 보관소

Status: proposed

Why now: 루트에 생성된 CODEMAPS/WORKSPACE 문서가 이미 워크스페이스의 실제 운영 기준이 되었으므로, 최신 스냅샷과 변경 이유를 vault에 함께 남겨야 오래된 노트가 다시 살아난다.

First slice: 각 코드맵 갱신 시점별로 파일 수, 핵심 결합점, 새로 생긴 운영 규칙을 요약한 노트를 하나씩 만들고 프로젝트 인덱스에서 바로 링크한다.

### 2026-04-14 - 워크스페이스 지시문 미러

Status: proposed

Why now: AGENTS, CODEMAPS, automation memory, 백로그 노트가 흩어져 있어서, 현재 작업 기준을 한 노트에서 다시 찾을 수 있어야 다음 작업의 진입 비용이 줄어든다.

First slice: 루트 AGENTS/CODEMAPS/idea 인덱스와 자주 바뀌는 운영 규칙을 연결한 단일 인덱스 노트를 만들고, 관련 프로젝트 노트에서 바로 왕복할 수 있게 한다.

### 2026-04-14 - 워크스페이스 일일 변화 다이제스트

Status: proposed

Why now: AGENTS, CODEMAPS, idea 인덱스, automation memory가 따로 움직여서, 오늘 바뀐 운영 기준을 한 번에 복원할 수 있는 요약 노트가 있으면 재진입 비용이 줄어든다.

First slice: 루트에서 갱신된 운영 문서와 메모리 조각을 모아 일일 다이제스트 노트를 만들고, 관련 프로젝트 노트로 바로 왕복 링크를 건다.

### 2026-04-16 - 워크스페이스 신뢰 기준선 보드

Status: proposed

Why now: 루트 AGENTS/CODEMAPS가 이미 신뢰 가능한 repo 집합, 제외 대상, pinning blocker를 정의하고 있어서, 이를 vault에 복원 가능한 한 장의 기준선 보드로 남기면 다음 작업에서 다시 해석하지 않아도 된다.

First slice: 현재 trusted set, excluded set, pinning blocker, 마지막 검증 시각을 묶은 노트를 만들고 루트 workspace 문서와 상호 링크한다.
