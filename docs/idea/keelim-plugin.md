# keelim-plugin

Last reviewed: 2026-07-14 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- `docs/CODEMAPS/projects/keelim-plugin.md`(2026-07-14)로 확인한 실제 스킬 인벤토리:
  `codebase-codemap`(28개 파일, `generate_codemap.py` 포함), `jira-ticket-desk`,
  `session-learning`, `session-usage-dashboard`. 이 중 `jira-ticket-desk`,
  `session-learning`, `session-usage-dashboard`는 이미 자체 `test_*.py`를 갖고 있어
  스킬별 최소 스모크 테스트는 부분적으로 존재하지만, Codex/Claude 설치 경로 동등성이나
  스킬 간 공통 검증은 아직 한곳에 모여 있지 않다.
- 루트 `docs/CODEMAPS/CODEGRAPH.md`는 `scripts/codegraph.sh`가 child repo `.codegraph/`
  인덱스로 CodeGraph 커맨드를 라우팅하는 디스패처라고 문서화하지만, 실제로는
  `scripts/`와 `package.json`에 해당 스크립트가 없다(2026-07-14 확인) — keelim-plugin이
  `generate_codemap.py`의 실제 호스트이므로 이 문서-구현 드리프트도 이 저장소의
  검증 범위에 포함하는 편이 자연스럽다.

## Open ideas

### 2026-04-12 - Generated skill catalog and install matrix

Status: proposed

Why now: As the skill set grows, a human-maintained README will become less
 useful than a generated catalog with tags, summaries, and installation targets.

First slice: Generate a catalog page from `skills/*/SKILL.md` metadata with
 quick filters for purpose, platform, and maintenance state.

### 2026-04-12 - Skill smoke-test harness

Status: proposed (2026-07-14 갱신 — 범위에 CodeGraph 디스패처 계약 추가)

Why now: Cross-tool skills are valuable only if install paths, metadata, and
 basic workflow assumptions stay valid for both Codex and Claude, and there is
 no single check that compares install/readme metadata across both toolchains.
 몇몇 스킬(`jira-ticket-desk`, `session-learning`, `session-usage-dashboard`)은
 이미 자체 `test_*.py`를 갖고 있지만 흩어져 있어 한곳에서 확인할 수 없다. 여기에
 더해 `docs/CODEMAPS/CODEGRAPH.md`가 문서화한 `scripts/codegraph.sh` 디스패처가
 실제 `scripts/`에는 없는 문서-구현 드리프트도 같은 성격의 문제다.

First slice: Add a lightweight verifier that checks required files, install
 commands, and any declared agent metadata for each skill folder, then surface
Codex/Claude install parity gaps before publishing. 같은 검증에 `scripts/codegraph.sh`
 존재 여부와 `CODEGRAPH.md`에 적힌 디스패치 커맨드의 실제 라우팅 가능성을 포함해,
 스킬 설치 계약과 코드그래프 디스패처 계약을 한 번에 잡는다.

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

### 2026-04-14 - 스킬 재사용 그래프

Status: proposed

Why now: 스킬이 늘수록 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어져서, 공통 프리미티브와 재사용 가능한 조합을 한 장의 그래프로 보면 중복 정리와 신규 설치 판단이 빨라진다.

First slice: `skills/*/SKILL.md`를 스캔해 공통 키워드·연관 스킬·설치 경로를 묶은 그래프를 만들고, 함께 묶어야 할 스킬 묶음을 표시한다.
