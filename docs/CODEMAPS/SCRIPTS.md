# Root Scripts Codemap

<!-- Generated: 2026-09-06 -->
Last updated: 2026-09-06

All scripts live under `scripts/`. Run them from the repo root.

## Core Workspace Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `test-workspace.sh` | `bun run test` | Lightweight root contract verifier (metadata, scripts, boundaries) |
| `update-subrepos.sh` | `./scripts/update-subrepos.sh` (direct) | Status/update helper for submodules + autonomous repos |
| `codex-app-server.sh` | `bun run dev:codex-app-server` | Local Codex app-server (WebSocket at ws://127.0.0.1:7331) |
| `codegraph.sh` | `bun run cg` / `bun run cg:status` / `bun run cg:root-check` | CodeGraph dispatch; delegates to child `.codegraph/` indexes |
| `local-automation.sh` | `bun run automation:local -- ...` | Local automation index/delegator for `rich`, `youtube` n8n, and `tools/agentgateway` |

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

## Changeset Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `test-changeset-manifest.mjs` | `bun run test:changeset` | Tests changeset manifest logic |
| `validate-changeset-manifest.mjs` | `bun run changeset:validate` | Validates a read-only, ordered cross-repository changeset manifest |

## Utility / Audit Scripts (not in package.json)

| Script | Invocation | Purpose |
| --- | --- | --- |
| `dep-audit.mjs` | `bun scripts/dep-audit.mjs` | Dependency audit helper |
| `dep-freshness.mjs` | `bun scripts/dep-freshness.mjs` | Checks dependency freshness/staleness |
| `security-scan.mjs` | `bun scripts/security-scan.mjs` | Security scanning utility |

## Knowledge Vault / Improvement Scripts (`scripts/improvements/`)

| Script | Purpose |
| --- | --- |
| `aggregate_improvements.py` | Aggregates improvement entries across projects |
| `build_detailed_report_input.py` | Builds detailed report input data |
| `build_report_input.py` | Builds summary report input data |
| `build_viewer_report.py` | Builds HTML viewer report from improvement data |
| `check_counts.py` | Checks item counts in improvement inventories |
| `init_progress_ledger.py` | Initializes a progress ledger for tracking |
| `verify_knowledge_vault_automation.py` | Verifies Knowledge Vault automation compliance |
| `verify_knowledge_vault_frontmatter.py` | Validates frontmatter in Knowledge Vault notes |
| `verify_knowledge_vault_links.py` | Checks internal links in Knowledge Vault |

## Key Package.json Scripts

```bash
bun run test                  # Root contract verifier (test-workspace.sh)
bun run test:changeset        # Changeset manifest test suite
bun run changeset:validate    # Validate cross-repo changeset manifest
bun run report:baseline       # Read-only trusted-baseline report
bun run report:shared-ui      # Shared UI contract report
bun run cg                    # CodeGraph dispatch (default)
bun run cg:status             # CodeGraph status for all child repos
bun run cg:root-check         # CodeGraph root-only check
bun run automation:local      # Local automation delegator (rich / youtube / agentgateway)
bun run dev:keelim-vercel     # Vercel Next.js dev server
bun run dev:rich-web          # Rich admin web dev server
bun run dev:codex-app-server  # Local Codex WebSocket server
bun run dev:strategy-builder  # Rich open-trading-api strategy builder UI
bun run dev:backtester        # Rich open-trading-api backtester UI
bun run build:web             # Build keelim-vercel + rich-admin-web
bun run typecheck:web         # Typecheck all-web-ui + keelim-vercel + rich-admin-web
bun run test:web              # Run rich-admin-web tests
```
