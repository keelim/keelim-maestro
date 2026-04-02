# Knowledge system review checklist

Use this checklist during implementation review and before handoff.

## Scope and ownership

- [ ] changes stay in root-owned files unless a child-repo change is explicitly approved
- [ ] the first-pass analyzer scope remains limited to `all`, `rich`, and `keelim-vercel`
- [ ] deferred items (`quant`, vault ingestion, plugin integration) remain out of scope

## SSOT and artifact boundaries

- [ ] manual YAML remains the source of truth
- [ ] generated analyzer output lands under `docs/knowledge/generated/**`
- [ ] analyzer output is not written directly into Neo4j without validation
- [ ] manual override behavior is documented when generated output disagrees with curated YAML

## Validator expectations

- [ ] duplicate node IDs are rejected
- [ ] dangling references are rejected
- [ ] relation-type validation is enforced
- [ ] node-type constraints are enforced for edges
- [ ] manual and generated artifact ID collisions are handled explicitly

## Analyzer expectations

- [ ] Kotlin analysis starts from the Gradle module graph
- [ ] Python analysis starts from FastAPI route declarations plus service imports
- [ ] TypeScript analysis starts from Drizzle schema definitions and later extends into routes/pages
- [ ] generated artifacts include source project, source files, generated timestamp, and analyzer version

## Neo4j and MCP expectations

- [ ] Neo4j compose and credentials are documented
- [ ] populate performs load -> validate -> merge ordering
- [ ] destructive cleanup remains opt-in
- [ ] MCP smoke tests cover discovery, traversal, and health checks

## Verification evidence

- [ ] package help output is captured (`uv run keelim-knowledge --help`)
- [ ] validation passes
- [ ] analyzer runs complete for `all`, `rich`, and `keelim-vercel`
- [ ] pytest passes for the docs/tools package
- [ ] populate and query smoke checks are recorded when Neo4j is available
