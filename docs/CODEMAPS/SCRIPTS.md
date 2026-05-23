# Root Helper Scripts

All scripts live under `scripts/` and are executed from the workspace root.

---

## `scripts/update-subrepos.sh`

Primary workspace maintenance script. Provides status reporting and safe
fast-forward updates for all tracked child repositories (both registered
submodules and autonomous local repos).

### Modes

| Invocation | Mode | Effect |
|------------|------|--------|
| `./scripts/update-subrepos.sh` | `status` | Print branch / dirty / ahead-behind summary |
| `./scripts/update-subrepos.sh status` | `status` | Same as above |
| `./scripts/update-subrepos.sh update` | `update` | Fetch + `pull --ff-only` for eligible repos |
| `./scripts/update-subrepos.sh update --dry-run` | `update (dry)` | Preview what would be fetched/pulled |
| `./scripts/update-subrepos.sh dry-run` | `update (dry)` | Alias for `update --dry-run` |

### Status output columns

```
<path>   branch=<current>   target=<default>   state=<clean|dirty>   ahead=<n>   behind=<n>   remote=<url>
```

- **branch** — currently checked-out branch inside the child repo
- **target** — branch declared in `.gitmodules` (or auto-detected `main`/`master`/`develop`)
- **state** — `clean` if `git status --porcelain` is empty, otherwise `dirty`
- **ahead** — local commits not on upstream
- **behind** — upstream commits not yet pulled

### Update eligibility rules

A child repo is updated only when **all** of the following hold:

1. Has an `origin` remote
2. Working tree is clean (no uncommitted changes)
3. Current branch is a supported branch: `main`, `master`, or `develop`
4. Current branch matches the declared target branch
5. No local commits ahead of upstream (`ahead == 0`)

If any condition fails the script prints `[skip] <path> <reason>` and moves on.

### Repo discovery

The script discovers child repos in two passes:

1. **Registered submodules** — reads paths from `.gitmodules` via `git config -f`
2. **Autonomous repos** — checks for `.git` in `all-web-ui`, `rich`, `quant`

Duplicate paths are deduplicated (awk `!seen[$0]++`).

### Exit behaviour

The script uses `set -eu`; any unexpected command failure causes an immediate
non-zero exit.

---

## `scripts/report-trusted-baseline.sh`

Read-only workspace evidence reporter for root-level pinning and submodule
safety decisions. It aggregates the current state from `.gitmodules`, active
gitlinks, root workspace manifests, root policy, and child Git status.

This script is an observation surface, not a source of truth and not permission
to pin, repair, or mutate child repositories.

### Invocation

| Invocation | Effect |
|------------|--------|
| `sh scripts/report-trusted-baseline.sh` | Print the live trusted-baseline table |
| `bun run report:baseline` | Same as above via the root package script |

### Output columns

| Column | Meaning |
|--------|---------|
| `path` | Child repo path being observed |
| `registration` | `registered-submodule`, `autonomous`, or `excluded-local` |
| `branch` | Current child repo branch, or `DETACHED` |
| `target` | `.gitmodules` branch or observed supported branch |
| `state` | `clean`, `dirty`, or `missing` |
| `ahead` / `behind` | Upstream divergence, or `-` when no upstream exists |
| `remote` | `origin` URL or `none` |
| `gitlink` | Active root `160000` gitlink evidence |
| `bun` | Root Bun workspace member path, if any |
| `uv` | Root uv workspace member path, if any |
| `eligibility` | `eligible-observed`, `blocked`, or `excluded` |
| `blocker` | Observed blocker reasons such as dirty state, branch mismatch, no remote, or no upstream |

### Source precedence

1. `.gitmodules` and `git ls-files --stage` for registered submodule/gitlink state
2. `package.json` for Bun workspace membership
3. `pyproject.toml` for uv workspace membership
4. Root policy/docs for known autonomous or excluded repos
5. Child Git commands for observation only

### Exit behaviour

Exits `0` when it can inspect the workspace and emit a report. Dirty repos,
branch mismatches, no upstream, no remote, and excluded-by-policy states are
reported in the table instead of causing a non-zero exit. Future strict/CI modes
should be added separately if they become necessary.

---

## `scripts/report-shared-ui-contract.sh`

Read-only control-tower report for the `@keelim/all-web-ui` provider and its
current downstream consumers: `keelim-vercel` and `rich/web`.

