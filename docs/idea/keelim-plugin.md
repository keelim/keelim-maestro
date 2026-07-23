# keelim-plugin

Last reviewed: 2026-07-23 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- `docs/CODEMAPS/CODEGRAPH.md`는 루트 `scripts/codegraph.sh` 디스패처와 자식 repo별 `.codegraph/` 인덱스 워크플로를 문서화하지만, 디스패처 스크립트는 아직 저장소에 없고 모든 자식 repo의 `.codegraph/` 상태가 "unknown"으로 남아 있다. `keelim-plugin`은 이미 `codebase-codemap` 스킬로 codemap 생성을 담당하므로 이 격차를 메우기 가장 좋은 위치다.

## Open ideas

### 2026-04-12 - Generated skill catalog and install matrix

Status: proposed

Why now: As the skill set grows, a human-maintained README will become less
 useful than a generated catalog with tags, summaries, and installation targets.

First slice: Generate a catalog page from `skills/*/SKILL.md` metadata with
 quick filters for purpose, platform, and maintenance state.

### 2026-04-12 - Skill smoke-test harness (+ 프롬프트 회귀 코퍼스)

Status: proposed

Why now: Cross-tool skills are valuable only if install paths, metadata, and
 basic workflow assumptions stay valid for both Codex and Claude, and there is
 no single check that compares install/readme metadata across both toolchains.
문서 정합성만으로는 충분하지 않아, 설치 검증과 함께 대표 프롬프트의 실행 품질도
 같이 봐야 한다.

First slice: Add a lightweight verifier that checks required files, install
 commands, and any declared agent metadata for each skill folder, then surface
Codex/Claude install parity gaps before publishing. 이어서 핵심 스킬별 대표
 질의·기대 출력 코퍼스를 추가해 Codex/Claude 양쪽 샘플 응답 형태를 함께 비교한다.

### 2026-04-13 - 스킬 변경 영향 노트

Status: proposed

Why now: Codex와 Claude가 같은 skill 폴더를 공유하므로, 작은 문서나 프롬프트 수정도 어떤 스킬이 어떻게 바뀌었는지 한눈에 보이지 않으면 리뷰 비용이 커진다.

First slice: 변경된 `SKILL.md`와 에이전트 메타데이터를 묶어 변경 유형별 영향 요약을 만드는 changelog를 생성하고, 배포 전에 어떤 스킬을 다시 확인해야 하는지 표시한다.

### 2026-04-14 - 스킬 수명주기 태그

Status: proposed

Why now: 스킬 수가 늘수록 active/experimental/deprecated 상태를 설치 전부터 보이게 해야, 검증되지 않은 스킬이나 내려가야 할 스킬을 잘못 쓰는 일을 줄일 수 있다.

First slice: `skills/*/SKILL.md`와 README 카탈로그에 lifecycle 메타데이터를 붙이고, deprecated 또는 unverified 스킬을 설치 화면에서 따로 표시한다.

### 2026-04-14 - 스킬 재사용 그래프

Status: proposed

Why now: 스킬이 늘수록 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어져서, 공통 프리미티브와 재사용 가능한 조합을 한 장의 그래프로 보면 중복 정리와 신규 설치 판단이 빨라진다.

First slice: `skills/*/SKILL.md`를 스캔해 공통 키워드·연관 스킬·설치 경로를 묶은 그래프를 만들고, 함께 묶어야 할 스킬 묶음을 표시한다.

### 2026-07-23 - CodeGraph 디스패처 부트스트랩

Status: proposed

Why now: `docs/CODEMAPS/CODEGRAPH.md`는 `scripts/codegraph.sh` 루트 디스패처와 자식 repo별 `.codegraph/` 인덱스 초기화 절차를 문서화하지만, 실제로는 디스패처 스크립트가 저장소에 없고 모든 자식 repo의 `.codegraph/` 상태가 "unknown"으로 남아 있다. `keelim-plugin`은 이미 `codebase-codemap` 스킬로 `docs/CODEMAPS/*` codemap 생성을 담당하므로, CodeGraph 부트스트랩도 같은 스킬 계열에서 다루는 것이 가장 leverage가 크다.

First slice: `codebase-codemap` 스킬에 `scripts/codegraph.sh` 디스패처 생성 스텝과 자식 repo `codegraph init -i` 체크리스트를 추가하고, 각 자식 repo의 실제 초기화 상태를 문서 서술이 아니라 스크립트 출력으로 확인할 수 있게 만든다.
