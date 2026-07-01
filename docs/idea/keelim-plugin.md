# keelim-plugin

Last reviewed: 2026-07-01 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.

## Open ideas

### 2026-04-12 - Generated skill catalog and install matrix

Status: proposed

Why now: As the skill set grows, a human-maintained README will become less
 useful than a generated catalog with tags, summaries, and installation targets.

First slice: Generate a catalog page from `skills/*/SKILL.md` metadata with
 quick filters for purpose, platform, and maintenance state — including an
 explicit active/experimental/deprecated lifecycle tag per skill so unverified
 or retiring skills are visibly flagged before install (2026-07-01: merged in
 the former "스킬 수명주기 태그" entry).

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

### 2026-04-14 - 스킬 재사용 그래프

Status: proposed

Why now: 스킬이 늘수록 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어져서, 공통 프리미티브와 재사용 가능한 조합을 한 장의 그래프로 보면 중복 정리와 신규 설치 판단이 빨라진다.

First slice: `skills/*/SKILL.md`를 스캔해 공통 키워드·연관 스킬·설치 경로를 묶은 그래프를 만들고, 함께 묶어야 할 스킬 묶음을 표시한다.

### 2026-07-01 - 코드맵 생성기 경로 계약 가드

Status: proposed

Why now: root의 `scripts/refresh-codemaps.py`는 `keelim-plugin/skills/codebase-codemap/scripts/generate_codemap.py`가 그 경로에 그대로 있어야 동작하는 암묵적 의존성을 갖고 있다(`docs/CODEMAPS/README.md`, `docs/CODEMAPS/projects/keelim-plugin.md`). 기존 `scripts/verify-keelim-plugin-rename.sh`는 README/gitlink 표기만 검사할 뿐 이 생성기 스크립트 경로·CLI 계약은 검사하지 않아서, `keelim-plugin`이 스킬 경로를 재구성하면 root 코드맵 리프레시가 조용히 깨질 수 있다.

First slice: `refresh-codemaps.py` 실행 전에 `generate_codemap.py`의 경로와 최소 CLI 시그니처가 유지되는지 확인하는 프리체크를 추가하고, 경로가 바뀌면 애매한 실패 대신 명확한 에러로 즉시 알린다.
