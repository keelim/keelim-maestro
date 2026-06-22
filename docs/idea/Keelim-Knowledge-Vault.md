# Keelim-Knowledge-Vault

Last reviewed: 2026-06-22 KST

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

### 2026-04-14 - 워크스페이스 운영 문서 미러와 변화 다이제스트

Status: proposed

Why now: AGENTS, CODEMAPS, idea 인덱스, automation memory가 모두 루트에서 따로 움직이는데, 활성 프로젝트에서 현재 기준을 한 곳에서 다시 찾게 해주는 Vault 내 연결 허브가 없으면 재진입 비용이 계속 누적된다.

First slice: 루트 AGENTS/CODEMAPS/idea 인덱스와 자주 바뀌는 운영 규칙을 연결한 단일 인덱스 노트를 만들고, 갱신된 운영 문서와 메모리 조각을 일일 다이제스트 형태로 모아 관련 프로젝트 노트로 왕복 링크를 달아 오래된 노트를 자동으로 위로 올린다.

### 2026-04-16 - 워크스페이스 신뢰 기준선 보드

Status: proposed

Why now: 루트 AGENTS/CODEMAPS가 이미 신뢰 가능한 repo 집합, 제외 대상, pinning blocker를 정의하고 있어서, 이를 vault에 복원 가능한 한 장의 기준선 보드로 남기면 다음 작업에서 다시 해석하지 않아도 된다.

First slice: 현재 trusted set, excluded set, pinning blocker, 마지막 검증 시각을 묶은 노트를 만들고 루트 workspace 문서와 상호 링크한다.

### 2026-06-22 - GBrain 소스-타깃 계약 정합성 검증

Status: proposed

Why now: `docs/knowledge/source-targets.md`와 `docs/knowledge/verification-contract.md`가 Vault에서 GBrain(`~/brain`)으로 임포트할 노트의 신뢰 집합과 제외 대상을 명시하지만, Vault 내용이 바뀔 때 소스-타깃 목록이 함께 갱신되는지 확인하는 연결 고리가 없다.

First slice: `Keelim-Knowledge-Vault`의 카테고리별 노트 목록과 `docs/knowledge/source-targets.md`의 curated import pool을 비교해, 새로 추가된 노트 중 GBrain 승격 후보와 폐기된 노트 중 제외 대상을 표시하는 검증 스크립트(`scripts/improvements/verify_knowledge_vault_*.py` 패턴 참조)를 만든다.
