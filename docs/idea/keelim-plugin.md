# keelim-plugin

Last reviewed: 2026-06-30 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- `skills/codebase-codemap/scripts/generate_codemap.py`가 루트 `scripts/refresh-codemaps.py`에서
  호출된다(2026-06-30 코드맵 확인). 이 플러그인이 워크스페이스 코드맵 생성의 실질 소스다.

## Open ideas

### 2026-04-12 - 스킬 카탈로그·설치 매트릭스·재사용 그래프

Status: proposed

Why now: 스킬 수가 늘수록 수동 README보다 생성형 카탈로그가 유용하며, 스킬 간 공통 키워드·연관 관계·설치 경로를 한 그래프로 묶으면 중복 정리와 신규 조합 판단이 빨라진다.

First slice: `skills/*/SKILL.md` 메타데이터에서 태그·요약·설치 대상을 모은 카탈로그 페이지를 생성하고, 공통 키워드와 연관 스킬을 함께 그래프로 표시해 함께 설치해야 할 묶음을 제안한다.

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

### 2026-06-30 - 코드맵 생성기 인터페이스 계약

Status: proposed

Why now: `skills/codebase-codemap/scripts/generate_codemap.py`가 루트 `scripts/refresh-codemaps.py`에서 직접 호출된다. 플러그인 서브모듈 pin이 갱신될 때 CLI 인자나 출력 포맷이 바뀌면 루트 코드맵이 조용히 깨지거나 잘못된 스냅샷을 남기게 된다.

First slice: `generate_codemap.py`의 CLI 인자·출력 포맷·오류 모드를 명세하고, 루트 `refresh-codemaps.py`와의 계약 정합성을 검증하는 자동 검사를 추가한다. 플러그인 pin 갱신 시 이 검사가 통과해야 코드맵 갱신이 완료로 간주된다.
