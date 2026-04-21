<!-- Generated: 2026-04-21 | Files scanned: 151+ | Token estimate: ~700 -->

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

### quant/myapi
SQLAlchemy models (`quant/myapi/models.py`):
- `user` (id, username, password, email)
- `question` (id, subject, content, create_date, user_id, modify_date)
- `answer` (id, content, create_date, question_id, user_id, modify_date)

Relationships:
- `question.user_id -> user.id`
- `answer.question_id -> question.id`
- `answer.user_id -> user.id`

### all (Android)
Room database (`core:database`):
- Entities and DAOs for app-specific data (grades, schedules, bookmarks, etc.)
- DataStore Proto for user preferences and settings

### c2g-proxy
- No persistent data store; stateless proxy
- Configuration via `.env` (API keys, endpoint URLs)

### toto (KBO dashboard)
- Local fixtures / CSV files (seeded via `bun run seed`)
- No remote database; read-only access pattern
- Provider interface abstracts data source for portability

## Migration History

### quant/myapi Alembic chain
`7c8fa79f62a0` -> create `question`, `answer`
`ed055cc1d720` -> create `user`
`ef8c465f4f72` -> unique constraints on `user.email`, `user.username`
`f79de755c055` -> add `question.user_id` FK
`798ce91f5f35` -> add `answer.user_id` FK
`3a6e8347d80e` -> add `modify_date` to `question`, `answer`

### quant/all_admin (Django)
- Migration files present: `0001`..`0004` (initial + notice/keyvalue evolution)

## Data Flow Summary (ASCII)
```text
UI -> API Route/Router -> Service/CRUD -> DB Client
  keelim-vercel: Next route -> Supabase/Drizzle -> Postgres
  rich/app: FastAPI -> services -> Supabase + external datasets
  quant/myapi: FastAPI router -> CRUD -> SQLAlchemy -> DB
  all (Android): ViewModel -> Repository -> Room DB / Retrofit
```
