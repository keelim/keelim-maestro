# rich 아이디어 백로그

<!-- 마지막 검토: 2026-06-17 -->
<!-- 열린 아이디어: 1 -->

**저장소:** https://github.com/keelim/rich  
**유형:** 자율 자식 저장소 (서브모듈 전환 대기)  
**현재 상태:** 워킹트리 더티 · 원격 동기화 필요 (코드맵 기준)

---

## RICH-001 워킹트리 동결 및 원격 동기화

**우선순위:** 높음  
**근거:** `docs/CODEMAPS/projects/rich.md`에서 "dirty working tree; commits ahead of origin; do not pin until reconciled" 확인.
이 상태가 지속되면 `all-web-ui` 서브모듈 전환 및 루트 워크스페이스 핀 확장이 모두 차단된다.
`SUBMODULES.md`의 "Expansion Blockers" 항목에도 `rich` 해결이 1순위로 명시되어 있다.

**행동 항목:**
1. `bun run report:baseline`으로 더티 파일·앞선 커밋 목록 확인
2. 분리 또는 동결 전략 결정: 브랜치 분기 후 원격 푸시, 또는 스태시 후 클린 푸시
3. `origin/master`와의 클린 상태 검증
4. `all-web-ui` UI-001 차단 해소 기록 후 루트 확장 계획 재개

**차단 해소 후 효과:**
- `all-web-ui` 서브모듈 전환 가능 (UI-001)
- 루트 `bun run report:baseline` 신뢰도 회복
- 향후 `rich` 데이터 현대화 작업 안전 진행 가능

**연관 아이디어:** [`all-web-ui` UI-001](all-web-ui.md#ui-001-서브모듈-전환-준비-체크리스트-관리)
