<!-- Generated: 2026-04-16 | Files scanned: 151+ | Token estimate: ~860 -->

# Backend Codemap

## Backend Surfaces
- `keelim-vercel/app/api/**` (Next.js route handlers)
- `rich/app/api/admin.py` (FastAPI router)
- `rich/web/src/app/api/**` (Next.js BFF routes)
- `quant/myapi/**` (FastAPI + router/crud split)

## Middleware Chain
- `rich/app/main.py`
  - `FastAPI` -> `CORSMiddleware` -> `include_router(admin_router)`
- `quant/myapi/main.py`
  - `FastAPI` -> `CORSMiddleware` -> `question/answer/user/etc routers`
  - Auth dependency via `Depends(get_current_user)` in protected routes
- Next.js route handlers (`keelim-vercel`, `rich/web`)
  - Request -> route module function (`GET/POST/...`) -> direct service/db calls

## Routes (Representative, route-style)

### keelim-vercel
GET `/api/faq` -> `app/api/faq/route.ts::GET` -> `supabase.from('faq').select...`
GET `/api/forex` -> `app/api/forex/route.ts::GET` -> `supabase.from('latest_forex_rates'|'forex_rates')`
GET `/api/notice` -> `route.ts::GET` -> `supabase.from('notices').select...`
GET `/api/notice/{id}` -> `route.ts::GET` -> `supabase.from('notices').eq(id).single()`
POST `/api/notice` (dev only) -> `route.ts::POST` -> `supabase.from('notices').insert...`
GET|POST|PUT|DELETE `/api/newsletter/drafts` -> `route.ts::{GET,POST,PUT,DELETE}` -> `supabase.from('newsletters')`
POST `/api/newsletter/subscribe` -> `route.ts::POST` -> `supabase.from('newsletter_subscribers').upsert...`
GET `/api/newsletter/unsubscribe` -> `route.ts::GET` -> `supabase.from('newsletter_subscribers').delete...`
GET `/api/products/export` -> `route.ts::GET` -> `getDb().select().from(products)`
POST `/api/products/import` -> `route.ts::POST` -> CSV parse/validate -> `getDb().insert(products)`
GET `/api/indices` -> `route.ts::GET` -> `yahoo-finance2.quote(...)`
GET `/api/fear-greed` -> `route.ts::GET` -> `fetch('https://api.alternative.me/fng/')`
POST `/api/og-parser` -> `route.ts::POST` -> `fetch(url)` + `cheerio` parse
GET `/api/og` -> `route.tsx::GET` -> `@vercel/og ImageResponse`

### rich/app
GET `/api/admin/me` -> `admin_me` -> `get_identity` -> `gh auth status` + `gh api user`
GET `/api/admin/workflows` -> `get_workflows` -> `resolve_default_ref` -> `list_workflow_cards`
POST `/api/admin/workflows/{workflow_id}/run` -> `run_workflow` -> `run_workflow_by_id`
POST `/api/admin/pykrx/foreign-flow/run` -> `run_pykrx_foreign_flow` -> `run_foreign_flow_ingestion`
GET `/api/admin/pykrx/foreign-flow/streaks` -> `get_pykrx_foreign_flow_streaks` -> `list_foreign_flow_streaks`
POST `/api/admin/pykrx/institution-flow/run` -> `run_pykrx_institution_flow` -> `run_institution_flow_ingestion`
GET `/api/admin/pykrx/common-flow/streaks` -> `get_pykrx_common_flow_streaks` -> `list_common_flow_streaks`
POST `/api/admin/pykrx/market-fundamental/lookup` -> `lookup_pykrx_market_fundamental` -> `lookup_market_fundamentals`
GET `/api/admin/weekly-review/summary` -> `get_admin_weekly_review_summary` -> `get_week_summary`
POST `/api/admin/weekly-review/generate-ai` -> `generate_admin_weekly_review_ai` -> `generate_ai_summary`
POST `/api/admin/weekly-review/save` -> `save_admin_weekly_review` -> `save_weekly_review`

### rich/web (BFF)
GET `/api/agenda` -> `route.ts::GET` -> Supabase user -> Google OAuth token -> Google Calendar fetch
GET `/api/google-sheets` -> `route.ts::GET` -> Supabase user -> Google OAuth token -> Sheets read
POST `/api/google-sheets` -> `route.ts::POST` -> Supabase user -> token -> Sheets append/update
GET `/auth/callback` -> callback handler -> OAuth finalize
GET `/logout` -> Supabase signOut -> redirect

### quant/myapi
GET `/api/question/list` -> `question_router.question_list` -> `question_crud.get_question_list` -> SQLAlchemy query
GET `/api/question/detail/{id}` -> `question_router.question_detail` -> `question_crud.get_question`
POST `/api/question/create` -> `question_router.question_create` -> `question_crud.create_question`
PUT `/api/question/update` -> `question_router.question_update` -> `question_crud.update_question`
DELETE `/api/question/delete` -> `question_router.question_delete` -> `question_crud.delete_question`
POST `/api/answer/create/{question_id}` -> `answer_router.answer_create` -> `answer_crud.create_answer`
POST `/api/user/create` -> `user_router.user_create` -> `user_crud.create_user`
POST `/api/user/login` -> `login_for_access_token` -> `user_crud.get_user` -> JWT issue
GET `/api/etc/d-day` -> `etc_router.get_d_day`

## Service -> Repository Mapping
- `keelim-vercel`: route handlers -> Supabase tables / Drizzle `products` table.
- `rich/app`: API router -> service modules (`gh_actions`, `pykrx_foreign_flow`, `weekly_review`) -> external systems (GitHub CLI, KRX/PyKRX, Supabase).
- `quant/myapi`: routers -> `*_crud.py` -> SQLAlchemy models (`Question`, `Answer`, `User`) -> SQLite/SQL DB via `SessionLocal`.
