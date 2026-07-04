# `keelim-vercel` Codemap

<!-- Generated: 2026-07-04 -->

**Type:** Registered Git submodule
**Remote:** https://github.com/keelim/keelim-vercel.git
**Branch:** develop
**Pinned commit:** `1304f1216351f268636c09e43a3315071ed6c769`

## Shape

Next.js 16 / App Router — main Vercel-deployed web application.

## Key Facts

- Deployed to Vercel; Vercel is pointed at `keelim-vercel/` directory, not repo root
- Part of root Bun workspace for local multi-repo frontend work
- Consumes `@keelim/all-web-ui` from GitHub Packages (`https://npm.pkg.github.com`)
- Has package-local `bun.lock` as standalone consumer fallback
- Requires `.npmrc` scope mapping for `@keelim` + `NODE_AUTH_TOKEN` in CI/Vercel builds

## Local Dev

```bash
bun run dev:keelim-vercel   # Root convenience wrapper
# or within submodule:
cd keelim-vercel && bun dev
```

## Notes

- Not initialized in a fresh root checkout. Run `git submodule update --init keelim-vercel` to hydrate.
- Full codemap requires child hydration. Re-run `scripts/refresh-codemaps.py` after initializing.
