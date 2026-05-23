<!-- Generated: 2026-05-23 | Files scanned: 151+ | Token estimate: ~670 -->

# Dependencies Codemap

## External Services / APIs
- Supabase (`@supabase/supabase-js`, `@supabase/ssr`, Python `supabase`)
- Neon Postgres (`@neondatabase/serverless` + Drizzle)
- Vercel runtime services (`@vercel/analytics`, `@vercel/speed-insights`); the OG image route uses `next/og`.
- Yahoo Finance (`yahoo-finance2`)
- Alternative.me Fear & Greed API (`https://api.alternative.me/fng/`)
- GitHub CLI (`gh`) for workflow control in `rich/app/services/gh_actions.py`
- Google Workspace APIs (Calendar + Sheets in `rich/web` BFF)
- KRX/PyKRX data sources (`pykrx`, KRX web endpoints in `pykrx_foreign_flow.py`)
- Google Play Android Publisher API (`@googleapis/androidpublisher` in `android-support`)

## Core Frameworks
- Next.js 16 + React 19 (`keelim-vercel`, `rich/web`)
- FastAPI (`rich/app`)
- Kotlin Multiplatform/Gradle (`all`)
- Jetpack Compose + Material 3 (`all` Android UI)
- Hilt (`all` DI)
- Streamlit (`toto` — KBO dashboard)

## Shared Libraries / Internal Coupling
- `@keelim/all-web-ui` GitHub Packages npm package consumed by:
  - `keelim-vercel`
  - `rich/web`
- TanStack Query across web frontends
- Zustand across web frontends
- Bun `catalog` in root `package.json` pins shared versions (Radix UI, Tailwind 4, React 19, Next.js 16, TypeScript 5.9, vitest, testing-library, clsx, lucide-react, date-fns, react-day-picker) across all workspace members; consumers reference `"catalog:<pkg>"` instead of explicit semver strings.

## Root Workspace Tooling
- **Bun** `1.3.12` — root JavaScript workspace package manager.
- **uv** — root Python workspace package manager; `pyproject.toml` + `uv.lock` pin shared Python packages for `toto` and `rich` (requires Python ≥ 3.13).
- Root `tool.uv.constraint-dependencies` aligns shared transitive packages (anyio, numpy, pandas, starlette, uvicorn, websockets, etc.) across all uv workspace members.

## Persistence Tooling
- Drizzle ORM + drizzle-zod (`keelim-vercel`)
- Supabase SDKs (JS + Python)
- Room + DataStore Proto (`all` Android)

## Dependency Hotspots
- `keelim-vercel` has the broadest JS dependency footprint (UI + finance + infra SDKs).
- `quant` is absent in this checkout and remains excluded until it has a remote-backed reproducible path.
- `rich` bridges both web and Python service dependencies, plus Google and GitHub integrations.
- `all` has the largest Kotlin dependency graph (Compose, Hilt, Room, Retrofit, KMP, Firebase, Rust).

## Risk Notes (high-level)
- Multi-repo shared UI (`@keelim/all-web-ui`) creates coordinated-release coupling.
- `rich/web` depends on stable contract of `rich/app` admin endpoints.
- Multiple data providers (Supabase, Neon, Yahoo, Alternative.me, KRX, Google) increase integration surface and failure modes.
