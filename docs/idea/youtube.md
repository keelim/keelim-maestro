# youtube

Last reviewed: 2026-09-08 KST

## Signals

- 루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`,
  `youtube/videos/*`)와 루트 uv 워크스페이스(`easy-release-note` 패키지)의
  활성 멤버로, Remotion 기반 렌더러와 자동화 서비스, 영상별 프로젝트 패키지로
  구성돼 있다.
- 로컬 미체크아웃 사설 저장소라 지금까지 `docs/idea/`에 전용 파일이 없었고,
  이번이 첫 등록이다.
- 반복적으로 관찰된 운영 리스크: 발행 공백(퍼블리시 갭), 에피소드 폴더가
  뒤섞인 대량 dirty 배치로 인한 안전하지 않은 자동 커밋, 렌더러가 같은
  골격을 재사용해 콘텐츠가 비슷해 보이는 문제.
- YouTube Studio와 Naver Clip처럼 플랫폼마다 게시 상태(업로드/검수/공개
  범위/임시저장)를 따로 추적해야 조용한 발행 실패를 피할 수 있었다.

## Open ideas

### 2026-09-08 - 퍼블리시 루프 복구 대시보드

Status: proposed

Why now: 최근 채널 감사에서 13일 발행 공백, 거의 무음에 가까운 렌더 결과,
완료되지 않은 human/critic 승인 게이트가 함께 발견됐고, 결론은 "새 제작
도구가 아니라 발행 루프 회복이 우선"이었다.

First slice: `lastPublishedAt`, `gapDays`, `nextCandidate`, `blockingAsset`,
`humanApprovalStatus`를 한 화면에 모아 다음에 무엇을 발행해야 하는지 바로
보여주는 얇은 대시보드를 만든다.

### 2026-09-08 - 에피소드 단위 커밋/정리 그룹퍼

Status: proposed

Why now: `youtube`의 dirty tree는 다수의 에피소드 폴더, 대량 tracked
deletion, 미디어·썸네일·매니페스트가 뒤섞여 있어 자동 커밋이 안전하지
않다는 평가가 여러 세션에 걸쳐 반복됐다.

First slice: `youtube/videos/*`와 `youtube/services/*`를 에피소드 슬러그
단위로 스캔해 `sourcePackage`/`renderArtifact`/`thumbnail`/`audio`/
`staleDeletion`/`needsHumanGrouping`으로 분류하는 스크립트를 추가한다.

### 2026-09-08 - 컨셉 선택 게이트와 플랫폼별 게시 상태 체크리스트

Status: proposed

Why now: 렌더러가 같은 골격을 반복 사용해 콘텐츠가 비슷해 보인다는 지적
이후 소스 스캐너/워크플로우 데스크/제품 스포트라이트/임팩트 레이더 중
하나를 렌더 전에 고르는 방식으로 품질이 개선된 사례가 있고, YouTube
Studio와 Naver Clip 업로드도 서로 다른 게시 상태 필드를 따로 추적해야
조용한 발행 실패를 막을 수 있었다.

First slice: 영상별로 선택된 컨셉과 그 컨셉이 실제로 바꾼 구조(렌더러/
모션/레이아웃 등), 그리고 플랫폼별 게시 상태(`uploaded-private`,
`checks`, `visibility`, `draft-saved`)를 함께 기록하는 얇은 매니페스트를
추가한다.