This script is an observation surface. It does not install dependencies, build
apps, publish packages, update lockfiles, or mutate child repositories.

### Invocation

| Invocation | Effect |
|------------|--------|
| `sh scripts/report-shared-ui-contract.sh` | Print the live shared UI contract report |
| `bun run report:shared-ui` | Same as above via the root package script |

### Sections

- **Provider** — checks `all-web-ui` package identity, exact version,
  GitHub Packages publish config, package exports, manifest export count, CSS
  entrypoints, and CSS `sideEffects` metadata.
- **Consumers** — checks exact downstream dependency specs, `.npmrc` GitHub
  Packages scope mapping, scoped import usage, and expected style/theme imports
  for `keelim-vercel` and `rich/web`.
- **Static verifier** — runs `sh scripts/verify-all-web-ui-integration.sh` and
  reports its PASS/FAIL counts.
- **Build canary inventory** — lists the package/app commands that should be
  used for heavier manual or CI canaries.
- **Visual regression readiness** — inventories whether each surface has an
  automated visual/e2e gate or still needs manual screenshot verification.

### Exit behaviour

Exits `0` when it can emit observations. `FAIL` rows are work-queue signals,
not this report's process exit contract. Use
`scripts/verify-all-web-ui-integration.sh` when a strict static non-zero exit is
needed.

---

## `scripts/verify-keelim-plugin-rename.sh`

Verification helper for the `keelim-skill` → `keelim-plugin` directory rename.

### Checks performed

**`.gitmodules` file**
- Section header is `[submodule "keelim-plugin"]`
- `path = keelim-plugin`
- `url = https://github.com/keelim/keelim-plugin.git`
- `branch = main`
- No remaining `keelim-skill` references

**Root `README.md`**
- Mentions `keelim-plugin`
- No remaining `keelim-skill` references

**Git index (gitlinks)**
- `git ls-files --stage` pins a `keelim-plugin` gitlink (mode `160000`)
- No `keelim-skill` gitlink present

**`git submodule status`**
- Lists `keelim-plugin`
- Does not list `keelim-skill`

**Root git config (`.git/config`)**
- `submodule.keelim-plugin.url` points at `https://github.com/keelim/keelim-plugin.git`
- No `submodule.keelim-skill` entries

**Submodule wiring**
- `keelim-plugin/.git` file contains `gitdir: ../.git/modules/keelim-plugin`
- `.git/modules/keelim-plugin/config` sets correct `worktree` and `url`

**Child `README.md`**
- Title uses `# keelim-plugin`
- Install command references `keelim/keelim-plugin`
- GitHub URL uses `keelim-plugin`
- Path examples use `/keelim-plugin/`
- No remaining `keelim-skill` references

**`update-subrepos.sh` integration**
- `./scripts/update-subrepos.sh status` reports `keelim-plugin` with `target=main`

### Exit behaviour

Exits with code `0` if all checks pass or `1` if any check fails (binary exit,
not a failure count). Prints `PASS: <description>` / `FAIL: <description>` per
check. Prints `Verification passed.` on success or
`Verification failed with N issue(s).` on failure.

Run after any operation that touches the plugin submodule path.

---

## `scripts/verify-all-web-ui-integration.sh`

Verification helper for the `all-web-ui` autonomous-repo integration contract.

### Modes

| Invocation | Mode | Effect |
|------------|------|--------|
| `./scripts/verify-all-web-ui-integration.sh` | `static` | Static contract checks only |
| `./scripts/verify-all-web-ui-integration.sh --full` | `full` | Static checks + runtime typecheck / test / build commands + GitHub Packages publish check |

### Static checks

The default mode runs the following checks:

