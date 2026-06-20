# keelim-plugin 아이디어

<!-- 마지막 검토: 2026-06-20 | 오픈 아이디어: 2 -->

프로젝트 유형: 등록 서브모듈 (Python 에이전트 스킬 및 자동화 플러그인)  
코드맵 참조: `docs/CODEMAPS/projects/keelim-plugin.md`

---

## [OPEN] 에이전트 스킬 인벤토리 루트 코드맵 문서화

**근거:** `docs/CODEMAPS/projects/keelim-plugin.md`에 `skills/codebase-codemap/scripts/generate_codemap.py`만 언급되어 있다. 실제 스킬 목록과 각 스킬의 입출력 계약이 루트 코드맵에 기술되어 있지 않아 에이전트 조율 시 어떤 스킬을 활용할 수 있는지 파악하기 어렵다.

**내용:**
1. `keelim-plugin` 서브모듈을 초기화하고 `skills/` 디렉터리 구조를 확인한다.
2. 각 스킬의 이름, 진입점, 파라미터, 출력 형식을 정리한다.
3. `docs/CODEMAPS/projects/keelim-plugin.md`에 스킬 인벤토리 섹션을 추가한다.
4. 새 스킬 추가 시 루트 코드맵을 갱신하는 절차를 문서화한다.

**가치:** 문서/코드맵 커버리지 갭 해소 — 에이전트가 활용 가능한 스킬을 명확히 파악할 수 있다.

---

## [OPEN] 코드맵 생성기 갱신 주기 및 트리거 자동화

**근거:** `docs/CODEMAPS/projects/keelim-plugin.md`에 `generate_codemap.py`가 루트 `scripts/refresh-codemaps.py`에서 호출된다고 명시되어 있으나, 코드맵 갱신이 수동 실행에만 의존한다. 코드맵이 오래되면 아이디어 가드닝 품질이 저하된다.

**내용:**
1. 코드맵 자동 갱신 트리거 조건을 정의한다 (예: 주 1회 cron, PR 병합 후, 서브모듈 핀 변경 후).
2. `scripts/refresh-codemaps.py` 실행 후 변경 사항을 자동으로 커밋/PR 생성하는 GitHub Actions 워크플로를 설계한다.
3. 초기화가 필요한 서브모듈(all, all-web-ui, rich, youtube 등)이 없는 환경에서도 부분 갱신이 가능한지 확인한다.

**가치:** 자동화 기회 — 코드맵이 항상 최신 상태를 유지하면 아이디어 가드닝의 증거 기반이 강화된다.
