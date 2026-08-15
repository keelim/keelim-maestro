# Claude Code Project Guidelines - keelim-maestro

## RTK (Rust Token Killer)
Headroom proxy routing is disabled for this workspace; do not route API calls through `http://127.0.0.1:8787`.
- **MCP Server**: Headroom MCP may still be registered globally in `~/.claude.json` for Content-Compressed Retrieval (CCR), but it is not the API proxy.
- **RTK Command Wrapper**: When executing shell commands, **always prefix with `rtk`** (e.g. `rtk git status`, `rtk pytest`). This compresses terminal output by 60-90% before it reaches the model context.

### Common RTK commands:
- Git: `rtk git status`, `rtk git diff`, `rtk git log`
- Files/Search: `rtk ls <path>`, `rtk read <file>`, `rtk grep <pattern>`, `rtk find <pattern>`, `rtk diff <file>`
- Build/Lint/Test: `rtk tsc`, `rtk lint`, `rtk cargo build`, `rtk pytest`, `rtk ruff check`
- Package managers: `rtk pnpm install`, `rtk npm run <script>`, `rtk bun run <script>`

---

## Workspace Build & Test Commands
- **Test entire workspace**: `bun run test` or `bun run test:workspace`
- **CodeGraph dispatcher**: `bun run cg -- <args>` (e.g. `bun run cg -- context keelim-plugin "<task>"`)
- **Web Build & Test**: `bun run build:web` / `bun run test:web`
- **Start Web Dev Servers**: `bun run dev:keelim-vercel` / `bun run dev:rich-web`
- **Local Automation Stack**: `bun run automation:local -- <args>`

---

## Codex Headless Harness
- Treat `claude -p --model fable` calls from Codex as bounded headless runs. Codex remains the orchestrator unless the prompt explicitly delegates writes.
- Keep project auto-discovery enabled; do not use `--bare` for this harness because it skips `CLAUDE.md`, hooks, plugins, and MCP config.
- Return JSON-compatible content with `status`, `summary`, `next_actions`, and `artifacts`. For errors, include a root-cause hint, safe retry, and stop condition.
- Default to advice-only. Edit files only when the prompt says `delegated-write`, names the target paths, and stays inside the root or named child-repo boundary.
- If asked to coordinate with Codex, use the existing `bun run dev:codex-app-server` bridge only on explicit request. Otherwise answer the headless prompt and exit.
- Preserve local rules: no Headroom API proxy, use `rtk` for shell commands, route MCP through `agentgateway`, and keep child repos autonomous.

---

## 하네스: keelim-maestro 크로스 프로젝트 개발

**목표:** 도메인 리드 팀(android-lead, python-lead, web-lead, qa)으로 하위 프로젝트를 넘나드는 구현·검증을 조율한다.

**트리거:** 하위 프로젝트(all, all-web-ui, android-support, keelim-plugin, keelim-vercel, rich, toto, youtube)를 대상으로 한 구현/수정/리팩터링/리뷰 요청 시 `maestro-orchestrator` 스킬을 사용하라. 단순 질문은 직접 응답 가능.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-07-04 | 리드 에이전트 4종 정의 | agents/ | 초기 팀 구성 |
| 2026-07-04 | 오케스트레이터·경계 검증 스킬 추가, 포인터 등록 | skills/, CLAUDE.md | 에이전트만 있고 조율 체계 부재(drift) 해소 |

---

## Environment & Shell Quirks
- **Python / uv Cache**: The default `~/.cache/uv` directory is not writable in the sandbox. In sandboxed agent sessions, **always** pass a local cache directory flag: `uv --cache-dir .omx/uv-cache run --python 3.13 ...` (or `.skillopt/uv-cache` depending on the repository).
- **Zsh Read-Only Variables**: `status` is a read-only variable in `zsh`. Never use `status` as a loop or local variable name in scripts (use `st` or `rc` instead).
- **macOS `open` Command**: `open <file>` may intermittently fail with error `-600 procNotFound`. Simply retry the command.
- **Repository Layout**: This is a coordination layer managing autonomous sub-projects (`keelim-vercel`, `all-web-ui`, `android-support`, `keelim-plugin`, `rich`, `youtube`, etc.). Read `.gitmodules` once for context. Planning/backlogs reside in `docs/idea/` (with `index.md` as the index) and research notes under `docs/research/`.
