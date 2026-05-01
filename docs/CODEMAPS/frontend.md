<!-- Generated: 2026-05-01 | Files scanned: 151+ | Token estimate: ~760 -->

# Frontend Codemap

## Frontend Surfaces
- `keelim-vercel` (Next.js App Router)
- `rich/web` (Next.js App Router)
- `all-web-ui` (shared UI component package)
- `all` (Android — Jetpack Compose)
- `toto` (Streamlit — KBO dashboard; hydrate required)

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
- `button`, `input`, `panel`, `badge`, `card`, `loading-status`, `empty-state`
- shared styles and theme files (`finance.css`, `admin-bw.css`)

### all (Android — Jetpack Compose)
App modules (`app-*/`):
- `app-my-grade`: grade calculator, study timer, analytics, vocabulary
- `app-arducon`: DeepLink tester, QR scanner, JSON formatter
- `app-nanda`: NANDA diagnosis, food/exercise tracker
- `app-comssa`: financial calculators, flashcards
- `app-cnubus`: real-time bus info + Google Maps
- `app-mysenior`: accessibility-focused minimal app

Feature modules (`feature/ui-*/`): settings, scheme, WebView screens

### toto (Streamlit — KBO dashboard)
Entry: `streamlit_app/Home.py`
- Read-only win/loss standings and game-result views
- Data pipeline: `bootstrap` → `seed` → Streamlit app
- Provider interface separates data source (CSV/fixture/API) from UI
- `bun run verify` smoke-tests boot + read-only contract

## Component Hierarchy (representative)
- `keelim-vercel`:
  - `RootLayout` -> `Providers` -> `DashboardClient` -> page components
- `rich/web`:
  - `RootLayout` -> `Providers` -> route page -> feature components (`src/features/**`)
- Android:
  - `Activity` -> `NavHost` -> Compose screens -> ViewModels -> `StateFlow`

## State Management Flow
- `keelim-vercel`
  - Server data: Next route handlers + fetch
  - Client cache: TanStack Query in `components/providers.tsx`
  - Local persisted UI/domain state: Zustand (`lib/store/use-financial-store.ts` + many `*-storage.ts` modules)

- `rich/web`
  - Server data: `src/lib/api.ts` -> `rich/app` admin API or BFF routes
  - Client cache: TanStack Query (`src/app/providers.tsx`, `src/features/**/queries.ts`)
  - Local UI state: Zustand (`src/features/admin/store.ts`)

- Android (`all`)
  - ViewModel exposes `StateFlow` / `SharedFlow`
  - Repositories consume `Flow` from Room DAOs and Retrofit
  - Hilt provides dependencies at ViewModel scope

## Navigation / Data Coupling
- `rich/web` admin pages are tightly coupled to `rich/app` endpoints (`/api/admin/**`).
- `keelim-vercel` pages consume both internal Next API routes and local storage-backed modules.
- `all-web-ui` ensures visual/system consistency across multiple repos.
- Android: `core:navigation` defines route destinations; each app builds its own `NavHost`.
