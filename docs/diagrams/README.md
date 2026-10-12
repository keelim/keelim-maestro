# keelim-maestro 구조도

산출물: `project-structure.svg` (1680 × 1600, 독립형 SVG)와 `project-structure.png` (3360 × 3200, 원본 SVG의 2배 해상도 렌더링).

2026-10-12 로컬 working tree를 읽기 전용으로 조사한 전체 구조도다. root 문서 소유자는 `keelim-maestro`이며 자식 소스·설정·Git 인덱스는 수정하지 않았다. 변경 중인 작업을 포함한 시점의 스냅샷이므로 커밋에 고정된 구조라고 해석하지 않는다.

## 표시 규칙

- 박스와 내부 목록: 디렉터리 소속 또는 명시적 빌드 등록. 모듈 간 호출/의존성은 뜻하지 않는다.
- G: `.gitmodules`와 root Git index mode `160000`에서 함께 확인한 submodule 4개.
- B: root `package.json`의 Bun workspace 선언. `youtube/videos/*` 같은 패턴은 선언 자체이며 모든 로컬 폴더에 package manifest가 있거나 Git 추적 중이라는 뜻은 아니다.
- U: root `pyproject.toml`의 uv workspace 선언. root는 `package = false`.
- 보라색 화살표: `all-web-ui` 패키지에서 두 소비자로 향하는 공급 방향. 두 소비자의 manifest와 실제 import를 함께 확인했다. 로컬 링크 해석, 배포 또는 런타임 검증 결과는 포함하지 않는다.

`all-web-ui`, `rich`, `youtube`, `tools`는 별도 로컬 Git checkout이며 root submodule과 구분했다. 캐시·보고서·임시 운영 상태는 제외했다. `android-support`, `quant`, `toto` 및 `tools/agentgateway`는 조사 시점에 없었다. `all/feature/ui-auth`, `all/feature/ui-labs` 폴더도 보였지만 `settings.gradle.kts`에 등록되지 않았으므로 11개 등록 feature 수에 포함하지 않았다.

## 소스 근거

| 내용 | 확인한 파일/명령 |
| --- | --- |
| 소유권과 문서 작업 규칙 | `AGENTS.md`, `docs/standards.md`, `docs/engineering-notes.md`, `docs/PROJECT.md`, `.agents/skills/*/AGENTS.md` |
| root 구성과 helper 위임 | root `package.json` scripts, `docs/architecture.md` |
| Bun 선언 | root `package.json`의 `workspaces` 배열 |
| uv 선언 | root `pyproject.toml`의 `[tool.uv]`, `[tool.uv.workspace]` |
| submodule 등록 | `.gitmodules`, `git ls-files --stage`의 mode `160000` 4개 |
| all 모듈 | `all/settings.gradle.kts`의 `include(...)` 37개와 `includeBuild("build-logic")`; 실제 `all/core/*`, `all/feature/*`, `all/app-*` 경로 |
| all 기타 빌드 단위 | `all/docs/package.json`, `all/all-rust-lib/Cargo.toml`, `all/allIos/all.xcodeproj` |
| 공유 UI 공급자 | `all-web-ui/package.json`의 이름, 버전, exports |
| keelim-vercel 소비 | `keelim-vercel/package.json`, `keelim-vercel/app/layout.tsx:1`, `keelim-vercel/components/shared/all-web-ui-adapters.tsx:3` |
| rich/web 소비 | `rich/web/package.json`, `rich/web/src/app/error.tsx:3`, `rich/web/src/features/admin/components/todo-panel.tsx:3` |
| Rich 단위 | `rich/pyproject.toml`, `rich/app/main.py`, `rich/web/package.json`, `rich/symphony/mix.exs`, `rich/supabase/functions/*/deno.json`, 실제 `rich/open-trading-api/` |
| YouTube 단위 | `youtube/pyproject.toml`의 `ern` entry point, `youtube/remotion/package.json`, `youtube/services/*/package.json`, `youtube/ops/n8n-k8s/` |
| Tools 단위 | `tools/.git`, `tools/crawler/.git`, `tools/crawler/pyproject.toml`, `tools/crawler/web/package.json`, 실제 디렉터리 목록 |
| 플러그인과 지식 저장소 | 실제 `keelim-plugin/skills/*/SKILL.md`, vault 디렉터리, 해당 Git submodule 등록 |

## Anatomy 사용 범위와 한계

설치된 root `node_modules/anatomy-figures`는 버전 `0.1.0`이다. 로컬 `README.md`, `package.json`, `dist/types.d.ts`와 `dist/themes.js`를 읽었다. README가 제공하는 사용법은 React component import와 custom element 등록이며, package에 `bin` 또는 범용 프로젝트 구조 SVG 생성 API는 없다.

root `.agents/skills`, `.claude`, 사용자 `~/.agents/skills`, `~/.codex/skills` 및 플러그인 cache에서 `/anatomy` 명령 또는 Anatomy `SKILL.md`를 찾지 못했다. 사용자 `~/.claude` 디렉터리는 존재하지 않았다. 다른 위치의 설치까지 없다고 단정하지 않는다.

따라서 이 산출물은 **설치된 anatomy-figures의 `paper` 테마 토큰을 읽어 적용한 맞춤 정적 SVG**다. `/anatomy figures` 명령이 실행된 결과나 기존 패키지 figure component를 렌더링한 결과로 주장하지 않는다. 외부 코드 설치·다운로드·실행은 하지 않았다. 정확한 slash command 방식의 사용은 해당 스킬/명령 위치가 확인되지 않아 남아 있는 제한이다.

## 검증

