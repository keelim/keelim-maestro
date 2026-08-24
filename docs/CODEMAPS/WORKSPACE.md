# Workspace Bootstrap Codemap

<!-- Generated: 2026-08-24 -->
Last updated: 2026-08-24

## Bun Workspace

Runtime: **Bun 1.3.12** (`packageManager` field in package.json)

### Members

```json
"workspaces": [
  "all-web-ui",
  "keelim-vercel",
  "rich/web",
  "youtube/remotion",
  "youtube/services/*",
  "youtube/videos/*"
]
```

| Path | Notes |
| --- | --- |
| `all-web-ui` | Shared UI library; publishes `@keelim/all-web-ui` to GitHub Packages |
| `keelim-vercel` | Vercel-linked Next.js app; also a registered submodule |
| `rich/web` | Rich admin dashboard; uses root Bun workspace for `catalog:` resolution |
| `youtube/remotion` | YouTube Remotion video renderer |
| `youtube/services/*` | YouTube automation services (glob) |
| `youtube/videos/*` | YouTube video projects (glob) |

**Prerequisites:** `all-web-ui` and `rich` must be hydrated locally before
`bun install` since they are autonomous repos (not submodules).
`youtube` is a Bun workspace member but its directory is not present in the root
checkout by default; hydrate it locally before running `bun install` if needed.

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
members = ["rich", "youtube"]
```

| Member | Package | Notes |
| --- | --- | --- |
| `rich` | `keelim-rich` | Admin API + open trading backend; requires Python >=3.13 |
| `youtube` | — | YouTube automation; requires Python >=3.13 |

### Constraint dependencies

The root `tool.uv.constraint-dependencies` pins shared packages (anyio, certifi, numpy,
pandas, playwright, pytest, ruff, etc.) to aligned ranges across workspace members.

### Key commands

```bash
uv run python scripts/verify-python-dependency-constraints.py
uv lock --check
uv workspace metadata
uv run --package keelim-rich --group dev pytest rich/tests
```

## Bun Catalog

The root `package.json` declares a shared Bun catalog for frontend dependency version
alignment. See [dependencies.md](dependencies.md) for the full catalog listing.

## Submodule Bootstrap

```bash
git submodule update --init --recursive
```

See [SUBMODULES.md](SUBMODULES.md) for pinned commit details.
