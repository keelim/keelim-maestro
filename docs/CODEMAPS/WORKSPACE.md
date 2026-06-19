# Workspace Bootstrap Codemap

<!-- Generated: 2026-06-19 -->
Last updated: 2026-06-19

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
| `rich/web` | Rich admin web; uses root Bun workspace for `catalog:` resolution |
| `youtube/remotion` | Remotion renderer for Shorts production |
| `youtube/services/*` | YouTube service tool packages |
| `youtube/videos/*` | Per-episode video packages |

**Prerequisites:** `all-web-ui`, `rich`, and `youtube` must be hydrated locally before
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
members = ["rich", "youtube"]
```

| Member | Package | Notes |
| --- | --- | --- |
| `rich` | `keelim-rich` | Requires Python >=3.13 |
| `youtube` | `easy-release-note` | Lower requires-python; resolved via parent workspace |

**Excluded:** `youtube/simple` (keeps its own lockfile/range), `toto` (archived)

### Constraint dependencies

The root `tool.uv.constraint-dependencies` pins shared packages (anyio, certifi, numpy,
pandas, pytest, etc.) to aligned ranges across workspace members.

### Key commands

```bash
uv run python scripts/verify-python-dependency-constraints.py
uv lock --check
uv workspace metadata
uv run --package keelim-rich --group dev pytest rich/tests
uv run --package easy-release-note --group dev pytest youtube/tests
```

## Bun Catalog

The root `package.json` declares a shared Bun catalog for frontend dependency version
alignment. See [dependencies.md](dependencies.md) for the full catalog listing.

## Submodule Bootstrap

```bash
git submodule update --init --recursive
```

See [SUBMODULES.md](SUBMODULES.md) for pinned commit details.
