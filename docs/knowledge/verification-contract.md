# Knowledge system verification contract

This document records the minimum verification evidence expected for semantic graph parity work on the root-owned knowledge-system.

## Parity target vs current scope

- **Parity target**: article-faithful semantic graph capabilities — semantic nodes, semantic relations, Neo4j-backed impact traversal, and deterministic verification.
- **Scope boundary**: root-owned files only (`docs/knowledge/**`, `docs/tools/**`, `.omx/**`) with read-only analysis of `all`, `rich`, and `keelim-vercel`.
- **Non-goal**: reproducing Channel’s production dataset size or private domain model names exactly.

## Required command groups

### Repository sanity

```bash
git diff --check
git status --short
git status --ignore-submodules=none
```

### Documentation sanity

For documentation-only changes, verify at least:

- referenced files exist
- fenced code blocks are balanced
- top-level headings exist
- root navigation points to the intended docs

### Python/package verification

When `docs/tools` is present, the expected command set is:

```bash
cd docs/tools
UV_CACHE_DIR=.uv-cache uv run keelim-knowledge --help
uv run keelim-knowledge --help
uv run keelim-knowledge validate
uv run pytest
```

### Analyzer verification

```bash
cd docs/tools
uv run keelim-knowledge analyze all
uv run keelim-knowledge analyze rich
uv run keelim-knowledge analyze keelim-vercel
find ../knowledge/generated -maxdepth 2 -type f | sort
```

When semantic parity work is in scope, also verify that generated artifacts contain semantic node/relation families such as `DomainEntity`, `TableColumn`, `READS`, `WRITES`, or `CALLS_API`.

### Neo4j verification

Preferred path:

```bash
docker compose -f ../knowledge/docker-compose.yaml up -d
uv run keelim-knowledge populate
uv run keelim-knowledge query "MATCH (n) RETURN labels(n), count(n)"
uv run keelim-knowledge impact product
```

If the Python `neo4j` driver cannot be installed in the current environment, record the populate/query step as **FAIL** with the exact dependency/runtime error instead of silently skipping it.
If Docker is unavailable but a local Neo4j service is available (for example via Homebrew), use that service and record the exact startup path in the verification notes.
If both Docker and a local Homebrew service exist, prefer Docker/OrbStack for reproducible verification and stop the Homebrew service first if it is using the same ports.

## PASS / FAIL conventions

Use the following review language in handoff notes:

- **PASS** — command executed and produced the expected artifact or output
- **FAIL** — command executed and exposed a concrete blocker
- **N/A** — command could not be run yet because a prerequisite lane has not merged

## First-pass acceptance expectations

A semantic parity delivery should not be called complete until these are true:

- root docs explain the workflow and scope boundaries
- `docs/tools` exists and exposes the documented CLI entrypoint
- validation and analyzer runs succeed
- generated artifacts are stored before Neo4j population
- semantic node/relation families are present in either generated or manual SSOT data
- Neo4j/MCP smoke checks are either passing or blocked with a documented reason
- at least one impact-analysis command is verified with fresh evidence

## Preferred evidence format

```text
Verification:
- PASS git diff --check
- PASS docs cross-link check
- PASS markdown sanity
- N/A uv run pytest (docs/tools package not merged in this lane)
- N/A uv run keelim-knowledge validate (depends on docs/tools package)
```
