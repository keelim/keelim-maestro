# keelim-plugin

Last reviewed: 2026-06-07 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- `jira-ticket-desk`, `session-learning`, `session-usage-dashboard` 스킬이 새로
  추가됐다. `session-learning`은 훅 설치·학습 옵저버·후보 리뷰를 포함하고,
  `session-usage-dashboard`는 세션 로그를 파싱해 HTML 보고서를 생성한다. 이 두
  스킬은 Codex·Claude 양쪽 세션 데이터를 수집·분석하는 연속 루프를 이룬다.

## Open ideas

### 2026-04-12 - 스킬 카탈로그·설치 매트릭스·재사용 그래프

Status: proposed

Why now: 스킬 수가 늘수록 인간이 유지하는 README보다 생성된 카탈로그가 더 유용하다. 또한 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어져서, 공통 프리미티브와 재사용 가능한 조합을 한 장의 그래프로 보면 중복 정리와 신규 설치 판단이 빨라진다.

First slice: `skills/*/SKILL.md` 메타데이터에서 태그·요약·설치 대상 필터를 포함한 카탈로그 페이지를 생성하고, 공통 키워드·연관 스킬·설치 경로를 묶은 재사용 그래프를 함께 표시해 함께 묶어야 할 스킬 묶음을 표면화한다.

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

### 2026-06-07 - 세션 학습·사용 대시보드 스킬 통합 검증 게이트

Status: proposed

Why now: `session-learning`(훅 설치, 학습 옵저버, 후보 리뷰)과 `session-usage-dashboard`(세션 로그 파싱, HTML 보고서 빌드) 스킬은 Codex·Claude 양쪽 세션 데이터를 수집·분석하는 연속 루프를 이루므로, 각 스킬의 입력·출력 계약과 Codex/Claude 설치 경로 패리티가 함께 검증돼야 한다. 두 스킬이 독립적으로만 테스트되면 파이프라인 연결 지점에서 조용히 깨질 수 있다.

First slice: `session-learning`의 훅 설치 스크립트·옵저버 출력 포맷·후보 리뷰 필드와 `session-usage-dashboard`의 JSONL 입력 스키마를 비교해 계약 불일치를 잡는 가벼운 통합 검사를 추가하고, 두 스킬의 Codex/Claude 설치 패리티 갭을 함께 표시한다.
