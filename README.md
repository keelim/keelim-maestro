# keelim-maestro

This root repository is a **workspace superproject bootstrap** for the child repositories in this folder.

## Current safe scope

This repository currently owns only root-level coordination files:

- `AGENTS.md`
- `README.md`
- `.gitignore`
- future `.gitmodules`
- future root-only helper scripts/docs

The child repositories remain autonomous for now. This root is **not** yet a submodule-backed superproject snapshot because some child repos are still dirty or ahead of their remotes.

## Child repositories in this workspace

| Path | Remote? | Current status | Notes |
| --- | --- | --- | --- |
| `all` | yes | clean vs `origin/develop` | candidate for later pinning |
| `android-support` | yes | ahead of `origin/main` by 3 | push/reconcile before pinning |
| `Keelim-Knowledge-Vault` | yes | ahead of `origin/main` by 1 | push/reconcile before pinning |
| `keelim-skill` | yes | clean vs `origin/main` | candidate for later pinning |
| `keelim-vercel` | yes | dirty, ahead of `origin/develop` by 5 | do not convert yet |
| `quant` | no | dirty local repo | intentionally excluded for now |
| `rich` | yes | dirty, ahead of `origin/master` by 29 | do not convert yet |

## Why `/quant` is excluded

`/quant` has **no remote**, so it is intentionally excluded from the initial root superproject/submodule scope.

Do **not**:

- create a remote for `/quant` unless explicitly requested
- add `/quant` as a local-path submodule

Keeping `/quant` autonomous preserves safety and avoids a non-reproducible clone workflow.

## Why submodule conversion is deferred

Safe submodule conversion requires child repos to be pin-ready first. Right now that is blocked by:

- dirty working trees in `keelim-vercel`, `quant`, and `rich`
- local commits ahead of remote in `android-support`, `Keelim-Knowledge-Vault`, `keelim-vercel`, and `rich`

Until those repos are normalized, do not convert them from the root.

## Bootstrap / inspection commands

```bash
git status --short
git status --ignore-submodules=none
git submodule status
git submodule foreach git status --short --branch
git submodule update --init --recursive
```

Note: the submodule commands above are for the later conversion stage; they are expected to be no-ops or fail until `.gitmodules` exists.

## Next safe steps before submodule conversion

1. Decide which ahead-of-remote child commits should be pushed.
2. Clean or explicitly preserve dirty child-repo work without discarding changes.
3. Create `.gitmodules` only after the remote-backed child repos are safe to pin.
4. Add submodules from remote URLs only.
5. Verify with:
   - `git submodule status`
   - `git ls-files --stage | grep 160000`
   - `git status --ignore-submodules=none`

## Clone / future bootstrap flow

After this root repo eventually has `.gitmodules`, the reproducible bootstrap flow will be:

```bash
git clone <root-repo>
cd keelim-maestro
git submodule update --init --recursive
```
