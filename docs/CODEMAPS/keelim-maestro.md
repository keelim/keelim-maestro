<!-- Generated: 2026-05-04 | Source-led root codemap reviewed after generator pass -->

# keelim-maestro Workspace Codemap

This map describes the root workspace coordination repository and the
maestro-managed child codemap snapshots kept under `docs/CODEMAPS/projects/`.
The `codebase-codemap` generator was run against the root on 2026-04-25, but its
raw pass scanned 3,594 files across nested child repositories. The reviewed
map below keeps the root boundary explicit while making child project maps
available from the maestro root.

## Read First

- `AGENTS.md` - top-level operating contract, child-repo autonomy rules, and root safe scope.
- `README.md` - human-facing workspace topology, Bun workspace bootstrap, and child repo status.
- `.gitmodules` - declared remote-backed child paths and tracked branches.
- `.gitignore` - root exclusions for local autonomous repos and runtime state.
- `package.json` - root Bun workspace membership and filtered web scripts.
- `docs/CODEMAPS/README.md` - index for the existing workspace codemap set.
- `docs/CODEMAPS/projects/README.md` - central index of generated child repo codemap snapshots.
- `docs/CODEMAPS/WORKSPACE.md` - federated workspace topology and policy.
- `docs/CODEMAPS/SUBMODULES.md` - submodule and autonomous repo catalogue.
- `docs/CODEMAPS/SCRIPTS.md` - root helper script behavior and verification notes.

## Repository Shape

`keelim-maestro` is a workspace superproject, not a source monorepo. Root-owned
surfaces are coordination files, docs, idea backlog files, root scripts,
`.gitmodules`, and the narrow Bun workspace bootstrap.

Current declared `.gitmodules` paths:

- `all` tracks `develop`
- `android-support` tracks `main`
- `Keelim-Knowledge-Vault` tracks `main`
- `keelim-plugin` tracks `main`
- `keelim-vercel` tracks `main`
- `toto` tracks `main`

Current live gitlink evidence from `git ls-files --stage | rg 160000` and
`git submodule status` shows active root gitlinks for:

- `all` - index pins `edac30d`
- `android-support` - index/live status align at `485a2e4`
- `Keelim-Knowledge-Vault` - index pins `e740973`
- `keelim-plugin` - index pins `3e41d10`
- `keelim-vercel` - index pins `5aa9c8b`
- `toto` - index pins `a942e6b`

Root `.gitignore` excludes `.omx`, `node_modules`, `all-web-ui`, `quant`, and
`rich`, so those local paths are intentionally not normal root source files.
Their source-level orientation is still centrally collected under
`docs/CODEMAPS/projects/` when the child repo exists locally.

## Entrypoints

There is no deployable application entrypoint at the root. Root entrypoints are
maintenance and verification surfaces:

- `scripts/update-subrepos.sh` - status and safe fast-forward update helper.
- `scripts/test-workspace.sh` - lightweight root superproject contract tests (package metadata, required scripts, autonomous-repo boundaries).
- `scripts/verify-keelim-plugin-rename.sh` - verifies the former
  `keelim-skill` submodule rename.
- `scripts/verify-all-web-ui-integration.sh` - verifies the shared UI
  integration contract across `all-web-ui`, `rich/web`, and `keelim-vercel`.
- `package.json` scripts:
  - `test` / `test:workspace` — root superproject contract tests via `test-workspace.sh`
  - `typecheck:web`
  - `build:web`
  - `test:web`
  - `dev:keelim-vercel`
  - `dev:rich-web`
  - `dev:toto`
  - `test:toto`
  - `verify:toto`
  - `dev:strategy-builder` — start `rich/open-trading-api/strategy_builder`
  - `dev:backtester` — start `rich/open-trading-api/backtester`

## Key Directories

- `docs/CODEMAPS/` - root architecture, workspace, submodule, script, dependency, frontend, backend, and data maps.
- `docs/CODEMAPS/projects/` - maestro-managed generated codemaps for available child repositories.
- `docs/design/` - workspace-level design system notes.
- `idea/` - per-project idea backlog and workspace idea index.
- `scripts/` - root shell helpers for workspace contract tests, child repo status, integration verification, and rename verification.
- `.omx/` - local OMX runtime state, logs, plans, and team worktrees; ignored root state, not source.
- `all/`, `android-support/`, `Keelim-Knowledge-Vault/`, `keelim-plugin/`, `keelim-vercel/`, `toto/` - current active root gitlink paths.
- `all-web-ui/`, `rich/`, `quant/` - autonomous local repos surfaced by helper scripts when present, not root-owned source.

