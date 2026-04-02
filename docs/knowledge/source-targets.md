# Knowledge system source-target map

This document grounds the first analyzer pass in concrete read-only source files.

## `all`

### Primary source
- `all/settings.gradle.kts`

### Why it matters
The file declares the project-wide module include list, which makes it the most reliable seed for `Subproject -> Module` edges.

### First-pass extraction targets
- `Module`
- optional `UIScreen` candidates from `feature/**` or `app-*/**`
- optional `Repository` or `DomainEntity` candidates from `core:data-api`, `core:data`, `core:domain`, and `shared`

### Grounded examples
- app modules: `:app-arducon`, `:app-cnubus`, `:app-my-grade`
- core modules: `:core:data`, `:core:data-api`, `:core:database`, `:core:domain`
- feature modules: `:feature:settings-admin`, `:feature:ui-web`
- shared modules: `:shared`, `:widget`

## `rich`

### Primary source
- `rich/app/api/admin.py`

### Why it matters
The file exposes FastAPI admin routes and imports the service layer directly, which provides a natural seed for `APIEndpoint -> Service` relationships.

### First-pass extraction targets
- `APIEndpoint`
- `Service`
- optional `DatabaseTable` once table or migration sources are wired

### Grounded examples
Imported services:
- `app.services.gh_actions`
- `app.services.pykrx_foreign_flow`
- `app.services.weekly_review`

Route examples:
- `GET /api/admin/me`
- `GET /api/admin/workflows`
- `POST /api/admin/workflows/{workflow_id}/run`
- `POST /api/admin/pykrx/foreign-flow/run`
- `GET /api/admin/pykrx/foreign-flow/streaks`
- `POST /api/admin/weekly-review/generate`

## `keelim-vercel`

### Primary sources
- `keelim-vercel/lib/db.ts`
- later extension: `keelim-vercel/app/**/page.tsx`
- later extension: `keelim-vercel/app/api/**/route.ts`

### Why it matters
`lib/db.ts` already contains a stable Drizzle schema definition and database helper functions, which makes it the best starting point for `DatabaseTable` extraction.

### First-pass extraction targets
- `DatabaseTable`
- optional `APIEndpoint`
- optional `UIScreen`

### Grounded examples
Schema signals:
- `statusEnum`
- `products` table
- columns such as `image_url`, `name`, `status`, `price`, `stock`, and `available_at`

DB helper signals:
- `getDb`
- `getProducts`
- `deleteProductById`

## Analyzer design notes

- start from stable structural signals already present in committed code
- keep child repos read-only during the initial workspace pass
- prefer deterministic IDs derived from project path + entity type + local name
- emit generated artifacts before Neo4j writes so diffs stay reviewable
