<!-- Generated: 2026-05-03 | Files scanned: 151+ | Token estimate: ~670 -->

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
- LiteLLM + Gemini API (`c2g-proxy` — Claude Code CLI proxy)

## Core Frameworks
- Next.js 16 + React 19 (`keelim-vercel`, `rich/web`)
- FastAPI (`rich/app`, `quant/myapi`, `c2g-proxy`)
- SQLAlchemy + Alembic (`quant/myapi`)
- Kotlin Multiplatform/Gradle (`all`)
- Jetpack Compose + Material 3 (`all` Android UI)
- Hilt (`all` DI)
- Streamlit (`toto` — KBO dashboard)

## Shared Libraries / Internal Coupling
- `all-web-ui` local package consumed by:
  - `keelim-vercel`
  - `rich/web`
- TanStack Query across web frontends
- Zustand across web frontends

## Persistence Tooling
- Drizzle ORM + drizzle-zod (`keelim-vercel`)
- Supabase SDKs (JS + Python)
- SQLAlchemy ORM (`quant`)
- Room + DataStore Proto (`all` Android)

## Dependency Hotspots
- `keelim-vercel` has the broadest JS dependency footprint (UI + finance + infra SDKs).
- `quant` has the broadest Python footprint (data science + web + auth + migration + Slack/MCP).
- `rich` bridges both web and Python service dependencies, plus Google and GitHub integrations.
- `all` has the largest Kotlin dependency graph (Compose, Hilt, Room, Retrofit, KMP, Firebase, Rust).

## Risk Notes (high-level)
- Multi-repo shared UI (`all-web-ui`) creates coordinated-release coupling.
- `rich/web` depends on stable contract of `rich/app` admin endpoints.
- Multiple data providers (Supabase, Neon, Yahoo, Alternative.me, KRX, Google) increase integration surface and failure modes.
- `c2g-proxy` adds a single-point dependency on LiteLLM / Gemini availability for Claude Code workflows.
