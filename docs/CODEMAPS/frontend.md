<!-- Generated: 2026-04-13 | Files scanned: 151 | Token estimate: ~760 -->

# Frontend Codemap

## Frontend Surfaces
- `keelim-vercel` (Next.js App Router)
- `rich/web` (Next.js App Router)
- `all-web-ui` (shared UI component package)

## Page Tree (high-level)

### keelim-vercel
`app/layout.tsx`
- global providers (`QueryClientProvider`, `ThemeProvider`, tooltip)
- analytics/deployment listeners

`app/(dashboard)/layout.tsx`
- wraps all dashboard routes with `DashboardClient`

Routes:
- Top-level: `/`, `/about`, `/faq`, `/contact`, `/changelog`, `/login`, `/unsubscribe/[token]`
- Dashboard group: large tool catalog (`/loan`, `/budget-*`, `/tax-*`, `/notice`, `/financial-wiki/*`, `/market-*`, `/subscription-*`, etc.)
- Characteristics: many page-level calculators/tools, centralized shell via dashboard layout

### rich/web
`src/app/layout.tsx`
- global styles + shared `all-web-ui` theme CSS
- global `Providers` (React Query)
- dev toolbar component

Main route groups:
- `/admin/*`: workflows, pykrx common-flow, inbox/loop, money pages, weekly review
- `/capture/inbox`
- `/agenda`
- `/login`, `/logout`, `/auth/callback`
- utility metadata routes (`robots`, `sitemap`)

API+BFF colocated under `src/app/api/*`.

### all-web-ui
Exports reusable primitives:
- `button`, `input`, `panel`, `badge`, `loading-status`, `empty-state`
- shared styles and theme files (`finance.css`, `admin-bw.css`)

## Component Hierarchy (representative)
- `keelim-vercel`:
  - `RootLayout` -> `Providers` -> `DashboardClient` -> page components
- `rich/web`:
  - `RootLayout` -> `Providers` -> route page -> feature components (`src/features/**`)

## State Management Flow
- `keelim-vercel`
  - Server data: Next route handlers + fetch
  - Client cache: TanStack Query in `components/providers.tsx`
  - Local persisted UI/domain state: Zustand (`lib/store/use-financial-store.ts` + many `*-storage.ts` modules)

- `rich/web`
  - Server data: `src/lib/api.ts` -> `rich/app` admin API or BFF routes
  - Client cache: TanStack Query (`src/app/providers.tsx`, `src/features/**/queries.ts`)
  - Local UI state: Zustand (`src/features/admin/store.ts`)

## Navigation / Data Coupling
- `rich/web` admin pages are tightly coupled to `rich/app` endpoints (`/api/admin/**`).
- `keelim-vercel` pages consume both internal Next API routes and local storage-backed modules.
- `all-web-ui` ensures visual/system consistency across multiple repos.
