# youtube

Last reviewed: 2026-08-30 KST

## Signals

- YouTube Shorts 제작과 Easy Release Note 생산 자동화를 함께 담당하는 private 자율
  저장소로, root Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 root uv 워크스페이스(`youtube` = `easy-release-note`
  패키지, Python >=3.13) 양쪽에 동시에 등록돼 있다.
- 신규 root 체크아웃에는 물리적으로 존재하지 않아서, `bun install`이나 uv 워크스페이스
  명령 전에 로컬 hydration이 선행돼야 한다는 점이 `WORKSPACE.md`/`architecture.md`
  코드맵에 명시돼 있다.
- root Bun catalog(`dependencies.md`)와 uv `constraint-dependencies`는 프론트엔드·
  파이썬 공용 버전을 고정하고, `rich`/프론트엔드 소비자에게는 이미
  `bun run report:shared-ui`, `verify-python-dependency-constraints.py` 같은 검증
  표면이 있지만, youtube 하위 세 workspace 영역이 실제로 같은 catalog/constraint를
  참조하는지는 root 코드맵에서 드러나지 않는다.
- `rich`(dirty/ahead), `all-web-ui`(submodule 전환 대기), 과거 `toto`(gitlink 미커밋)
  사례에서 반복된 패턴과 마찬가지로, "root 워크스페이스에는 멤버로 선언돼 있지만
  로컬에 없다"는 비대칭이 youtube에도 그대로 존재한다.

## Open ideas

### 2026-08-30 - 워크스페이스 hydration 사전 점검

Status: proposed

Why now: youtube는 Bun과 uv 워크스페이스 멤버로 등록돼 있지만 신규/정리된
체크아웃에는 디렉터리 자체가 없어서, `bun install`이나 `uv lock --check`가 조용히
해당 패키지를 건너뛰거나 알기 어려운 에러로 실패할 수 있다. `./scripts/update-subrepos.sh`가
이미 자율 저장소 hydration 상태를 보고하는 패턴을 갖고 있어 같은 방식을 설치
직전 점검으로 확장하기 좋다.

First slice: 워크스페이스 설치/락 명령 실행 전에 `youtube/remotion`,
`youtube/services`, `youtube/videos`, uv `youtube` 패키지 경로의 존재 여부를
확인하고, 없으면 hydration 안내 메시지로 먼저 실패시키는 프리플라이트 체크를
추가한다.

### 2026-08-30 - youtube 워크스페이스 카탈로그 정합 리포트

Status: proposed

Why now: root Bun catalog와 uv constraint-dependencies는 `rich`와 프론트엔드
소비자 쪽에는 이미 정합성 리포트가 있지만, youtube의 세 workspace 영역
(`remotion`, `services/*`, `videos/*`)이 같은 catalog/constraint를 실제로
참조하는지는 root 문서에서 확인되지 않아 버전 표류를 조기에 잡을 방법이 없다.

First slice: youtube가 로컬에 hydrate된 상태에서 각 하위 패키지의 의존성 선언을
root catalog/constraint와 비교하는 가벼운 리포트를 만들어, `bun run
report:shared-ui`와 같은 결로 표류한 버전을 표면화한다.
