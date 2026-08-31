# youtube

Last reviewed: 2026-08-31 KST

## Signals

- YouTube Shorts / Easy Release Note 제작을 담당하는 private 자율 저장소로,
  루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 루트 uv 워크스페이스(`easy-release-note` 패키지)에
  동시에 편입돼 있다.
- `youtube/videos/*`는 신규 영상마다 패키지가 하나씩 늘어나는 반복형
  프로덕션 워크플로우이고, `youtube/services/*`도 같은 glob 패턴으로
  자동화 서비스가 추가된다.
- `youtube/simple`은 자체 lockfile과 호환 범위를 갖고 있어 의도적으로 루트
  uv 워크스페이스 밖에 남아 있는 예외 케이스다.
- `docs/CODEMAPS/WORKSPACE.md`는 이미 "youtube는 Bun 워크스페이스 멤버이지만
  기본 루트 체크아웃에는 디렉터리가 없을 수 있다"는 하이드레이션 비대칭을
  프로즈로만 남겨 두고 있다 (`rich`, `all-web-ui`와 같은 성격의 위험).
- 루트에는 아직 `docs/idea/youtube.md`가 없어 다른 프로젝트 대비 아이디어
  커버리지 공백이 있었다.

## Open ideas

### 2026-08-31 - 신규 video/service 패키지 온보딩 체크리스트

Status: proposed

Why now: `youtube/videos/*`와 `youtube/services/*`는 glob 기반 Bun 워크스페이스
멤버라서 새 영상·서비스 패키지가 추가될 때마다 자동으로 워크스페이스에
편입되지만, 그 패키지가 루트 Bun 카탈로그(`package.json` catalog) 및 루트 uv
constraint-dependencies와 정합한지 확인하는 절차는 문서화돼 있지 않다.
`youtube/simple`처럼 의도적으로 워크스페이스 밖에 남아야 하는 예외도 있어
혼동 위험이 크다.

First slice: 새 `youtube/videos/<name>` 또는 `youtube/services/<name>` 패키지의
`package.json` / `pyproject.toml`을 루트 카탈로그·constraint 핀과 비교하는
짧은 체크리스트(또는 기존 `scripts/verify-python-dependency-constraints.py`와
같은 패턴의 검증 스크립트)를 정의하고, `youtube/simple`류 의도적 예외는
allowlist로 명시한다.

### 2026-08-31 - 워크스페이스 미하이드레이션 상태 가시화

Status: proposed

Why now: `docs/CODEMAPS/WORKSPACE.md`가 이미 "youtube 디렉터리가 기본 루트
체크아웃에 없을 수 있다"고 프로즈로 경고하지만, `rich`·`all-web-ui`와 달리
`./scripts/update-subrepos.sh status`나 `bun run report:baseline` 같은
운영 helper의 실제 출력에는 이 상태가 별도 행으로 나타나지 않는다. 문서와
운영 도구 출력이 어긋나면 신규 클론 직후 `bun install`이 조용히 일부
워크스페이스 멤버를 건너뛰는 원인을 늦게 알아차리게 된다.

First slice: `./scripts/update-subrepos.sh status`(또는 `report:baseline`)
출력에 `youtube` 하이드레이션 여부를 `all-web-ui`/`rich`와 동일한 형식의
행으로 추가해, 문서에만 있던 경고를 실제 상태 점검 경로로 옮긴다.