- `all-web-ui`, `rich`, and `keelim-vercel` repos exist as Git worktrees
- `all-web-ui` has a reachable `origin` remote
- Root `.gitignore` excludes `/all-web-ui/` from root index
- `update-subrepos.sh status` lists `all-web-ui`
- `all-web-ui` default branch is `main`
- `all-web-ui/package.json` exists and declares `typecheck` + `test` scripts
- `all-web-ui/src/components/` exports the shared shadcn-compatible primitive set (`button.tsx`, `input.tsx`, `panel.tsx`, `card.tsx`, `calendar.tsx`, `badge.tsx`, `table.tsx`, `tabs.tsx`, `tooltip.tsx`, `sheet.tsx`, `dropdown-menu.tsx`, `breadcrumb.tsx`, `accordion.tsx`, `select.tsx`, `toast.tsx`, …)
- `all-web-ui` defines shared CSS entrypoints (styles and theme files)
- `all-web-ui` manifest lists package exports for shared primitives
- `rich/web/package.json` depends on `@keelim/all-web-ui`
- `rich/web` resolves dependencies through the root Bun workspace/catalog rather than package-local lockfile enforcement
- `rich/web` imports `@keelim/all-web-ui` somewhere under `src/`
- `rich/web` admin layout still applies `admin-bw-theme`
- `rich/web` root layout still renders `AgentationToolbar`
- `keelim-vercel/package.json` depends on `@keelim/all-web-ui`
- standalone consumer `bun.lock` files use the scoped GitHub Packages package and do not retain unscoped `all-web-ui` entries
- `@keelim/all-web-ui` consumer dependency specs match the exact GitHub Packages version and the root `bun.lock` consumer entries, while allowing valid root workspace package registrations
- `keelim-vercel` keeps generic `components/ui/` files as shim-only re-exports from `@keelim/all-web-ui`
- `keelim-vercel` `@keelim/all-web-ui` imports stay in adapter-safe locations (`components/shared/`, `lib/ui-adapters/`, app-level theme imports)
- `rich/web` uses the `--kui-*` token contract instead of legacy `--color-*` tokens
- `rich/web` generic primitive drift is constrained by `scripts/all-web-ui-rich-allowed-drift.txt`

### Full runtime checks (`--full`)

Only executed when all static checks pass:

```bash
mkdir -p /tmp/keelim-maestro-bun-tmp
cd .           && TMPDIR=/tmp/keelim-maestro-bun-tmp bun install --frozen-lockfile
cd all-web-ui  && bun run typecheck
cd all-web-ui  && bun test
cd all-web-ui  && bun run build
npm view @keelim/all-web-ui@0.1.4 version --registry=https://npm.pkg.github.com  # uses NODE_AUTH_TOKEN or gh auth token when needed
cd rich/web    && bun run typecheck
cd rich/web    && bun run test
cd rich/web    && NEXT_PUBLIC_SUPABASE_URL=https://example.supabase.co NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_test SUPABASE_SERVICE_ROLE_KEY=service-role-test GOOGLE_OAUTH_CLIENT_ID=client-id GOOGLE_OAUTH_CLIENT_SECRET=client-secret GOOGLE_TOKEN_ENCRYPTION_KEY=0123456789abcdef0123456789abcdef GOOGLE_SHEETS_SPREADSHEET_ID=sheet-id bun run build
cd keelim-vercel && bun run typecheck
cd keelim-vercel && bun run lint
cd keelim-vercel && bun run verify:maintenance
cd keelim-vercel && bun run build   # retried once on lock-file errors
```

### Workspace root resolution

The script resolves the workspace root via:
1. `$OMX_TEAM_STATE_ROOT` environment variable (CI / team-state override), or
2. Presence of both `rich/.git` and `keelim-vercel/.git` under the current
   `git rev-parse --show-toplevel`, or
3. `git rev-parse --show-toplevel` as fallback.

### Exit behaviour

Exits with the number of failures (0 = all checks passed). Prints
`PASS  <description>` / `FAIL  <description>` per check.

---

## `scripts/test-workspace.sh`

Lightweight root superproject contract test suite. Verifies that the root
`package.json`, required helper scripts, and autonomous-repo boundaries all
meet the documented workspace contract. Run via `bun run test` or
`bun run test:workspace` from the workspace root.

### Checks performed

**Package contract (`check_package_contract`)**
- `package.json` is private
- `packageManager` starts with `bun@`
- `workspaces` is an array
- `scripts` is an object
- Required script keys exist: `test`, `test:workspace`, `report:baseline`, `report:shared-ui`, `typecheck:web`, `build:web`, `test:web`, `dev:codex-app-server`, `verify:toto`

