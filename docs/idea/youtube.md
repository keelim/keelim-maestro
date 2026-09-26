# youtube

Last reviewed: 2026-09-26 KST

## Signals

- `youtube`는 원격 저장소가 있는 private autonomous child repo이며, root Bun
  워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와
  root uv 워크스페이스(`easy-release-note` 패키지) 양쪽에 동시에 걸려 있다.
- `docs/CODEMAPS/WORKSPACE.md`는 "youtube는 Bun 워크스페이스 멤버지만 디렉터리가
  기본 루트 체크아웃에는 없다"고 이미 명시하고 있어서, 워크스페이스 glob과 uv
  workspace member 선언이 하이드레이션 없이도 조용히 빈 상태로 풀릴 위험이
  root 코드맵 자체에 기록돼 있다.
- Remotion 렌더러, services(자동화 서비스), videos(영상별 프로젝트) 세 표면이
  함께 움직이고, `bun run automation:local`이 별도로 n8n 기반 youtube 자동화를
  시작/중지한다.
- `youtube/simple`은 자체 lockfile과 호환 범위를 가진 별도 Python 프로젝트로,
  명시적 승격 전까지 root uv workspace 밖에 유지해야 한다.
- 지금까지 `docs/idea/`에 `youtube` 전용 파일이 없어, root 코드맵·`AGENTS.md`
  정책과 idea backlog 사이에 커버리지 공백이 있었다.

## Open ideas

### 2026-09-26 - 워크스페이스 하이드레이션 프리플라이트

Status: proposed

Why now: `docs/CODEMAPS/WORKSPACE.md`에 이미 "youtube 디렉터리가 기본 체크아웃에는
없다"고 적혀 있고, root `package.json`의 `youtube/remotion`·`youtube/services/*`·
`youtube/videos/*` glob과 root `pyproject.toml`의 uv workspace member(`rich`,
`youtube`)는 디렉터리가 없어도 에러 없이 조용히 빈 목록으로 풀리기 때문에,
`bun install`이나 `uv lock --check`가 겉보기엔 성공해도 실제로는 일부
워크스페이스 멤버가 통째로 빠진 채 넘어갈 위험이 있다.

First slice: `bun install` 또는 `uv lock --check` 실행 전에 root
`package.json`의 workspaces 배열과 `pyproject.toml`의 uv workspace members에
선언된 경로별로 실제 디렉터리·`.git` 존재 여부를 확인하고, 빠진 멤버가 있으면
하이드레이션 안내(`git clone https://github.com/keelim/youtube.git youtube` 등)와
함께 경고를 내는 프리플라이트 스크립트를 `scripts/`에 추가한다.

### 2026-09-26 - youtube 자동화 파이프라인 상태 콘솔

Status: proposed

Why now: `youtube`는 Remotion 렌더러, services(자동화 서비스), videos(영상별
프로젝트) 세 갈래로 나뉘어 있고, `automation:local` 헬퍼가 n8n 기반 youtube
자동화를 별도로 관리한다고 문서화돼 있지만, rendering/services/n8n 세 표면의
상태를 한 곳에서 보여주는 뷰는 아직 없어서 실패나 정체를 놓치기 쉽다.

First slice: `youtube/remotion`, `youtube/services/*`, `youtube/videos/*` 각각의
마지막 실행·렌더 상태와 `automation:local` n8n 워크플로 상태를 모아 보여주는
얇은 상태 리포트를 `bun run automation:local` 하위 명령으로 추가한다.

### 2026-09-26 - 루트-child 의존성 정렬 감사 (easy-release-note)

Status: proposed

Why now: 루트 `CLAUDE.md`는 `youtube`가 root uv workspace에 `easy-release-note`
패키지로 참여하며 "child-local dependency declarations aligned with root
constraints" 유지가 필요하다고 명시하지만, `scripts/verify-python-dependency-constraints.py`가
`youtube`(및 별도 취급해야 하는 `youtube/simple`)까지 실제로 비교 범위에
포함하는지는 아직 검증된 적이 없다.

First slice: `uv run python scripts/verify-python-dependency-constraints.py`
실행 결과에 `easy-release-note` 패키지의 의존성 선언이 실제로 검사되는지,
`youtube/simple`이 의도대로 제외되는지 확인하고, 빠져 있다면 child
`pyproject.toml` 선언과 루트 `tool.uv.constraint-dependencies`를 비교하는 항목을
추가한다.
