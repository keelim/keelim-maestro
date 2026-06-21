# Frontend Codemap

<!-- Generated: 2026-06-21 -->

## Frontend Workspace Members

All frontend packages are part of the root Bun workspace.

| Package | Path | Framework | Purpose |
| --- | --- | --- | --- |
| `@keelim/all-web-ui` | `all-web-ui/` | React 19 + Tailwind 4 | Shared UI component library; publishes to GitHub Packages |
| `keelim-vercel` | `keelim-vercel/` | Next.js 16 / App Router | Main Vercel-deployed web application |
| `rich-admin-web` | `rich/web/` | React 19 + Vite | Rich admin dashboard; uses root Bun workspace for catalog resolution |
| `@keelim/youtube-remotion` | `youtube/remotion/` | Remotion | YouTube Shorts video renderer |
| YouTube services | `youtube/services/*` | TypeScript | Production service tools |
| YouTube videos | `youtube/videos/*` | TypeScript + Remotion | Per-episode video packages |

## Shared UI Contract (`all-web-ui`)

- Published as `@keelim/all-web-ui@0.1.4` to `https://npm.pkg.github.com`
- Consumers: `keelim-vercel` (submodule), `rich/web` (autonomous)
- Standalone consumers need `.npmrc` scope mapping for `@keelim` + `NODE_AUTH_TOKEN`
- Root Bun workspace is the authoritative install/verification surface
- Package-local `bun.lock` files in `keelim-vercel` are standalone consumer fallbacks

### Verification

```bash
bun run report:shared-ui                        # Read-only contract report
./scripts/verify-all-web-ui-integration.sh      # Strict static pass/fail gate
./scripts/verify-all-web-ui-integration.sh --full  # Includes GitHub Packages registry check
bun run typecheck:web                           # Typecheck all three consumers
bun run build:web                               # Build keelim-vercel + rich-admin-web
```

## Dependency Catalog

The root `package.json` `catalog:` field pins shared frontend versions for catalog
resolution in `rich/web`. See [dependencies.md](dependencies.md) for the full list.

Key catalog entries: React 19.2.5, Next.js 16.2.4, Tailwind 4.2.2, TypeScript 5.9.3,
Radix UI, Lucide React 0.562.0, Vitest 2.1.1.

## Vercel Deployment

`keelim-vercel` is the Vercel-linked app. Vercel is pointed at the `keelim-vercel/`
directory, not the root. The root Bun workspace is used locally; Vercel reads the
submodule's own `package.json` and `bun.lock`.

## Registry Requirements

For local multi-repo frontend work requiring `@keelim/all-web-ui`:
- Root Bun workspace resolves it from the local workspace package
- Standalone installs require: `NODE_AUTH_TOKEN` or GitHub CLI token + `.npmrc` scope mapping
