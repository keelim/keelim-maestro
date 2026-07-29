# keelim-plugin

Last reviewed: 2026-07-29 KST

## Signals

- Personal skill repository shared across Codex and Claude.
- Current value depends on discoverability, installation clarity, and confidence
  that a skill still works as documented.
- The repository already has a clear `skills/<name>/SKILL.md` contract.
- README가 Vercel skills CLI와 수동 symlink 설치 경로를 함께 설명하므로,
  카탈로그와 smoke-test가 설치 방식별 차이를 계속 드러내야 한다.
- 최신 코드맵(2026-07-29, 30 files) 기준 실제 스킬 구성은 `codebase-codemap`(이 워크스페이스의 `generate_codemap.py`를 호스팅), `jira-ticket-desk`, `session-learning`(observer → candidate 승격 → hook 설치), `session-usage-dashboard`이며, 일부는 이미 자체 `test_*.py`를 갖고 있다 — 카탈로그·smoke-test 아이디어는 이제 이 구체적 스킬 이름에 앵커링해야 한다.
- 이 저장소가 호스팅하는 `skills/codebase-codemap/scripts/generate_codemap.py`는 하이드레이션 여부를 감지하지 않는다 — 스캔한 파일이 0개일 때 "정말 빈 저장소"와 "그냥 로컬에 없음"을 구분하지 못하고, 그 구분은 지금 `docs/CODEMAPS/projects/README.md`의 사람이 쓴 문장에만 남아 있다.

## Open ideas

### 2026-04-12 - Generated skill catalog and install matrix

Status: proposed

Why now: As the skill set grows, a human-maintained README will become less
 useful than a generated catalog with tags, summaries, and installation targets.

First slice: Generate a catalog page from `skills/*/SKILL.md` metadata with
 quick filters for purpose, platform, and maintenance state.

### 2026-04-12 - Skill smoke-test harness

Status: proposed

Why now: Cross-tool skills are valuable only if install paths, metadata, and
 basic workflow assumptions stay valid for both Codex and Claude, and there is
 no single check that compares install/readme metadata across both toolchains.

First slice: Add a lightweight verifier that checks required files, install
 commands, and any declared agent metadata for each skill folder, then surface
Codex/Claude install parity gaps before publishing.

### 2026-04-13 - 스킬 변경 검증 번들 (영향 노트 + 회귀 코퍼스)

Status: proposed

Why now: Codex와 Claude가 같은 skill 폴더를 공유하므로, 작은 문서나 프롬프트 수정도 어떤 스킬이 어떻게 바뀌었는지, 실제 실행 예시나 프롬프트 품질까지 깨지지 않았는지 한눈에 보이지 않으면 리뷰 비용이 커진다. 문서 정합성 확인과 회귀 확인은 같은 배포 전 게이트에서 함께 다뤄야 중복 작업이 줄어든다.

First slice: 변경된 `SKILL.md`/에이전트 메타데이터로 변경 유형별 영향 요약 changelog를 생성하고, 핵심 스킬(`codebase-codemap`, `jira-ticket-desk`, `session-learning`, `session-usage-dashboard`)별 대표 질의·기대 출력을 모은 코퍼스로 Codex/Claude 양쪽 샘플 응답을 비교하는 스모크 테스트를 같은 검증 단계에 붙인다.

### 2026-04-14 - 스킬 수명주기 태그

Status: proposed

Why now: 스킬 수가 늘수록 active/experimental/deprecated 상태를 설치 전부터 보이게 해야, 검증되지 않은 스킬이나 내려가야 할 스킬을 잘못 쓰는 일을 줄일 수 있다.

First slice: `skills/*/SKILL.md`와 README 카탈로그에 lifecycle 메타데이터를 붙이고, deprecated 또는 unverified 스킬을 설치 화면에서 따로 표시한다.

### 2026-04-14 - 스킬 재사용 그래프

Status: proposed

Why now: 스킬이 늘수록 같은 절차나 판별 규칙이 여러 `SKILL.md`에 흩어져서, 공통 프리미티브와 재사용 가능한 조합을 한 장의 그래프로 보면 중복 정리와 신규 설치 판단이 빨라진다.

First slice: `skills/*/SKILL.md`를 스캔해 공통 키워드·연관 스킬·설치 경로를 묶은 그래프를 만들고, 함께 묶어야 할 스킬 묶음을 표시한다.

### 2026-07-29 - 코드맵 생성기 하이드레이션 인지 표시

Status: proposed

Why now: `skills/codebase-codemap/scripts/generate_codemap.py`는 디렉터리를 그대로 걷기만 하고 하이드레이션 여부를 확인하지 않는다. 그 결과 루트 `docs/CODEMAPS/projects/*.md` 다수가 "Files scanned: 0"으로 나오는데, 이는 진짜 빈 저장소인지 단순히 로컬에 체크아웃되지 않은 것인지 구분이 안 되고, 그 구분은 `projects/README.md`의 사람이 쓴 캐비트 문장에만 의존하고 있어 다음 갱신에서 쉽게 누락될 수 있다.

First slice: `generate_codemap.py`가 대상 디렉터리가 비어 있으면서 상위에서 gitlink/서브모듈로 등록돼 있는 경우 "unhydrated"로 명시적으로 표시하도록 최소 분기를 추가하고, 생성된 마크다운의 헤더에 그 상태를 그대로 남긴다.
