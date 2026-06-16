# 아이디어 — android-support

<!-- 마지막 검토: 2026-06-16 -->

프로젝트: `android-support`  
스택: Android / Kotlin — 공유 지원 라이브러리  
현재 버전: `v0.0.8-4` (태그 고정)  
상태: 서브모듈 (detached, 핀 `485a2e40`, 로컬 업스트림 없음)  
오픈 아이디어: 2

---

## 열린 아이디어

### [ASUP-001] v0.0.8-4 이후 업스트림 추적 재개 방안 수립

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 운영 위험 감소 / 워크플로우 통합
- **근거:** `docs/CODEMAPS/SUBMODULES.md`. `android-support`가 "detached clean at pinned commit `485a2e40`; no local upstream"으로 명시. 현재 `main` 브랜치를 추적하지 않는 detached HEAD 상태.

새 버전(`v0.0.9` 이상)이 `android-support` 업스트림에 릴리스될 때 루트가 이를 인지하는 방법이 없다. `update-subrepos.sh`도 로컬 업스트림이 없어 업데이트를 건너뛸 가능성이 있다. `git submodule set-branch --branch main android-support`로 브랜치를 복원하고, 이후 `update-subrepos.sh`가 정상 동작하는지 확인한다. 새 릴리스 시 `all` 앱에서 의존성 업그레이드가 필요한지도 함께 검토한다.

---

### [ASUP-002] `all` 앱에서 `android-support` 실제 사용 여부 검증

- **상태:** 열림
- **우선순위:** P3
- **카테고리:** 문서화 / 운영 위험 감소
- **근거:** `docs/CODEMAPS/architecture.md`. `android-support`가 "`all` 앱 의존 공유 지원 라이브러리"로 설명되지만, 루트 코드맵에 구체적인 의존 관계가 없음.

`android-support`가 `all` 앱에서 실제로 Gradle 의존성으로 선언되어 있는지, 아니면 역할이 변경되어 사용 안 할 가능성이 있는지 확인해야 한다. 사용 여부에 따라 서브모듈 핀 갱신의 우선순위(ASUP-001)가 달라진다. `all` 서브모듈 체크아웃 후 `build.gradle.kts` 파일에서 `android-support` 의존성 선언을 검색한다.

---

## 닫힌 아이디어

_없음_
