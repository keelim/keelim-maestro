# `youtube` 아이디어 백로그

<!-- 마지막 검토: 2026-06-19 | 열린 아이디어: 1 -->

**유형:** 프라이빗 자율 저장소 (서브모듈 아님)
**스택:** TypeScript + Remotion / Python (easy-release-note) / n8n (Kubernetes)
**코드맵 출처:** `docs/CODEMAPS/backend.md`, `docs/CODEMAPS/SUBMODULES.md`
**현재 상태:** 원격 없음, `docs/CODEMAPS/projects/` 코드맵 스텁 누락

---

## 열린 아이디어

### YT-01: 프라이빗 원격 저장소 생성 및 clean 상태 확보로 서브모듈 등록 선행 조건 해소

**근거:** `docs/CODEMAPS/SUBMODULES.md` — "youtube: private (no upstream yet) — Private local checkout; not a submodule"
**유형:** 운영 리스크 감소
**우선순위:** 높음

`youtube` 저장소는 원격이 없어 서브모듈로 등록할 수 없고 새 환경 온보딩 시 수동 복구가 필요하다.
루트 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(`easy-release-note`)가 이 경로에 의존하므로, 원격 없이는 CI 재현성을 보장할 수 없다.

**실행 단계:**
1. GitHub 에 프라이빗 원격 저장소 생성 (`github.com/keelim/youtube`)
2. 로컬 커밋을 원격으로 푸시하여 clean 상태 확인
3. `./scripts/update-subrepos.sh status` 로 원격 동기화 상태 검증
4. `docs/CODEMAPS/SUBMODULES.md` 원격 URL 및 브랜치 정보 업데이트
5. `docs/CODEMAPS/projects/` 에 `youtube.md` 코드맵 추가
6. `rich` 블로커 해소(RICH-01) 후 서브모듈 고정 진행

**차단 조건:** rich 더티 상태 해소(RICH-01) 선행 권장
**해제 후 효과:** youtube 코드맵 수화 자동화, n8n 워크플로우 원격 백업, CI 재현성 확보
