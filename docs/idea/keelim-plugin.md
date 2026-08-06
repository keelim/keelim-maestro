# keelim-plugin

Last reviewed: 2026-08-06 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- `CATALOG.md`/`catalog.json`은 이미 `scripts/gen-catalog.mjs`로 생성되고
  `--check` + `git diff --check`로 drift가 막혀 있으며, `scripts/verify-skills.sh
  --require-codex-meta`가 매 스킬의 frontmatter·capability 스키마(`read_only`,
  `local_write`, `network_read`, `external_write`, `credentials`, `hooks`)와
  `agents/openai.yaml` 존재를 이미 검증한다.

## Open ideas

### 2026-04-12 - 카탈로그 capability 필터 뷰

Status: proposed

Why now: 카탈로그 생성과 drift 방지는 이미 자동화돼 있지만, `CATALOG.md`/`catalog.json` 둘 다
평면 목록이라 목적·설치 대상(Codex/Claude)·capability(`network_read`, `credentials` 등)
조합으로 걸러보려면 사람이 직접 스캔해야 한다.

First slice: `catalog.json`의 capability 필드를 이용해 목적·설치 대상·capability로 필터링할
수 있는 얇은 정적 조회 뷰(HTML 또는 CLI)를 만든다.

### 2026-04-13 - 스킬 변경 영향 노트

Status: proposed

Why now: Codex와 Claude가 같은 skill 폴더를 공유하므로, 작은 문서나 프롬프트 수정도 어떤 스킬이 어떻게 바뀌었는지 한눈에 보이지 않으면 리뷰 비용이 커진다.

First slice: 변경된 `SKILL.md`와 에이전트 메타데이터를 묶어 변경 유형별 영향 요약을 만드는 changelog를 생성하고, 배포 전에 어떤 스킬을 다시 확인해야 하는지 표시한다.

### 2026-04-14 - 스킬 프롬프트 회귀 코퍼스 & Codex/Claude 설치 동등성

Status: proposed

Why now: 설치 경로와 메타데이터가 맞아도 실제 실행 예시나 프롬프트 품질이 깨지면 스킬은 곧바로 재사용성을 잃기 때문에, 문서 정합성만으로는 충분하지 않다. `scripts/check.sh`/`verify-skills.sh`는 이미 frontmatter·capability 스키마와 `agents/openai.yaml` 존재를 검증하지만, 같은 스킬을 Codex와 Claude 양쪽에서 실제로 실행했을 때 동작이 동일한지는 여전히 검증하지 않는다.

First slice: 핵심 스킬별 대표 질의와 기대 출력 요약을 모은 코퍼스를 만들고, Codex/Claude 양쪽에서 같은 프롬프트를 실행해 응답 형태(성공/실패, 산출물 유무)를 비교하는 최소 스모크 러너를 붙인다.

### 2026-04-14 - 스킬 수명주기 태그

Status: proposed

Why now: 스킬 수가 늘수록 active/experimental/deprecated 상태를 설치 전부터 보이게 해야, 검증되지 않은 스킬이나 내려가야 할 스킬을 잘못 쓰는 일을 줄일 수 있다.

First slice: `skills/*/SKILL.md`와 README 카탈로그에 lifecycle 메타데이터를 붙이고, deprecated 또는 unverified 스킬을 설치 화면에서 따로 표시한다.

### 2026-04-14 - 스킬 재사용 그래프

Status: proposed

Why now: 스킬이 늘수록 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어져서, 공통 프리미티브와 재사용 가능한 조합을 한 장의 그래프로 보면 중복 정리와 신규 설치 판단이 빨라진다.

First slice: `skills/*/SKILL.md`를 스캔해 공통 키워드·연관 스킬·설치 경로를 묶은 그래프를 만들고, 함께 묶어야 할 스킬 묶음을 표시한다.
