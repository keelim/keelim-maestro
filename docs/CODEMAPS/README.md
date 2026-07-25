# keelim-maestro Codemaps

<!-- Generated: 2026-07-25 -->
Last updated: 2026-07-25

This directory contains codemap snapshots for the **keelim-maestro** workspace superproject.
Codemaps are coordination-layer documentation only; child repo implementation details live
in each child's own codebase.

## Index

| File | Purpose |
| --- | --- |
| [keelim-maestro.md](keelim-maestro.md) | Root superproject structure and key files |
| [WORKSPACE.md](WORKSPACE.md) | Bun + uv workspace membership and bootstrap |
| [SUBMODULES.md](SUBMODULES.md) | Registered Git submodules and pinned commits |
| [SCRIPTS.md](SCRIPTS.md) | Root helper scripts inventory |
| [architecture.md](architecture.md) | High-level architecture and MCP routing |
| [frontend.md](frontend.md) | Frontend workspace members and shared UI contract |
| [backend.md](backend.md) | Backend/Python workspace and local automation |
| [data.md](data.md) | Data, knowledge, and storage patterns |
| [dependencies.md](dependencies.md) | Bun catalog and uv constraint dependencies |
| [CODEGRAPH.md](CODEGRAPH.md) | CodeGraph setup and dispatch contract |
| [projects/README.md](projects/README.md) | Per-project codemap snapshots index |

## Refresh

To regenerate all codemaps, run:

```bash
python3 scripts/refresh-codemaps.py
```

The generator script requires `keelim-plugin` to be initialized (it hosts `generate_codemap.py`).
For a root-only timestamp refresh when no structural changes occurred, update dates in each file
and run `git add docs/CODEMAPS/ && git commit -m "chore: update codemaps [skip ci]"`.

## Scope

These codemaps cover:
- Root superproject files (this repo's coordination layer)
- Registered submodules (as gitlink pointers)
- Autonomous child repos (`all-web-ui`, `rich`) — structural notes only
- Excluded: `quant` (no remote)
