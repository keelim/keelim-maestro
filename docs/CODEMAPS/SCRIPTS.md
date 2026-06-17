# Root Scripts Codemap

<!-- Generated: 2026-06-17 -->
Last updated: 2026-06-17

All scripts live under `scripts/`. Run them from the repo root.

## Core Workspace Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `test-workspace.sh` | `bun run test` | Lightweight root contract verifier (metadata, scripts, boundaries) |
| `update-subrepos.sh` | `bun run update-subrepos` / direct | Status/update helper for submodules + autonomous repos |
| `codegraph.sh` | `bun run cg -- <args>` | CodeGraph dispatcher for child repos |
| `codex-app-server.sh` | `bun run dev:codex-app-server` | Local Codex app-server (WebSocket at ws://127.0.0.1:7331) |
| `local-automation.sh` | `bun run automation:local -- <cmd>` | Local automation stack delegator (rich, n8n, agentgateway) |

## Reporting / Verification Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `report-trusted-baseline.sh` | `bun run report:baseline` | Read-only trusted-baseline report (submodule/workspace state) |
| `report-shared-ui-contract.sh` | `bun run report:shared-ui` | Shared UI contract report (all-web-ui + consumers) |
| `verify-all-web-ui-integration.sh` | direct | Strict static verifier for all-web-ui integration |
| `verify-keelim-plugin-rename.sh` | direct | Verifies keelim-plugin rename contract |
| `verify-python-dependency-constraints.py` | `uv run python scripts/...` | Checks uv workspace constraint alignment |

## Dependency / Security Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `dep-audit.mjs` | direct via `bun` | Dependency audit (frontend packages) |
| `dep-freshness.mjs` | direct via `bun` | Dependency freshness check |
| `security-scan.mjs` | direct via `bun` | Security scan across workspace |

## Codemap Scripts

| Script | Invocation | Purpose |
| --- | --- | --- |
| `refresh-codemaps.py` | `python3 scripts/refresh-codemaps.py` | Generates per-child codemap docs; updates timestamps |

## Improvements Scripts (`scripts/improvements/`)

| Script | Purpose |
| --- | --- |
| `aggregate_improvements.py` | Aggregates improvement items across projects |
| `build_detailed_report_input.py` | Builds detailed report input data |
| `build_report_input.py` | Builds summary report input data |
| `build_viewer_report.py` | Generates human-readable improvement viewer report |
| `check_counts.py` | Counts improvement items by status |
| `init_progress_ledger.py` | Initializes progress ledger for improvement tracking |
| `verify_knowledge_vault_automation.py` | Verifies Knowledge Vault automation |
| `verify_knowledge_vault_frontmatter.py` | Verifies Knowledge Vault frontmatter compliance |
| `verify_knowledge_vault_links.py` | Verifies internal links in Knowledge Vault |

## Local Automation Commands

```bash
bun run automation:local -- list
bun run automation:local -- status
bun run automation:local -- standby        # Stop Rich Skaffold loop + scale deployments to zero
bun run automation:local -- verify rich
bun run automation:local -- status gbrain
bun run automation:local -- start agentgateway
bun run automation:local -- stop n8n
```

`agentgateway` is fixed/always-on. `rich` and `n8n` are on-demand — start when needed, standby when done.
