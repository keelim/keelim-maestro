# youtube

Last reviewed: 2026-09-07 KST

## Signals

- `youtube`는 자율 child 저장소이자 루트 Bun 워크스페이스(`youtube/remotion`,
  `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(`rich`와 함께)에
  동시에 소속된 활성 멤버다.
- Remotion 기반 렌더러, 자동화 서비스, 비디오 프로젝트가 각각 별도 패키지로
  분리되어 있어 워크스페이스 glob 해석과 하이드레이션 상태에 민감하다.
- 루트 `docs/CODEMAPS/WORKSPACE.md`는 "youtube 디렉터리가 루트 체크아웃에
  기본으로 존재하지 않으니 `bun install` 전에 로컬에서 하이드레이션하라"고
  명시적으로 경고하고 있어, 이 프로젝트는 지금까지 idea 백로그에서 완전히
  누락되어 있었다.

## Open ideas

### 2026-09-07 - 워크스페이스 하이드레이션 부트스트랩 가드

Status: proposed

Why now: `youtube`는 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
`youtube/videos/*` glob)와 uv 워크스페이스 멤버로 선언되어 있지만, 디렉터리가
로컬에 없으면 glob이 조용히 아무것도 매칭하지 않아 `bun install`/`uv sync`가
겉보기엔 성공한 채로 `youtube` 하위 패키지만 빠질 수 있다.

First slice: 루트 부트스트랩 스크립트에 `youtube/` 존재 여부와 예상 하위
패키지(`remotion`, `services/*`, `videos/*`) 매칭 개수를 확인하는 사전 점검을
추가하고, 하이드레이션이 안 된 상태에서 설치가 실행되면 경고 또는 실패로
드러나게 한다.

### 2026-09-07 - Bun catalog / uv constraint 정합성 점검 확장

Status: proposed

Why now: 루트 `dependencies.md`는 Bun catalog와 uv `constraint-dependencies`를
`rich`와 `youtube` 양쪽에 적용한다고 문서화하지만, 실제 검증 스크립트
(`scripts/verify-python-dependency-constraints.py`)가 `youtube`의 로컬 선언까지
비교하는지는 코드맵만으로 확인되지 않는다. `rich`는 이미 이 계약을 반복 검증
경로로 갖고 있지만 `youtube`는 대칭적인 점검이 문서화되어 있지 않다.

First slice: `youtube`가 하이드레이션된 상태에서 constraint 검증 스크립트를
실행해 `youtube`의 Python 의존성 선언이 루트 constraint 범위와 실제로
정렬되는지 확인하고, 어긋나는 패키지가 있으면 루트 constraint 문서와 함께
정리한다.
