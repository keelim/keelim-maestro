# keelim-plugin

Last reviewed: 2026-07-31 KST

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
 quick filters for purpose, platform, and maintenance state. (2026-07-31 정리:
 2026-04-14 "스킬 재사용 그래프" 아이디어를 이 항목에 통합 — 카탈로그에 공통
 키워드·연관 스킬 그래프 뷰를 함께 붙여 중복 정리와 신규 설치 판단을 같이
 지원한다.)

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

### 2026-07-31 - 코드맵 하이드레이션 상태 가드

Status: proposed

Why now: 오늘 갱신된 `docs/CODEMAPS/projects/*.md` 중 `all`, `android-support`,
`Keelim-Knowledge-Vault`, `keelim-vercel`, `toto` 5개가 서브모듈이 초기화되지
않은 상태에서 생성돼 "Files scanned: 0 / No obvious entrypoint files
detected"로 그대로 커밋되어 있다. 실제로는 소스가 있는 저장소인데도 스냅샷만
보면 빈 저장소처럼 보여, 다음에 이 스냅샷을 기준선으로 참고하는 작업이 잘못된
결론을 낼 위험이 있다.

First slice: `skills/codebase-codemap/scripts/generate_codemap.py`가 스캔한
파일 수가 0이거나 placeholder 판정일 때 스냅샷 상단에 "hydration 필요" 배지를
강제로 남기게 하고, 루트 `scripts/refresh-codemaps.py`가 이런 placeholder로
기존의 실측 스냅샷을 덮어쓰지 않도록 가드를 추가한다.
