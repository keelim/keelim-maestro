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

Checks that:
- The old path `keelim-skill/` no longer exists
- The new path `keelim-plugin/` is present
- `.gitmodules` references `keelim-plugin` (not `keelim-skill`)
- The submodule metadata is consistent

Run after any operation that touches the plugin submodule path.

---

## `scripts/verify-all-web-ui-integration.sh`

Verification helper for `all-web-ui` autonomous-repo integration.

Checks that `all-web-ui` is correctly surfaced through the root helper scripts
and that it has a reachable `origin` remote, without requiring it to be a
registered submodule.

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
