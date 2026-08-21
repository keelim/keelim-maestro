# youtube

Last reviewed: 2026-08-21 KST

## Signals

- `youtube`는 원격 저장소가 아직 없는 private 로컬 checkout이며, 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 루트 uv 워크스페이스(`easy-release-note` 패키지) 양쪽에 동시에 소속된 유일한 autonomous child repo다.
- YouTube Shorts와 Easy Release Note 제작 파이프라인을 함께 다루며, 렌더러(Remotion)·서비스·개별 비디오 프로젝트가 각각 별도 패키지 glob으로 워크스페이스에 편입된다.
- `youtube/videos/*` glob은 신규 비디오 프로젝트가 추가될 때마다 루트 `bun.lock`을 변경시킨다는 점이 루트 문서에 이미 명시돼 있다.
- 로컬 자동화 스택에서 `rich`와 나란히 `n8n Kubernetes`가 `youtube`의 운영 런타임으로 문서화돼 있지만(`scripts/local-automation.sh status|verify n8n`), 해당 명령은 배포/서비스/포트 liveness만 확인하고 워크플로 실행 이력(성공/실패, 다음 실행)은 보여주지 않는다.
- `youtube`는 루트보다 낮은 자체 `requires-python`을 선언하고, 중첩 프로젝트 `youtube/simple`은 별도 lockfile과 호환 범위를 이유로 루트 uv 워크스페이스에서 의도적으로 제외돼 있다.
- 다른 트래킹 대상 프로젝트와 달리 `docs/CODEMAPS/projects/`에 `youtube` 코드맵 스냅샷이 아직 없다(하이드레이션되지 않은 checkout이라 codemap 생성기가 건너뜀).

## Open ideas

### 2026-08-21 - 비디오 패키지 락파일 변동 리포트

Status: proposed

Why now: `youtube/videos/*` glob이 새 비디오 프로젝트를 추가할 때마다 루트 `bun.lock`을 바꾼다는 사실이 이미 루트 문서에 적혀 있지만, 어떤 비디오 패키지가 락파일 변동을 유발했는지 보여주는 리포트가 없어서 리뷰어가 전체 lockfile diff를 직접 읽어야 한다.

First slice: 커밋 전/CI에서 `bun.lock` diff를 `youtube/videos/*`·`youtube/services/*`·`youtube/remotion` 경로별로 분류해, 신규/변경된 패키지 이름과 버전만 요약하는 짧은 리포트를 만든다.

### 2026-08-21 - n8n 워크플로 실행 이력 패널

Status: proposed

Why now: `scripts/local-automation.sh status n8n`/`verify n8n`은 deployment·service·port·렌더 디렉터리 존재 여부 같은 인프라 liveness만 확인하고, 실제 n8n 워크플로가 마지막으로 언제 성공했는지·실패했는지·다음 실행이 언제인지는 보여주지 않는다. Shorts 발행 자동화가 조용히 실패해도 인프라는 정상으로 보일 수 있다.

First slice: 기존 `status n8n`/`verify n8n` 인프라 체크에 더해, n8n API 또는 실행 로그에서 최근 워크플로 실행의 성공/실패와 다음 예정 실행을 뽑아 한 줄 요약으로 보여주는 하위 명령을 추가한다.

### 2026-08-21 - youtube 독립 실행 요구사항 드리프트 체크

Status: proposed

Why now: `youtube`는 루트 uv 워크스페이스보다 낮은 자체 `requires-python`을 선언하고, `youtube/simple`은 별도 lockfile로 워크스페이스 밖에 남아 있다. `rich`는 `scripts/verify-python-dependency-constraints.py`로 루트 constraint와의 정합성을 검증받지만, `youtube`의 독립 실행 요구사항이 루트 uv workspace 해석 결과와 갈라지는지 확인하는 절차는 아직 없다.

First slice: `verify-python-dependency-constraints.py` 옆에 `youtube`의 선언된 `requires-python`과 핵심 의존성 버전을 루트 `tool.uv.constraint-dependencies`와 비교해 드리프트만 보고하는 가벼운 체크를 추가하되, `youtube/simple`은 계속 워크스페이스 밖에 둔다.
