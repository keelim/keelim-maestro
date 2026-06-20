# `all-web-ui` Codemap

<!-- Generated: 2026-06-20 -->

**Type:** Autonomous child repo (not a submodule)
**Remote:** https://github.com/keelim/all-web-ui (public)
**Branch:** main
**Status:** Clean vs origin/main; pending submodule conversion

## Shape

React 19 + Tailwind 4 shared UI component library.

## Key Facts

- Published as `@keelim/all-web-ui@0.1.4` to `https://npm.pkg.github.com`
- Part of root Bun workspace (`all-web-ui` path)
- Consumers: `keelim-vercel` and `rich/web`
- Must remain independently cloneable/versionable for standalone consumer repos and Vercel builds
- Root `.gitignore` excludes `/all-web-ui/` so root index stays coordination-only

## Submodule Conversion Blockers

- `rich` dirty/ahead-of-origin state must be resolved first
- Broader workspace blockers must be clear before adding `all-web-ui` to `.gitmodules`
- When added, must use the remote URL: `https://github.com/keelim/all-web-ui`

## Verification

```bash
bun run report:shared-ui
./scripts/verify-all-web-ui-integration.sh --full
bun run typecheck:web
```

## Notes

- Absent in a fresh root checkout. Clone separately: `git clone https://github.com/keelim/all-web-ui.git all-web-ui`
- Full codemap requires local hydration. Re-run `scripts/refresh-codemaps.py` after cloning.
