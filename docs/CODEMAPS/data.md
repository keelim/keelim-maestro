# Data Codemap

<!-- Generated: 2026-06-23 -->

## Knowledge and Storage Patterns

This workspace coordinates multiple data stores across child repositories.
The root owns contracts; child repos own implementation and migrations.

## Knowledge Vault (`Keelim-Knowledge-Vault`)

- **Type:** Obsidian/Markdown knowledge base
- **Submodule:** `Keelim-Knowledge-Vault/` — pinned at `15b29c11` on `main`
- **GBrain integration:** Knowledge Vault content is a curated import source for the
  GBrain knowledge system (separate `~/brain` repo)
- **Verification:** `scripts/improvements/verify_knowledge_vault_*.py` scripts check
  frontmatter, internal links, and automation compliance

## GBrain (`~/brain`)

- **Type:** Separate operator brain repo (not under keelim-maestro)
- **Integration:** Synced from curated sources including Keelim-Knowledge-Vault
- **Root contract:** `docs/knowledge/` documents scope, runbook, and verification
- **MCP exposure:** via `agentgateway` at `http://localhost:3000/mcp`

## Rich Data Layer

`rich/` contains:
- PostgreSQL / database migrations (Python/SQLAlchemy)
- Open Trading API data: market data, strategy parameters, backtest results
- Kubernetes PVCs for persistent data (not managed from root)

## Idea / Backlog

Root idea backlog lives under `docs/idea/`:
- `docs/idea/index.md` — workspace index
- `docs/idea/<project>.md` — per-project idea files

Idea gardener runs read `docs/CODEMAPS/*` first, then each project's `README.md`/`AGENTS.md`.

## Ops Documentation

Local automation stack audit: `docs/ops/local-automation-stack.md`
- Covers: `rich` Kubernetes, `tools/agentgateway`
- Root owns cross-runtime contract; child repos own manifests, scripts, secrets
