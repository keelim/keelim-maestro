# Keelim-Knowledge-Vault

Last reviewed: 2026-07-19 KST

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

### 2026-04-13 - 워크스페이스 기준선 미러 노트 (통합: 코드맵 스냅샷 보관소 · 지시문 미러 · 신뢰 기준선 보드)

Status: proposed (2026-07-19에 기존 3개 유사 항목을 하나로 통합)

Why now: `docs/CODEMAPS/*`, 루트 `AGENTS.md`, `.gitmodules`/`SUBMODULES.md`가 이미 워크스페이스의 실제 운영 기준(코드맵 스냅샷, trusted/excluded repo 집합, pinning blocker)을 담고 있는데, 이 정보를 vault에서 다시 찾으려면 매번 루트로 왕복해야 한다. 코드맵 보관·지시문 미러·신뢰 기준선 보드는 결국 "루트의 현재 진실을 vault에 정적으로 미러링한다"는 같은 문제였으므로 하나의 노트로 묶는다.

First slice: 루트 `AGENTS.md`/`docs/CODEMAPS/*`/`docs/idea/index.md`의 핵심 표(등록 submodule과 pinned commit, autonomous repo와 blocker, idea 프로젝트 목록)를 그대로 옮긴 단일 기준선 노트를 vault에 만들고, 코드맵이 갱신될 때마다(예: `chore: update codemaps` 커밋 시점) 이 노트도 함께 갱신하도록 프로젝트 인덱스에서 상호 링크한다.

### 2026-04-14 - 워크스페이스 일일 변화 다이제스트

Status: proposed

Why now: AGENTS, CODEMAPS, idea 인덱스, automation memory가 따로 움직여서, 오늘 바뀐 운영 기준을 한 번에 복원할 수 있는 요약 노트가 있으면 재진입 비용이 줄어든다. 위 기준선 미러 노트가 "현재 상태의 정적 스냅샷"이라면, 이 항목은 "무엇이 바뀌었는지"에 집중하는 시계열 다이제스트로 구분한다.

First slice: 루트에서 갱신된 운영 문서와 메모리 조각을 모아 일일 다이제스트 노트를 만들고, 관련 프로젝트 노트로 바로 왕복 링크를 건다.
