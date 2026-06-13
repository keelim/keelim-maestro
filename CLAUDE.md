# Claude Code Project Guidelines - keelim-maestro

## Headroom & RTK (Rust Token Killer)
This project is configured to run with **Headroom** (a context optimization layer) and **RTK (Rust Token Killer)**.
- **Proxy Server**: All API calls route through the Headroom proxy at `http://127.0.0.1:8787` (configured in `.claude/settings.local.json`). Ensure the proxy is running (`headroom proxy`).
- **MCP Server**: The Headroom MCP server is registered globally in `~/.claude.json`. It exposes `headroom_retrieve` (which appears as `mcp__headroom__headroom_retrieve` in Claude Code) for Content-Compressed Retrieval (CCR).
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

## Environment & Shell Quirks
- **Python / uv Cache**: The default `~/.cache/uv` directory is not writable in the sandbox. In sandboxed agent sessions, **always** pass a local cache directory flag: `uv --cache-dir .omx/uv-cache run --python 3.13 ...` (or `.skillopt/uv-cache` depending on the repository).
- **Zsh Read-Only Variables**: `status` is a read-only variable in `zsh`. Never use `status` as a loop or local variable name in scripts (use `st` or `rc` instead).
- **macOS `open` Command**: `open <file>` may intermittently fail with error `-600 procNotFound`. Simply retry the command.
- **Repository Layout**: This is a coordination layer managing autonomous sub-projects (`keelim-vercel`, `all-web-ui`, `android-support`, `keelim-plugin`, `rich`, `youtube`, etc.). Read `.gitmodules` once for context. Planning/backlogs reside in `docs/idea/` (with `index.md` as the index) and research notes under `docs/research/`.
