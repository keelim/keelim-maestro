# [digest] N9 — youtube 백로그 신설 + 롱폼→Shorts 재목적화 계획서

- 사이클: 4 / 날짜: 2026-07-06
- 시드: docs/idea/net-new-2026-07-02.md §N9 (Likely home: youtube — 백로그 파일 신설 필요)
- 루프는 백로그 파일을 직접 만들지 않음(리포트-온리) — 아래 골격을 승인 시 그대로 생성하면 됨.

## 배경·목표

youtube는 CLAUDE.md에 서브 프로젝트로 명시돼 있으나 `docs/idea/`에 백로그 파일이 없는 유일한 공백 프로젝트 (사이클 2 garden 감사에서도 재확인). First slice는 두 단계: (1) `docs/idea/youtube.md` 신설, (2) 롱폼 1편에서 Shorts 후보 3개를 뽑는 로컬 스크립트.

## 현황 조사 (2026-07-06)

- 기존 파이프라인: `youtube/src/easy_release_note/` 단일 패키지, CLI `ern`(pyproject `[project.scripts]`). derive→validate→remotion 렌더 흐름은 사이클 1 watch에서 경계 PASS 확인.
- 의존성: google-api-python-client, crawl4ai뿐 — **whisper/ffmpeg 계열 없음** → first slice는 신규 의존성 추가 필요.
- 자산 디렉터리 기존재: `videos/`, `uploads/`, `media/`, `renders/`, `outputs/` — 산출물 배치 관례 있음.

## (1) docs/idea/youtube.md 신설 골격 (제안 원문)

```markdown
# youtube — Idea Backlog

Last reviewed: 2026-07-06 KST
Open ideas: 1

## Signals
- 파이프라인: easy_release_note (derive→validate→remotion), CLI `ern`
- 자산: videos/, uploads/, renders/ — 롱폼 원본 보유
- 2026 콘텐츠 자동화 표준: 롱폼→Shorts 재목적화 + 사람 QA 게이트(15~20개당 1개 반려)
- 리텐션 우선 알고리즘: 30초·85% 리텐션 > 60초·50%

## Open ideas

### 2026-07-02 - 롱폼→Shorts 재목적화 파이프라인 (N9)
Status: proposed
출처: docs/idea/net-new-2026-07-02.md §N9
First slice: 로컬 스크립트 1본 — 기존 롱폼 1편 → Whisper 캡션 → 하이라이트 구간 선정
→ FFmpeg 세로 크롭(9:16) → Shorts 후보 3개 + 캡션 파일을 outputs/shorts-candidates/에 산출.
업로드는 범위 외(사람 QA 게이트 후 수동).
```

인덱스 반영: index.md Projects 표에 `youtube | youtube.md | 2026-07-06 KST | 1 | 롱폼→Shorts 재목적화` 행 추가.

## (2) Shorts 재목적화 first slice 설계

- 신규 파일: `youtube/scripts/extract_shorts_candidates.py` (기존 scripts/ CLI 관례 준수, argparse)
- 신규 의존성 (uv add, 로컬 실행 전제): `faster-whisper`(캡션·타임스탬프), ffmpeg는 시스템 바이너리 호출(`subprocess`, 의존성 추가 없이 — youtube에 이미 미디어 처리 관례 존재)
- 흐름: `--input videos/<파일>` → faster-whisper로 세그먼트 전사 → 휴리스틱 스코어(발화 밀도·키워드·30초 창)로 상위 3구간 선정 → ffmpeg `crop=ih*9/16:ih` 세로 크롭 + 구간 컷 → `outputs/shorts-candidates/{원본slug}/{n}.mp4` + `{n}.srt`
  - ponytail 원칙: 하이라이트 선정은 1차로 단순 휴리스틱 — LLM 선정은 후속 단계
- 검증: `uv --cache-dir .omx/uv-cache run --python 3.13 pytest tests/test_extract_shorts_candidates.py -q` (전사·ffmpeg는 목 처리, 구간 스코어링 로직만 단위 테스트) + 실제 롱폼 1편 드라이런
- 리스크: (a) faster-whisper 모델 다운로드 용량/속도 — small 모델 기본, (b) 크롭 중심 고정(얼굴 추적 없음)은 1차 한계로 명시, (c) 30초·85% 리텐션 기준은 산출 후 사람 QA로 판정 — 스크립트는 후보만 생성.

## 다음 액션

승인 시: "maestro-orchestrator로 (1) docs/idea/youtube.md를 위 골격으로 신설하고 index.md에 행 추가(문서 작업, 즉시 가능), (2) python-lead에게 extract_shorts_candidates.py first slice 구현 위임 — TDD로 스코어링 로직 테스트 선작성, faster-whisper small 모델, ffmpeg subprocess, 산출 후 qa가 실제 롱폼 1편으로 드라이런 검증."
