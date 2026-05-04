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
| `./scripts/verify-all-web-ui-integration.sh --full` | `full` | Static checks + runtime typecheck / test / build commands |

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
- `rich/web/package.json` depends on `all-web-ui`
- `rich/web` imports `all-web-ui` somewhere under `src/`
- `rich/web` admin layout still applies `admin-bw-theme`
- `rich/web` root layout still renders `AgentationToolbar`
- `keelim-vercel/package.json` depends on `all-web-ui`
- `all-web-ui` consumer dependency specs match the selected protocol (`file:` or `workspace:*`) and the root `bun.lock` consumer entries, while allowing valid root workspace package registrations
- `keelim-vercel` keeps generic `components/ui/` files as shim-only re-exports from `all-web-ui`
- `keelim-vercel` `all-web-ui` imports stay in adapter-safe locations (`components/shared/`, `lib/ui-adapters/`)
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
- Required script keys exist: `test`, `test:workspace`, `typecheck:web`, `build:web`, `test:web`, `verify:toto`

**Root files (`check_root_files`)**
- `README.md`, `.gitignore`, `.gitmodules` exist
- `scripts/update-subrepos.sh`, `scripts/verify-all-web-ui-integration.sh`, `scripts/verify-keelim-plugin-rename.sh` exist

**Autonomous repo contract (`check_autonomous_repo_contract`)**
- `.gitignore` excludes `all-web-ui`, `agent-skill-console`, `quant`, and `rich`
- `workspaces` array does **not** include `agent-skill-console`, `quant`, or `rich`
- If `agent-skill-console` is present locally: it must be git-ignored, not tracked by root, and be its own git repo

### Exit behaviour

Exits `0` if all checks pass or `1` with failure count printed. Prints
`PASS  <description>` / `FAIL  <description>` per check.

Safe to run at any time; does not invoke child-repo builds or dirty-state-sensitive suites.

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
