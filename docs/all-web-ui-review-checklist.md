# all-web-ui review & documentation checklist

This document captures the review gates for the approved shared UI rollout between `rich/web` and `keelim-vercel`.

## Intent

Create `all-web-ui/` as an **autonomous child repo** under the workspace root so shared tokens/themes and low-level UI primitives can be reused without collapsing the workspace into a monorepo.

## Required repository boundaries

- `all-web-ui/` must be its own Git repository.
- the default branch must be `main`.
- the package should stay framework-light:
  - allow `react` / `react-dom` peer dependencies
  - avoid `next/*` imports from the shared package
- the root repo remains a coordination layer, not the package host

## Approved shared surface

Start with primitives and styling contracts only:

- CSS tokens
- theme presets (`finance`, `admin-bw`)
- `Button`
- `Input`
- `Panel` / `Card`
- `Badge`
- `LoadingStatus`
- `EmptyState`

## Explicit non-goals

- do not move feature/business logic from `rich/web` into `all-web-ui`
- do not directly replace or repurpose `keelim-vercel/components/ui/*`
- do not migrate route/layout ownership into the shared package
- do not force a root workspace/monorepo conversion

## Integration order

### 1) `rich/web` first

Review for:

- local dependency wiring to `all-web-ui`
- required Next transpilation config only if package transpilation actually needs it
- root style/theme import placement
- preservation of:
  - `admin-bw` contract
  - Agentation toolbar behavior
  - existing admin navigation/shell structure

Recommended first-pass touchpoints:

- `rich/web/package.json`
- `rich/web/next.config.ts`
- `rich/web/src/app/layout.tsx`
- `rich/web/src/app/globals.css`
- `rich/web/src/features/admin/components/loading-status.tsx`
- `rich/web/src/features/admin/components/todo-panel.tsx`
- `rich/web/src/features/admin/components/admin-shell.tsx`

### 2) `keelim-vercel` second

Review for:

- local dependency wiring to `all-web-ui`
- app-specific global CSS remaining intact around shared token imports
- wrapper/adapter usage instead of direct edits inside shadcn-managed `components/ui/*`

Recommended first-pass touchpoints:

- `keelim-vercel/package.json`
- `keelim-vercel/next.config.js`
- `keelim-vercel/app/globals.css`
- `keelim-vercel/components/shared/*` or `keelim-vercel/lib/ui-adapters/*`
- `keelim-vercel/AGENTS.md` lesson updates when `app/`, `components/`, `lib/`, or `scripts/` change

## Review gates

Mark the rollout ready only when all items below are satisfied.

### Repo/package gates

- [ ] `all-web-ui/` exists under the workspace root
- [ ] `all-web-ui/.git` exists and uses `main`
- [ ] shared package exports tokens/themes and at least five primitives
- [ ] shared package does not depend on `next/*`

### Styling/contract gates

- [ ] `finance` and `admin-bw` themes are represented as shared token/theme contracts
- [ ] `rich` keeps the admin black/white look after integration
- [ ] `keelim-vercel` keeps shadcn ownership boundaries intact

### App integration gates

- [ ] `rich/web` uses shared primitives in at least one real admin surface
- [ ] `keelim-vercel` uses shared primitives through adapters/wrappers in at least one real surface
- [ ] no feature-specific business logic was moved into `all-web-ui`

## Verification commands

Run and capture PASS/FAIL evidence for each changed project.

### Shared package

```bash
cd all-web-ui
bun run typecheck
bun test
```

### rich/web

```bash
cd rich/web
bun run typecheck
bun run test
bun run build
```

Manual spot checks:

- `/admin` navigation
- panel/list loading states
- todo/bucket/admin shell visuals under `admin-bw`
- Agentation toolbar still mounting in development

### keelim-vercel

```bash
cd keelim-vercel
bun run typecheck
bun run lint
bun run build
```

Additional guard when `app/`, `components/`, `lib/`, or `scripts/` change:

```bash
cd keelim-vercel
bun run verify:maintenance
```

## Reviewer notes

- prefer small, reversible integration diffs
- favor CSS variables + semantic classes over Tailwind-version-coupled abstractions
- escalate if a change requires direct edits to `keelim-vercel/components/ui/*` or broad shared ownership of a single file
