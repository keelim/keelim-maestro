# Project: rich Backlog Cleanup

## Architecture
- **Backend (FastAPI)**: Python service-role API endpoints, Pykrx market analysis services, KIS fear candidates rating, and daily price caching services.
- **Frontend (Next.js/React)**: Admin portal (`/admin`) utilizing Tailwind CSS v4, Zustand UI state management, and React Query server state management. Consumes shared components from `@keelim/all-web-ui`.
- **Integrations**: Standalone Open Trading API and local backtesting engine interfaces linked via API proxy routes.

## Milestones
| # | Name | Scope | Dependencies | Status | Conversation ID |
|---|---|---|---|---|---|
| 1 | T42 Backend Quality | Implement fixes for RICH-008, RICH-009, and RICH-033 to RICH-046 in python modules | None | IN_PROGRESS | 3c8a8e72-a75b-4c4a-86d7-c468d156ca78 (Worker) |
| 2 | T43 Frontend Quality | Implement fixes for RICH-047 to RICH-060 in Next.js/React code | M1 | PLANNED | TBD |
| 3 | T44 Performance | Latency and query batching improvements (RICH-061 to RICH-072) | M1, M2 | PLANNED | TBD |

## Interface Contracts
### Backend (FastAPI) ↔ Frontend (Next.js)
- API requests default to JSON content type.
- Shared UI primitives: must conform to `@keelim/all-web-ui` tokens and styles, and should run `bun run report:shared-ui` to inspect compliance.
- Google Auth & Sheets connection state: Managed by Supabase RLS policies and server-side connection tokens.
