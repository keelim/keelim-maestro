# Knowledge system operator runbook

This runbook documents the operator flow for the root-owned semantic knowledge-system implementation.

## Preconditions

- run from the workspace root unless a step explicitly changes directories
- keep child repos read-only during analyzer development
- keep the target set limited to `all`, `rich`, and `keelim-vercel`

## Bootstrap sequence

### 1. Inspect repository state

```bash
git status --short
git status --ignore-submodules=none
git submodule status
```

### 2. Inspect the knowledge workspace tree

```bash
find docs/knowledge -maxdepth 4 | sort
find docs/tools -maxdepth 4 | sort
```

### 3. Install and inspect the Python package

```bash
cd docs/tools
uv run keelim-knowledge --help
```

## Validation and analysis workflow

Run validation before and after generated-artifact refreshes.

```bash
cd docs/tools
uv run keelim-knowledge validate
uv run keelim-knowledge analyze all
uv run keelim-knowledge analyze rich
uv run keelim-knowledge analyze keelim-vercel
find ../knowledge/generated -maxdepth 2 -type f | sort
```

Review semantic seeds before loading Neo4j:

```bash
find ../knowledge/nodes -maxdepth 3 -type f | sort
find ../knowledge/relationships -maxdepth 3 -type f | sort
```

## Neo4j workflow

Preferred path on macOS with OrbStack or Docker Desktop:

```bash
docker compose -f docs/knowledge/docker-compose.yaml up -d
cd docs/tools
uv run keelim-knowledge populate
uv run keelim-knowledge query "MATCH (n) RETURN labels(n), count(n)"
```

Once the semantic impact command is available, include:

```bash
uv run keelim-knowledge impact product
docker exec knowledge-neo4j-1 cypher-shell -u neo4j -p keelim-knowledge \
  "MATCH ()-[r:CALLS_API]->() RETURN count(r) AS call_edges;"
```

Notes:

- On this workspace, OrbStack-backed Docker is a valid implementation of the Docker path.
- If a local Homebrew Neo4j service is already bound to `7474` / `7687`, stop it before running Docker compose to avoid port conflicts:

```bash
brew services stop neo4j
```

If Docker is unavailable on the operator machine, a Homebrew install is an acceptable fallback:

```bash
brew install neo4j
brew services start neo4j
cypher-shell -u neo4j -p neo4j --change-password
cd docs/tools
NEO4J_URI=bolt://localhost:7687 NEO4J_USER=neo4j NEO4J_PASSWORD=<password> uv run keelim-knowledge populate
```

### Recommended safety defaults

- keep stale cleanup off unless explicitly requested
- prefer manual YAML overrides over analyzer-produced defaults when semantics disagree
- treat generated artifacts as reproducible cache, not the long-term source of truth

## MCP smoke checks

After the database is populated and the server is running, smoke-check these tools first:

- `list_subprojects`
- `find_entity`
- `find_endpoint`
- `get_neighbors`
- `find_path`
- `trace_data_flow`
- `check_graph_health`
- `analyze_entity_impact` (or the CLI-equivalent `impact`)

## Verification checklist

Use this sequence for completion evidence:

```bash
cd docs/tools
uv run pytest
uv run keelim-knowledge validate
uv run keelim-knowledge analyze all
uv run keelim-knowledge analyze rich
uv run keelim-knowledge analyze keelim-vercel
```

If Neo4j is available, continue with:

```bash
docker compose -f ../knowledge/docker-compose.yaml up -d
uv run keelim-knowledge populate
uv run keelim-knowledge query "MATCH (n) RETURN labels(n), count(n)"
uv run keelim-knowledge impact product
```

## Current capability notes

- `quant` is intentionally excluded
- `Keelim-Knowledge-Vault` note ingestion is deferred
- `keelim-plugin` integration is deferred
- capability parity is expected to come from a mix of semantic YAML seeds plus conservative analyzer inference
