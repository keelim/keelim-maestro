# keelim-maestro Root Superproject Codemap

<!-- Generated: 2026-06-18 -->

## Overview

`keelim-maestro` is a **workspace superproject / coordination layer** for a family of
autonomous child Git repositories. It does not merge child history; it owns only:

- Root coordination files (AGENTS.md, README.md, .gitignore, .gitmodules)
- Bun workspace bootstrap (package.json, bun.lock)
- Python uv workspace bootstrap (pyproject.toml, uv.lock)
- Root helper scripts (scripts/)
- Documentation (docs/)

Child repositories remain independently cloneable, deployable, and git-owned.

## Root File Map

```
keelim-maestro/
├── AGENTS.md                  # Agent/AI guidance for this repo
├── CLAUDE.md                  # Claude Code guidance (empty — not yet populated)
├── README.md                  # Human-facing workspace overview
├── .gitignore                 # Excludes child working trees, env, generated
├── .gitmodules                # Registered submodule pointers
├── .gitattributes             # Git attributes
├── .npmrc                     # npm/bun registry config (GitHub Packages)
├── package.json               # Bun workspace bootstrap + script catalog
├── bun.lock                   # Bun lockfile (root workspace)
├── pyproject.toml             # uv workspace bootstrap (coordination-only)
├── uv.lock                    # uv lockfile (root workspace)
├── scripts/                   # Root helper scripts (see SCRIPTS.md)
├── docs/
│   ├── CODEMAPS/              # This directory — workspace codemap snapshots
│   ├── ops/                   # Local automation stack docs
│   ├── idea/                  # Per-project idea/backlog files
│   └── knowledge/             # GBrain knowledge system docs
└── .reports/
    └── codemap-diff.txt       # Last codemap diff report
```

## Child Repositories

| Path | Type | Remote | Default branch | Status |
| --- | --- | --- | --- | --- |
| `all` | submodule | github.com/keelim/all | develop | pinned `0643bab4` |
| `android-support` | submodule | github.com/keelim/android-support | main | pinned `485a2e40` (v0.0.8-4) |
| `Keelim-Knowledge-Vault` | submodule | github.com/keelim/Keelim-Knowledge-Vault | main | pinned `15b29c11` |
| `keelim-plugin` | submodule | github.com/keelim/keelim-plugin | main | pinned `a3463396` |
| `keelim-vercel` | submodule | github.com/keelim/keelim-vercel | develop | pinned `8d29b510` |
| `all-web-ui` | autonomous | github.com/keelim/all-web-ui | main | clean vs origin/main; pending submodule conversion |
| `rich` | autonomous | github.com/keelim/rich | master | dirty working tree; ahead of origin |
| `youtube` | autonomous | private (no upstream yet) | — | local private checkout |
| `quant` | autonomous | none | — | intentionally excluded |
| `toto` | archived | github.com/keelim/toto | main | archived 2026-06-04; ignored |

## Key Policies

- Root-level changes must prefer the smallest reversible diff.
- Child repos may not be modified from root unless explicitly requested.
- `quant` has no remote — do not create one or add it to .gitmodules.
- `toto` is archived — do not reactivate in submodules, workspaces, or idea backlog.
- `youtube` is private and autonomous — include in subrepo helper and Bun/uv workspaces, but keep out of .gitmodules until a private remote and clean working tree are established.

## Open Questions

- `docs/knowledge/` is referenced in README.md but may be absent from this checkout.
- `all-web-ui` pending formal submodule registration (blocked until rich is reconciled and workspace is safe to pin).
- `rich` local commits ahead of origin pending reconciliation before pinning.