## Tests and Verification

Use root checks when changing root docs, metadata, scripts, or workspace
bootstrap:

```bash
git status --short
git status --ignore-submodules=none
git submodule status
git ls-files --stage | rg '160000'
git diff --check docs/CODEMAPS/keelim-maestro.md docs/CODEMAPS/README.md
```

Use helper checks when touching their contracts:

```bash
./scripts/update-subrepos.sh status
./scripts/update-subrepos.sh update --dry-run
./scripts/verify-keelim-plugin-rename.sh
./scripts/verify-all-web-ui-integration.sh
./scripts/verify-all-web-ui-integration.sh --full
```

The `--full` integration check runs Bun install/typecheck/test/build commands
across the shared web workspace and can require the hydrated autonomous child
repos plus test environment variables documented in `docs/CODEMAPS/SCRIPTS.md`.

## Dependencies and Tooling

- Root package manager: `bun@1.3.12`.
- Root workspaces: `all-web-ui`, `keelim-vercel`, `rich/open-trading-api/strategy_builder/frontend`, `rich/open-trading-api/backtester/frontend`, `rich/web`, `toto`.
- Shell helpers rely on `git`, `awk`, `jq`, `rg`, `grep`, and POSIX `sh`.
- The root docs intentionally summarize child repo relationships; use each
  child repo's own README, AGENTS, tests, and codemaps before editing child
  source.

## Useful Commands

- `bun run test` / `bun run test:workspace` - root superproject contract tests.
- `bun run typecheck:web` - root-filtered typecheck for `all-web-ui`, `keelim-vercel`, and `rich/web`.
- `bun run build:web` - root-filtered build for `keelim-vercel` and `rich/web`.
- `bun run test:web` - root-filtered `rich/web` test lane.
- `bun run dev:keelim-vercel` - start the `keelim-vercel` dev server from the root workspace.
- `bun run dev:rich-web` - start the `rich/web` dev server from the root workspace.
- `bun run dev:toto` - start the local `toto` dashboard workspace member.
- `bun run test:toto` - run `toto` tests through the root workspace.
- `bun run verify:toto` - run the `toto` verification script through the root workspace.
- `bun run dev:strategy-builder` - start the open-trading strategy builder frontend/backend.
- `bun run dev:backtester` - start the open-trading backtester frontend/backend.

## Symbol Landmarks

- `scripts/update-subrepos.sh:50` - `list_repo_paths`, combining `.gitmodules`
  paths with autonomous `all-web-ui`, `rich`, and `quant`.
- `scripts/update-subrepos.sh:61` - `resolve_branch`, deriving the safe target
  branch from `.gitmodules`, current branch, or `origin/HEAD`.
- `scripts/update-subrepos.sh:147` - `update_repo`, skip-first update logic for
  dirty, branch-mismatched, remote-less, or locally-ahead repos.
- `scripts/verify-keelim-plugin-rename.sh:19` - root/child string checks for
  rename verification.
- `scripts/verify-all-web-ui-integration.sh:151` -
  `all_web_ui_dependency_protocol_is_lockfile_coherent`, guarding the selected
  `file:` or `workspace:*` dependency protocol.
- `scripts/verify-all-web-ui-integration.sh:275` -
  `all_web_ui_manifest_lists_exports`, checking shared primitive exports.
- `scripts/verify-all-web-ui-integration.sh:401` - `run_static_checks`, the
  default shared UI integration verification lane.
- `scripts/verify-all-web-ui-integration.sh:516` - `run_full_checks`, the
  runtime verification lane.

## Open Questions

- Child codemap snapshots under `projects/` are generated from child sources and may lag if child repos have new commits since the last codemap refresh; verify against live source before relying on project-level claims.
- The raw generator scan crosses into child repo source; future root codemap
  refreshes should either use this reviewed root-only file or run the generator
  separately inside each child repo.
