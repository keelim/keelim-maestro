# [garden] docs/idea 백로그 감사 — 수정 제안 7건

- 사이클: 2 / 날짜: 2026-07-06
- 근거 파일: docs/idea/index.md, docs/idea/{all,all-web-ui,keelim-vercel,rich,keelim-plugin,android-support,Keelim-Knowledge-Vault}.md, net-new-2026-06-06.md, net-new-2026-07-02.md, future.md
- 본 리포트는 제안만 담음 — 백로그 파일은 수정하지 않았음.

## 인덱스 불일치

- open ideas 카운트: **전 프로젝트 일치** (all 12, all-web-ui 9, android-support 5, Knowledge-Vault 6, keelim-plugin 6, keelim-vercel 9, rich 8).
- Last reviewed 날짜 불일치 4건: `all`, `all-web-ui`, `keelim-vercel`, `rich` — 인덱스는 `2026-06-06`, 파일 헤더는 `2026-05-16`. (N1~N7 추가 시 파일 헤더를 안 올린 것이 원인.)
- 인덱스 미등재 파일 1건: `product-design-service-improvements-2026-06-06.md` (35.9K, 2026-07-05까지 갱신된 활성 로그)가 index.md 어디에도 없음.

## 구현됐는데 open으로 남은 항목 (문서 미갱신 의심)

- `scripts/security-scan.mjs`, `scripts/dep-audit.mjs`, `scripts/dep-freshness.mjs` 존재 → net-new-2026-06-06의 N2a/N2b/N3이 여전히 "즉시 실행 가능(미실행)".
- `keelim-vercel/scripts/check-bundle-budget.mjs`, `all-web-ui/scripts/check-bundle-budget.mjs` 존재 → 두 프로젝트 파일의 "웹 성능 예산 게이트(N4)"가 여전히 `Status: proposed`. (스크립트가 시드 요건을 충족하는지는 확인 필요.)
- N9(youtube 백로그 신설), N13(routines.md 신설)이 지시한 `docs/idea/youtube.md`, `docs/idea/routines.md` 미생성 — youtube 작업 커밋은 이미 존재.

## 중복 후보

- N4 "웹 성능 예산 게이트"가 all-web-ui/keelim-vercel/rich 3파일에 거의 동일 문구로 등재 → open 카운트 3중 계상.
- `future.md`(2026-04-16 inbox) 항목 다수가 프로젝트 파일로 라우팅 완료 후에도 원본이 남아 이중 계상 (Next-best-action, freshness watchdog, 토큰 소비 가시화 등).
- 인접 주제 (분리 정당하나 링크 권장): N7 프리미티브↔여정, N6 텔레메트리↔usage heatmap, N12 임베딩 인덱스↔N5a 위키 Q&A.

## 스테일

- 7개 프로젝트 파일 전부 파일 헤더 기준 `2026-05-16` = 51일 경과. index.md 자체도 `2026-06-06` = 30일.

## 다음 액션

다음 지시문을 승인하면 그대로 실행 가능: "docs/idea 정비 — (1) all/all-web-ui/keelim-vercel/rich의 Last reviewed 헤더를 2026-07-06으로 갱신하고 index.md와 동기화, (2) check-bundle-budget·security-scan·dep-audit·dep-freshness 스크립트가 N2a/N2b/N3/N4 시드 요건을 충족하는지 확인 후 해당 항목 Status를 done으로 전환하고 카운트 반영, (3) product-design-service-improvements 파일을 index.md inbox 표에 등재, (4) N4 3중 등재를 상위 1건+소비자별 체크리스트로 통합, (5) future.md의 라우팅 완료 항목 아카이브, (6) youtube.md 백로그 파일 신설(N9)."
