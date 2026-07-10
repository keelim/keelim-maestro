# future

Last updated: 2026-07-10 KST

## Purpose

이 문서는 `docs/idea/<project>.md`로 바로 라우팅하기 전에 잠깐 모아두는 **임시 공용 inbox**다.

- source of truth는 계속 각 `docs/idea/<project>.md`
- 여기는 cross-project 관점에서 한 번 더 묶어보는 곳
- 실행 계획/태스크 분해는 하지 않음
- 비슷한 아이디어는 프로젝트가 여러 개여도 **하나로 통합**해서 적음

## Review rule

- 첫 리뷰 오너: 이번 정리의 lead/synthesizer
- 첫 리뷰 시점: 생성 후 72시간 이내
- 각 항목은 이후 `docs/idea/<project>.md`로 라우팅, 분기, 폐기, 혹은 1회 연장 중 하나를 택함

## 2026-07-10 triage note

2026-04-16에 쌓인 24개 항목이 72시간 리뷰 기한을 크게 넘겨 방치되어 있었다. 이번 라운드에서
각 항목을 현재 `docs/idea/index.md` 및 프로젝트별 파일과 대조해 triage했다:

- 대부분(계약 드리프트 관제, 릴리스 계약/증적, 지식 미러·다이제스트, 공용 토큰 소비 가시화,
  next-best-action, 스킬 카탈로그, 릴리스 준비도/빌드 병목, backlink·resurfacer 등)은 이미
  `all.md`, `all-web-ui.md`, `android-support.md`, `Keelim-Knowledge-Vault.md`,
  `keelim-plugin.md`, `keelim-vercel.md`, `rich.md`에 동등하거나 더 구체적인 항목으로
  라우팅되어 있음을 확인했다. 중복 재등록 없이 폐기한다.
- "workspace trusted-baseline scoreboard" 항목은 `bun run report:baseline`으로 이미
  구현되어 더 이상 아이디어가 아니므로 폐기한다.
- 나머지 cross-project 운영 레이어 제안들(operator feedback layer, triage funnel,
  capture artifact workflow, execution mode contract registry, review cadence registry 등)은
  근거 있는 관찰이지만, 대상 프로젝트(`rich`, `keelim-vercel`, `all-web-ui`, `keelim-plugin`)가
  이미 프로젝트당 오픈 아이디어 상한(6개)에 도달해 있어 이번 라운드에서는 신규 등록하지 않았다.
  프로젝트 파일에서 기존 항목이 정리되어 슬롯이 열리면 재검토 대상으로 남긴다.

## Temporary inbox

(현재 대기 중인 항목 없음 — 위 triage로 모두 라우팅/폐기 처리됨)
