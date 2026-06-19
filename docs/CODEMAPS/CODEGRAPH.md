# CodeGraph Setup and Dispatch Contract

<!-- Generated: 2026-06-19 -->

## Overview

Each child repository may have its own `.codegraph/` index. The root exposes a
**dispatcher** (`scripts/codegraph.sh`) that routes CodeGraph commands to the correct
child repo without initializing a root aggregate graph.

## Dispatch Commands

```bash
# Route to a child repo graph
bun run cg -- files rich --max-depth 2
bun run cg -- context keelim-plugin "skill inventory"
bun run cg -- query all "MainActivity"

# Root-level checks
bun run cg:status              # CodeGraph status of 'all'
bun run cg:root-check          # Check for unwanted root graph initialization
```

## When to Use Root vs Child Graph

| Task type | Use |
| --- | --- |
| Workspace maps, root docs/scripts, shared config | Root graph (if initialized) |
| Implementation, bug analysis, call/symbol context | Target child repo graph |
| Cross-project contract discovery | Root dispatcher |

## Initialization Checklist

Before using CodeGraph in a child repo:

1. Check `ls <child>/.codegraph/` — if absent, initialize:
   ```bash
   cd <child>
   codegraph init -i
   ```
2. Verify `.gitignore` in child repo excludes `.codegraph/`
3. Do NOT initialize a root aggregate graph for child source trees

## Root CodeGraph Policy

- Root `.gitignore` excludes `/.codegraph/` so the root index never swallows child source trees
- Root CodeGraph is coordination-only (workspace maps, root-owned docs/scripts)
- Child implementation search must go through child repo graph via the dispatcher

## Setup Checklist for New Child Repos

When adding a new child repo to CodeGraph dispatch:

1. Initialize child `.codegraph/` with `codegraph init -i`
2. Add ignore patterns for build artifacts, node_modules, .venv, etc.
3. Verify dispatcher routes correctly: `bun run cg -- files <child> --max-depth 1`
4. Add child to the dispatcher's known repo list in `scripts/codegraph.sh`

## Current Graph Status

| Child repo | `.codegraph/` present | Notes |
| --- | --- | --- |
| `all` | unknown — submodule not initialized in this checkout | — |
| `all-web-ui` | unknown — autonomous repo, check locally | — |
| `keelim-plugin` | unknown — submodule not initialized in this checkout | — |
| `keelim-vercel` | unknown — submodule not initialized in this checkout | — |
| `rich` | unknown — autonomous repo, check locally | — |
| `youtube` | unknown — autonomous repo, check locally | — |
