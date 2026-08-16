# youtube

Last reviewed: 2026-08-16 KST

## Signals

- `youtube`는 Remotion 렌더러(`youtube/remotion/`), 자동화 서비스(`youtube/services/*`), 개별 영상 프로젝트(`youtube/videos/*`)로 구성된 자율(autonomous) 저장소이며, 루트 Bun 워크스페이스에 세 개의 glob 멤버로 등록돼 있다.
- 동시에 루트 uv 워크스페이스의 Python 멤버이기도 해서(Python >=3.13), `rich`와 함께 numpy/pandas/playwright/pytest/ruff 등 공유 `constraint-dependencies` 정합성을 지켜야 한다.
- 루트 체크아웃에는 기본적으로 존재하지 않아("hydrate locally before running bun install") 로컬에서 하이드레이션하지 않으면 워크스페이스 설치·타입체크·의존성 검증이 조용히 이 멤버를 건너뛸 수 있다.
- `videos/*` glob 특성상 영상 하나당 새 워크스페이스 패키지가 반복 생성되는 구조라, 부트스트랩 절차가 매번 수작업으로 반복될 가능성이 크다.

## Open ideas

### 2026-08-16 - 영상 프로젝트 부트스트랩 템플릿화

Status: proposed

Why now: `youtube/videos/*`는 영상 하나당 새 워크스페이스 패키지가 생기는 반복 구조인데, 루트 문서에는 생성 절차나 템플릿이 없어 매 영상마다 Remotion 설정과 서비스 연동을 수작업으로 다시 맞출 위험이 있다.

First slice: 최근 생성된 영상 프로젝트 1~2개의 구조를 비교해 공통 스캐폴딩(설정 파일, 서비스 연결, catalog 의존성)을 뽑아내고, 새 영상 패키지를 만들 때 쓸 최소 템플릿/체크리스트를 만든다.

### 2026-08-16 - Bun/uv 이중 워크스페이스 의존성 정합성 게이트

Status: proposed

Why now: `youtube`는 Bun 워크스페이스(remotion/services/videos)와 uv 워크스페이스(Python, `rich`와 constraint-dependencies 공유) 양쪽에 동시에 걸쳐 있는데, 저장소가 루트 체크아웃에 기본으로 존재하지 않아 하이드레이션을 건너뛰면 두 런타임의 버전 드리프트가 오래 감지되지 않을 수 있다.

First slice: `uv run python scripts/verify-python-dependency-constraints.py`와 `bun run typecheck:web` 계열 검증 앞에 `youtube`가 하이드레이션된 상태인지 확인하는 사전 점검을 추가하고, 누락 시 명확한 경고를 남긴다.
