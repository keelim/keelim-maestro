# youtube

Last reviewed: 2026-08-19 KST

## Signals

- YouTube Shorts와 Easy Release Note 제작 자동화를 담당하는 비공개 자율
  저장소로, TypeScript(Remotion 렌더러·services)와 Python(uv 워크스페이스의
  `easy-release-note` 패키지)이 함께 쓰인다.
- 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 루트 uv 워크스페이스 양쪽의 활성 멤버지만, `youtube/`
  디렉터리는 루트 체크아웃에 기본적으로 존재하지 않아 로컬 하이드레이션이
  선행되어야 `bun install`/uv 명령이 정상 동작한다.
- `services/*`, `videos/*`는 glob 패턴 워크스페이스 멤버라서 패키지 수가
  늘어날수록 루트 Bun catalog·uv `constraint-dependencies`와의 정합성이
  개별적으로 조용히 벌어질 수 있다.
- 다른 자율 저장소(all, all-web-ui, rich 등)와 달리 지금까지 root idea
  backlog에 프로젝트 파일이 없어 커버리지 공백이었다.

## Open ideas

### 2026-08-19 - 워크스페이스 하이드레이션 가드

Status: proposed

Why now: `docs/CODEMAPS/WORKSPACE.md`에 따르면 youtube는 Bun/uv 워크스페이스
활성 멤버이지만 루트 체크아웃에 기본 하이드레이션되어 있지 않아서, 디렉터리가
없는 상태로 `bun install`이나 uv 명령을 실행하면 실패 원인이 바로 드러나지
않는다.

First slice: `./scripts/update-subrepos.sh status` 또는 `bun run test`
(root contract verifier)에 youtube 디렉터리 부재를 사전 감지해 하이드레이션
안내 메시지를 띄우는 검사를 추가한다.

### 2026-08-19 - services/videos 카탈로그 정합성 리포트

Status: proposed

Why now: `youtube/services/*`와 `youtube/videos/*`는 glob 워크스페이스
멤버로 계속 늘어나는 구조라서, 개별 패키지의 의존성 선언이 루트 Bun
catalog·uv constraint-dependencies와 조용히 어긋날 위험이 있다.

First slice: 각 하위 패키지의 `package.json`/`pyproject.toml` 의존성 선언을
루트 catalog·constraint 목록과 비교해 드리프트를 표로 보여주는 리포트를
`bun run report:*` 계열 스크립트로 추가한다.

### 2026-08-19 - 렌더링 파이프라인 스모크 게이트

Status: proposed

Why now: Remotion 렌더러(TypeScript)와 자동화 services(Python 포함)가 함께
동작하는 혼합 파이프라인은 한쪽만 검증해서는 실제 산출물 회귀를 놓치기
쉽다.

First slice: 최소 입력으로 스크립트 생성 → 렌더 → 산출물 검증까지 파이프라인
전체를 한 번 실행해 실패 지점을 표시하는 스모크 테스트를 추가하고, 로컬
자동화 인덱스(`bun run automation:local`)에서 호출 가능하게 연결한다.