- Python XML parser: SVG parse 성공.
- 설치된 Playwright/Chromium으로 로컬 SVG 렌더링 및 PNG 캡처 성공, 이미지 시각 확인 완료.
- SVG `getBBox()` 기반 text 검사: 98개 text, 캔버스 밖 0개, text끼리 겹침 0개, 카드 경계 잘림 0개.
- root `git diff --check` 성공. normal/submodule-aware status를 확인했고 기존 dirty 상태는 보존했다.
- 최초 저장 시 `docs/diagrams/`는 기존 `.gitignore`의 `/docs/*` 규칙으로 ignored였다. 후속 요청에 따라 root `.gitignore`에 이 디렉터리와 `project-structure.svg`, `project-structure.png`, `README.md` 세 파일만 허용하는 예외를 추가했다. 세 파일에는 intent-to-add를 적용해 일반 `git diff`로 내용을 검토할 수 있게 했다. 이는 파일 내용을 staged commit에 올린 상태가 아니다.

이 작업은 원본 SVG, PNG와 이 근거 문서를 추가하고 요청에 따라 root `.gitignore`에 세 파일만 허용하는 예외를 추가한다. commit/push/배포는 수행하지 않았다.

## PR #2236 작업 결과 대조 (2026-10-12 추가 확인)

원래 구조도는 로컬 working tree 조사 결과이며, 생성 시점에 PR 종료 상태나 특정 최종 커밋을 기준으로 고정한 그림은 아니었다. 따라서 원래 완료 답변만으로 “PR #2236의 변경과 빌드 검증까지 모두 포함했다”고 해석하면 범위를 넘는다. 후속 질문에 따라 아래를 읽기 전용으로 대조하고 SVG metadata와 하단 주석을 최신화했다.

- 최종 커밋: `9abc1918a866573927b26be5d46ed0f20b21187f` (`chore: align main and develop on the verified Android tree`). 로컬 `origin/main`, `origin/develop` 추적 ref가 모두 이 커밋을 가리켰다. fetch나 branch 변경은 하지 않았다. 현재 로컬 `develop` checkout HEAD는 `317ca443291788f45dd1b21af161e293969c8c2e`로 별개이며, 원래 그림도 최종 branch 전체를 checkout해서 작성한 것은 아니다.
- 호환성 수정 커밋: `fb1dc777adf2b318f0ccb5b31a06cd406df0503c`. 최종 커밋의 첫 번째 부모이며 두 커밋의 tree ID는 모두 `85695d54f2333bc5b5630d1996cee367cf709968`로 동일하다. 최종 정렬 커밋은 수정된 내용과 기존 main 이력을 통합한 결과다.
- `all/settings.gradle.kts` 현재 파일과 최종 커밋 파일은 byte-for-byte 동일했다. 등록된 37개 모듈(7 apps, 15 core, 11 features, 기타 4개)과 `build-logic` included build가 같다. 최종 커밋에도 `docs/package.json`, `all-rust-lib/Cargo.toml`, `allIos/all.xcodeproj/project.pbxproj`가 존재한다.
- 호환성 수정은 compile SDK minor API 2, AppFunctions 버전, Firebase lite protobuf 제약, JSON/Compose BOM 의존성 및 기존 FileProvider·Kotest·Maps·Compose 호출 수정 등 15개 파일이다. **빌드 설정만 바뀐 것은 아니지만**, 등록 모듈 추가/삭제나 구조도 수준의 소속 변화는 없다. 내부 클래스나 외부 라이브러리 의존성은 이 전체 구조도의 표현 범위 밖이다.
- GitHub `gh pr view 2236 --repo keelim/all --json ...` 결과: [PR #2236 release/261003](https://github.com/keelim/all/pull/2236), `develop` → `main`, `state=CLOSED`, `closedAt=2026-10-12T08:51:31Z`, `mergedAt=null`, `mergeCommit=null`. **PR 자체가 merge된 것은 아니다.** 최종 branch 정렬 결과와 PR 종료 상태를 구분한다.

결론: **전체 프로젝트 구조는 PR #2236 처리 후 최종 all 트리와 일치한다.** 모듈 배치를 바꿀 누락은 없어 그림 배치는 유지했다. 이 구조도 작업에서는 Android 빌드·테스트를 다시 실행하지 않았으며, 수정 커밋 메시지의 APK/테스트 검증 기록을 독립 재검증한 것으로 주장하지 않는다. 수정된 SVG도 XML·브라우저 렌더링·텍스트 겹침/잘림을 재검증했다. Library 업로드는 수행하지 않았다.

## Git diff 가시성 수정

소유자는 root `keelim-maestro`다. `/docs/*` 규칙(수정 전 `.gitignore:39`)이 `docs/diagrams` 부모 디렉터리를 무시했기 때문에 untracked SVG가 status/diff에 나타나지 않았다. `!/docs/diagrams/`, `/docs/diagrams/*`, `!/docs/diagrams/project-structure.svg`, `!/docs/diagrams/project-structure.png`, `!/docs/diagrams/README.md`의 좁은 예외만 추가했다. 다른 docs와 diagram 파일은 계속 ignored다. 세 산출물은 `git add -N -- <세 경로>`로 intent-to-add 표시했으며 commit/push와 Library 업로드는 수행하지 않았다.

## PNG 내보내기

원본 SVG를 설치된 Playwright/Chromium으로 deviceScaleFactor=2에서 렌더링했다. 3360 × 3200 PNG이며 재생성 이미지나 도형 재해석이 아니다. SVG 원본과 동일한 내용이고 SVG를 함께 유지하므로 해상도와 무관한 확대/편집도 가능하다. XML parse, 브라우저 렌더링, 98개 텍스트의 겹침/캔버스 밖/카드 잘림 0건을 확인했다. PNG는 Git의 일반 diff에서 binary addition으로 표시되며 시각 검토는 이미지 뷰어로 한다.
