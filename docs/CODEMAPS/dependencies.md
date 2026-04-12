<!-- Generated: 2026-04-12 | Files scanned: 151 | Token estimate: ~670 -->

# Dependencies Codemap

## External Services / APIs
- Supabase (`@supabase/supabase-js`, `@supabase/ssr`, Python `supabase`)
- Neon Postgres (`@neondatabase/serverless` + Drizzle)
- Vercel runtime services (`@vercel/analytics`, `@vercel/speed-insights`, `@vercel/og`)
- Yahoo Finance (`yahoo-finance2`)
- Alternative.me Fear & Greed API (`https://api.alternative.me/fng/`)
- GitHub CLI (`gh`) for workflow control in `rich/app/services/gh_actions.py`
- Google Workspace APIs (Calendar + Sheets in `rich/web` BFF)
- KRX/PyKRX data sources (`pykrx`, KRX web endpoints in `pykrx_foreign_flow.py`)
- Google Play Android Publisher API (`@googleapis/androidpublisher` in `android-support`)
- LiteLLM proxy (`litellm[proxy]` in `c2g-proxy`)

## Core Frameworks
- Next.js 16 + React 19 (`keelim-vercel`, `rich/web`)
- FastAPI (`rich/app`, `quant/myapi`)
- SQLAlchemy + Alembic (`quant/myapi`)
- Kotlin Multiplatform/Gradle (`all`)

## Shared Libraries / Internal Coupling
- `all-web-ui` local package consumed by:
  - `keelim-vercel`
  - `rich/web`
- TanStack Query across web frontends
- Zustand across web frontends

## Persistence Tooling
- Drizzle ORM + drizzle-zod (`keelim-vercel`)
- Supabase SDKs (JS + Python)
- SQLAlchemy ORM (quant)

## Dependency Hotspots
- `keelim-vercel` has the broadest JS dependency footprint (UI + finance + infra SDKs).
- `quant` has the broadest Python footprint (data science + web + auth + migration + Slack/MCP).
- `rich` bridges both web and Python service dependencies, plus Google and GitHub integrations.

## Risk Notes (high-level)
- Multi-repo shared UI (`all-web-ui`) creates coordinated-release coupling.
- `rich/web` depends on stable contract of `rich/app` admin endpoints.
- Multiple data providers (Supabase, Neon, Yahoo, Alternative.me, KRX, Google) increase integration surface and failure modes.
