# Workspace Bootstrap Codemap

<!-- Generated: 2026-07-08 -->
Last updated: 2026-07-08

## Bun Workspace

Runtime: **Bun 1.3.12** (`packageManager` field in package.json)

### Members

```json
"workspaces": [
  "all-web-ui",
  "keelim-vercel",
  "rich/web",
  "toto"
]
```

| Path | Notes |
| --- | --- |
| `all-web-ui` | Shared UI library; publishes `@keelim/all-web-ui` to GitHub Packages |
| `keelim-vercel` | Vercel-linked Next.js app; also a registered submodule |
| `rich/web` | Rich admin dashboard; uses root Bun workspace for `catalog:` resolution |
| `toto` | KBO Streamlit dashboard; registered submodule (`toto-kbo-streamlit-dashboard`) |

**Prerequisites:** `all-web-ui` and `rich` must be hydrated locally before
`bun install` since they are autonomous repos (not submodules).

### Key scripts

```bash
bun install                # Install all workspace packages
bun run test               # Root contract verifier (lightweight)
bun run typecheck:web      # Typecheck all-web-ui + keelim-vercel + rich-admin-web
bun run build:web          # Build keelim-vercel + rich-admin-web
bun run test:web           # Run rich-admin-web tests
```

## Python uv Workspace

Runtime: **Python >=3.13** (required by `rich`)

### Members

```toml
[tool.uv.workspace]
members = ["toto", "rich"]
```

| Member | Package | Notes |
| --- | --- | --- |
| `toto` | `kbo-dashboard` | KBO Streamlit dashboard; pinned submodule |
| `rich` | `keelim-rich` | Requires Python >=3.13 |

### Constraint dependencies

The root `tool.uv.constraint-dependencies` pins shared packages (anyio, certifi, numpy,
pandas, pytest, etc.) to aligned ranges across workspace members.

### Key commands

```bash
uv run python scripts/verify-python-dependency-constraints.py
uv lock --check
uv workspace metadata
uv run --package keelim-rich --group dev pytest rich/tests
uv run --package kbo-dashboard --group dev pytest toto/tests
```

## Bun Catalog

The root `package.json` declares a shared Bun catalog for frontend dependency version
alignment. See [dependencies.md](dependencies.md) for the full catalog listing.

## Submodule Bootstrap

```bash
git submodule update --init --recursive
```

See [SUBMODULES.md](SUBMODULES.md) for pinned commit details.
