# keelim-maestro Root Superproject Codemap

<!-- Generated: 2026-09-04 -->

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
├── AGENTS.md                  # Agent/AI guidance for this repo (authoritative)
├── CLAUDE.md -> AGENTS.md     # Symlink; CLAUDE.md and AGENTS.md are identical
├── README.md                  # Human-facing workspace overview
├── PROJECT.md                 # Project-level goals and status
├── .gitignore                 # Excludes child working trees, env, generated
├── .gitmodules                # Registered submodule pointers
├── .npmrc                     # npm/bun registry config (GitHub Packages)
├── package.json               # Bun workspace bootstrap + script catalog
├── bun.lock                   # Bun lockfile (root workspace)
├── pyproject.toml             # uv workspace bootstrap (coordination-only)
├── uv.lock                    # uv lockfile (root workspace)
├── mise.toml                  # mise tool version pinning
├── mise.lock                  # mise lockfile
├── scripts/                   # Root helper scripts (see SCRIPTS.md)
├── docs/
│   ├── CODEMAPS/              # This directory — workspace codemap snapshots
│   ├── design/                # Keelim Design System documentation
│   ├── idea/                  # Per-project idea/backlog files
│   ├── research/              # Derived research artifacts (read-only analysis)
│   └── videos/                # Video documentation assets (subproject-intros)
```

## Child Repositories

| Path | Type | Remote | Default branch | Status |
| --- | --- | --- | --- | --- |
| `all` | submodule | github.com/keelim/all | develop | pinned `dbd6ce9e` |
| `Keelim-Knowledge-Vault` | submodule | github.com/keelim/Keelim-Knowledge-Vault | main | pinned `2cfffa10` |
| `keelim-plugin` | submodule | github.com/keelim/keelim-plugin | main | pinned `0e05ea44` |
| `keelim-vercel` | submodule | github.com/keelim/keelim-vercel | develop | pinned `c0e87692` |
| `all-web-ui` | autonomous | github.com/keelim/all-web-ui | main | pending submodule conversion |
| `rich` | autonomous | github.com/keelim/rich | master | dirty working tree; ahead of origin |
| `youtube` | autonomous | github.com/keelim/youtube | — | active Bun + uv workspace member |
| `quant` | autonomous | none | — | intentionally excluded |

## Key Policies

- Root-level changes must prefer the smallest reversible diff.
- Child repos may not be modified from root unless explicitly requested.
- `quant` has no remote — do not create one or add it to .gitmodules.
- `youtube` is an active Bun and uv workspace member.

## Open Questions

- `docs/design/` contains the Keelim Design System spec (CSS tokens, themes, components) in Korean.
- `docs/videos/subproject-intros/` contains per-project video documentation assets.
- `docs/research/` contains derived analysis artifacts (HTML/Markdown); child source files are read-only during root research runs.
- `all-web-ui` pending formal submodule registration (blocked until rich is reconciled and workspace is safe to pin).
- `rich` local commits ahead of origin pending reconciliation before pinning.
- `youtube` not physically present in this checkout; hydrate locally before running `bun install` or uv commands.
