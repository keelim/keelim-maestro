<!-- Generated: 2026-04-28 | Files scanned: 151+ | Token estimate: ~620 -->

# Architecture Codemap (Workspace)

## Project Type
`keelim-maestro` is a root superproject coordinating multiple autonomous repos (mixed stack: Next.js, FastAPI, SQLAlchemy, Android/Kotlin, Python tooling).

## System Topology (ASCII)
```text
[keelim-maestro root]
  |-- docs/CODEMAPS/ (architecture documentation)
  |-- all (Kotlin Multiplatform apps/modules)
  |-- keelim-vercel (Next.js app + API routes + Drizzle/Supabase)
  |-- rich
  |    |-- app (FastAPI admin API)
  |    \-- web (Next.js admin/capture web)
  |-- quant (Python multi-service: FastAPI + Django + dashboards)
  |-- all-web-ui (shared React UI package)
  |-- c2g-proxy (Claude Code ↔ LiteLLM ↔ Gemini bridge)
  |-- android-support (GitHub Action for Play Console upload)
  |-- toto (KBO baseball Streamlit dashboard — declared in .gitmodules; no gitlink yet)
  \-- Keelim-Knowledge-Vault (documentation)
```

## Service Boundaries
- `keelim-vercel`: user-facing finance web app; server routes in `app/api/**`; mixed data access via Supabase + Drizzle/Neon.
- `rich/app`: operational/admin FastAPI API (`/api/admin/**`) for GitHub workflow ops, PyKRX ingestion, weekly review workflows.
- `rich/web`: Next.js frontend + BFF routes (`/api/agenda`, `/api/google-sheets`) bridging Supabase auth and Google APIs.
- `quant/myapi`: standalone FastAPI domain API (`question/answer/user/etc`) with SQLAlchemy + Alembic.
- `all-web-ui`: shared UI components consumed by both `keelim-vercel` and `rich/web`.
- `c2g-proxy`: Python bridge enabling Claude Code CLI to use LiteLLM / Gemini as the backend provider. _(Declared in `.gitmodules` but gitlink removed from index; source at github.com/keelim/c2g-proxy.)_
- `toto`: KBO baseball win/loss Streamlit dashboard. _(Declared in `.gitmodules`; no gitlink committed; directory absent; hydrate via `git clone https://github.com/keelim/toto.git toto`.)_

## High-Level Data Flow
```text
Client Browser
  -> Next.js pages (keelim-vercel or rich/web)
  -> Route handlers / API clients
  -> Service layer
      -> Supabase (Postgres tables + auth)
      -> Neon Postgres via Drizzle (products table)
      -> External APIs (Yahoo, Alternative.me, Google, KRX)
      -> GitHub CLI (rich/app GH Actions control)
  <- JSON/SSR payloads back to UI

Claude Code CLI
  -> c2g-proxy (LiteLLM gateway)
  -> Gemini API
```

## Runtime Surfaces
- Frontend-heavy: `keelim-vercel`, `rich/web`
- Backend-heavy: `rich/app`, `quant/myapi`
- Infra/tooling: `android-support`, `c2g-proxy`, `Keelim-Knowledge-Vault`
- Dashboard: `toto` (Streamlit)

## Notable Couplings
- `all-web-ui` linked via local file dependency into `keelim-vercel` and `rich/web`.
- `rich/web` depends on `rich/app` admin API contract (`/api/admin/**`) via `src/lib/api.ts`.
- `keelim-vercel` / `rich` depend on Supabase auth and external data APIs (Yahoo Finance, Alternative.me, KRX/PyKRX, Google Workspace).
- `c2g-proxy` is independent of other web services; it proxies Claude Code CLI traffic only.
