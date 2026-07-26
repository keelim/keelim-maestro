# keelim-plugin

Last reviewed: 2026-07-26 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.

## Open ideas

### 2026-04-12 - Generated skill catalog and install matrix (수명주기 태그 통합)

Status: proposed

Why now: As the skill set grows, a human-maintained README will become less
 useful than a generated catalog with tags, summaries, and installation targets —
 and lifecycle state (active/experimental/deprecated) needs to be visible before
 install, not discovered after something breaks. This absorbs the earlier
 standalone "스킬 수명주기 태그" idea, since lifecycle state is just another catalog field.

First slice: Generate a catalog page from `skills/*/SKILL.md` metadata with
 quick filters for purpose, platform, and maintenance state; add a `lifecycle`
 field to each `SKILL.md` and surface deprecated/unverified skills distinctly
 on the install screen.

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

### 2026-07-26 - CodeGraph 디스패처 문서-구현 갭 해소

Status: proposed

Why now: `docs/CODEMAPS/CODEGRAPH.md`는 `scripts/codegraph.sh`를 통해 child repo CodeGraph 명령을 라우팅하는 디스패치 계약을 정의하지만, 실제로는 `scripts/codegraph.sh`가 저장소에 존재하지 않는다(이번 점검에서 확인). `keelim-plugin`이 `codebase-codemap` 스킬과 codemap 생성 스크립트(`generate_codemap.py`)를 호스팅하는 저장소이므로, 문서가 약속한 디스패처를 실제로 만들거나 문서를 현재 워크플로(각 child repo에서 직접 실행)에 맞게 고치는 결정이 필요하다.

First slice: `scripts/codegraph.sh`를 최소 라우팅 버전(child repo 이름 → `cd <child> && codegraph ...`)으로 만들거나, 만들지 않기로 하면 `CODEGRAPH.md`의 Dispatch Commands 섹션을 "child repo에서 직접 실행" 현실에 맞게 수정한다.
