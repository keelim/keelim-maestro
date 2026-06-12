# Workspace Knowledge Layer

This directory owns the root-level knowledge-system contract for
`keelim-maestro`.

The root repository remains a coordination layer. GBrain is adopted as an
operator knowledge layer beside the workspace, not as a vendored dependency and
not as a reason to edit child repository source from the root.

## Documents

- `gbrain.md` - GBrain adoption contract and boundaries
- `source-targets.md` - curated import pool and explicit exclusions
- `operator-runbook.md` - install, local smoke, MCP, migration, and maintenance
- `verification-contract.md` - required evidence before calling the brain ready

## Current Decision

GBrain is adopted in stages:

1. Run a local PGLite smoke against root-owned docs.
2. Confirm the search mode with the operator before broad import.
3. Import the curated workspace knowledge pool.
4. Promote to Postgres or Supabase before treating the 5,000+ markdown corpus as
   a durable full-brain surface.

Credentials, tokens, database URLs, and provider keys stay outside the
repository.
