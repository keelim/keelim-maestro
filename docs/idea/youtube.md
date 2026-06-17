# youtube 아이디어 백로그

<!-- 마지막 검토: 2026-06-17 -->
<!-- 열린 아이디어: 1 -->

**저장소:** 프라이빗 (원격 미설정)  
**유형:** 자율 자식 저장소  
**현재 상태:** 로컬 체크아웃만 존재 · 업스트림 없음

---

## YT-001 프라이빗 원격 저장소 설정 및 워킹트리 정리

**우선순위:** 보통  
**근거:** `docs/CODEMAPS/SUBMODULES.md`에서 `youtube`: "Private local checkout; not a submodule" 확인.
`docs/CODEMAPS/WORKSPACE.md`에 따르면 Bun 워크스페이스(`youtube/remotion`, `youtube/services/*`, `youtube/videos/*`)와 uv 워크스페이스(`easy-release-note` 패키지) 모두 `youtube`를 멤버로 포함하는데, 원격이 없어 재현 가능한 클론·CI·협업이 불가능한 운영 리스크가 존재한다.
또한 n8n 워크플로우가 로컬 K8s에만 존재해 유실 시 복구 수단이 없다.

**행동 항목:**
1. 프라이빗 GitHub 원격 저장소 생성
2. 현재 워킹트리 클린 여부 확인 후 첫 푸시 및 업스트림 추적 설정
3. n8n 워크플로우 JSON 내보내기 후 저장소 내 버전 관리
4. 안정화 후 `.gitmodules` 추가 여부 검토 (전제: 원격 확보 + 워킹트리 클린)
5. `bun run automation:local -- verify youtube` 검증 명령 문서화

**연관 시스템:** 루트 자동화 스택(`bun run automation:local -- start n8n`)
