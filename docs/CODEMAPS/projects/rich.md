# `rich` Codemap

<!-- Generated: 2026-08-10 -->

**Type:** Autonomous child repo (not a submodule)
**Remote:** https://github.com/keelim/rich
**Branch:** master
**Status:** Dirty working tree; commits ahead of origin; do not pin until reconciled

## Shape

Mixed Python + React/TypeScript admin stack.

## Key Components

| Component | Path | Stack |
| --- | --- | --- |
| Admin web | `rich/web/` | React 19 + Vite; root Bun workspace member |
| Python backend | `rich/` (root) | Python >=3.13; root uv workspace member (`keelim-rich`) |
| Strategy builder | `rich/open-trading-api/strategy_builder/` | Python + FastAPI; root helper: `bun run dev:strategy-builder` |
| Backtester | `rich/open-trading-api/backtester/` | Python; root helper: `bun run dev:backtester` |
| Kubernetes stack | `rich/` (k8s manifests) | Skaffold-managed local dev cluster |

## Local Dev

```bash
bun run dev:rich-web                   # Root: start admin web dev server
bun run dev:strategy-builder           # Root: start strategy builder
bun run dev:backtester                 # Root: start backtester
bun run automation:local -- start rich # Start full local K8s stack
bun run automation:local -- standby    # Stop rich Skaffold loop
```

## Pre-Pinning Requirements

Before this repo can become a root submodule:
1. Freeze/split the mixed dirty working tree state
2. Push ahead-of-origin commits to remote
3. Confirm clean state vs `origin/master`
4. Run `bun run report:baseline` to verify

## Notes

- Absent in a fresh root checkout. Clone separately: `git clone https://github.com/keelim/rich.git rich`
- Root `.gitignore` excludes `/rich/` so root index stays coordination-only.
- Full codemap requires local hydration. Re-run `scripts/refresh-codemaps.py` after cloning.
