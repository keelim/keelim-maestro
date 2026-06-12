# GBrain Adoption Contract

## Intent

GBrain is the full-brain layer for the `keelim-maestro` workspace. It gives
Codex and other agents a searchable, cited, graph-aware memory over the
workspace's durable docs, vault notes, project operating rules, creator
packages, and reusable skills.

It is not a root package dependency and it does not collapse child repositories
into a monorepo.

## Ownership Boundary

- Root owns this contract, the source manifest, and verification expectations.
- The brain repository is separate from this checkout, for example `~/brain` or
  another operator-approved path.
- Child repositories remain autonomous. Importing their documentation into
  GBrain does not grant permission to edit their source from the root.
- Secrets live in the operator secret plane: shell env, GBrain config, Keychain,
  or the chosen database provider. They must not be committed here.

## Backend Strategy

Use a staged rollout:

1. **PGLite smoke** - initialize a local zero-config brain and import only
   root-owned docs plus `AGENTS.md` and `README.md`.
2. **Curated full import** - import the curated source pool after the smoke
   proves search, sync, and MCP access.
3. **Postgres/Supabase promotion** - move the full 5,000+ markdown corpus to a
   Postgres-backed brain before treating it as production-grade memory.

PGLite is acceptable for local proof. Postgres or Supabase is the expected
long-term backend for large corpus, remote access, and multi-agent use.

## Search Mode Gate

After `gbrain init`, the operator must explicitly choose the search mode before
broad import or recurring jobs:

- `conservative` - lower context and cost
- `balanced` - default for this workspace
- `tokenmax` - maximum recall and highest likely cost

Do not silently accept an init default. Record the chosen mode in local operator
notes, not in a committed secret file.

## MCP Routing

Local smoke may connect Codex directly to local stdio:

```bash
codex mcp add gbrain -- gbrain serve
```

Remote or shared operation should use GBrain's Codex connector path with the
bearer token kept in an environment variable:

```bash
gbrain connect https://YOUR-Gbrain-HOST/mcp --token "$GBRAIN_REMOTE_TOKEN" --agent codex --install
```

The workspace's general MCP routing model still treats `agentgateway` as the
fixed local MCP ingress. If GBrain is later proxied behind `agentgateway`, update
this document and `docs/ops/local-automation-stack.md` together.

## Skillpack Boundary

`gbrain skillpack scaffold --all` should target the chosen agent or brain
operating workspace, not this root superproject, unless a later explicit request
changes that boundary.

Root docs may reference the skillpack resolver and verification flow, but should
not vendor GBrain's skills into this repository by default.
