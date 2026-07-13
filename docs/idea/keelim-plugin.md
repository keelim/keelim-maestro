# keelim-plugin

Last reviewed: 2026-07-13 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- 루트 코드맵 재생성 스크립트(`scripts/refresh-codemaps.py`)가 이 저장소의
  `skills/codebase-codemap/scripts/generate_codemap.py`를 직접 호출한다 —
  `docs/CODEMAPS/` 전체가 이 스킬 하나에 의존한다. 확인된 스킬 폴더는
  `codebase-codemap`, `jira-ticket-desk`, `session-learning`,
  `session-usage-dashboard` 4종이다.

## Open ideas

### 2026-04-12 - Generated skill catalog and install matrix

Status: proposed

Why now: As the skill set grows, a human-maintained README will become less
 useful than a generated catalog with tags, summaries, and installation targets.

First slice: Generate a catalog page from `skills/*/SKILL.md` metadata with
 quick filters for purpose, platform, and maintenance state.

### 2026-04-12 - Skill verification harness (install parity + prompt regression)

Status: proposed

Why now: Cross-tool skills are valuable only if install paths, metadata, and
 basic workflow assumptions stay valid for both Codex and Claude, and even
 when install metadata is correct, actual prompt/output quality can regress
 silently. Neither concern currently has a single check. (2026-07-13: merged
 with the former "스킬 프롬프트 회귀 코퍼스" entry — both are the same
 verification-harness problem at different layers.)

First slice: Add a lightweight verifier that checks required files, install
 commands, and any declared agent metadata for each skill folder to surface
 Codex/Claude install parity gaps, then extend it with a small corpus of
 representative queries and expected-output summaries per core skill
 (starting with `codebase-codemap`, `session-learning`) to smoke-test sample
 responses across both toolchains.

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

### 2026-07-13 - 코드맵 하이드레이션 게이트

Status: proposed

Why now: `docs/CODEMAPS/projects/*.md`는 최근 세 차례 갱신(07-07 → 07-08 → 07-12/13)에서도 `all`, `android-support`, `Keelim-Knowledge-Vault`, `keelim-vercel`, `toto`가 "Files scanned: 0", `all-web-ui`/`rich`가 "Unknown"으로 그대로다. 이 저장소가 제공하는 `skills/codebase-codemap/scripts/generate_codemap.py`가 하이드레이션되지 않은 자식 저장소를 빈 스냅샷으로 조용히 남기기 때문에, `scripts/refresh-codemaps.py`를 돌려도 실제로는 최신화되지 않은 코드맵이 방금 갱신된 것처럼 보인다.

First slice: `generate_codemap.py` 실행 전에 대상 자식 저장소가 실제로 하이드레이션됐는지 확인하고, 비어 있으면 스냅샷 상단에 "stale/stub — hydrate first" 배지를 명시적으로 남기거나 해당 파일 갱신을 건너뛰도록 스킬을 보강한다.
