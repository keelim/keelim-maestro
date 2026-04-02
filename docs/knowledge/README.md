# Knowledge system workspace guide

This directory is the root-owned home for the OMX knowledge-system and the parity work needed to reach the semantic graph capabilities described in the Channel.io graph knowledge article.

## Scope

Execution remains intentionally limited to:

- root-owned docs and helper scripts in this repository
- read-only analysis of these workspace targets:
  - `all`
  - `rich`
  - `keelim-vercel`

The workspace still does **not** include `quant`, `Keelim-Knowledge-Vault` ingestion, or `keelim-plugin` skill integration.
Parity work is therefore scoped to **capability parity** inside root-owned docs/tooling, not Channel-scale dataset parity.

## Workspace contract

The knowledge system is split into four layers:

1. **Manual SSOT** — YAML under `docs/knowledge/nodes/**` and `docs/knowledge/relationships/**`
2. **Generated artifacts** — analyzer output under `docs/knowledge/generated/**`
3. **Python tooling** — CLI, loaders, validators, analyzers, Neo4j integration, and MCP server under `docs/tools/**`
4. **Operator docs** — this guide plus the runbook, source-target map, and review checklist in `docs/knowledge/**`

## Expected layout

```text
docs/knowledge/
├── config.yaml
├── docker-compose.yaml
├── generated/
├── nodes/
├── relationships/
├── README.md
├── operator-runbook.md
├── review-checklist.md
└── source-targets.md
```

## Semantic graph target

The parity target expects the graph to support at least these semantic node families:

- `Service`
- `APIEndpoint`
- `DomainEntity`
- `BoundedContext`
- `BusinessRule`
- `DomainWorkflow`
- `DatabaseTable`
- `TableColumn`
- `EventQueue`
- `Workspace`
- `Subproject`
- `Module`
- `Repository`
- `UIScreen`

And at least these relation families:

- `PROVIDES`
- `IMPLEMENTS`
- `ACCESSES`
- `READS`
- `WRITES`
- `DELETES`
- `CALLS_API`
- `STORED_IN`
- `GOVERNED_BY`
- `BELONGS_TO`
- `PUBLISHES_TO`
- `CONSUMES_FROM`
- `TRIGGERS`

## Supported read-only extraction targets

### `all`
Primary signal: Gradle module graph from `all/settings.gradle.kts`.

Current module groups visible in the root include:

- app modules such as `:app-arducon`, `:app-my-grade`, and `:app-nanda`
- core modules such as `:core:data`, `:core:data-api`, `:core:database`, and `:core:domain`
- feature modules such as `:feature:settings-core`, `:feature:settings-admin`, and `:feature:ui-web`
- shared modules such as `:shared` and `:widget`

### `rich`
Primary signal: FastAPI admin routes from `rich/app/api/admin.py`.

Current route families include:

- GitHub Actions admin endpoints (`/me`, `/workflows`, `/workflows/{workflow_id}/run`)
- PyKRX ingestion and streak endpoints
- weekly review endpoints

The same module imports service modules from `app.services.*`, which makes it a good seed for endpoint-to-service relations.

### `keelim-vercel`
Primary signal: Drizzle schema and DB helpers from `keelim-vercel/lib/db.ts`.

Current schema signals include:

- `statusEnum`
- `products` table
- helper functions such as `getProducts` and `deleteProductById`

Route and page discovery already extends into `app/**/page.tsx` and `app/api/**/route.ts`; parity work now focuses on enriching these signals into semantic entities, tables, columns, and impact edges.

## Recommended execution flow

1. create or update manual semantic YAML seeds
2. run analyzers to produce generated artifacts
3. validate the merged graph inputs
4. populate Neo4j
5. query via CLI or Neo4j-backed MCP tools

See `docs/knowledge/operator-runbook.md` for the exact command sequence.

## Preferred Neo4j runtime

For reproducible local verification, prefer the committed Docker compose file under `docs/knowledge/docker-compose.yaml`.
On macOS, OrbStack-backed Docker is an acceptable implementation of this preferred path.
Use a Homebrew Neo4j service only as a fallback when Docker is unavailable.
