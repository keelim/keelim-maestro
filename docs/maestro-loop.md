# Maestro Loop — 사이클 지시문

`/loop`(자율 페이스)가 매 사이클 이 문서를 따른다. **한 사이클 = 레인 1개 실행 + 리포트 1개 산출 + 상태 갱신.** 코드·백로그 파일은 절대 수정하지 않는다 — 산출물은 계획서/리포트뿐이다.

## 0. 상태 읽기

`reports/loop/state.json`을 읽는다. 없으면 아래로 초기화한다:

```json
{
  "cycle": 0,
  "lastDriftCheck": null,
  "lastGardening": null,
  "backlogCursor": []
}
```

- `cycle`: 완료한 사이클 수 (int)
- `lastDriftCheck` / `lastGardening`: ISO 8601 날짜 (`"2026-07-06"`)
- `backlogCursor`: 이미 계획서를 산출한 백로그 항목 슬러그 배열

## 1. 레인 선택 (우선순위 순, 첫 매치 실행)

### watch — `lastDriftCheck`가 없거나 24시간 이상 경과 시

`qa` 에이전트를 read-only로 스폰해 `boundary-check` 스킬 관점으로 점검:

- all-web-ui exports ↔ 소비 프로젝트(keelim-vercel, rich/web) 사용처
- rich API 스키마 ↔ 프론트 타입
- youtube 파이프라인 스키마 ↔ remotion renderer

기준선: `scripts/all-web-ui-rich-allowed-drift.txt` 허용 목록. 기준선에 없는 드리프트만 FAIL로 보고.

### garden — `lastGardening`이 없거나 7일 이상 경과, 또는 `cycle % 7 == 0` (cycle > 0)

`docs/idea/`를 감사하고 **수정 제안 리포트**만 산출 (직접 수정 금지):

- `index.md`의 last-reviewed 날짜·open ideas 카운트가 각 프로젝트 파일과 일치하는가
- 근접 중복 아이디어
- 이미 구현/폐기됐는데 open으로 남은 항목 (git log·코드로 확인)

### digest — 기본 레인

`docs/idea/`에서 `backlogCursor`에 없는 최우선 항목 1건 선정:

1. net-new 시드 우선: N8~N13 (`net-new-2026-07-02.md`) → N1~N7 (`net-new-2026-06-06.md`)
2. 그 다음 프로젝트 백로그(`all.md`, `rich.md` 등) 상단 항목

해당 도메인 리드 에이전트(android-lead/python-lead/web-lead)를 **read-only 지시**로 스폰하거나 Explore→Plan으로 **구현 계획서**를 산출:

- 배경·목표 (시드 원문 요약)
- 대상 파일 경로, 재사용할 기존 코드/유틸
- 단계별 구현 순서
- 검증 방법 (빌드/테스트 명령)
- 예상 리스크·열린 질문

## 2. 리포트 산출

`reports/loop/YYYY-MM-DD-<lane>-<slug>.md`로 저장. 공통 형식:

```markdown
# [lane] <제목>
- 사이클: N / 날짜: YYYY-MM-DD
- 근거 파일: ...

<본문: 레인별 내용>

## 다음 액션
<사용자가 승인하면 그대로 maestro-orchestrator에 넘길 수 있는 한 문단 지시문>
```

## 3. 상태 갱신 & 대기

1. `state.json` 갱신: `cycle` +1, 실행한 레인의 타임스탬프 갱신, digest면 슬러그를 `backlogCursor`에 추가.
2. 사용자에게 1~3줄 요약 보고 (레인, 산출 리포트 경로, 핵심 발견).
3. ScheduleWakeup 1200~1800초. watch 직후처럼 후속 없으면 3600초.

## 종료 조건

- 사용자가 중단을 요청하면 즉시 종료.
- digest 대상이 소진되고 watch/garden도 최신이면: 요약 보고 후 3600초 대기로 전환.
