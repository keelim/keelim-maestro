# Keelim-Knowledge-Vault

Last reviewed: 2026-05-20 KST

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

### 2026-04-14 - 워크스페이스 운영 기준 미러 & 변화 다이제스트

Status: proposed

Why now: AGENTS, CODEMAPS, idea 인덱스, automation memory가 모두 따로 움직여서 오늘 바뀐 운영 기준을 한 번에 복원하기 어렵다. 루트 지시문과 코드맵을 연결한 단일 인덱스 노트와 최근 변화 요약을 vault에 함께 유지하면 재진입 비용이 크게 줄어든다.

First slice: 루트 AGENTS/CODEMAPS/idea 인덱스를 연결한 단일 인덱스 노트를 만들고 관련 프로젝트 노트로 왕복 링크를 건 뒤, 갱신된 운영 문서와 메모리 조각을 변화 다이제스트 형태로 함께 기록한다.

### 2026-05-20 - docs/knowledge 디렉터리 부재 격차 해소

Status: proposed

Why now: 루트 `README.md`가 `docs/knowledge/`를 operator-runbook, source-targets, review-checklist, merge-guidance, verification-contract의 저장소로 참조하지만, 2026-05-20 기준 해당 디렉터리가 존재하지 않는다. 이 참조가 깨진 상태로 유지되면 신규 오퍼레이터가 운영 지침을 찾지 못하는 위험이 생기고, vault의 워크스페이스 인덱스 노트도 연결할 대상이 없어진다.

First slice: vault에 workspace operator section을 만들어 README.md가 참조하는 5가지 문서(operator-runbook, source-targets, review-checklist, merge-guidance, verification-contract) 최소 스텁을 작성하고, 루트 README.md와 상호 링크하거나 `docs/knowledge/` 디렉터리를 root에 생성해 참조를 복원한다.

### 2026-04-16 - 워크스페이스 신뢰 기준선 보드

Status: proposed

Why now: 루트 AGENTS/CODEMAPS가 이미 신뢰 가능한 repo 집합, 제외 대상, pinning blocker를 정의하고 있어서, 이를 vault에 복원 가능한 한 장의 기준선 보드로 남기면 다음 작업에서 다시 해석하지 않아도 된다.

First slice: 현재 trusted set, excluded set, pinning blocker, 마지막 검증 시각을 묶은 노트를 만들고 루트 workspace 문서와 상호 링크한다.
