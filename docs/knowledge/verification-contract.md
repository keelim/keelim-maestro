# GBrain Verification Contract

This file defines the evidence required before calling the GBrain adoption
ready.

## Root Safety

Run from `/Users/keelim/Desktop/keelim-maestro`:

```bash
git status --short
git status --ignore-submodules=none
bun run report:baseline
bun run test
```

Expected:

- Only root-owned rollout files are changed by the implementation.
- Existing child repository dirtiness is reported but not normalized.
- Root tests pass.

## GBrain CLI

```bash
command -v gbrain
gbrain --version
gbrain doctor --json
gbrain stats
```

Expected:

- `gbrain` is available.
- `doctor` returns actionable health output.
- `stats` reports pages after import.

## Search Smoke

```bash
gbrain search "keelim-maestro"
gbrain query "current workspace child repository boundaries"
```

Expected:

- Search results cite root workspace docs.
- Query output distinguishes root coordination files from autonomous child
  repositories.

## MCP Smoke

From Codex after MCP registration:

- call `get_brain_identity`
- call `list_skills`
- call one `search` or `query`

Expected:

- The connected brain identity is visible.
- Core GBrain tools are callable.
- Secrets are not printed or committed.

## Sync Smoke

Use a non-sensitive test page in the brain repo:

1. Add or edit a test sentence.
2. Run `gbrain sync --repo "$GBRAIN_REPO"`.
3. Run `gbrain embed --stale`.
4. Search for the exact test sentence.

Expected:

- Search returns the updated text, not the old version.

## Graph Smoke

```bash
gbrain extract links --source db --dry-run
gbrain extract links --source db
gbrain extract timeline --source db
gbrain stats
gbrain graph-query projects/keelim-maestro --depth 2
```

Expected:

- `links` and `timeline_entries` are non-zero when the imported corpus has
  linkable references.
- Graph traversal works for at least one representative slug.

## Blockers

Do not mark the full-brain rollout complete if any of these are true:

- Search mode was not explicitly confirmed after init.
- Provider keys or database URLs were written into repo files.
- Broad import included archived `toto`, no-remote `quant`, generated output, or
  secrets.
- MCP was registered but no actual tool call was verified.
- Sync ran but search still returns stale content.
