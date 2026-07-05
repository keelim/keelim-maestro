# CodeGraph Setup and Dispatch Contract

<!-- Generated: 2026-07-05 -->

## Overview

Each child repository may have its own `.codegraph/` index. The root exposes a
**dispatcher** (`scripts/codegraph.sh`) that routes CodeGraph commands to the correct
child repo without initializing a root aggregate graph.

## Dispatch Commands

```bash
# Route to a child repo graph (run from within child repo)
cd rich && codegraph files . --max-depth 2
cd keelim-plugin && codegraph context . "skill inventory"
cd all && codegraph query . "MainActivity"
```

Note: `scripts/codegraph.sh` is not present in this checkout; CodeGraph commands must be
run directly within each initialized child repo.

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
