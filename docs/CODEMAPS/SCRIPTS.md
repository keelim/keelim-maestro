# Root Scripts Codemap

<!-- Generated: 2026-08-03 -->
Last updated: 2026-08-03

All scripts live under `scripts/`. Run them from the repo root.

## Core Workspace Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `test-workspace.sh` | `bun run test` | Lightweight root contract verifier (metadata, scripts, boundaries) |
| `update-subrepos.sh` | `./scripts/update-subrepos.sh` (direct) | Status/update helper for submodules + autonomous repos |
| `codex-app-server.sh` | `bun run dev:codex-app-server` | Local Codex app-server (WebSocket at ws://127.0.0.1:7331) |

## Reporting / Verification Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `report-trusted-baseline.sh` | `bun run report:baseline` | Read-only trusted-baseline report (submodule/workspace state) |
| `report-shared-ui-contract.sh` | `bun run report:shared-ui` | Shared UI contract report (all-web-ui + consumers) |
| `verify-all-web-ui-integration.sh` | direct | Strict static verifier for all-web-ui integration |
| `verify-keelim-plugin-rename.sh` | direct | Verifies keelim-plugin rename contract |
| `verify-python-dependency-constraints.py` | `uv run python scripts/...` | Checks uv workspace constraint alignment |

## Support / Config Files

| File | Purpose |
| --- | --- |
| `all-web-ui-rich-allowed-drift.txt` | Temporary allowlist of `rich/web` files still using local design-system primitives; read by `verify-all-web-ui-integration.sh` to suppress false positives during migration |

## Codemap Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `refresh-codemaps.py` | `python3 scripts/refresh-codemaps.py` | Generates per-child codemap docs; updates timestamps |

## Key Package.json Scripts

```bash
bun run test                  # Root contract verifier (test-workspace.sh)
bun run report:baseline       # Read-only trusted-baseline report
bun run report:shared-ui      # Shared UI contract report
bun run dev:keelim-vercel     # Vercel Next.js dev server
bun run dev:rich-web          # Rich admin web dev server
bun run dev:toto              # Toto KBO dashboard dev server
bun run dev:codex-app-server  # Local Codex WebSocket server
bun run dev:strategy-builder  # Rich open-trading-api strategy builder UI
bun run dev:backtester        # Rich open-trading-api backtester UI
bun run build:web             # Build keelim-vercel + rich-admin-web
bun run typecheck:web         # Typecheck all-web-ui + keelim-vercel + rich-admin-web
bun run test:web              # Run rich-admin-web tests
bun run test:toto             # Run toto tests
bun run verify:toto           # Verify toto (test + compile)
```
