<!-- Generated: 2026-06-07 | Files scanned: 151+ | Token estimate: ~700 -->

# Data Codemap

## Data Stores by Subsystem

### keelim-vercel
1. Neon Postgres via Drizzle (`lib/db.ts`)
- Table: `products`
- Columns: `id`, `image_url`, `name`, `status(enum: active|inactive|archived)`, `price`, `stock`, `available_at`
- Access paths:
  - `GET /api/products/export` (read)
  - `POST /api/products/import` (bulk insert)

2. Supabase tables (queried from route handlers)
- `faq`
- `notices`
- `newsletters`
- `newsletter_subscribers`
- Additional Supabase-backed domains in lib: `financial_terms`, `term_proposals`, `wiki_questions`, `wiki_answers`, `sector_history`, `sector_items`, `tool_clicks`

### rich/app
Supabase tables used in services (`weekly_review.py` + pykrx service):
- `personal_inbox_items`
- `personal_loop_items`
- `daily_profit_notes`
- `personal_weekly_reviews`
- PyKRX ingestion/streak tables are managed by service logic (upsert/query pattern)

### rich/web
- No primary schema definitions; uses Supabase auth/session and calls:
  - `rich/app` admin API
  - Google Calendar/Sheets via OAuth tokens persisted in Supabase connection data

### quant
`quant/` is absent in this checkout and intentionally excluded from the root
superproject because it has no remote-backed reproducible path. There is no
active root-observable data model for it in this checkout.

### all (Android)
Room database (`core:database`):
- Entities and DAOs for app-specific data (grades, schedules, bookmarks, etc.)
- DataStore Proto for user preferences and settings

### toto (KBO dashboard)
- Local fixtures / CSV files (seeded via `bun run seed`)
- No remote database; read-only access pattern
- Provider interface abstracts data source for portability

## Migration History

### quant historical notes
Prior codemaps referenced FastAPI, SQLAlchemy, and Alembic surfaces under the
missing `quant/` tree. Those files are not present in the current checkout.
Refresh this section only after `quant/` is restored with a remote-backed
reproducible path.

## Data Flow Summary (ASCII)
```text
UI -> API Route/Router -> Service/CRUD -> DB Client
  keelim-vercel: Next route -> Supabase/Drizzle -> Postgres
  rich/app: FastAPI -> services -> Supabase + external datasets
  all (Android): ViewModel -> Repository -> Room DB / Retrofit
```
