# youtube

Last reviewed: 2026-09-25 KST

## Signals

- TypeScript + Python 혼합 자동화 워크스페이스로, YouTube Shorts 제작과 Easy
  Release Note 생산을 함께 다룬다.
- Remotion 렌더러(`youtube/remotion`), 서비스 자동화(`youtube/services/*`),
  영상별 프로젝트(`youtube/videos/*`)가 각각 루트 Bun 워크스페이스 glob
  멤버로 등록되어 있다.
- Python 쪽은 루트 uv 워크스페이스의 `easy-release-note` 패키지로 참여하며,
  루트 `constraint-dependencies`와 정렬을 유지해야 한다.
- 아직 서브모듈이 아닌 자율(autonomous) 저장소라서 루트 체크아웃에는 기본적으로
  존재하지 않고 별도 hydration이 필요하다.
- 다른 child repo(all, all-web-ui, android-support, Keelim-Knowledge-Vault,
  keelim-plugin, keelim-vercel, rich, toto)와 달리
  `docs/CODEMAPS/projects/`에 전용 코드맵이 없어 근거 자료가 가장 얇다.

## Open ideas

### 2026-09-25 - 렌더러·서비스·릴리즈 노트 파이프라인 상태판

Status: proposed

Why now: `youtube/remotion`, `youtube/services/*`, `youtube/videos/*`가 각각
별도 Bun 워크스페이스 패키지로 쪼개져 있고 `easy-release-note`는 uv
워크스페이스로 따로 관리되어, 영상 렌더링과 자동화 서비스와 릴리즈 노트
생성이 서로 다른 실행 흐름에서 조용히 어긋나기 쉽다.

First slice: 각 video 프로젝트의 렌더 상태, 연결된 service 실행 로그,
easy-release-note 산출물을 한 번에 모아 어떤 영상이 어느 단계에서 막혔는지
보여주는 요약 리포트를 만든다.

### 2026-09-25 - youtube 코드맵 스냅샷 생성

Status: proposed

Why now: `docs/CODEMAPS/projects/`에는 all, all-web-ui, android-support,
Keelim-Knowledge-Vault, keelim-plugin, keelim-vercel, rich, toto의 코드맵은
있지만, 실제로 활성 Bun+uv 워크스페이스 멤버인 youtube만 빠져 있어서 다음
idea gardener나 리뷰 작업이 이 프로젝트를 근거 없이 판단하게 된다.

First slice: 다른 child repo와 같은 코드맵 생성 절차를 youtube에도 실행해
`docs/CODEMAPS/projects/youtube.md`를 만들고, architecture/backend/frontend
코드맵에서 상호 참조를 잇는다.
