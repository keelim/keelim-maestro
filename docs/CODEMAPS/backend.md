# Backend Codemap

<!-- Generated: 2026-06-23 -->

## Python Workspace Members

Root uv workspace provides shared dependency constraints for:

| Member | Package | Path | Runtime | Notes |
| --- | --- | --- | --- | --- |
| `kbo-dashboard` | `toto` package | `toto/` | Python | KBO Streamlit dashboard; pinned submodule |
| `keelim-rich` | `rich` package | `rich/` | Python >=3.13 | Admin API + open trading backend; dirty working tree |

**Excluded from root uv workspace:**
- `youtube` — removed from root workspaces

## Rich Backend

`rich/` is an autonomous child repo with a mixed Python + TypeScript stack:

- **Python/FastAPI backend** — admin API, data pipelines
- **Open Trading API** — algo trading platform with two sub-apps:
  - `rich/open-trading-api/strategy_builder/` — strategy builder (root helper: `bun run dev:strategy-builder`)
  - `rich/open-trading-api/backtester/` — backtesting engine (root helper: `bun run dev:backtester`)
- **Local Kubernetes** — managed via Skaffold; start/stop via local automation helper

## Toto (KBO Dashboard)

`toto/` is a registered submodule and active workspace member:

- **Streamlit app** (`toto/streamlit_app/`) — KBO baseball prediction dashboard
- **Python library** (`toto/src/kbo_dashboard/`) — data contracts, repository, UI support
- **Tests** (`toto/tests/`) — DTO, repository, state, and filter tests
- Run locally: `bun run dev:toto` (via `bun --filter toto-kbo-streamlit-dashboard dev`)

## Local Automation Stack

`agentgateway` and `rich` run in local Kubernetes.
See `docs/ops/local-automation-stack.md` for the full runtime audit.

## GBrain Knowledge System

GBrain uses a separate operator brain repository (`~/brain`). The root owns only:
- `docs/knowledge/README.md` — workspace contract and scope
- `docs/knowledge/gbrain.md` — staged full-brain adoption contract
- `docs/knowledge/operator-runbook.md` — install, local smoke, MCP, migration
- `docs/knowledge/source-targets.md` — curated import pool and exclusions
- `docs/knowledge/verification-contract.md` — expected verification evidence

## Python Commands

```bash
# Constraint verification
uv run python scripts/verify-python-dependency-constraints.py

# Lock check
uv lock --check

# Tests
uv run --package keelim-rich --group dev pytest rich/tests
uv run --package kbo-dashboard --group dev pytest toto/tests
```
