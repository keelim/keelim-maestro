# keelim-knowledge

Root-owned knowledge graph tooling for the keelim-maestro workspace.

## Parity direction

The current execution target is semantic graph capability parity with the Channel.io graph knowledge article:

- semantic node families such as entities, workflows, rules, bounded contexts, columns, and event queues
- semantic relation families such as `READS`, `WRITES`, `DELETES`, `CALLS_API`, and `GOVERNED_BY`
- Neo4j-backed impact analysis instead of file-only graph inspection

## Verified locally

- `uv run pytest`
- `uv run keelim-knowledge --help`
- `uv run keelim-knowledge validate`
- `uv run keelim-knowledge analyze all|rich|keelim-vercel`
- `uv run keelim-knowledge populate`
- `uv run keelim-knowledge query "MATCH (n) RETURN count(n)"`

## Runtime notes

- If the environment blocks access to the default UV cache, run commands with `UV_CACHE_DIR=.uv-cache`.
- `populate` and `query` require the Python `neo4j` driver to be installable in the current environment.
- Prefer OrbStack/Docker with `docs/knowledge/docker-compose.yaml` for reproducible Neo4j verification.
