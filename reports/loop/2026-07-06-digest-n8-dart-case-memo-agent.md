# [digest] N8 — DART 공시 이벤트 → 케이스 메모 초안 에이전트 설계 계획서

- 사이클: 3 / 날짜: 2026-07-06
- 시드: docs/idea/net-new-2026-07-02.md §N8 (Likely home: rich)
- 게이트: **P1(rich freeze) 해제 전 코드 착수 금지** — 본 리포트는 기획·스키마 설계만 담음. 파일 수정 없음.
- 작성: python-lead (read-only)

## 배경·목표

omx_wiki 케이스 메모(IPO 단타·내부자 매수 등)는 현재 수동 작성. OpenDART 공시를 하루 1회 폴링해 관심 이벤트를 필터하고, frontmatter 골격 + 공시 링크만 채운 초안 md를 `rich/omx_wiki/_drafts/`에 자동 생성한다. LLM 요약은 2단계.

## 제안 frontmatter 스키마 (schemaVersion 1)

기존 메모(`rich/omx_wiki/외국인-선물-매수와-베이시스-선행-신호.md`)의 9개 필드를 100% 유지 (omx MCP 위키 린터·인덱서 호환):

- `title`: `"[초안] {회사명} {이벤트명_ko} ({rcept_dt})"`
- `tags`: `["draft","dart-event","krx", <event-slug>]`
- `created`/`updated`: 생성 시각 (ISO 8601 UTC Z, 기존 포맷)
- `sources`: `["https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"]`
- `links`: `[]` (승격 시 사람이 연결)
- `category`: 신규 값 `draft` (인덱서 분리 노출)
- `confidence`: `low` (자동 초안, 미검증)
- `schemaVersion`: `1`

신규 필드 3개: `draftStatus`(pending/promoted/discarded), `event`(reportCode·corpCode·rceptNo·rceptDt — 중복 방지 키), `generatedBy`(`dart-case-memo-agent@1`). 린터가 최상위 신규 키를 거부하면 `draftMeta:` 단일 매핑으로 중첩.

## First slice 설계

신규 파일: `rich/app/services/dart_event_polling.py`(폴링·필터), `dart_case_memo_draft.py`(md 렌더러), `dart_event_store.py`(처리 완료 rcept_no sqlite), `rich/scripts/collect_dart_event_drafts.py`(CLI), `install_dart_event_draft_cron.sh`(cron 등록), 테스트 3본, 산출 디렉터리 `rich/omx_wiki/_drafts/`.

재사용:
- `rich/opendart_json/client.py:26` `OpenDartClient` — `from_env()`로 `DART_API_KEY` 로드, 재시도/429 흡수 내장.
- `rich/opendart_json/endpoints.py:84` `list`(공시검색 2019001) — bgn_de/end_de/pblntf_ty/corp_cls/페이지네이션.
- `rich/app/services/daily_market_snapshot_store.py:19` — sqlite upsert/idempotency 패턴 모사.
- `rich/scripts/collect_daily_market_snapshot.py`, `install_daily_market_snapshot_cron.sh` — CLI·cron 등록 관례 차용 (태그 `rich-dart-event-draft`).

흐름: 오늘자 `list` 폴링 (corp_cls=Y) → report_nm 키워드 룰 필터 → store에서 처리된 rcept_no 제외 → frontmatter 골격+본문 스텁 렌더 → `_drafts/{날짜}-{corp}-{event-slug}-{rcept_no}.md` → rcept_no 기록.

이벤트 필터 (전부 endpoints.py 기등록): 유상증자 2020023, 무상증자 2020024, 유무상증자 2020025, 감자 2020026, CB 발행 2020033, 자사주 취득 2020038/2020040, 내부자 소유보고 2019022, 5%룰 2019021. IPO는 발행공시 키워드 룰 근사(2단계 정교화). 1차는 탐지만, DS004/DS005 상세 호출은 2단계.

## 검증 방법 (P1 해제 후)

```bash
cd rich
uv --cache-dir .omx/uv-cache run --python 3.13 pytest tests/test_dart_event_polling.py tests/test_dart_case_memo_draft.py tests/test_dart_event_store.py -q
uv --cache-dir .omx/uv-cache run --python 3.13 ruff check opendart_json app/services scripts
PYTHONPATH=. uv --cache-dir .omx/uv-cache run --python 3.13 python scripts/collect_dart_event_drafts.py --dry-run --date 2026-07-06
```

테스트는 `requests.Session` 목 주입(기존 `test_opendart_client.py` 패턴)으로 실 API 미호출. 커버리지 목표 3모듈 80%+.

## 리스크·열린 질문

1. **P1 freeze**: 코드 착수는 rich freeze/split 결정 이후로만 (`docs/idea/rich.md:86` 근거). 착수 승인은 오케스트레이터/사용자 판단.
2. **list 엔드포인트 해상도**: 세부 report code 직접 필터 불가 → 키워드 룰 오탐/누락 가능. 룰을 config로 분리할지 결정 필요.
3. **중복 초안**: rcept_no 유일 키 + 파일명 포함으로 이중 방어. 정정공시(다중 rcept_no) 정책 미정.
4. **Rate limit**: 일 20,000건 제한 — 1차는 여유, 2단계 상세 엔드포인트 확장 시 배치 상한 필요.
5. **omx_wiki 린터 호환**: `_drafts/`가 인덱서 스캔에서 제외되는지, `category: draft` 허용 여부 — omx 위키 도구 소유자 확인 필요.

## 다음 액션

P1(rich freeze) 해제가 확인되면: "maestro-orchestrator로 python-lead에게 본 계획서(reports/loop/2026-07-06-digest-n8-dart-case-memo-agent.md) 기반 first slice 구현을 위임 — TDD(테스트 3본 선작성), 구현 후 qa가 omx_wiki 린터 호환·cron 등록 멱등성 검증." P1 미해제 상태라면 열린 질문 5번(omx 린터 호환)만 먼저 확인해 두는 것을 권장.
