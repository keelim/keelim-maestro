# Knowledge system merge guidance

This note is for the leader or any follow-up integrator combining the parallel worker lanes.

## Intended lane boundaries

### Lane 1 — root knowledge scaffold
Expected ownership:

- `docs/knowledge/config.yaml`
- `docs/knowledge/schema.yaml`
- `docs/knowledge/docker-compose.yaml`
- `docs/knowledge/nodes/**`
- `docs/knowledge/relationships/**`
- `docs/knowledge/generated/**` seed structure only

### Lane 2 — Python implementation
Expected ownership:

- `docs/tools/pyproject.toml`
- `docs/tools/src/keelim_knowledge/**`
- `docs/tools/tests/**`

### Lane 3 — review and documentation
Expected ownership:

- `README.md` knowledge-docs pointer
- `docs/knowledge/*.md` guidance, review, runbook, and handoff material

## Recommended integration order

1. merge the `docs/knowledge` scaffold first so package/config paths exist
2. merge the `docs/tools` package next
3. merge generated artifact examples only after the analyzers are settled enough to keep diffs reviewable
4. run validation and test commands only after the first two steps are both present

## Likely conflict hotspots

- `docs/knowledge/README.md` if multiple workers document the same directory
- `docs/knowledge/generated/**` if analyzers are run before IDs stabilize
- `README.md` if multiple lanes add new top-level navigation sections

## Conflict-resolution defaults

- prefer the stricter scope statement when docs disagree
- prefer manual YAML / curated docs over generated examples when the graph story is inconsistent
- prefer deterministic IDs and reproducible analyzer outputs over richer but unstable extraction
- keep child-repo modifications out of the first merge unless there is an explicit follow-up task for them

## Handoff questions to answer before final verification

- do the docs describe the same node and relation vocabulary as the validator?
- do the analyzer commands write into the same generated-artifact locations described by the runbook?
- does the populate flow still validate before merge/upsert?
- do README pointers still match the final file set after squashing or rebasing?
