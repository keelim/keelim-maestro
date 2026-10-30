# Backend Codemap

<!-- Generated: 2026-10-30 -->
## Python Workspace Members

Root uv workspace provides shared dependency constraints for:

| Member | Package | Path | Runtime | Notes |
| --- | --- | --- | --- | --- |
| `keelim-rich` | `rich` package | `rich/` | Python >=3.13 | Admin API + open trading backend; dirty working tree |
| `youtube` | — | `youtube/` | Python >=3.13 | YouTube automation stack |

**Excluded from root uv workspace:**
- `quant` — no remote; intentionally excluded

## Rich Backend

`rich/` is an autonomous child repo with a mixed Python + TypeScript stack:

- **Python/FastAPI backend** — admin API, data pipelines
- **Open Trading API** — algo trading platform with two sub-apps:
  - `rich/open-trading-api/strategy_builder/` — strategy builder (root helper: `bun run dev:strategy-builder`)
  - `rich/open-trading-api/backtester/` — backtesting engine (root helper: `bun run dev:backtester`)
- **Local Kubernetes** — managed via Skaffold; start/stop via local automation helper

## YouTube Automation

`youtube/` is an autonomous child repo and active workspace member:

- **Remotion renderer** (`youtube/remotion/`) — TypeScript/React-based video renderer
- **Services** (`youtube/services/`) — backend automation services
- **Video projects** (`youtube/videos/`) — per-video project packages

## Local Automation Stack

`agentgateway` and `rich` run in local Kubernetes (Skaffold-managed).
Architecture details are in [architecture.md](architecture.md).

## Python Commands

```bash
# Constraint verification
uv run python scripts/verify-python-dependency-constraints.py

# Lock check
uv lock --check

# Tests
uv run --package keelim-rich --group dev pytest rich/tests
```