**Root files (`check_root_files`)**
- `README.md`, `.gitignore`, `.gitmodules` exist
- `scripts/update-subrepos.sh`, `scripts/report-trusted-baseline.sh`, `scripts/report-shared-ui-contract.sh`, `scripts/verify-all-web-ui-integration.sh`, `scripts/verify-keelim-plugin-rename.sh`, `scripts/codex-app-server.sh` exist
- The trusted-baseline and shared UI contract reporters run successfully in read-only mode

**Autonomous repo contract (`check_autonomous_repo_contract`)**
- `.gitignore` excludes `all-web-ui`, `quant`, and `rich`
- `workspaces` array does **not** include `quant` or `rich`

### Exit behaviour

Exits `0` if all checks pass or `1` with failure count printed. Prints
`PASS  <description>` / `FAIL  <description>` per check.

Safe to run at any time; does not invoke child-repo builds or dirty-state-sensitive suites.

---

## `scripts/verify-python-dependency-constraints.py`

Verification helper for shared Python dependency constraints across uv workspace members (`toto`, `rich`).

### Purpose

Ensures that any package declared in more than one workspace member uses a consistent version specifier, and that all such shared packages are pinned under `tool.uv.constraint-dependencies` in the root `pyproject.toml`.

### Invocation

```bash
uv run python scripts/verify-python-dependency-constraints.py
```

In sandboxed agent sessions, add `--cache-dir .omx/uv-cache` if the default uv cache is not writable.

### Checks performed

1. **Root constraint coverage** — any package declared in ≥ 2 workspace member `pyproject.toml` files must appear in the root `tool.uv.constraint-dependencies` list.
2. **Specifier alignment** — each workspace member declaration for a shared package must match the root constraint specifier exactly.
3. **Reverse check** — each package listed in root constraints and present in any member must have a declaration that matches the constraint.

### Output

Prints `OK: Python dependency constraints are aligned.` on success, with a summary of workspace members, shared packages, and root constraints. Prints drift details to `stderr` and exits non-zero on failure.

### Exit behaviour

Exits `0` on success, `1` on constraint drift, `2` if Python < 3.11 is detected.

Run after any change to `pyproject.toml` in the root or in `toto`/`rich`.

---

## `scripts/refresh-codemaps.py`

Automation script to generate/refresh all child project codemaps and dynamically update the root index table and date stamps.

### Invocation

| Invocation | Effect |
|------------|--------|
| `python3 scripts/refresh-codemaps.py` | Generate codemaps for all available child repos and update documentation indices |

### Subprojects scanned
- `all`
- `all-web-ui`
- `android-support`
- `Keelim-Knowledge-Vault`
- `keelim-plugin`
- `keelim-vercel`
- `rich`
- `toto`

### Exit behaviour

Exits `0` on success, or a non-zero code on failures.

---

## `scripts/codex-app-server.sh`

Start a Codex app-server bound to the workspace root, defaulting to a local-only WebSocket transport.

### Invocation

| Invocation | Effect |
|------------|--------|
| `sh scripts/codex-app-server.sh` | Start app-server at `ws://127.0.0.1:7331` |
| `bun run dev:codex-app-server` | Same via root package script |
| `sh scripts/codex-app-server.sh --listen unix:///tmp/codex-app.sock` | Unix socket transport |

### Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CODEX_APP_SERVER_LISTEN` | `ws://127.0.0.1:7331` | Transport endpoint for the app-server |
| `CODEX_BIN` | `codex` | Codex executable; set to full path if not on `PATH` |

### Security gate

The script refuses to start a non-loopback WebSocket listener (`ws://`) unless
`--ws-auth` or `--ws-auth=<...>` is explicitly passed. Local-only transports
(`ws://127.0.0.1:*`, `ws://localhost:*`, `ws://[::1]:*`), stdio, and Unix
socket (`unix://`) transports are always allowed.

### Exit behaviour

Exits `127` if the Codex executable is not found. Exits `2` if a non-loopback
WebSocket endpoint is requested without `--ws-auth`. Otherwise `exec`s into
`codex app-server`; exit code propagates from the Codex process.

---

## Adding New Scripts

Follow the existing conventions:

1. Place under `scripts/`
2. Use `#!/bin/sh` with `set -eu`
3. Support a `--dry-run` flag for any mutating operations
4. Print a `[skip] <path> <reason>` line rather than erroring when a repo is
   ineligible for an operation
5. Begin by `cd "$(git rev-parse --show-toplevel)"` to ensure paths are relative
   to the workspace root
