# GBrain Operator Runbook

This runbook is the execution checklist for the full-brain rollout.

## Prerequisites

- Bun is available on the operator machine.
- Network access is approved for installing `github:garrytan/gbrain`.
- Any provider keys are supplied by the operator at execution time.
- The target brain repo path is chosen outside this root checkout.

Recommended local paths:

```bash
export GBRAIN_REPO="$HOME/brain"
export KEELIM_MAESTRO_ROOT="/Users/keelim/Desktop/keelim-maestro"
```

## Install And Initialize

```bash
bun install -g github:garrytan/gbrain
gbrain --version
gbrain init --pglite
gbrain doctor --json
```

If init prints a search-mode cost matrix, stop and confirm the mode with the
operator. This workspace default is `balanced` unless the operator chooses a
different mode.

```bash
gbrain config set search.mode balanced
gbrain search modes
```

## Create Brain Repo Skeleton

Create this outside the root repository:

```bash
mkdir -p "$GBRAIN_REPO"/{projects,concepts,media,sources,inbox}
cd "$GBRAIN_REPO"
git init
```

Minimum files:

- `RESOLVER.md` - filing decision tree
- `schema.md` - page conventions
- `index.md` - human-readable catalog
- `log.md` - chronological ingest log

Do not store credentials in the brain repo.

## Local Smoke Import

Start with root-owned files only:

```bash
gbrain import "$KEELIM_MAESTRO_ROOT/AGENTS.md" --no-embed
gbrain import "$KEELIM_MAESTRO_ROOT/README.md" --no-embed
gbrain import "$KEELIM_MAESTRO_ROOT/docs" --no-embed
gbrain embed --stale
gbrain search "keelim-maestro"
gbrain query "current workspace child repository boundaries"
gbrain stats
```

## Codex Local MCP Smoke

```bash
codex mcp add gbrain -- gbrain serve
```

Then verify from Codex with:

- `get_brain_identity`
- `list_skills`
- one `search` or `query` call

## Curated Full Import

Use `docs/knowledge/source-targets.md` as the manifest. Import only approved
paths and keep exclusions intact.

After import:

```bash
gbrain embed --stale
gbrain extract links --source db --dry-run
gbrain extract links --source db
gbrain extract timeline --source db
gbrain stats
```

If the corpus is too large for local operation, stop broad usage and promote the
brain to Postgres or Supabase.

## Postgres Or Supabase Promotion

Promotion requires operator-provided database credentials. Keep values in local
env or GBrain config only.

```bash
gbrain migrate --to supabase
gbrain doctor --json
gbrain stats
```

If hosted over HTTP MCP for Codex:

```bash
export GBRAIN_REMOTE_TOKEN="..."
gbrain connect https://YOUR-Gbrain-HOST/mcp --token "$GBRAIN_REMOTE_TOKEN" --agent codex --install
```

## Maintenance Loop

Manual safe loop:

```bash
gbrain sync --repo "$GBRAIN_REPO"
gbrain embed --stale
gbrain doctor --json
```

Recurring jobs require explicit operator approval before registration:

- every 15-30 minutes: sync and embed stale content
- nightly: `gbrain dream`
- weekly: `gbrain doctor --json` and `gbrain embed --stale`

Do not register cron jobs from root documentation work without a direct request.
