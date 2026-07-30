# keelim-plugin

Last reviewed: 2026-07-30 KST

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
 quick filters for purpose, platform, and maintenance state.

### 2026-04-13 - 스킬 변경 영향 노트

Status: proposed

Why now: Codex와 Claude가 같은 skill 폴더를 공유하므로, 작은 문서나 프롬프트 수정도 어떤 스킬이 어떻게 바뀌었는지 한눈에 보이지 않으면 리뷰 비용이 커진다.

First slice: 변경된 `SKILL.md`와 에이전트 메타데이터를 묶어 변경 유형별 영향 요약을 만드는 changelog를 생성하고, 배포 전에 어떤 스킬을 다시 확인해야 하는지 표시한다.

### 2026-07-30 - 설치·실행 검증 하네스 (2026-04-12, 2026-04-14 아이디어 통합)

Status: proposed

Why now: "설치 경로/메타데이터 정합성 검사"와 "프롬프트·실행 회귀 코퍼스"를 별도로 다뤘지만, 둘 다 "이 스킬이
Codex/Claude 양쪽에서 여전히 동작하는가"라는 같은 질문을 문서 층과 실행 층에서 나눠 물은 것이었다. 두 계층을
하나의 검증 하네스로 합치면 설치 파일 정합성과 실행 품질을 같은 리포트에서 함께 볼 수 있다.

First slice: 각 스킬 폴더의 필수 파일·설치 명령·에이전트 메타데이터를 검사하는 가벼운 검증기와, 핵심 스킬별
대표 질의·기대 출력 요약 코퍼스를 같은 하네스에 묶어, Codex/Claude 설치 패리티 격차와 실행 회귀를 함께
publish 전에 표시한다.

### 2026-07-30 - CodeGraph 디스패처 격차 해소

Status: proposed

Why now: `docs/CODEMAPS/CODEGRAPH.md`는 루트가 `scripts/codegraph.sh` 디스패처로 각 child repo의 `.codegraph/`
그래프를 라우팅한다고 계약을 정의하지만, 같은 문서가 "`scripts/codegraph.sh` is not present in this checkout"라고
명시하고 있어 문서와 실제 스크립트 인벤토리(`docs/CODEMAPS/SCRIPTS.md`) 사이에 격차가 있다. `keelim-plugin`은
codemap 생성기(`skills/codebase-codemap/scripts/generate_codemap.py`)를 호스팅하는 저장소라서, 이 디스패처 계약을
실제로 채우거나 문서를 실제 상태에 맞게 좁히는 결정을 내리기 가장 적합한 위치다.

First slice: `scripts/codegraph.sh`를 실제로 만들지, 아니면 CODEGRAPH.md의 디스패처 설명을 "수동으로 각 child repo에서
직접 실행" 계약으로 정정할지 결정하고, 결정에 맞춰 문서와 (필요하다면) 최소 스크립트를 함께 정리한다.

### 2026-04-14 - 스킬 수명주기 태그

Status: proposed

Why now: 스킬 수가 늘수록 active/experimental/deprecated 상태를 설치 전부터 보이게 해야, 검증되지 않은 스킬이나 내려가야 할 스킬을 잘못 쓰는 일을 줄일 수 있다.

First slice: `skills/*/SKILL.md`와 README 카탈로그에 lifecycle 메타데이터를 붙이고, deprecated 또는 unverified 스킬을 설치 화면에서 따로 표시한다.

### 2026-04-14 - 스킬 재사용 그래프

Status: proposed

Why now: 스킬이 늘수록 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어져서, 공통 프리미티브와 재사용 가능한 조합을 한 장의 그래프로 보면 중복 정리와 신규 설치 판단이 빨라진다.

First slice: `skills/*/SKILL.md`를 스캔해 공통 키워드·연관 스킬·설치 경로를 묶은 그래프를 만들고, 함께 묶어야 할 스킬 묶음을 표시한다.
