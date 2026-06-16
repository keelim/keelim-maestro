# Backend Codemap

<!-- Generated: 2026-06-16 -->

## Python Workspace Members

Root uv workspace provides shared dependency constraints for:

| Member | Package | Path | Runtime | Notes |
| --- | --- | --- | --- | --- |
| `keelim-rich` | `rich` package | `rich/` | Python >=3.13 | Admin API + open trading backend; dirty working tree |
| `easy-release-note` | `youtube` package | `youtube/` | Python >=3.x | YouTube Shorts tooling + release note automation |

**Excluded from root uv workspace:**
- `youtube/simple` — standalone Python project with its own lockfile and range
- `toto` — archived 2026-06-04

## Rich Backend

`rich/` is an autonomous child repo with a mixed Python + TypeScript stack:

- **Python/FastAPI backend** — admin API, data pipelines
- **Open Trading API** — algo trading platform with two sub-apps:
  - `rich/open-trading-api/strategy_builder/` — strategy builder (root helper: `bun run dev:strategy-builder`)
  - `rich/open-trading-api/backtester/` — backtesting engine (root helper: `bun run dev:backtester`)
- **Local Kubernetes** — managed via Skaffold; start/stop via local automation helper

## YouTube / Easy Release Note

`youtube/` is a private autonomous child repo:

- **Remotion renderer** (`youtube/remotion/`) — TypeScript + Remotion for Shorts video generation
- **Services** (`youtube/services/*`) — TypeScript service tools
- **Videos** (`youtube/videos/*`) — Per-episode packages
- **Easy Release Note** — Python package for automated release note generation
- **n8n workflows** — Local Kubernetes n8n for automation

## Local Automation Stack

`agentgateway` + `rich` + `youtube` n8n run in local Kubernetes.
See `docs/ops/local-automation-stack.md` for the full runtime audit.

```bash
bun run automation:local -- list
bun run automation:local -- status
bun run automation:local -- standby       # Stop on-demand runtimes (rich, n8n)
bun run automation:local -- start agentgateway
bun run automation:local -- verify rich
```

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
uv run --package easy-release-note --group dev pytest youtube/tests
```
