# keelim-plugin

Last reviewed: 2026-08-10 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- `keelim-plugin`은 `skills/codebase-codemap/scripts/generate_codemap.py`를 직접 호스팅해 루트 `docs/CODEMAPS/`를 생성하므로, 루트 CodeGraph 디스패처 계약(`docs/CODEMAPS/CODEGRAPH.md`)의 정합성도 이 저장소가 가장 잘 검증할 수 있는 위치에 있다.

## Open ideas

### 2026-04-12 - Generated skill catalog and install matrix

Status: proposed

Why now: As the skill set grows, a human-maintained README will become less
 useful than a generated catalog with tags, summaries, and installation targets.
 스킬이 늘수록 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어지므로, 카탈로그가 공통
 키워드·연관 스킬 관계까지 함께 보여줘야 중복 정리와 신규 설치 판단이 빨라진다.

First slice: Generate a catalog page from `skills/*/SKILL.md` metadata with
 quick filters for purpose, platform, and maintenance state, plus a common-keyword/
 related-skill grouping so skill bundles that should be installed or deduplicated
 together are visible in the same view.

### 2026-04-12 - Skill smoke-test harness

Status: proposed

Why now: Cross-tool skills are valuable only if install paths, metadata, and
 basic workflow assumptions stay valid for both Codex and Claude, and there is
 no single check that compares install/readme metadata across both toolchains.

First slice: Add a lightweight verifier that checks required files, install
 commands, and any declared agent metadata for each skill folder, then surface
Codex/Claude install parity gaps before publishing.

### 2026-04-13 - 스킬 변경 영향 노트

Status: proposed

Why now: Codex와 Claude가 같은 skill 폴더를 공유하므로, 작은 문서나 프롬프트 수정도 어떤 스킬이 어떻게 바뀌었는지 한눈에 보이지 않으면 리뷰 비용이 커진다.

First slice: 변경된 `SKILL.md`와 에이전트 메타데이터를 묶어 변경 유형별 영향 요약을 만드는 changelog를 생성하고, 배포 전에 어떤 스킬을 다시 확인해야 하는지 표시한다.

### 2026-04-14 - 스킬 프롬프트 회귀 코퍼스

Status: proposed

Why now: 설치 경로와 메타데이터가 맞아도 실제 실행 예시나 프롬프트 품질이 깨지면 스킬은 곧바로 재사용성을 잃기 때문에, 문서 정합성만으로는 충분하지 않다.

First slice: 핵심 스킬별 대표 질의와 기대 출력 요약을 모은 코퍼스를 만들고, Codex/Claude 양쪽에서 샘플 응답 형태를 비교하는 스모크 테스트를 붙인다.

### 2026-04-14 - 스킬 수명주기 태그

Status: proposed

Why now: 스킬 수가 늘수록 active/experimental/deprecated 상태를 설치 전부터 보이게 해야, 검증되지 않은 스킬이나 내려가야 할 스킬을 잘못 쓰는 일을 줄일 수 있다.

First slice: `skills/*/SKILL.md`와 README 카탈로그에 lifecycle 메타데이터를 붙이고, deprecated 또는 unverified 스킬을 설치 화면에서 따로 표시한다.

### 2026-08-10 - CodeGraph 디스패처 초기화 갭 점검

Status: proposed

Why now: 루트 `docs/CODEMAPS/CODEGRAPH.md`는 `scripts/codegraph.sh`를 child repo용 CodeGraph 디스패처 계약으로 정의하지만, 실제로는 이 스크립트가 아직 존재하지 않고(`SCRIPTS.md`에도 없음) `all`/`keelim-plugin`/`keelim-vercel`/`rich` 등 모든 child repo의 `.codegraph/` 초기화 여부도 "unknown"으로 남아 있다. `keelim-plugin`이 codemap 생성 스크립트(`generate_codemap.py`)를 직접 소유하므로, 디스패처 계약과 실제 child 초기화 상태 사이의 격차를 점검할 책임이 가장 잘 맞는 위치다.

First slice: `scripts/codegraph.sh` 존재 여부와 각 child repo `.codegraph/` 초기화 상태를 스캔해 `CODEGRAPH.md`의 계약(설정 체크리스트, 디스패치 커맨드)과 실제 상태의 차이를 보여주는 짧은 점검 리포트를 만들고, 누락된 디스패처 라우팅 항목을 표시한다.
