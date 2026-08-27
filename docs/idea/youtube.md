# youtube

Last reviewed: 2026-08-27 KST

## Signals

- `youtube`는 root Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 root uv 워크스페이스(`youtube` 멤버, Python
  `>=3.13`) 양쪽에 동시에 걸쳐 있는 활성 자율 저장소다.
- Fresh root checkout에는 `youtube/` 디렉터리가 기본으로 없어 hydrate가
  필요하고, README에 operator-approved clone 경로가 이미 문서화돼 있다.
- `docs/CODEMAPS/projects/`에는 `all-web-ui.md`·`rich.md` 스냅샷이 있지만
  `youtube.md`는 아직 없어서, 활성 워크스페이스 멤버인데도 구조 파악이
  매번 새로 시작된다.
- root `package.json`의 `typecheck:web`/`build:web`/`test:web`은
  `all-web-ui`·`keelim-vercel`·`rich-admin-web`만 묶고 있어, 같은 Bun
  워크스페이스 멤버인 `youtube/remotion`·`youtube/services/*`·
  `youtube/videos/*`는 root 검증 경로에서 빠져 있다.
- README는 `youtube/videos/*` glob이 새 video 폴더가 추가될 때마다 root
  `bun.lock`을 바꿀 수 있다고 이미 경고하지만, 그 변화가 의도된 것인지
  리뷰에서 확인하는 절차는 없다.

## Open ideas

### 2026-08-27 - youtube 코드맵 스냅샷 생성

Status: proposed

Why now: `docs/CODEMAPS/projects/README.md`의 "Generated Snapshots" 표에는
`all-web-ui`·`rich`가 이미 올라 있지만 `youtube`만 빠져 있어서, 활성
워크스페이스 멤버인데도 구조·엔트리포인트 파악이 항상 처음부터 다시
시작된다.

First slice: `youtube`를 로컬에 hydrate한 뒤 `python3
scripts/refresh-codemaps.py`를 실행해 `docs/CODEMAPS/projects/youtube.md`를
생성하고, `projects/README.md`의 스냅샷 표와 재생성 커맨드 목록에 반영한다.

### 2026-08-27 - root 검증 스크립트에 youtube 워크스페이스 포함

Status: proposed

Why now: `typecheck:web`/`build:web`/`test:web`이 `all-web-ui`·
`keelim-vercel`·`rich-admin-web`만 다뤄서, 같은 Bun workspace 멤버인
`youtube/remotion`·`youtube/services/*`·`youtube/videos/*`는 root에서
타입 오류나 빌드 깨짐을 감지할 방법이 전혀 없다.

First slice: `bun run --filter` 기반으로 youtube 패키지들을 도는
`typecheck:youtube`/`build:youtube` 스크립트를 추가하고, hydrate된 상태에서
로컬 점검 경로(및 가능하면 CI)에 연결한다.

### 2026-08-27 - videos 글롭 변경 시 lockfile 리뷰 게이트

Status: proposed

Why now: README는 이미 `youtube/videos/*` glob이 새 video 폴더 추가 시
root `bun.lock`을 바꿀 수 있다고 명시하지만, 그 변경이 의도된 추가인지
확인하는 절차는 아직 없어 우발적인 lockfile drift를 놓치기 쉽다.

First slice: PR에서 `youtube/videos/*` 신규 패키지 추가와 `bun.lock` diff가
함께 있는지 확인하는 가벼운 체크(스크립트 또는 리뷰 체크리스트 항목)를
root 검증 경로에 추가한다.
